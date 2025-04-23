from flask import Flask, render_template, request, jsonify
from chatbot_model import get_response

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form.get('message', '')
    answer = get_response(question)
    return jsonify({'reply': answer})

if __name__ == '__main__':
    app.run(debug=True)
