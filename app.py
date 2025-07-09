from flask import Flask, render_template, request
import wikipedia
import pyttsx3
import threading
import requests

app = Flask(__name__)
chat_history = []

# Replace with your actual API key
OPENWEATHER_API_KEY = "your_api_key_here"

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"The weather in {city} is {weather} with a temperature of {temp}°C."
    else:
        return "Sorry, I couldn't find the weather for that location."

@app.route("/")
def home():
    return render_template("index.html", chat=chat_history)

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["message"]

    if "weather" in user_input.lower():
        city = user_input.lower().replace("weather in", "").strip()
        answer = get_weather(city)
    else:
        try:
            answer = wikipedia.summary(user_input, sentences=2)
        except:
            answer = "Sorry, I couldn't find an answer."

    chat_history.append({"you": user_input, "tri": answer})
    threading.Thread(target=speak, args=(answer,)).start()
    return render_template("index.html", chat=chat_history)

if __name__ == "__main__":
    app.run(debug=True)