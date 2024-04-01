from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash



def createchamber(name):
    sql = text("SELECT name FROM chambers WHERE name=:name")
    result = db.session.execute(sql, {"name":name})
    chamber = result.fetchone()
    if not chamber:
        sql = text("INSERT INTO chambers (name) VALUES (:name)")
        db.session.execute(sql, {"name":name})
        db.session.commit()
        return True
    else:
        return False
    
def fetch():
    result = db.session.execute(text("SELECT name, name FROM chambers"))
    return result.fetchall()