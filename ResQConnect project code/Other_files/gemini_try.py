from flask import Flask, render_template, request, jsonify
from gemini_api import generate_gemini_response  # Import function

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.json.get("prompt")
    response = generate_gemini_response(prompt)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
