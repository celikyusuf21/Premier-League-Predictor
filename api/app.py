import sys
import os

from flask_cors import CORS
from flask import request, Flask, jsonify
import joblib
import numpy as np

# Path fix ⭐
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.database import db, User
from payment import create_checkout


# -------------------------
# APP INIT
# -------------------------

app = Flask(__name__)
CORS(app)

# -------------------------
# DATABASE SETUP
# -------------------------

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# -------------------------
# MODEL LOAD
# -------------------------

base_dir = os.path.dirname(__file__)
model_path = os.path.join(base_dir, "../models/model.pkl")

model = joblib.load(model_path)


# -------------------------
# HOME
# -------------------------

@app.route("/")
def home():
    return "🔥 AI Betting API Running"


# -------------------------
# PREDICTION
# -------------------------

@app.route("/predict")
def predict():

    try:

        sample = np.array([[
            1.5,1.2,
            12,9,
            6,4,
            7,5,
            2,1
        ]])

        prob = model.predict_proba(sample)[0]

        home = round(prob[0] * 100, 2)
        draw = round(prob[1] * 100, 2)
        away = round(prob[2] * 100, 2)

        confidence = max(home, draw, away)

        strength = "LOW"

        if confidence > 70:
            strength = "HIGH"
        elif confidence > 50:
            strength = "MEDIUM"

        return jsonify({
            "home_win": home,
            "draw": draw,
            "away_win": away,
            "confidence": confidence,
            "signal_strength": strength
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# -------------------------
# LIVE MATCHES
# -------------------------

@app.route("/live")
def live_matches():

    teams = [
        "Arsenal","Aston Villa","Bournemouth","Brentford","Brighton",
        "Chelsea","Crystal Palace","Everton","Fulham","Liverpool",
        "Man City","Man United","Newcastle","Nottingham Forest",
        "Tottenham","West Ham","Wolves","Burnley","Luton","Sheffield United"
    ]

    matches = []

    for i in range(3):

        home = np.random.choice(teams)
        away = np.random.choice(teams)

        while away == home:
            away = np.random.choice(teams)

        matches.append({
            "home": home,
            "away": away,
            "status": "LIVE",
            "minute": int(np.random.randint(1,90))
        })

    return jsonify({"matches": matches})


# -------------------------
# PREMIUM CHECK
# -------------------------

@app.route("/premium-check", methods=["POST"])
def premium_check():

    try:
        data = request.json
        username = data.get("username")

        user = User.query.filter_by(username=username).first()

        return jsonify({
            "premium": bool(user and user.is_premium)
        })

    except:
        return jsonify({"premium": False})


# -------------------------
# STRIPE VIP PAYMENT
# -------------------------

@app.route("/buy-vip")
def buy_vip():

    try:
        url = create_checkout()

        return jsonify({
            "checkout_url": url
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })


# -------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)