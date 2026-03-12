import sys
import os

# Path fix ⭐ (models/ klasöründen import yapmadan önce olmalı)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask_cors import CORS
from flask import request, Flask, jsonify
import joblib
import numpy as np
#from models.football_api import get_today_matches
from models.sportsdb_api import get_today_matches
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
    try:
        matches = get_today_matches()
        return jsonify({"matches": matches})
    except Exception as e:
        return jsonify({"matches": [], "error": str(e)}), 500


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