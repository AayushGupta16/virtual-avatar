from flask import Flask, render_template, request
from starter import process_message

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/chat", methods=["GET", "POST"])
def chat():
    user_message = request.form["message"]
    chat_text, audio_data = process_message(user_message)
    return chat_text


if __name__ == "__main__":
    app.run()