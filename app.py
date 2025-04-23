from flask import Flask, render_template, request, jsonify, session
from chatbot_model import get_response

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = 'asdhju1hj29ue1'
app.config['GEMINI_API_KEY'] = os.environ.get('GEMINI_API_KEY')

@app.route('/')
def home():
    # Initialize session history
    if 'history' not in session:
        session['history'] = []
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form.get('message', '').strip()
    # Retrieve chat history from session
    history = session.get('history', [])
    answer = get_response(question, history=history)
    # Update history
    history.append({'user': question, 'bot': answer})
    # Keep only last 5 exchanges
    session['history'] = history[-5:]
    return jsonify({'reply': answer})

if __name__ == '__main__':
    app.run(debug=True)
