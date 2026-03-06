import requests

API_KEY = "dddec5da64ded80fb8a954dc87d4b45e"


def get_epl_odds():

    url = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds"

    params = {
        "apiKey": API_KEY,
        "regions": "eu",
        "markets": "h2h"
    }

    res = requests.get(url, params=params)

    return res.json()

def implied_probability(odds):

    return round(1 / odds, 4)

def value_bet_score(model_prob, bookmaker_odds):

    market_prob = implied_probability(bookmaker_odds)

    value = model_prob - market_prob

    return round(value * 100, 2)