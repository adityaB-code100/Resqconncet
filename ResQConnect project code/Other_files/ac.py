from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# Connect to MongoDB using your URI
client = MongoClient("mongodb://localhost:27017/emergencyDB")
db = client.get_default_database()  # or db = client["emergencyDB"]
collection = db["complaints"]

# 50 Common Indian names
names = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Krishna", "Ishaan", "Arjun", "Sai", "Reyansh", "Shaurya",
    "Ananya", "Diya", "Myra", "Aarohi", "Ira", "Meera", "Saanvi", "Prisha", "Riya", "Kavya",
    "Om", "Atharva", "Kabir", "Rudra", "Devansh", "Tanvi", "Ishita", "Pihu", "Avni", "Navya",
    "Yash", "Harsh", "Rohan", "Manav", "Nikhil", "Neha", "Swara", "Gauri", "Trisha", "Sneha",
    "Ayaan", "Dhruv", "Raj", "Vihan", "Divya", "Kriti", "Tanya", "Mira", "Ved", "Naira"
]

# Maharashtra cities
locations = [
    "Mumbai", "Pune", "Nagpur", "Nashik", "Thane", "Aurangabad", "Solapur", "Amravati", "Kolhapur", "Latur"
]

# Emergency types and descriptions
emergency_types = ["Medical", "Fire", "Accident", "Natural Disaster", "Crime"]
descriptions = [
    "Severe injury reported",
    "Fire outbreak in building",
    "Multiple vehicle accident",
    "Flooding due to heavy rain",
    "Robbery in progress"
]

# Generate and insert 50 documents
base_time = datetime.utcnow()
records = []

for i in range(50):
    record = {
        "name": names[i],
        "contact": f"+91-98765{random.randint(10000, 99999)}",
        "emergency_type": random.choice(emergency_types),
        "location": random.choice(locations),
        "description": random.choice(descriptions),
        "timestamp": base_time - timedelta(minutes=i)
    }
    records.append(record)

# Insert into MongoDB
collection.insert_many(records)
print("✅ Inserted 50 emergency reports into emergencyDB.emergency_reports")
