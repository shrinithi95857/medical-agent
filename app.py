from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# -------------------------------------------------
# Load Knowledge Base (PythonAnywhere safe)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KB_PATH = os.path.join(BASE_DIR, "knowledge_base.json")

with open(KB_PATH, "r", encoding="utf-8") as file:
    knowledge_base = json.load(file)

# -------------------------------------------------
# Reasoning Function (AI Decision Logic)
# -------------------------------------------------
def diagnose(symptoms):
    results = []

    for disease, data in knowledge_base.items():
        disease_symptoms = set(data.get("symptoms", []))
        match_count = len(set(symptoms).intersection(disease_symptoms))

        if match_count > 0:
            confidence = round((match_count / len(disease_symptoms)) * 100, 1)
            results.append((disease, data.get("advice", ""), confidence))

    return sorted(results, key=lambda x: x[2], reverse=True)

# -------------------------------------------------
# Flask Routes
# -------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():
    user_input = request.form.get("symptoms", "").lower()
    symptoms = [s.strip() for s in user_input.split(",") if s.strip()]
    results = diagnose(symptoms)

    return render_template(
        "result.html",
        results=results,
        symptoms=symptoms
    )

# -------------------------------------------------
# Local run (ignored by PythonAnywhere)
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)