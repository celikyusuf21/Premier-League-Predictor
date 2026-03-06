import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")

URL = "https://v3.football.api-sports.io/fixtures"


def get_today_matches():

    if not API_KEY:
        print("Football API Key not found")
        return []

    try:

        headers = {
            "x-apisports-key": API_KEY
        }

        params = {
            "league": 39,
            "season": 2025,
            "status": "NS",
            "timezone": "Europe/London"
        }

        res = requests.get(
            URL,
            headers=headers,
            params=params,
            timeout=10
        )

        data = res.json()

        matches = []

        for m in data.get("response", []):

            matches.append({
                "home": m["teams"]["home"]["name"],
                "away": m["teams"]["away"]["name"]
            })

        return matches

    except Exception as e:

        print("Football API error:", e)
        return []