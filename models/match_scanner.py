import requests
from datetime import datetime

API_KEY = "YOUR_API_KEY"

def get_today_matches():

    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

    query = {
        "league": "39",   # Premier League
        "season": "2024",
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=query)

    data = response.json()

    matches = []

    for match in data["response"]:

        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]

        matches.append({
            "home": home,
            "away": away
        })

    return matches