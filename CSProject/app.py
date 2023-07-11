from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
# from flask_mail import Message, Mail
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import lookup
import sqlite3
import os

app = Flask(__name__)

# Session Configure
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Mail Configuration - Getting some big problems We need to implement OAuth 2.0 which will take some work
# app.config["MAIL_DEFAULT_SENDER"] = os.environ["MAIL_DEFAULT_SENDER"]
# app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
# app.config["MAIL_PORT"] = 587
# app.config["MAIL_SERVER"] = "smtp.gmail.com"
# app.config["MAIL_USE_TLS"] = True
# app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
# mail = Mail(app)

# main page
@app.route("/")
def index():
    if not session.get("user_id"):
        return redirect("/login")
    return render_template("index.html")

# Login page
# Validate the email and password (pwd is check using hash pwd)
# set session["user_id"]
@app.route("/login", methods=["GET", "POST"])
def login():
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
    session["user_id"] = None
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        
        email = request.form.get("email")
        pwd = request.form.get("pwd")
        rpwd = request.form.get("rpwd")

        if not email or not pwd or not rpwd:
            flash("Please enter Your information!", "danger")
            msg = "hello"
            return render_template("register.html")
        
        # Validatiting email id 
        # - Checking if it is'nt already registered -done
        # - Verifing the email id - Will do this later 
        # - Subtitute - mail the user that he has registered

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        try:
            cur.execute("SELECT * FROM users WHERE email = ?", (email, ))
            ans = cur.fetchall()

            if ans:
                conn.rollback()
                flash("This email has already been registered", "danger")
                return render_template("register.html")
        
            # msg = Message("You have registered!", recipients=[email])
            # msg.body = "You have Registered at Sky.net\n Thank you for registing!"
            # mail.send(msg)

            # Validating Passwords 
            # - Checking if passwords are same -done
            # - Hashing the password and then storeing it in database -done

            if pwd != rpwd:
                conn.rollback()
                flash("Passwords Not Equal!", "danger")
                return render_template("register.html")
        
            phash = generate_password_hash(pwd)

            cur.execute("INSERT INTO users (email, hash) VALUES (?, ?)", (email, phash))
            cur.execute("SELECT id FROM users WHERE email = (?)", (email, ))

            result = cur.fetchall()
            session["user_id"] = result[0][0]
            conn.commit()
            flash("Registered Sucessfully", "success")

        except Exception as e:
            conn.rollback()
            flash("Something went wrong while registering!", "danger")
            return render_template("register.html")
        
        finally:
            conn.close()
            
        return redirect("/")

    else:
        return render_template("register.html")
    
@app.route("/weather")
def weather():
    return render_template("weather.html")

@app.route("/today", methods=["GET", "POST"])
def today():

    if request.method == "post":
        city = request.form.get("city")
        if not city:
            latitude = request.form.get("latitude")
            longitude = request.form.get("longitude")
            if not latitude:
                flash("Please enter the city you want see weather of!")
                return render_template("today.html")
            q = f"{latitude},{longitude}"
        else:
            q = f"{city}"
        weather = lookup(q)
        return render_template("today.html")
    else:
        return render_template("today.html")