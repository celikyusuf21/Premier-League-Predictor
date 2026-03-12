import requests

def get_today_matches():
    url = "https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php"
    
    params = {
        "id": "4328"  # Premier League ID
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    matches = []

    for event in data.get("events", [])[:10]:
        if str(event.get("idLeague")) != "4328":
            continue
        matches.append({
            "home": event["strHomeTeam"],
            "away": event["strAwayTeam"],
            "status": "NS"
        })

    return matches