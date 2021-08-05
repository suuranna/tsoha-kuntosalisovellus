from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from flask import render_template, redirect, request, session
from db import db
import functions

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    hashed_password = functions.get_password(username)
    if hashed_password == None:
        return "Virhe!"
    else:
        hash_value = hashed_password[0]
        if check_password_hash(hash_value,password):
            session["username"] = username
            return redirect("/")
        else:
            return "Virhe!"

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")

@app.route("/sign_up-action", methods=["POST"])
def sign_up_action():
    username = request.form["username"]
    password = request.form["password"]
    password_again = request.form["password_again"]
    if username == "" or password == "":
        return "Syötä käyttäjänimi ja salasana"
    if len(username) > 15 or len(username) < 5:
        return "Syötä käyttäjänimi, joka vastaa pituusvaatimuksia"
    if len(password) > 18 or len(password) < 8:
        return "Syötä salasana, joka vastaa pituusvatimuksia"
    if password != password_again:
        return "Salasanat eivät täsmää"
    hash_value = generate_password_hash(password)
    successful_sign_up = functions.sign_up(username, hash_value)
    if successful_sign_up:
        return redirect("/")
    else:
        return "Käyttäjätunnuksen luonti epäonnistui"


