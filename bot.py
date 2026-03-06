import requests
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from models.signal_engine import generate_signal
from models.football_api import get_today_matches

# -------------------------
# CONFIG
# -------------------------

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("API_FOOTBALL_KEY")
API_URL = "http://127.0.0.1:5001"

CHANNEL_ID = -1003718264705

if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN not found in .env file")


# -------------------------
# PREMIUM CHECK FUNCTION
# -------------------------

def check_premium(username):

    if not username:
        return False

    try:

        res = requests.post(
            f"{API_URL}/premium-check",
            json={"username": username},
            timeout=5
        )

        if res.status_code != 200:
            return False

        return res.json().get("premium", False)

    except:
        return False


# -------------------------
# START COMMAND
# -------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 AI Betting Signal Bot Ready\n\n"
        "/signal → VIP Prediction\n"
        "/vip → Buy VIP Access\n"
        "/matches → Premier League Matches"
    )


# -------------------------
# MATCHES COMMAND ⚽ (FIXED VERSION)
# -------------------------

async def matches(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        games = get_today_matches()

        if not games:
            await update.message.reply_text("❌ No matches found")
            return

        msg = "⚽ Premier League Matches\n\n"

        for g in games:
            msg += f"🏟 {g['home']} vs {g['away']}\n"

        await update.message.reply_text(msg)

    except Exception as e:
        print("Matches error:", e)
        await update.message.reply_text("❌ Match API error")


# -------------------------
# SIGNAL COMMAND
# -------------------------

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        username = update.message.from_user.username

        if not check_premium(username):

            await update.message.reply_text(
                "❌ VIP Required\nUse /vip to buy access"
            )
            return

        res = requests.get(
            f"{API_URL}/predict",
            timeout=5
        )

        data = res.json()

        odds = 2.10

        signal_data = generate_signal(
            data["home_win"] / 100,
            odds
        )

        msg = f"""
🔥 VIP SIGNAL

🏠 Home Win: {data['home_win']}%
🤝 Draw: {data['draw']}%
🚀 Away Win: {data['away_win']}%

⭐ Confidence: {signal_data['confidence']}%
⚡ Signal Strength: {signal_data['signal']}
💰 Value Edge: {signal_data['value_edge']}%
"""

        await update.message.reply_text(msg)

    except Exception as e:
        print(e)
        await update.message.reply_text("❌ Signal error")


# -------------------------
# VIP BUY
# -------------------------

async def vip(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        res = requests.get(f"{API_URL}/buy-vip")

        url = res.json().get("checkout_url")

        await update.message.reply_text(f"💎 VIP Payment:\n{url}")

    except:
        await update.message.reply_text("Payment error")


# -------------------------
# AUTO SIGNAL
# -------------------------

async def auto_signal(context: ContextTypes.DEFAULT_TYPE):

    try:

        res = requests.get(f"{API_URL}/predict")

        data = res.json()

        odds = 2.10

        signal_data = generate_signal(
            data["home_win"] / 100,
            odds
        )

        msg = f"""
🚨 AUTO VIP SIGNAL

🏠 Home Win: {data['home_win']}%
🤝 Draw: {data['draw']}%
🚀 Away Win: {data['away_win']}%

⭐ Confidence: {signal_data['confidence']}%
⚡ Signal Strength: {signal_data['signal']}
💰 Value Edge: {signal_data['value_edge']}%
"""

        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=msg
        )

    except:
        print("Auto signal error")


# -------------------------
# BOT START
# -------------------------

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("signal", signal))
app.add_handler(CommandHandler("vip", vip))
app.add_handler(CommandHandler("matches", matches))

job_queue = app.job_queue

if job_queue:

    job_queue.run_repeating(
        auto_signal,
        interval=1800,
        first=10
    )

print("🔥 Bot Ready")

app.run_polling()