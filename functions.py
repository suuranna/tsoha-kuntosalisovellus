from db import db
from datetime import datetime

def get_password(username):
    sql = "select password from users where username=:username"
    result = db.session.execute(sql, {"username":username})
    password = result.fetchone()
    return password

def sign_up(username, hash_value):
    try:
        sql = "insert into users (username, password, admin) values (:username, :password, False)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return True

def is_admin(username):
    sql = "select admin from users where username=:username"
    result = db.session.execute(sql, {"username":username})
    admin = result.fetchone()[0]
    return admin

def get_user_id(username):
    sql = "select id from users where username=:username"
    result = db.session.execute(sql, {"username":username})
    user_id = result.fetchone()
    if user_id == None:
        return None
    return user_id[0]

def add_gym_plan(user_id, description, name):
    try:
        sql = "insert into gym_plans (user_id, name, description, created, deleted) values (:user_id, :name, :description, NOW(), False)"
        result = db.session.execute(sql, {"user_id":user_id, "name":name, "description":description})
        db.session.commit()
    except:
        return False
    return True

def get_gym_plans(user_id):
    sql = "select name, description, created, id from gym_plans where user_id=:user_id and deleted=False"
    result = db.session.execute(sql, {"user_id":user_id})
    plans = result.fetchall()
    return plans

def get_s_machines_in_a_plan(plan_id):
    sql = "select m.name, m.targeted_muscles, m.in_order, s.weight_info, s.reps_info, s.additional_info from machines m, strength_machine_in_a_plan s where m.id=s.machine_id and s.gym_plan_id=:plan_id"
    result = db.session.execute(sql, {"plan_id":plan_id})
    machines = result.fetchall()
    return machines

def get_c_machines_in_a_plan(plan_id):
    sql = "select m.name, m.targeted_muscles, m.in_order, c.time_info, c.resistance_info, c.additional_info from machines m, cardio_machine_in_a_plan c where m.id=c.machine_id and c.gym_plan_id=:plan_id"
    result = db.session.execute(sql, {"plan_id":plan_id})
    machines = result.fetchall()
    return machines

def get_machines(machine_type):
    if machine_type == "all":
        sql = "select * from machines order by in_order"
        result = db.session.execute(sql)
        machines = result.fetchall()
    else:
        sql = "select id, name from machines where machine_type=:machine_type"
        result = db.session.execute(sql, {"machine_type":machine_type})
        machines = result.fetchall()
    return machines

def get_one_machine(id):
    sql = "select * from machines where id=:id"
    result = db.session.execute(sql, {"id":id})
    machine = result.fetchone()
    return machine

def add_c_machine_in_a_plan(machine_id, gym_plan_id, time_info, resistance_info, additional_info):
    try:
        sql = "insert into cardio_machine_in_a_plan (machine_id, gym_plan_id, time_info, resistance_info, additional_info) values (:machine_id, :gym_plan_id, :time_info, :resistance_info, :additional_info)"
        result = db.session.execute(sql, {"machine_id":machine_id, "gym_plan_id":gym_plan_id, "time_info":time_info, "resistance_info":resistance_info, "additional_info":additional_info})
        db.session.commit()
    except:
        return False
    return True

def add_s_machine_in_a_plan(machine_id, gym_plan_id, weight_info, reps_info, additional_info):
    try:
        sql = "insert into strength_machine_in_a_plan (machine_id, gym_plan_id, weight_info, reps_info, additional_info) values (:machine_id, :gym_plan_id, :weight_info, :reps_info, :additional_info)"
        result = db.session.execute(sql, {"machine_id":machine_id, "gym_plan_id":gym_plan_id, "weight_info":weight_info, "reps_info":reps_info, "additional_info":additional_info})
        db.session.commit()
    except:
        return False
    return True

def delete_gym_plan(id):
    sql = "update gym_plans set deleted=True where id=:id"
    result = db.session.execute(sql, {"id":id})
    db.session.commit()

def edit_machine(id, name, target, type):
    sql = "update machines set name=:name, targeted_muscles=:target, machine_type=:type where id=:id"
    result = db.session.execute(sql, {"id":id, "name":name, "target":target, "type":type})
    db.session.commit()

