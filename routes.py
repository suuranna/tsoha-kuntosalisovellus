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
            session["admin"] = functions.is_admin(username)
            session["user_id"] = functions.get_user_id(username)
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

@app.route("/add_gym_plan", methods=["GET", "POST"])
def add_gym_plan():
    if request.method == "GET":
        return render_template("add_gym_plan.html")
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        succesful_adding = functions.add_gym_plan(session["user_id"], description, name)
        if succesful_adding:
            return "Salisuunnitelman luominen onnistui"
        else:
            return "Salisuunnitelman luonti epäonnistui"

@app.route("/delete_gym_plan/<int:id>", methods=["GET", "POST"])
def delete_gym_plan(id):
    if request.method == "GET":
        return render_template("delete_gym_plan.html", id=id)
    if request.method == "POST":
        functions.delete_gym_plan(id)
        return redirect("/gym_plans")

@app.route("/gym_plans")
def gym_plans():
    gym_plans = functions.get_gym_plans(session["user_id"])
    return render_template("gym_plans.html", plans=gym_plans)

@app.route("/edit_gym_plan/<int:id>", methods=["GET", "POST"])
def edit_gym_plan(id):
    if request.method == "GET":
        c_machines = functions.get_machines("cardio")
        s_machines = functions.get_machines("strength")
        c_m_in_a_plan = functions.get_c_machines_in_a_plan(id)
        s_m_in_a_plan = functions.get_s_machines_in_a_plan(id)
        return render_template("edit_gym_plan.html", id=id, c_machines=c_machines, s_machines=s_machines, c_m_in_a_plan=c_m_in_a_plan, s_m_in_a_plan=s_m_in_a_plan)
    if request.method == "POST":
        if request.form["button"] == "Lisää aerobinen laite":
            machine_id = request.form["c_machine"]
            time_info = request.form["time_info"]
            resistance_info = request.form["resistance_info"]
            additional_info = request.form["additional_info"]
            succesful_adding = functions.add_c_machine_in_a_plan(machine_id, id, time_info, resistance_info, additional_info)
        elif request.form["button"] == "Lisää voimailulaite":
            machine_id = request.form["s_machine"]
            weight_info = request.form["weight_info"]
            reps_info = request.form["reps_info"]
            additional_info = request.form["additional_info"]
            succesful_adding = functions.add_s_machine_in_a_plan(machine_id, id, weight_info, reps_info, additional_info)
        else:
            return "Virhe!"
        if succesful_adding:
            return "Laitteen lisääminen onnistui!"
        else:
            return "Laitteen lisääminen epäonnistui"

