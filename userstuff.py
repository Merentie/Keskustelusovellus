from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash


def register(username, password):
    hash_value = generate_password_hash(password)
    sql = text("SELECT id, username FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:        
            sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
            db.session.execute(sql, {"username":username, "password":hash_value})
            db.session.commit()
            return True
    else:
        return False
    
def login(username, password):
    sql = text("SELECT id, password, username FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user:
        hash_value = user[1]
        if check_password_hash(hash_value, password):
            return True
        else:
            return False
    else:
        return False
    
def findadude(username):
    sql = text("SELECT id, username FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user:
        return user
    else:
        return None

def findadudebyid(id):
    sql = text("SELECT id, username FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    user = result.fetchone()
    if user:
        return user
    else:
        return None
    
def echosum(username):
    uid = findadude(username)[0]
    sql = text("SELECT SUM(echo) FROM messages where user_id=:user_id")
    result = db.session.execute(sql, {"user_id":uid}).fetchone()
    return result