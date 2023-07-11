import os
import requests
import urllib.parse

def lookup(type):
     # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={urllib.parse.quote_plus(type)}&aqi=yes"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        weather = response.json()
        return weather
    except (KeyError, TypeError, ValueError):
        return None

