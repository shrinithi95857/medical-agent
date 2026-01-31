from flask import Flask, render_template, request
import json

app = Flask(__name__)

# --- Load Knowledge Base from JSON ---
with open("knowledge_base.txt", "r") as file:
    knowledge_base = json.load(file)

# --- Reasoning Function (AI Decision Logic) ---
def diagnose(symptoms):
    results = []
    for disease, data in knowledge_base.items():
        match_count = len(set(symptoms).intersection(data["symptoms"]))
        if match_count > 0:
            confidence = round((match_count / len(data["symptoms"])) * 100, 1) 
            results.append((disease, data["advice"], confidence))
    return sorted(results, key=lambda x: x[2], reverse=True)

# --- Flask Routes ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():
    user_input = request.form["symptoms"].lower()
    symptoms = [s.strip() for s in user_input.split(",") if s.strip()]
    results = diagnose(symptoms)
    return render_template("result.html", results=results, symptoms=symptoms)

if __name__ == "__main__":
    app.run(debug=True)
