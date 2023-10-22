import os
import requests
import urllib.parse
import datetime
from functools import wraps
from flask import render_template, session, flash
import sqlite3
import json

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

# Add city in favourite table in database of user
def add(city):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO favourite (id ,city) VALUES (? ,?)", (session["user_id"], city))
        conn.commit()
    except Exception as e:
        conn.rollback()
        flash("Something went wrong!", "danger")
        return render_template("favourite.html")
    finally:
        conn.close()
        flash("City add Sucessfully!!", "success")

# remove city from favourite table form user database
def remove(city):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM favourite WHERE id = ? AND city = ?", (session['user_id'], city))
        conn.commit()
        flash("City Deleted Sucessfully!!", "success")
    except Exception as e:
        conn.rollback()
        flash("Something went wrong!", "danger")
    finally:
        conn.close()
        

# Given a array of all favourite cities user have in his favourite list
def favArray() :
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    try:
        cur.execute("SELECT city FROM favourite WHERE id = (?)", (session['user_id'], ))
        conn.commit()
        cities = cur.fetchall()
    except Exception as e:
        conn.rollback()
        flash("Something went wrong!", "danger")
        return render_template("favourite.html")
    finally:
        conn.close()
    
    cities = [t[0] for t in cities]
    return json.dumps(cities)

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

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Please Login/Register first to access your Favourite Feature.", "danger")
            return render_template("login.html")
        return f(*args, **kwargs)
    return decorated_function