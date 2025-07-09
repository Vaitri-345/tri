from flask import Flask, request, render_template
import wikipedia

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    if request.method == "POST":
        query = request.form.get("question")
        try:
            answer = wikipedia.summary(query, sentences=2)
        except wikipedia.exceptions.DisambiguationError:
            answer = "Too many results. Please be specific."
        except wikipedia.exceptions.PageError:
            answer = "Nothing found on that topic."
        except:
            answer = "Something went wrong."
    return render_template("index.html", answer=answer)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
