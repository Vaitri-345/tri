from flask import Flask, render_template, request
import wikipedia
import pyttsx3
import threading

app = Flask(__name__)
chat_history = []

# Voice speaking function in a safe thread
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

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

    # Speak using a separate thread to avoid RuntimeError
    threading.Thread(target=speak, args=(answer,)).start()

    return render_template("index.html", chat=chat_history)

if __name__ == "__main__":
    app.run()
