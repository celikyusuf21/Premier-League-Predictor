import requests
from datetime import datetime

def get_today_matches():
    """
    SportsDB üzerinden Premier League (EPL) için
    sıradaki 10 maçı getirir.
    """
    url = "https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php"
    
    params = {
        
        "d": datetime.now().strftime("%Y-%m-%d"),
        "s": "Soccer"
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    matches = []

    for event in data.get("events", [])[:200]:
    if str(event.get("idLeague")) != "4328":
        continue
    matches.append({
        "home": event["strHomeTeam"],
        "away": event["strAwayTeam"],
        "status": event.get("strStatus") or "NS"
    })

    return matches