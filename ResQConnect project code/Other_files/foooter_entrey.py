from pymongo import MongoClient

# Connect to MongoDB
url = "mongodb://localhost:27017/"
client = MongoClient(url)
db = client["emergencyDB"]
collection = db["info_sections"]

# Documents with manually assigned slugs
documents = [
    {
        "title": "Copyright",
        "slug": "copyright",
        "description": "© 2025 ResQConnect. All rights reserved. This platform, including its content, design, and functionality, is protected under applicable copyright laws. Unauthorized use or reproduction is strictly prohibited."
    },
    {
        "title": "Disclaimer",
        "slug": "disclaimer",
        "description": "ResQConnect serves as a bridge to help users connect with emergency services such as police, ambulance, disaster relief, and more. While we strive for accuracy and timely response, we do not guarantee outcomes, service availability, or real-time assistance. Users are advised to directly contact official helplines in urgent situations. We are not liable for any loss or delay resulting from the use of this service."
    },
    {
        "title": "Privacy Policy",
        "slug": "privacy-policy",
        "description": "ResQConnect respects your privacy. Any personal information such as name, location, or contact details submitted via this platform is used solely for emergency response purposes and will not be shared without consent, except with authorized agencies. We implement reasonable security measures to protect your data from misuse or unauthorized access."
    },
    {
        "title": "Terms and Conditions",
        "slug": "terms-and-conditions",
        "description": "By using ResQConnect, you agree to use the platform responsibly and only for genuine emergency assistance. Misuse of the service, false reporting, or impersonation may result in legal action. The platform is intended to assist and not replace any official emergency services. Your continued use implies acceptance of these terms."
    },
    {
        "title": "Feedback",
        "slug": "feedback",
        "description": "We welcome your feedback to improve ResQConnect. If you have suggestions, complaints, or want to report an issue, please use our Feedback Form or email us at support@resqconnect.com. Your input helps us serve you better."
    },
    {
        "title": "Help",
        "slug": "help",
        "description": "Need assistance using ResQConnect? Visit our Help Center for guides on how to raise alerts, contact emergency services, and understand platform features. For urgent support, you can also call our helpline at 1800-XXX-XXXX."
    },
    {
        "title": "ResQConnect: One-Stop Emergency Service",
        "slug": "resqconnect-one-stop-emergency-service",
        "description": "ResQConnect is a one-stop emergency assistance service designed to provide immediate help in critical situations such as medical emergencies, road accidents, natural disasters, cybercrime, and threats to women, children, or senior citizens. It connects users directly with appropriate emergency services through a single, easy-to-use platform. By integrating various helplines like police, ambulance, and fire services, ResQConnect ensures faster response and improved safety. Users can quickly raise an alert, share their location, and get guided support through real-time updates and verified responders. It also offers features like first aid tips, live tracking, and category-specific help like for women, senior citizens, and children. With ResQConnect, help is just a click away — anytime, anywhere."
    }
]

# Insert documents into the collection
collection.insert_many(documents)

print("Documents with slugs inserted successfully.")
