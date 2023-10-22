from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_mail import Message, Mail
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import search, dateToDay, login_required, add, remove, favArray
from flask_cors import CORS
import sqlite3
import os
import random
from dotenv import load_dotenv

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5000"}}) 

API_KEY = os.environ["API_KEY"]
app.config["SECRET_KEY"] = os.urandom(24)

# Set your static folder path
app.config['UPLOAD_FOLDER'] = 'static' 

# Session Configure
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

load_dotenv()

# Mail Configuration - Getting some big problems We need to implement OAuth 2.0 which will take some work
app.config["MAIL_DEFAULT_SENDER"] = os.environ["MAIL_DEFAULT_SENDER"]
app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
mail = Mail(app)

# main page
@app.route("/")
def index():
    # if not session.get("user_id"):
    #     return redirect("/login")

    return redirect('/today')

# Login page
# Validate the email and password (pwd is check using hash pwd)
# set session["user_id"]
@app.route("/login", methods=["GET", "POST"])
def login():

    if session.get("code", None):
        code = request.form.get('code')
        if not code:
            flash("Please enter your code", "danger")
            return render_template("verifcode.html")

        if not int(code) == session.get('code', None):
            flash("Invaild code", "danger")
            return render_template("verifcode.html")
        
        session.pop('code')
        flash("You code was vaild now you can resent your password!", "success")
        return render_template("resetpassword.html")

    if request.method == "POST":
        email = request.form.get("email")
        pwd = request.form.get("pwd")

        if not email or not pwd:
            flash("Please input information", "danger")
            return render_template("login.html")
        
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        try:
            cur.execute("SELECT * FROM users WHERE email = ?", (email,))

            row = cur.fetchall()

            if not row:
                conn.close()
                flash("Your email address is not registered", "danger")
                return render_template("login.html")

            if not check_password_hash(row[0][2], pwd):
                flash("Your password is incorrect please try again!", "danger")
                return render_template("login.html")
        
            session["user_id"] = row[0][0]    
            flash("You have sucessfully logged in", "success")
            conn.commit()

        except Exception as e:
            conn.rollback()
            flash("Some thing went wrong while logging", "danger")
            return render_template("login.html")
        
        finally:
            conn.close()
        
        return redirect('/')
    
    else:
        return render_template("login.html")


# logging the user out
@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    
    if session.get('code', None):
        code = request.form.get('code')
        if not code:
            flash("Please enter your code", "danger")
            return render_template("verifcode.html")

        if not int(code) == session.get('code', None):
            flash("Invaild code", "danger")
            return render_template("verifcode.html")

        email = session.get("email")
        pwd = session.get("pwd")

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        try:
            phash = generate_password_hash(pwd)

            cur.execute("INSERT INTO users (email, hash) VALUES (?, ?)", (email, phash))
            cur.execute("SELECT id FROM users WHERE email = (?)", (email, ))

            result = cur.fetchall()
            session["user_id"] = result[0][0]
            conn.commit()
            flash("Registered And Email Verification Sucessfully", "success")

        except Exception as e:
            conn.rollback()
            flash("Something went wrong while registering!", "danger")
            return render_template("register.html")
        
        finally:
            conn.close()
            session.pop('code')
            session.pop('pwd')
            
        return redirect("/")

    if request.method == "POST":
        email = request.form.get("email")
        pwd = request.form.get("pwd")
        rpwd = request.form.get("rpwd")

        if not email or not pwd or not rpwd:
            flash("Please enter Your information!", "danger")
            return render_template("register.html")

        if pwd != rpwd:
                flash("Passwords Not Equal!", "danger")
                return render_template("register.html")
        
        # Checking if the user is already registed or not
        # Continuing to register is user is not already registered
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE email = ?", (email, ))
            ans = cur.fetchall()

            if ans:
                conn.rollback()
                flash("This email has already been registered", "danger")
                return render_template("register.html")
            conn.commit()

        except Exception as e:
            conn.rollback()
            flash("Something went wrong while registering!", "danger")
            return render_template("register.html")
        
        finally:
            conn.close()

        session["email"] = email
        session["pwd"] = pwd
        session["code"] = random.randint(100000, 999999)

        msg = Message(subject="Your Verification Code", recipients=[email])
        msg.html = render_template("email.html")
        
        try:
            mail.send(msg)
            return render_template("verifcode.html")
        except Exception as e:
            print(e)
            flash(f"An Error occurred {e}")
            return render_template("register.html")

    else:
        return render_template("register.html")


@app.route("/today", methods=["GET", "POST"])
def today():

    if request.method == "POST":
        city = request.form.get("city")
        if not city:
            latitude = request.form.get("latitude")
            longitude = request.form.get("longitude")
            if not latitude:
                flash("Please enter the city you want see weather of!", "warning")
                return render_template("today.html")
            q = f"{latitude},{longitude}"
        else:
            q = f"{city}"
        weather = search(q)
        if not weather:
            flash("you got nothing!")
            return render_template("today.html")
 
        location = weather["location"]
        current = weather["current"]
        condition = current["condition"]
        airQua = current["air_quality"]

        day1 = weather["forecast"]["forecastday"][0]
        day2 = weather["forecast"]["forecastday"][1]
        day3 = weather["forecast"]["forecastday"][2]

        context = {
            "API_KEY": API_KEY,
            "isweather": True,
            "location": location,
            "current": current,
            "condition": condition,
            "airQua": airQua,
            "day1": day1,
            "day2": day2,
            "day3": day3,
            "dateToDay": dateToDay
        }
            
        return render_template("today.html", **context)
    else:
        
        return render_template("today.html", isweather=False, API_KEY=API_KEY)
    
        
@app.route("/map", methods=['GET', 'POST'])
def map():
    if request.method == "POST":
        city = request.form.get("city")
        if not city:
            latitude = request.form.get("latitude")
            longitude = request.form.get("longitude")
            if not latitude:
                flash("Please enter the city you want see weather of!", "warning")
                return render_template("today.html")
            q = f"{latitude},{longitude}"
        else:
            q = f"{city}"
        weather = search(q)
        if not weather:
            flash("you got nothing!")
            return render_template("today.html")
 
        location = weather["location"]
        current = weather["current"]

        context = {
            "API_KEY": API_KEY,
            "isweather": True,
            "location": location,
            "current": current,
        }

        return render_template("map.html", **context)
    
    else:
        return render_template("map.html", isweather=False, API_KEY=API_KEY)


@app.route("/favourite", methods=["GET", "POST"])
@login_required
def favourite():
    if request.method == "POST":
        if request.form.get('add'):
            city = request.form.get('add')
            add(city)
        elif request.form.get('remove'):
            city = request.form.get('remove')
            remove(city)

        cities = favArray()
        return render_template("favourite.html", API_KEY=API_KEY, cities=cities)
    else:
        cities = favArray()
        return render_template("favourite.html", API_KEY=API_KEY, cities=cities)


@app.route("/resetPassword", methods=["GET", "POST"])
def send_email():
    
    email = request.form.get('email')
    if not email:
        flash("Please Enter your email address and then click on forgot password to resent your email password", "info")
        return render_template("login.html")
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE email = ?", (email, ))
        ans = cur.fetchall()

        if not ans:
            conn.rollback()
            flash("This email has not been registered", "danger")
            return render_template("register.html")
        conn.commit()

    except Exception as e:
        conn.rollback()
        flash("Something went wrong while registering!", "danger")
        return render_template("register.html")
    
    finally:
        conn.close()

    session["email"] = email
    session["code"] = random.randint(100000, 999999)
   
    msg = Message(subject="Your Verification Code", recipients=[email])
    msg.html = render_template("email.html")
    try:
        mail.send(msg)
        return render_template("verifcode.html")
    except Exception as e:
        print(e)
        flash(f"An Error occurred {e}")
        return render_template("login.html")


@app.route("/resetpassword", methods=["POST"])
def resetPassword():
    pwd = request.form.get("pwd")
    rpwd = request.form.get("rpwd")
    email = session.get("email")
    if not pwd == rpwd:
        flash("Invail Passwords not equal", "danger")
        return render_template("resetpassword.html")
    
    # Updating user's password to new one
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    try:
        phash = generate_password_hash(pwd)
        cur.execute("UPDATE users SET hash = (?) WHERE email = (?)", (phash, email))
        cur.execute("SELECT id FROM users WHERE email = (?)", (email, ))
        result = cur.fetchall()
        session["user_id"] = result[0][0]
        conn.commit()
        flash("Your password has been reset SuccessFully!", "success")

    except Exception as e:
        conn.rollback()
        print(e)
        flash("Something went wrong while resetting password! Try Again!", "danger")
        return render_template("login.html")
    
    finally:
        conn.close()
    flash("Password resetted Successfully", "success")

    return redirect("/")

    