import google.generativeai as genai
import json

# ✅ Load API key from config.json
with open('config.json', 'r') as c:
    config = json.load(c)
    api_key = config["gemini_api"]

genai.configure(api_key=api_key)

# Load the Gemini model
model = genai.GenerativeModel('models/gemma-3-12b-it')

def remove_asterisks(text):
    return text.replace('*', '')

def generate_gemini_response(prompt):
    if not prompt:
        return "Error: Empty prompt provided."
    try:
        response = model.generate_content(prompt)
        clean_response = remove_asterisks(response.text)
        return clean_response
    except Exception as e:
        return f"Error: {e}"
