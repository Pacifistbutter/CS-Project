import os
import requests
import urllib.parse
import datetime

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


def search(name):
    # Contact the website via API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={urllib.parse.quote_plus(name)}&days=3&aqi=yes&alerts=no"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None
    
    # Parse response
    try:
        places = response.json()
        return places
    except (KeyError, TypeError, ValueError):
        return None

# A function which takes date and return its day
def dateToDay(date):
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    day_of_week = date_obj.strftime("%a")
    return day_of_week