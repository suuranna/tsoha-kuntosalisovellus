from db import db
from datetime import datetime

def right_length(min, max, text):
    if len(text) > max or len(text) < min:
        return False
    return True

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

def count_gym_plans(id):
    sql = "select count(*) from gym_plans where deleted=False and user_id=:id"
    result = db.session.execute(sql, {"id":id})
    amount = result.fetchone()[0]
    return amount

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
    sql = "select m.name, m.targeted_muscles, m.in_order, s.weight_info, s.reps_info, s.additional_info, s.id from machines m, strength_machine_in_a_plan s where m.id=s.machine_id and s.gym_plan_id=:plan_id"
    result = db.session.execute(sql, {"plan_id":plan_id})
    machines = result.fetchall()
    return machines

def get_c_machines_in_a_plan(plan_id):
    sql = "select m.name, m.targeted_muscles, m.in_order, c.time_info, c.resistance_info, c.additional_info, c.id from machines m, cardio_machine_in_a_plan c where m.id=c.machine_id and c.gym_plan_id=:plan_id"
    result = db.session.execute(sql, {"plan_id":plan_id})
    machines = result.fetchall()
    return machines

def get_machine_from_a_plan(id, type):
    sql = ""
    if type == 1:
        sql = "select m.name, c.time_info, c.resistance_info, c.additional_info, c.gym_plan_id from machines m, cardio_machine_in_a_plan c where c.id=:id and c.machine_id=m.id"
    if type == 2:
        sql = "select m.name, s.weight_info, s.reps_info, s.additional_info, s.gym_plan_id from machines m, strength_machine_in_a_plan s where s.id=:id and s.machine_id=m.id"
    result = db.session.execute(sql, {"id":id})
    machine_info = result.fetchone()
    return machine_info

def get_machines(machine_type):
    if machine_type == "all":
        sql = "select * from machines"
        result = db.session.execute(sql)
        machines = result.fetchall()
    else:
        sql = "select id, name from machines where machine_type=:machine_type and in_order=True"
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

def delete_machine_from_a_plan(id, type):
    sql = ""
    if type == 1: 
        sql = "delete from cardio_machine_in_a_plan where id=:id"
    if type == 2:
        sql = "delete from strength_machine_in_a_plan where id=:id"
    result = db.session.execute(sql, {"id":id})
    db.session.commit()

def delete_achievement(id):
    sql = "delete from achievements where id=:id"
    result =db.session.execute(sql, {"id":id})
    db.session.commit()

def edit_machine(id, name, target, type):
    sql = "update machines set name=:name, targeted_muscles=:target, machine_type=:type where id=:id"
    result = db.session.execute(sql, {"id":id, "name":name, "target":target, "type":type})
    db.session.commit()

def edit_c_machine(id, time_info, resistance_info, additional_info):
    sql = "update cardio_machine_in_a_plan set time_info=:time_info, resistance_info=:resistance_info, additional_info=:additional_info where id=:id"
    result = db.session.execute(sql, {"time_info":time_info, "resistance_info":resistance_info, "additional_info":additional_info, "id":id})
    db.session.commit()

def edit_s_machine(id, weight_info, reps_info, additional_info):
    sql = "update strength_machine_in_a_plan set weight_info=:weight_info, reps_info=:reps_info, additional_info=:additional_info where id=:id"
    result = db.session.execute(sql, {"weight_info":weight_info, "reps_info":reps_info, "additional_info":additional_info, "id":id})
    db.session.commit()

def change_in_order(id, in_order):
    if in_order:
        in_order = False
    else:
        in_order = True
    sql = "update machines set in_order=:in_order where id=:id"
    result = db.session.execute(sql, {"id":id, "in_order":in_order})
    db.session.commit()

def get_in_order(id):
    sql = "select in_order from machines where id=:id"
    result = db.session.execute(sql, {"id":id})
    in_order = result.fetchone()[0]
    return in_order

def new_machine(name, type, target):
    sql = "insert into machines (name, targeted_muscles, machine_type, in_order) values (:name, :target, :type, True)"
    result = db.session.execute(sql, {"name":name, "target":target, "type":type})
    db.session.commit()

def get_gym_plan_info(id):
    sql = "select * from gym_plans where id=:id"
    result = db.session.execute(sql, {"id":id})
    info = result.fetchone()
    return info

def edit_gym_plan_info(id, name, description):
    sql = "update gym_plans set name=:name, description=:description where id=:id"
    result = db.session.execute(sql, {"id":id, "name":name, "description":description})
    db.session.commit()

def get_achievements(user_id):
    sql = "select a.machine_id, m.name, a.achievement, a.date, a.id from machines m, achievements a where a.user_id=:user_id and m.id=a.machine_id"
    result = db.session.execute(sql, {"user_id":user_id})
    achievements = result.fetchall()
    return achievements

def get_one_achievement(id):
    sql = "select a.machine_id, m.name, a.achievement, a.date from machines m, achievements a where a.id=:id"
    result = db.session.execute(sql, {"id":id})
    achievement = result.fetchone()
    return achievement

def add_new_achievement(user_id, machine_id, achievement):
    sql = "insert into achievements (user_id, machine_id, achievement, date) values (:user_id, :machine_id, :achievement, NOW())"
    result = db.session.execute(sql, {"user_id":user_id, "machine_id":machine_id, "achievement":achievement})
    db.session.commit()

def edit_achievement(id, achievement):
    sql = "update achievements set achievement=:achievement where id=:id"
    result = db.session.execute(sql, {"achievement":achievement, "id":id})
    db.session.commit()

def count_achievements(user_id):
    sql = "select count(*) from achievements where user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    count = result.fetchone()[0]
    return count
