from flask import Flask, request, jsonify, render_template, session
from chatbot_model import get_response
import os

from google import genai

app = Flask(__name__)
app.secret_key = 'secret_key'

# Configure Gemini API
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    use_reasoning = data.get("reasoning", False)

    if "history" not in session:
        session["history"] = []

    if use_reasoning:
        try:            
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[message]
            ).text

            print(response)
            
        except Exception as e:
            response = "Gemini error: " + str(e)
    else:
        response = get_response(message, session["history"])

    session["history"].append({"user": message, "bot": response})
    session.modified = True

    return jsonify({"response": response})
