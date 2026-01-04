import re
import json
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["emergencyDB"]
collection = db["card"]
import re
import json
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["emergencyDB"]
collection = db["card"]

documents = [
    {
        "id": 1,
        "title": "National Emergency Number",
        "image_url": "https://th.bing.com/th/id/R.f1818b1d113fcbfa98a9a53861c0d5b5?rik=yej9QAFzuDIhag&riu=http%3a%2f%2fgetdrawings.com%2ffree-icon-bw%2femergency-icon-1.png&ehk=mmDTdBS63%2bmSQsyUsoWmLcLYW8xKmB8ywu2zyFGj2G8%3d&risl=&pid=ImgRaw&r=0",
        "number": "112",
        "description": "If you are facing a national emergency, stay calm and try to understand the situation around you. Move to a safe location if you are in immediate danger. Call the national emergency number 112, which is the all-in-one emergency helpline in India. Clearly explain the nature of the emergency. Mention if it involves medical help, police, fire, or any other urgent situation. Give your exact location or nearby landmarks. Provide details like what happened, when it happened, and who is affected. Mention if there are any injuries, threats, or dangers like fire, violence, or natural disasters. Answer all questions asked by the operator. Follow their instructions carefully. Stay on the call until they ask you to disconnect. If possible, provide your name and contact number for coordination. Stay alert and help others around you if it is safe to do so"
    },
    {
        "id": 4,
        "title": "Police",
        "image_url": "https://clipartcraft.com/images/police-logo-transparent-7.png",
        "number": "100",
        "description": "If you're in immediate danger, find a safe place first if possible. Take a deep breath and try to stay calm while speaking. Dial the Emergency Number: 100 or 112 (all-in-one emergency number). Tell the police: What happened (briefly and clearly) Where it happened (exact address or nearby landmarks) When it happened Who is involved (description of people, if any) Are weapons involved? Mention if there's any weapon or threat. Answer any questions from the operator. Do not hang up until they say you can. If they give you safety or medical instructions, follow them. They may tell you to stay put or move somewhere else safely. If safe, give your name and contact number for follow-up. You can remain anonymous if needed (depending on the country's policy)"
    },
    {
        "id": 6,
        "title": "Fire",
        "image_url": "https://static.vecteezy.com/system/resources/thumbnails/019/787/016/small_2x/fire-icon-on-transparent-background-free-png.png",
        "number": "102",
        "description": "If there is a fire, stay calm and act quickly. Raise an alarm to alert others nearby. If it is a small fire and safe to do so, try to extinguish it using a fire extinguisher. If the fire is spreading or you are unsure, evacuate the area immediately. Do not use lifts, use stairs to exit the building. Call the fire emergency number 101 or 112 from a safe location. Tell the operator that there is a fire. Give the exact location and any nearby landmarks. Explain what is burning and if anyone is trapped or injured. Follow all instructions given by the operator. Stay on the call until you are told to hang up. Do not go back inside until the fire department says it is safe. Help others evacuate if you can do so safely. Cover your nose and mouth with a cloth to avoid smoke inhalation. Stay low to the ground if there is heavy smoke"
    },
    {
        "id": 7,
        "title": "Ambulance",
        "image_url": "https://static.vecteezy.com/system/resources/previews/016/314/491/original/transparent-ambulance-icon-free-png.png",
        "number": "102 / 108",
        "description": "If someone is seriously injured or unwell, stay calm and check if they are conscious and breathing. Move them to a safe place if needed and possible. Call the ambulance emergency number 102 or 112 from your phone. Tell the operator that you need an ambulance. Clearly explain what happened and the condition of the person. Give the exact location and any nearby landmarks. Mention how many people are injured and if they are unconscious, bleeding, or not breathing. Follow the instructions given by the operator carefully. Do not hang up until they tell you to. If trained, give basic first aid while waiting for the ambulance. Keep the person calm and comfortable. Stay with them and keep monitoring their condition. Make space for the ambulance and guide them when they arrive"
    },
    {
        "id": 8,
        "title": "Disaster Management",
        "image_url": "https://th.bing.com/th/id/R.5209c537477f2b963061850329714ba3?rik=2EtFQait4n3Qhw&riu=http%3a%2f%2fgetdrawings.com%2ffree-icon%2fdisaster-icon-58.png&ehk=BHm%2f%2ff%2f17DISZnVZjbs5kaCxRRokSi%2f3UKhJ77j1PJ0%3d&risl=&pid=ImgRaw&r=0",
        "number": "1070",
        "description": "If a disaster occurs such as an earthquake, flood, cyclone, or building collapse, stay calm and act quickly. Ensure your safety and move to a safe place if possible. Help others only if it is safe to do so. Call the emergency number 112 and report the disaster. Clearly explain what type of disaster it is and describe the situation. Provide the exact location and nearby landmarks. Inform if people are trapped, injured, or need urgent help. Mention if buildings, roads, or bridges are damaged. Follow the instructions given by the operator. Do not hang up until you are told to. Stay alert for official warnings or announcements. Cooperate with emergency services when they arrive. If indoors, turn off gas, electricity, and water supply if safe to do so. Keep emergency supplies like water, food, torch, and first aid kit ready. Stay connected with family and local authorities for updates"
    },
    {
        "id": 9,
        "title": "Road Accident Assistance",
        "image_url": "https://cdn0.iconfinder.com/data/icons/accident/425/road-accident-car-003-1024.png",
        "number": "1073",
        "description": "If a road accident occurs, stay calm and ensure your own safety first. Move to a safe spot away from traffic if possible. Check if anyone is injured and call the emergency number 112 or 102 for an ambulance. Clearly tell the operator that a road accident has occurred. Give the exact location and nearby landmarks. Describe the number of people injured and their condition, such as unconscious, bleeding, or trapped. If someone is seriously injured, do not move them unless there is a danger like fire or traffic. Follow any instructions given by the operator. Do not hang up until they say you can. Provide your name and contact number if asked. While waiting for help, offer first aid if trained and safe to do so. Keep the injured person calm and reassure them. Guide emergency services to the spot when they arrive. Help manage traffic if needed, without putting yourself at risk"
    },
    {
        "id": 10,
        "title": "Railway Accident",
        "image_url": "https://cdn.iconscout.com/icon/premium/png-512-thumb/train-station-827029.png",
        "number": "139",
        "description": "If a railway accident occurs, stay calm and assess the situation around you. Move to a safe area away from the tracks, damaged coaches, or fire if there is any danger. Call the emergency number 112 immediately. Inform the operator that a railway accident has occurred. Give the exact location, such as the nearest station name, kilometer post, or any nearby landmark. Describe the type of accident, such as derailment, collision, or fire. Mention how many people are injured or trapped. Follow the instructions given by the operator and do not hang up until they tell you to. If possible, help others who are injured, but do not move them unless it is absolutely necessary. If you are inside a train and it is safe, use the emergency chain or alarm to alert the crew. Keep yourself and others calm and wait for emergency services to arrive. Cooperate fully with rescue teams and follow official instructions"
    },
    {
        "id": 11,
        "title": "Air Ambulance",
        "image_url": "https://cdn.iconscout.com/icon/premium/png-256-thumb/air-ambulance-3777345-3158157.png",
        "number": "9540161344",
        "description": "If someone needs urgent medical help in a remote or critical situation, and an air ambulance is required, stay calm and act quickly. First, ensure the patient is safe and stable as much as possible. Call the emergency number 112 or contact a registered air ambulance service directly. Clearly mention that you need an air ambulance and explain the medical emergency. Provide details about the patient's condition, such as unconsciousness, severe trauma, or the need for rapid transport to a hospital. Give the exact location, including GPS coordinates or nearby landmarks, especially if the area is hard to access by road. Mention if a landing area is available, like an open ground or helipad. Answer all questions from the operator and follow their instructions carefully. Do not hang up until they say you can. Prepare the landing area by clearing obstacles and keeping people away. Keep communicating with the air ambulance team and guide them once they are near. Ensure the patient is ready with basic medical details, ID, and any essential items"
    },
    {
        "id": 12,
        "title": "Women Helpline",
        "image_url": "https://cdn.iconscout.com/icon/premium/png-256-thumb/women-safety-4320006-3645361.png",
        "number": "1091",
        "description": "If a woman is in danger or needs urgent help due to harassment, domestic violence, abuse, or any other threat, stay calm and act immediately. Call the women's helpline number 1091 or the emergency number 112. Clearly explain the situation to the operator and mention if the woman is in immediate danger. Give the exact location and nearby landmarks. Describe what is happening, who is involved, and if the woman is injured or being threatened. Follow all instructions given by the operator. Do not hang up until they say you can. If possible, move the woman to a safe place and stay with her until help arrives. If you are the woman needing help, speak clearly and ask for police or women's help without fear. If calling is not possible, try to message or alert someone you trust. You can also use safety apps or panic buttons if available on your phone. Always prioritize safety and seek support from legal and medical services after the emergency is handled"
    },
    {
        "id": 13,
        "title": "Child Helpline",
        "image_url": "https://cdn.iconscout.com/icon/premium/png-256-thumb/child-support-982131.png",
        "number": "1098",
        "description": "If a child is in danger, lost, abused, or needs urgent help, stay calm and act quickly. Ensure the child is safe and away from immediate harm if possible. Call the child helpline number 1098, which is a 24-hour toll-free service in India. Clearly explain the situation to the operator. Mention what has happened, the age of the child (if known), and whether the child is injured, crying, scared, or unconscious. Provide the exact location and nearby landmarks. Tell them if the child is alone or if someone suspicious is involved. Follow all instructions given by the operator and do not hang up until they say you can. Stay with the child if it is safe to do so and try to comfort them. Do not force the child to speak if they are scared—wait for professionals to arrive. Cooperate with the rescue team and provide all necessary information. If the child is in your care, seek further help from child welfare authorities or NGOs for long-term safety and support"
    },
    {
        "id": 14,
        "title": "Senior Citizen Helpline",
        "image_url": "https://cdn.iconscout.com/icon/premium/png-256-thumb/son-meet-by-father-4297361-3565360.png",
        "number": "14567",
        "description": "If a senior citizen is in danger, injured, lost, or needs urgent help, stay calm and ensure their safety first. Move them to a safe and comfortable place if possible. Call the senior citizen helpline number 14567 or the emergency number 112. Clearly explain the situation to the operator. Mention if the person is sick, injured, lost, or being mistreated. Provide their age if known and describe their condition. Give the exact location and nearby landmarks. Inform if the person has any medical condition or needs special care. Follow the instructions given by the operator and do not hang up until told. Stay with the senior citizen and offer comfort and support. If they are unwell, keep them warm and hydrated. Guide emergency services when they arrive. If long-term help is needed, contact elderly care services, local authorities, or NGOs working for senior citizens"
    },
    {
        "id": 15,
        "title": "Cyber Crime Helpline",
        "image_url": "https://cdn.iconscout.com/icon/premium/png-256-thumb/cyber-crime-6525373-5431510.png",
        "number": "1930",
        "description": "If you or someone else is a victim of cybercrime, stay calm and do not respond to the attacker. Do not delete any messages, emails, or evidence. Take screenshots and save all related information. Call the cybercrime helpline number 1930 or report the incident online at www.cybercrime.gov.in Clearly explain what happened, such as online fraud, hacking, blackmail, cyberbullying, or identity theft. Provide details like website links, phone numbers, email addresses, and any payment information involved. Give your contact details and location if asked. Follow the instructions given by the operator or the website. Do not share personal or banking details with anyone claiming to be a helper unless verified. Inform your bank immediately if money is involved. Change your passwords and enable two-factor authentication. File a complaint with the local police station if needed. Stay alert and educate others to prevent future cybercrimes"
    }
]

# Insert the documents
try:
    result = collection.insert_many(documents)
    print(f"Successfully inserted {len(result.inserted_ids)} documents")
except Exception as e:
    print(f"An error occurred: {e}")