from flask import Flask, render_template, redirect, request, session, url_for, jsonify
from bson.objectid import ObjectId
import requests
import json
from datetime import datetime
from gemini_api import generate_gemini_response
from data_fetcher import alert_store, wether_store, cleanup_old_alerts, cleanup_old_weather
from extension import mongo  # ✅ New import
from admin_routes import admin_bp  # ✅ Now this won't cause circular import
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from twilio.rest import Client


app = Flask(__name__)
app.secret_key = "your_secret_key"

# ✅ Load configuration from config.json
with open('config.json', 'r') as c:
    config = json.load(c)

params = config["params"]
twilio_config = config["twilio"]

# ✅ MongoDB setup
app.config["MONGO_URI"] = params["mongo_uri"]
mongo.init_app(app)

# ✅ Register Blueprints
app.register_blueprint(admin_bp)

# ✅ Twilio setup
account_sid = twilio_config["account_sid"]
auth_token = twilio_config["auth_token"]
twilio_number = twilio_config["from_number"]
resq_team_number = twilio_config["resq_team_number"]

client = Client(account_sid, auth_token)

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

        try:
            # ✅ Alert SMS to ResQ team
            team_sms = (
                f"🚨 Emergency Alert 🚨\n"
                f"Type: {emergency_type}\n"
                f"Name: {name}\n"
                f"Contact: {contact}\n"
                f"Location: {location}\n"
                f"Details: {description}\n"
                f"⚠️ Please respond immediately!"
            )
            client.messages.create(
                body=team_sms,
                from_=twilio_number,
                to=resq_team_number
            )

            # ✅ Confirmation SMS to user
            user_contact = contact if contact.startswith('+') else '+91' + contact
            user_sms = "✅ Your complaint has been registered. Help is on the way."
            client.messages.create(
                body=user_sms,
                from_=twilio_number,
                to=user_contact
            )

        except Exception as e:
            print("❌ Failed to send SMS:", e)

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

        # Prepare SMS
        user_contact = contact_number if contact_number.startswith('+') else '+91' + contact_number
        user_sms = "✅ Your contact request has been registered. We will contact you as early as possible."

        try:
            client.messages.create(
                body=user_sms,
                from_=twilio_number,
                to=user_contact
            )
        except Exception as e:
            print("❌ Failed to send SMS:", e)

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
    cards = mongo.db.card.find()
    return render_template('service.html', cards=cards)

@app.route("/contactus")
def contactus():
    return render_template('contact.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/policy")
def policy():
    return render_template('policy.html')

@app.route('/alerts')
def show_recent_global_alerts():
    recent_alerts = list(mongo.db.alerts.find().sort("date", -1))
    seen = set()
    filtered_alerts = []
    for alert in recent_alerts:
        key = (alert['title'], alert['date'])
        if key not in seen:
            seen.add(key)
            filtered_alerts.append(alert)
        if len(filtered_alerts) == 5:
            break
    return render_template('alerts.html', events=filtered_alerts)

@app.route('/weather')
def show_weather():
    weather = mongo.db.weather.find_one(sort=[("time", -1)])
    return render_template('weather.html', weather=weather)

@app.route('/g')
def indexb():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_response():
    data = request.get_json()
    prompt = data.get('prompt', '')
    response = generate_gemini_response(prompt)
    return jsonify({'response': response})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# ------------------- MAIN -------------------


# 🕒 Schedule your jobs here
scheduler = BackgroundScheduler()

scheduler.add_job(alert_store, 'interval', minutes=1)

scheduler.add_job(wether_store, 'interval', minutes=1)

scheduler.add_job(lambda: cleanup_old_alerts(7), 'cron', hour=0, minute=0)

scheduler.add_job(lambda: cleanup_old_weather(1), 'cron', hour=0, minute=30)

scheduler.start()

atexit.register(lambda: scheduler.shutdown())


@app.route('/info/<slug>')
def get_info(slug):
    info = mongo.db.info_sections.find_one({"slug": slug})
    return render_template("policy.html", info=info)



if __name__ == "__main__":
    
    app.run(debug=True)
