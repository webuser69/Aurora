from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re
import random
import wikipedia
import os  # NEW

# Import your existing modules
from open_task import open_web, open_app, close_app
from greet import greetings, greeting, greets, name, hru
from speak import speak
from maths import calculate, advanced_calculation, trigonometry, geometry, convert_units

app = Flask(__name__, static_folder="frontend", template_folder="frontend")
CORS(app)  # Allow frontend requests

# ---------------- PROCESS MESSAGE FUNCTION ---------------- #
def process_message(user, mute=False):
    """Process the user message using existing rule-based logic"""
    user = user.strip().lower()
    user_input = re.sub(r"(.)\1+", r"\1", user)

    # ---- GREETINGS ----
    if any(greet in user_input.split() for greet in greeting):
        result = f"{random.choice(greetings).capitalize()}, {random.choice(greets)}"

    # ---- CLOSE APP ----
    elif "close" in user or "exit" in user or "shutdown" in user:
        result = close_app(user)
        if not result:
            result = "Sorry, I couldn't close that app. Try again."

    # ---- OPEN APP/WEB ----
    elif "open" in user or "launch" in user:
        result = open_web(user)
        if not result:
            result = open_app(user)
        if not result:
            result = "Sorry, I couldn't open that. Try another site or app."

    # ---- BASIC CALCULATIONS ----
    elif any(word in user for word in ["plus", "+", "minus", "-", "times", "x", "*", "divide", "/", "mod", "power", "calculate", "half", "third", "quarter", "^"]):
        result = f"The result is {calculate(user)}"

    # ---- ADVANCED CALCULATIONS ----
    elif any(word in user for word in ["square root", "factorial", "log", "ln", "exp", "exponential", "abs", "absolute", "round", "ceil", "floor"]):
        result = f"The result is {advanced_calculation(user)}"

    # ---- TRIGONOMETRY ----
    elif any(func in user for func in ["sin", "cos", "tan"]):
        result = f"The result is {trigonometry(user)}"

    # ---- GEOMETRY ----
    elif any(shape in user for shape in ["area", "volume"]):
        result = f"The result is {geometry(user)}"

    # ---- UNIT CONVERSIONS ----
    elif any(unit in user for unit in ["meters to feet", "feet to meters", "celsius to fahrenheit", "fahrenheit to celsius", "kilograms to pounds", "pounds to kilograms"]):
        result = f"The result is {convert_units(user)}"

    # ---- BASIC INFO ----
    elif "your name" in user_input:
        result = random.choice(name).capitalize()
    elif "who are you" in user_input:
        result = f"{random.choice(name).capitalize()}, your personal assistant"
    elif "how are you" in user_input:
        result = random.choice(hru).capitalize()

    # ---- WIKIPEDIA FALLBACK ----
    else:
        try:
            summary = wikipedia.summary(user, sentences=2)
            result = summary
        except wikipedia.exceptions.DisambiguationError as e:
            result = f"Your query is ambiguous. Did you mean: {', '.join(e.options[:3])}?"
        except wikipedia.exceptions.PageError:
            result = "Sorry, I don't understand."
        except Exception:
            result = "Sorry, I couldn't fetch information from Wikipedia."

    # ---- SPEAK RESULT ----
    if not mute:
        speak(result)
    return result

# ---------------- FRONTEND ROUTES ---------------- #
@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("frontend", path)

# ---------------- API ROUTE ---------------- #
@app.route("/message", methods=["POST"])
def message():
    data = request.json
    user_message = data.get("message", "")
    mute = data.get("Mute", False)
    response = process_message(user_message, mute)
    return jsonify({"response": response})

# ---------------- RUN SERVER ---------------- #
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render provides PORT
    app.run(host="0.0.0.0", port=port)