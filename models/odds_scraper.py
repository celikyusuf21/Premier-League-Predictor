import requests
from bs4 import BeautifulSoup

def scrape_odds():

    url = "https://www.oddsportal.com"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    return [o.text for o in soup.select(".odds")]