from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from flask import render_template, redirect, request, session
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

@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")

@app.route("/sign_up-action", methods=["POST"])
def sign_up_action():
    return "Kesken"
