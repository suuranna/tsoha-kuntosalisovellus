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
        return render_template("message.html", route="/", message1="Väärä käyttäjätunnus tai salasana", message2="Siirry takaisin kirjautumiseen")
    else:
        hash_value = hashed_password[0]
        if check_password_hash(hash_value,password):
            session["username"] = username
            session["admin"] = functions.is_admin(username)
            session["user_id"] = functions.get_user_id(username)
            return redirect("/")
        else:
            return render_template("message.html", route="/", message1="Väärä käyttäjätunnus tai salasana", message2="Siirry takaisin kirjautumiseen")

@app.route("/achievements", methods=["GET", "POST"])
def achievements():
    if request.method == "GET":
        machines = functions.get_machines("all")
        count = functions.count_achievements(session["user_id"])
        achievements = functions.get_achievements(session["user_id"])
        return render_template("achievements.html", machines=machines, achievements=achievements, count=count)
    if request.method == "POST":
        machine_id = request.form["machine"]
        achievement = request.form["achievement"]
        if not functions.right_length(0, 350, achievement):
            return render_template("message.html", message1="Kirjoittamasi teksti oli liian pitkä", message2="Yritä uudelleen siirtymällä takaisin suunnitelmiin", route="/achievements")
        functions.add_new_achievement(session["user_id"], machine_id, achievement)
        return render_template("message.html", message1="Uusi saavutus lisätty onnistuneesti", message2="Takaisin saavutuksiin", route="/achievements")

@app.route("/delete_achievement/<int:id>", methods=["GET", "POST"])
def delete_achievement(id):
    if request.method == "GET":
        return render_template("delete.html", route="/delete_achievement/"+str(id), message="Haluatko varmasti poistaa tämän saavutuksen?", back="/achievements", submit="Poista tämä saavutus")
    if request.method == "POST":
        functions.delete_achievement(id)
        return render_template("message.html", message1="Saavutus poistettu onnistuneesti", message2="Palaa takaisin saavutuksiin", route="/achievements")

@app.route("/edit_achievement/<int:id>", methods=["GET", "POST"])
def edit_achievement(id):
    if request.method == "GET":
        achievement = functions.get_one_achievement(id)
        return render_template("edit_achievement.html", id=id, achievement=achievement)
    if request.method == "POST":
        achievement = request.form["achievement"]
        if not functions.right_length(0, 350, achievement):
            return render_template("message.html", message1="Kirjoittamasi teksti oli liian pitkä", message2="Yritä uudelleen siirtymällä takaisin suunnitelmiin", route="/achievements")
        functions.edit_achievement(id, achievement)
        return render_template("message.html", message1="Saavutusta muokattu onnistuneesti", message2="Palaa takaisin saavutuksiin", route="/achievements")

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    del session["admin"]
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
        return render_template("message.html", message1="Käyttäjätunnuksen luonti epäonnistui", route="/sign_up", message2="Siirry takaisin käyttäjätunnuksenluontiin")

@app.route("/add_gym_plan", methods=["GET", "POST"])
def add_gym_plan():
    if request.method == "GET":
        return render_template("add_gym_plan.html")
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        if not functions.right_length(0, 50, name) or not functions.right_length(0,200,description):
            return render_template("message.html", message1="Kirjoittamasi teksti oli liian pitkä", message2="Yritä uudelleen", route="/add_gym_plan")
        succesful_adding = functions.add_gym_plan(session["user_id"], description, name)
        if succesful_adding:
            return render_template("message.html", message1="Kuntosalisuunnitelman luominen onnistui", message2="Siirry takaisin omiin kuntosalisuunnitelmiin", route="/gym_plans")
        else:
            return render_template("message.html", message1="Salisuunnitelman luonti epäonnistui", message2="Yritä uudelleen", route="/add_gym_plan")

@app.route("/delete_gym_plan/<int:id>", methods=["GET", "POST"])
def delete_gym_plan(id):
    if request.method == "GET":
        return render_template("delete.html", message="Haluatko varmasti poistaa tämän alueen", route="/delete_gym_plan/"+str(id), back="/gym_plans", submit="Haluan poistaa tämän kuntosaliohjelman")
    if request.method == "POST":
        functions.delete_gym_plan(id)
        return render_template("message.html", message1="Kuntosalisuunnitelman poistaminen onnistui", route="/gym_plans", message2="Siirry takaisin kuntosalisuunnitelmiin")

@app.route("/gym_plans")
def gym_plans():
    amount = functions.count_gym_plans(session["user_id"])
    gym_plans = functions.get_gym_plans(session["user_id"])
    return render_template("gym_plans.html", plans=gym_plans, amount=amount)

@app.route("/edit_gym_plan/<int:id>", methods=["GET", "POST"])
def edit_gym_plan(id):
    if request.method == "GET":
        info = functions.get_gym_plan_info(id)
        c_machines = functions.get_machines("cardio")
        s_machines = functions.get_machines("strength")
        c_m_in_a_plan = functions.get_c_machines_in_a_plan(id)
        s_m_in_a_plan = functions.get_s_machines_in_a_plan(id)
        return render_template("edit_gym_plan.html", id=id, c_machines=c_machines, s_machines=s_machines, c_m_in_a_plan=c_m_in_a_plan, s_m_in_a_plan=s_m_in_a_plan, info=info)
    if request.method == "POST":
        if request.form["button"] == "Lisää aerobinen laite":
            machine_id = request.form["c_machine"]
            time_info = request.form["time_info"]
            resistance_info = request.form["resistance_info"]
            additional_info = request.form["additional_info"]
            if not functions.right_length(0, 100, time_info) or not functions.right_length(0,100,resistance_info) or not functions.right_length(0,100,additional_info):
                return render_template("message.html", message1="Kirjoittamasi teksti oli liian pitkä", message2="Yritä uudelleen", route="/edit_gym_plan/"+str(id))
            succesful_adding = functions.add_c_machine_in_a_plan(machine_id, id, time_info, resistance_info, additional_info)
        elif request.form["button"] == "Lisää voimailulaite":
            machine_id = request.form["s_machine"]
            weight_info = request.form["weight_info"]
            reps_info = request.form["reps_info"]
            additional_info = request.form["additional_info"]
            if not functions.right_length(0, 100, weight_info) or not functions.right_length(0,100,reps_info) or not functions.right_length(0,100,additional_info):
                return render_template("message.html", message1="Kirjoittamasi teksti oli liian pitkä", message2="Yritä uudelleen", route="/edit_gym_plan/"+str(id))
            succesful_adding = functions.add_s_machine_in_a_plan(machine_id, id, weight_info, reps_info, additional_info)
        else:
            return "Virhe!"
        if succesful_adding:
            return render_template("message.html", message1="Laitteen lisääminen onnistui!", message2="Takaisin muokkaamaan kuntosalisuunnitelmaa", route="/edit_gym_plan/"+str(id))
        else:
            return render_template("message.html", message1="Laitteen lisääminen epäonnistui", message2="Yritä uudelleen", route="/edit_gym_plan/"+str(id))

@app.route("/machines", methods=["GET", "POST"])
def machines():
    if not session["admin"]:
        return render_template("message.html", message1="Sinulla ei ole oikeutta hallinnoida salin laitteita", message2="Siirry etusivulle", route="/")
    if request.method == "GET":
        machines = functions.get_machines("all")
        return render_template("machines.html", machines=machines)
    if request.method == "POST":
        name = request.form["name"]
        target = request.form["target"]
        type = request.form["type"]
        if not functions.right_length(0, 50, name) or not functions.right_length(0,100,target):
            return render_template("message.html", message1="Kirjoittamasi teksti oli liian pitkä", message2="Yritä uudelleen", route="machines")

        functions.new_machine(name, type, target)
        return render_template("message.html", route="/machines", message1="Laite lisätty onnistuneesti", message2="Palaa takaisin laitteisiin")

@app.route("/change_in_order/<int:id>", methods=["GET", "POST"])
def change_in_order(id):
    if not session["admin"]:
        return render_template("message.html", message1="Sinulla ei ole oikeutta hallinnoida salin laitteita", message2="Siirry etusivulle", route="/")
    in_order = functions.get_in_order(id)
    if request.method == "GET":
        if in_order:
            question = "Haluatko poistaa tämän laitteen käytöstä?"
            submit = "Haluan poistaa tämän laitteen käytöstä"
        else:
            question = "Haluatko laittaa tämän laitteen käyttöön?"
            submit = "Haluan laittaa tämän laitteen käyttöön"
        return render_template("change_in_order.html", question=question, submit=submit, id=id)
    if request.method == "POST":
        functions.change_in_order(id, in_order)
        return render_template("message.html", route="/machines", message1="Laitteen käytössä-tila on vaihdettu onnistuneesti", message2="Siirry takaisin laitteisiin")

@app.route("/edit_machine/<int:id>", methods=["GET", "POST"])
def edit_machine(id):
    if not session["admin"]:
        return render_template("message.html", message1="Sinulla ei ole oikeutta hallinnoida salin laitteita", message2="Siirry etusivulle", route="/")
    if request.method == "GET":
        machine = functions.get_one_machine(id)
        return render_template("edit_machine.html", id=id, machine=machine)
    if request.method == "POST":
        type = request.form["type"]
        if type == "empty":
            return render_template("message.html", message2="Yritä uudelleen", route="/edit_machine/"+str(id), message1="Laitteen tietojen muokkaaminen epäonnistui, koska laitteen tyyppi jätettiin valitsematta.")
        name = request.form["name"]
        target = request.form["target"]
        type = request.form["type"]
        functions.edit_machine(id, name, target, type)
        if name == "" or target == "" or type == "":
            return render_template("message.html", message1="Kirjoita jokaiseen kenttään jotakin", message2="Yritä uudelleen", route="/edit_machine/"+str(id))
        return render_template("message.html", message1="Laitteen tietojen muokkaus onnistui", message2="Siirry takaisin laitteisiin", route="/machines")

@app.route("/edit_gym_plan_machine/<int:type>/<int:id>", methods=["GET", "POST"])
def edit_gym_plan_machine(type, id):
    if request.method == "GET":
         machine_info = functions.get_machine_from_a_plan(id, type)
         return render_template("edit_gym_plan_machine.html", type=type, id=id, machine_info=machine_info)

    if request.method == "POST":
        gym_plan_id = request.form["gym_plan_id"]
        if type == 1:
            time_info = request.form["time_info"]
            resistance = request.form["resistance_info"]
            additional = request.form["additional_info"]
            functions.edit_c_machine(id, time_info, resistance, additional)
        else:
            weight_info = request.form["weight_info"]
            reps_info = request.form["reps_info"]
            additional = request.form["additional_info"]
            functions.edit_s_machine(id, weight_info, reps_info, additional)
        return render_template("message.html", message1="Laitteen treenitietoja muokattu onnituneesti!", message2="Palaa takaisin muokkaamaan salisuunnitelmaa", route="/edit_gym_plan/"+str(gym_plan_id))

@app.route("/delete_machine_from_a_plan/<int:type>/<int:id>", methods=["GET", "POST"])
def delete_machine_from_a_plan(type, id):
    if request.method == "GET":
        route = "/delete_machine_from_a_plan/" + str(type) + "/" + str(id)
        return render_template("delete.html", route=route, message="Haluatko varmasti poistaa tämän laitteen tästä salisuunnitelmasta?", back="/gym_plans", submit="Poista tämä laite tästä suunnitelmasta")
    if request.method == "POST":
        functions.delete_machine_from_a_plan(id, type)
        return render_template("message.html", message1="Laite poistettu onnistuneesti", message2="Siirry takaisin salisuunnitelmiin", route="/gym_plans")

@app.route("/edit_gym_plan_info/<int:id>", methods=["GET", "POST"])
def edit_gym_plan_info(id):
    if request.method == "GET":
        info = functions.get_gym_plan_info(id)
        return render_template("edit_gym_plan_info.html", info=info)
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        functions.edit_gym_plan_info(id, name, description)
        return render_template("message.html", message1="Salisuunnitelman tietoja muutettu onnistuneesti!", message2="Takaisin salisuunnitelmaan", route="/edit_gym_plan/"+str(id))
