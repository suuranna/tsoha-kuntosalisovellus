from db import db

def get_password(username):
    sql = "select password from users where username=:username"
    result = db.session.execute(sql, {"username":username})
    password = result.fetchone()
    return password

