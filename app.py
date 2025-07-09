from flask import Flask, render_template, request
import wikipedia

app = Flask(__name__)
chat_history = []

@app.route("/")
def home():
    return render_template("index.html", chat=chat_history)

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["message"]
    try:
        answer = wikipedia.summary(user_input, sentences=2)
    except:
        answer = "Sorry, I couldn't find an answer."

    chat_history.append({"you": user_input, "tri": answer})
    return render_template("index.html", chat=chat_history)

if __name__ == "__main__":
    app.run(debug=True)
