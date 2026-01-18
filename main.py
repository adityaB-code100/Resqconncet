from flask import Flask, render_template, redirect, request, session, url_for, jsonify
from bson.objectid import ObjectId
import requests
import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

from data_fetcher import alert_store, wether_store, cleanup_old_alerts, cleanup_old_weather
from extension import mongo
from admin_routes import admin_bp


# --------------------------------------------------
# APP SETUP
# --------------------------------------------------

app = Flask(__name__)

# ✅ Secret key (MUST be env var in production)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key")

# --------------------------------------------------
# MONGODB CONFIG (NO LOCALHOST ❌)
# --------------------------------------------------

mongo_uri = os.environ.get("MONGO_URI")
if not mongo_uri:
    raise RuntimeError("❌ MONGO_URI environment variable not set")

app.config["MONGO_URI"] = mongo_uri
mongo.init_app(app)

# ✅ Test MongoDB connection
try:
    with app.app_context():
        mongo.db.list_collection_names()
        print("✅ MongoDB connected successfully")
except Exception as e:
    print("❌ MongoDB connection failed:", e)
    raise e


# --------------------------------------------------
# BLUEPRINTS
# --------------------------------------------------

app.register_blueprint(admin_bp)


# --------------------------------------------------
# ROUTES
# --------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        complaint = {
            "name": request.form["name"],
            "contact": request.form["contact"],
            "emergency_type": request.form["emergency"],
            "location": request.form["location"],
            "description": request.form["description"],
            "timestamp": datetime.utcnow()
        }
        mongo.db.complaints.insert_one(complaint)
        return redirect("/register")

    return render_template("Home.html")


@app.route("/home")
def home():
    return render_template("Home.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/contactus", methods=["GET", "POST"])
def contactus():
    if request.method == "POST":
        contact_data = {
            "name": request.form["name"],
            "contact": request.form["contact"],
            "location": request.form["location"],
            "description": request.form["description"],
            "timestamp": datetime.utcnow()
        }
        mongo.db.contacts.insert_one(contact_data)
        return redirect("/contactus")

    return render_template("contact.html")


@app.route("/service")
def service():
    try:
        cards = list(mongo.db.card.find())
        return render_template("service.html", cards=cards)
    except Exception as e:
        print("Service route error:", e)
        return render_template("service.html", cards=[])


@app.route("/service/<string:card_id>")
def first_aid(card_id):
    card = mongo.db.card.find_one({"_id": ObjectId(card_id)})
    if not card:
        return "Card not found", 404

    steps = card.get("description", "").split(".")
    return render_template("first_aid.html", card=card, firstaid_list=steps)


@app.route("/tagline/<string:emergency_id>")
def tagline(emergency_id):
    emergency = mongo.db.emergencies.find_one({"_id": ObjectId(emergency_id)})
    return render_template("tagline.html", emergency=emergency)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/policy")
def policy():
    info = {
        "title": "Policy Information",
        "description": "ResQConnect policies, privacy rules and terms of use."
    }
    return render_template("policy.html", info=info)


@app.route("/info/<slug>")
def get_info(slug):
    info = mongo.db.info_sections.find_one({"slug": slug})
    return render_template("policy.html", info=info)


# --------------------------------------------------
# API ROUTES
# --------------------------------------------------

@app.route("/api/weather")
def api_weather():
    try:
        weather = mongo.db.weather.find_one(sort=[("time", -1)]) or {}
        if not weather:
            return jsonify({
                "temperature": "N/A",
                "windspeed": "N/A",
                "time": "No data"
            }), 404

        weather["_id"] = str(weather["_id"])
        return jsonify(weather)

    except Exception as e:
        print("Weather API error:", e)
        return jsonify({"error": "Failed to fetch weather"}), 500


@app.route("/api/alerts")
def api_alerts():
    try:
        alerts = list(mongo.db.alerts.find().sort("date", -1))
        unique = []
        seen = set()

        for alert in alerts:
            key = (alert.get("title"), alert.get("date"))
            if key not in seen:
                seen.add(key)
                alert["_id"] = str(alert["_id"])
                unique.append(alert)
            if len(unique) == 5:
                break

        return jsonify({"events": unique})

    except Exception as e:
        print("Alerts API error:", e)
        return jsonify({"events": []}), 500


# --------------------------------------------------
# ERROR HANDLERS
# --------------------------------------------------
@app.route("/health")
def health():
    return "OK", 200

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# --------------------------------------------------
# BACKGROUND SCHEDULER (RENDER SAFE)
# --------------------------------------------------

scheduler = BackgroundScheduler(job_defaults={"max_instances": 1})

scheduler.add_job(alert_store, "interval", minutes=10, id="alert_store", replace_existing=True)
scheduler.add_job(wether_store, "interval", minutes=1, id="weather_store", replace_existing=True)
scheduler.add_job(lambda: cleanup_old_alerts(7), "cron", hour=0, minute=0)
scheduler.add_job(lambda: cleanup_old_weather(1), "cron", hour=0, minute=30)

# ✅ Start scheduler ONLY ONCE in Render
if os.environ.get("RENDER_INSTANCE_ID"):
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    print("✅ Background scheduler started")


# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
else:
    print("Application loaded in WSGI mode")
