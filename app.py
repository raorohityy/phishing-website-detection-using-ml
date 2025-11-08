from flask import Flask, render_template, request
import pickle
import re
import os
import json
from flask_mail import Mail, Message

app = Flask(__name__)

# ===============================
# Load Model and Vectorizer
# ===============================
vector = pickle.load(open("vectorizer.pkl", 'rb'))
model = pickle.load(open("phishing.pkl", 'rb'))

# ===============================
# Email Configuration (Contact Page)
# ===============================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # your Gmail
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # app password
mail = Mail(app)

# ===============================
# Stats Handling (Saved Persistently)
# ===============================
stats_file = "stats.json"

# Default counters
stats = {"total": 0, "safe": 0, "phishing": 0}

# Load saved stats from file
def load_stats():
    global stats
    if os.path.exists(stats_file):
        with open(stats_file, "r") as f:
            stats.update(json.load(f))

# Save stats to file
def save_stats():
    with open(stats_file, "w") as f:
        json.dump(stats, f)

# Load stats initially
load_stats()

# ===============================
# ROUTES
# ===============================

@app.route("/", methods=["GET", "POST"])
def index():
    global stats
    prediction = None

    if request.method == "POST":
        url = request.form["url"]
        cleaned_url = re.sub(r'^https?://(www\.)?', '', url)
        result = model.predict(vector.transform([cleaned_url]))[0]

        # Update stats dynamically
        stats["total"] += 1
        if result == "good":
            stats["safe"] += 1
            prediction = "✅ This is a Safe and Trusted Website."
        elif result == "bad":
            stats["phishing"] += 1
            prediction = "⚠️ Warning! This is a Phishing Website."
        else:
            prediction = "❌ Something went wrong during prediction."

        # Save the updated counts
        save_stats()

    return render_template("index.html", predict=prediction, stats=stats)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        email = request.form["email"]
        message = request.form["message"]

        msg = Message(subject="📩 Phishing Detector - New Message",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[app.config['MAIL_USERNAME']],
                      body=f"From: {email}\n\n{message}")
        try:
            mail.send(msg)
            return render_template("contact.html", success=True)
        except Exception as e:
            return render_template("contact.html", success=False, error=str(e))

    return render_template("contact.html")


# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    app.run(debug=True)
