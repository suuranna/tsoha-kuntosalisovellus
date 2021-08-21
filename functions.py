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
        #return True
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
        #return True
    except:
        return False
    return True

def get_gym_plans(user_id):
    sql = "select name, description, created from gym_plans where user_id=:user_id and deleted=False"
    result = db.session.execute(sql, {"user_id":user_id})
    plans = result.fetchall()
    return plans
