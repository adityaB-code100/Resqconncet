import requests
from datetime import datetime, timedelta
from pymongo import MongoClient
import json
import os
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Load config for Mongo URI
try:
    with open('config.json', 'r') as c:
        params = json.load(c)["params"]
    mongo_uri = params["mongo_uri"]
except FileNotFoundError:
    print("⚠️ config.json not found. Using environment variable for MongoDB URI.")
    mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/emergencyDB")

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client.emergencyDB  # Use the emergencyDB database directly



def alert_store():
    url = (
        "https://earthquake.usgs.gov/fdsnws/event/1/query"
        "?format=geojson"
        "&starttime=" + (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")
    )

    # ---- Retry-enabled session ----
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)

    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        print("⏳ USGS API timeout")
        return
    except requests.exceptions.RequestException as e:
        print("❌ USGS API error:", e)
        return

    events = data.get("features", [])
    recent_events = []

    for event in events:
        props = event.get("properties", {})
        geom = event.get("geometry", {})

        if not geom or not props:
            continue

        event_id = event.get("id")

        # ---- Avoid duplicate insert ----
        if db.alerts.find_one({"event_id": event_id}):
            continue

        event_time = datetime.utcfromtimestamp(props["time"] / 1000)

        recent_events.append({
            "event_id": event_id,
            "title": props.get("title", "Earthquake"),
            "category": "Earthquake",
            "date": event_time.strftime("%d-%b-%Y %H:%M"),
            "coordinates": geom.get("coordinates"),  # [lon, lat, depth]
            "magnitude": props.get("mag"),
            "source": "USGS"
        })

    if recent_events:
        db.alerts.insert_many(recent_events)

    print(f"✅ Inserted {len(recent_events)} new alerts from USGS.")

def wether_store():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': 28.6139,
        'longitude': 77.2090,
        'current_weather': 'true',
        'timezone': 'auto'
    }

    response = requests.get(url, params=params)
    data = response.json()

    weather_data = data.get('current_weather', {})

    weather = {
        'temperature': weather_data.get('temperature'),
        'windspeed': weather_data.get('windspeed'),
        'winddirection': weather_data.get('winddirection'),
        'time': weather_data.get('time'),
        'weathercode': weather_data.get('weathercode')
    }

    db.weather.insert_one(weather)
    print("Inserted current weather data.")

def cleanup_old_alerts(days=7):
    """
    Delete alerts older than `days` days.
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    alerts = db.alerts.find()
    deleted_count = 0

    for alert in alerts:
        try:
            alert_date = datetime.strptime(alert['date'], '%d-%b-%Y %H:%M')
            if alert_date < cutoff_date:
                db.alerts.delete_one({'_id': alert['_id']})
                deleted_count += 1
        except Exception as e:
            print(f"Skipping alert  due to parse error: {e}")

    print(f"Deleted {deleted_count} old alerts.")

def cleanup_old_weather(days=1):
    """
    Delete weather entries older than `days` days.
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    weather_entries = db.weather.find()
    deleted_count = 0

    for weather in weather_entries:
        try:
            weather_time = datetime.strptime(weather['time'], '%Y-%m-%dT%H:%M')
            if weather_time < cutoff_date:
                db.weather.delete_one({'_id': weather['_id']})
                deleted_count += 1
        except Exception as e:
            print(f"Skipping weather  due to parse error: {e}")

    print(f"Deleted {deleted_count} old weather records.")
