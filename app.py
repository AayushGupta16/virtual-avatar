from flask import Flask, render_template, request
from starter import process_message

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('chat.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    response = process_message(user_message)
    return render_template('chat.html', response=response)