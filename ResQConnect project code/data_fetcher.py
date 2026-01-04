import requests
from datetime import datetime, timedelta
from pymongo import MongoClient
import json

# Load config for Mongo URI
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

# Connect to MongoDB
client = MongoClient(params["mongo_uri"])
db = client.get_default_database()

def alert_store():
    url = "https://eonet.gsfc.nasa.gov/api/v3/events"
    response = requests.get(url)
    data = response.json()
    all_events = data.get('events', [])

    recent_events = []
    one_week_ago = datetime.utcnow() - timedelta(days=7)

    for event in all_events:
        if event.get('geometry'):
            geometry = event['geometry'][0]
            date_str = geometry['date']
            event_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')

            if event_date >= one_week_ago:
                category = event.get('categories')[0]['title'] if event.get('categories') else 'Unknown'
                event_id = event.get('id')

                # Check if alert with same id already exists
                existing_alert = db.alerts.find_one({'event_id': event_id})
                if existing_alert:
                    continue  # Skip if already exists

                recent_events.append({
                    'event_id': event_id,
                    'title': event['title'],
                    'category': category,
                    'date': event_date.strftime('%d-%b-%Y %H:%M'),
                    'coordinates': geometry['coordinates']
                })

    if recent_events:
        db.alerts.insert_many(recent_events)
    print(f"Inserted {len(recent_events)} new alerts.")

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
