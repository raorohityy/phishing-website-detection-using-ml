from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pickle
import re
import os
import json
from flask_mail import Mail, Message
from dotenv import load_dotenv


load_dotenv(os.path.join(os.path.dirname(__file__), '.env'), override=True)

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend/static')
CORS(app, resources={r"/*": {"origins": "*"}}) # Enable CORS for all routes with explicit permissions

# ===============================
# Load Model and Vectorizer
# ===============================
@app.route('/favicon.ico')
def favicon():
    return '', 204


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# vector = pickle.load(open(os.path.join(BASE_DIR, "vectorizer.pkl"), 'rb'))
# model = pickle.load(open(os.path.join(BASE_DIR, "phishing.pkl"), 'rb'))

# Global variables for lazy loading
vector = None
model = None

def get_vectorizer():
    global vector
    if vector is None:
        print("Loading vectorizer...")
        vector = pickle.load(open(os.path.join(BASE_DIR, "vectorizer.pkl"), 'rb'))
    return vector

def get_model():
    global model
    if model is None:
        print("Loading model...")
        model = pickle.load(open(os.path.join(BASE_DIR, "phishing.pkl"), 'rb'))
    return model

# ===============================
# Email Configuration (Contact Page)
# ===============================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# Debug prints to verify loading (Temporary)
print(f"DEBUG: MAIL_USERNAME value: {app.config['MAIL_USERNAME']}")
if app.config['MAIL_PASSWORD']:
    print(f"DEBUG: MAIL_PASSWORD loaded (length: {len(app.config['MAIL_PASSWORD'])})")

mail = Mail(app)

# ===============================
# Stats Handling (Saved Persistently)
# ===============================
stats_file = os.path.join(BASE_DIR, "stats.json")

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
# API ROUTES
# ===============================

@app.route("/api/stats", methods=["GET"])
def api_stats():
    return jsonify(stats)

@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "No URL provided"}), 400
    
    url = data['url']
    cleaned_url = re.sub(r'^https?://(www\.)?', '', url)
    result = get_model().predict(get_vectorizer().transform([cleaned_url]))[0]

    global stats
    stats["total"] += 1
    
    prediction_message = ""
    is_phishing = False

    if result == "good":
        stats["safe"] += 1
        prediction_message = "✅ This is a Safe and Trusted Website."
    elif result == "bad":
        stats["phishing"] += 1
        is_phishing = True
        prediction_message = "⚠️ Warning! This is a Phishing Website."
    else:
        prediction_message = "❌ Something went wrong during prediction."

    save_stats()
    
    return jsonify({
        "result": result,
        "message": prediction_message,
        "is_phishing": is_phishing,
        "stats": stats
    })

# ===============================
# LEGACY ROUTES (Optional / Fallback)
# ===============================

@app.route("/", methods=["GET", "POST"])
def index():
    global stats
    # For backward compatibility or testing
    return render_template("index.html", predict=None, stats=stats)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    # Keep contact logic if needed, or convert to API too
    if request.method == "POST":
        email = request.form.get("email")
        message = request.form.get("message")
        
        # Supporting JSON for contact API if needed later
        if not email and request.is_json:
            data = request.get_json()
            email = data.get("email")
            message = data.get("message")

        msg = Message(subject="📩 Phishing Detector - New Message",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[app.config['MAIL_USERNAME']],
                      body=f"From: {email}\n\n{message}")
        try:
            mail.send(msg)
            if request.is_json:
                return jsonify({"success": True})
            return render_template("contact.html", success=True)
        except Exception as e:
            if request.is_json:
                return jsonify({"success": False, "error": str(e)}), 500
            return render_template("contact.html", success=False, error=str(e))

    return render_template("contact.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    app.run(debug=True)
