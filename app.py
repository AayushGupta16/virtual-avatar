from flask import Flask, render_template, request
from starter import process_message

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/chat", methods=["GET", "POST"])
def chat():
    user_message = request.form["message"]
    print("Herro")
    return process_message(user_message)


if __name__ == "__main__":
    app.run()
