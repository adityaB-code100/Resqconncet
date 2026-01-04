from flask import Flask, render_template, redirect, request, session, url_for, jsonify
from bson.objectid import ObjectId
import requests
import json
import os
from datetime import datetime
from data_fetcher import alert_store, wether_store, cleanup_old_alerts, cleanup_old_weather
from extension import mongo  # ✅ New import
from admin_routes import admin_bp  # ✅ Now this won't cause circular import
from apscheduler.schedulers.background import BackgroundScheduler
import atexit


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "your_default_secret_key_here")

# ✅ Load configuration from config.json or environment variables
try:
    with open('config.json', 'r') as c:
        config = json.load(c)
except FileNotFoundError:
    print("⚠️ config.json not found. Using environment variables or defaults.")
    config = {
        "params": {
            "mongo_uri": os.environ.get("MONGO_URI", "mongodb://localhost:27017/emergencyDB")
        }
        
    }

params = config["params"]

# ✅ MongoDB setup
app.config["MONGO_URI"] = params["mongo_uri"]
mongo.init_app(app)

# Test MongoDB connection
try:
    with app.app_context():
        # Test the connection
        mongo.db.list_collection_names()
        print("✅ MongoDB connection successful!")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    print(f"URI: {params['mongo_uri']}")

# ✅ Register Blueprints
app.register_blueprint(admin_bp)



# ✅ Route for complaint submission
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        emergency_type = request.form['emergency']
        location = request.form['location']
        description = request.form['description']

        complaint = {
            "name": name,
            "contact": contact,
            "emergency_type": emergency_type,
            "location": location,
            "description": description,
            "timestamp": datetime.utcnow()
        }

        # Save complaint to MongoDB
        mongo.db.complaints.insert_one(complaint)
        return redirect('/register')

    return render_template('Home.html')


@app.route('/c', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        contact_number = request.form['contact']
        location = request.form['location']
        description = request.form['description']

        contact_data = {
            "name": name,
            "contact": contact_number,
            "location": location,
            "description": description,
            "timestamp": datetime.utcnow()
        }

        
        mongo.db.contacts.insert_one(contact_data)
        return redirect('/contactus')

    return render_template('Home.html')


@app.route("/tagline/<string:Emergency_id>")
def tagline(Emergency_id):
    emergency = mongo.db.emergencies.find_one({"_id": ObjectId(Emergency_id)})
    return render_template('tagline.html', emergency=emergency)

@app.route("/home")
def home():
    return render_template('Home.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/service/<string:card_id>")
def first_aid(card_id):
    card = mongo.db.card.find_one({"_id": ObjectId(card_id)})
    if not card:
        return "Card not found", 404
    firstaid_para = card.get('description', '')
    firstaid_list = firstaid_para.split('.')
    return render_template('first_aid.html', card=card, firstaid_list=firstaid_list)

@app.route("/service")
def service():
    try:
        cards = mongo.db.card.find()
        return render_template('service.html', cards=cards)
    except Exception as e:
        print(f"Error in service route: {e}")
        return render_template('service.html', cards=[])

@app.route("/contactus")
def contactus():
    return render_template('contact.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/policy")
def policy():
    # Provide default context to prevent errors when info is not provided
    default_info = {
        "title": "Policy Information",
        "description": "This section contains important policy information about ResQConnect services, user guidelines, privacy policies, and terms of use.",
    }
    return render_template('policy.html', info=default_info)



# ✅ API Endpoints for Dynamic Content Loading
@app.route('/api/weather')
def api_weather():
    """API endpoint to get weather data as JSON"""
    try:
        weather = mongo.db.weather.find_one(sort=[("time", -1)])
        if weather:
            # Convert ObjectId to string for JSON serialization
            weather['_id'] = str(weather['_id'])
            return jsonify(weather)
        else:
            return jsonify({
                "temperature": "N/A",
                "windspeed": "N/A", 
                "winddirection": "0",
                "time": "No data available"
            }), 404
    except Exception as e:
        return jsonify({"error": "Failed to fetch weather data"}), 500

@app.route('/api/alerts')
def api_alerts():
    """API endpoint to get alerts data as JSON"""
    try:
        recent_alerts = list(mongo.db.alerts.find().sort("date", -1))
        seen = set()
        filtered_alerts = []
        for alert in recent_alerts:
            key = (alert['title'], alert['date'])
            if key not in seen:
                seen.add(key)
                # Convert ObjectId to string for JSON serialization
                alert['_id'] = str(alert['_id'])
                filtered_alerts.append(alert)
            if len(filtered_alerts) == 5:
                break
        
        return jsonify({"events": filtered_alerts})
    except Exception as e:
        return jsonify({"events": [], "error": "Failed to fetch alerts data"}), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# ------------------- MAIN -------------------


# 🕒 Schedule your jobs here
scheduler = BackgroundScheduler()

scheduler.add_job(
    alert_store,
    trigger="interval",
    minutes=10,             
    id="alert_store_job",   
    replace_existing=True,  
    max_instances=1,       
    coalesce=True          
)



scheduler.add_job(
    wether_store,
    trigger="interval",
    minutes=1,
    max_instances=1,        # keep 1 (safe)
    coalesce=True           # merge missed runs
)

scheduler.add_job(lambda: cleanup_old_alerts(7), 'cron', hour=0, minute=0)

scheduler.add_job(lambda: cleanup_old_weather(1), 'cron', hour=0, minute=30)

scheduler.start()

atexit.register(lambda: scheduler.shutdown())


@app.route('/info/<slug>')
def get_info(slug):
    info = mongo.db.info_sections.find_one({"slug": slug})
    return render_template("policy.html", info=info)



# For Render deployment, we should be careful with background jobs
# Render free tier web services sleep after 15 mins of inactivity
# For production deployment on Render, consider using a separate background worker
if __name__ == "__main__":
    # Get port from environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

# For WSGI compatibility (used by Render and other production servers)
else:
    # In production environments like Render, the scheduler might not run continuously
    # due to the sleeping behavior of free tier services
    print("Application loaded in WSGI mode. Background scheduler active.")
