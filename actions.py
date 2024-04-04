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

def createthread(uid, cid, title, content):
    sql = text("INSERT INTO threads (user_id, chamber_id, title, content) VALUES (:uid, :cid, :title, :content)")
    db.session.execute(sql, {"user_id":uid, "chamber_id":cid, "title":title, "content":content})
    db.session.commit()
    return db.session.execute(text("SELECT currval(pg_get_serial_sequence('threads','id'))")).fetchone()

def chambercheck(chamber):
    result = db.session.execute(text("SELECT id, name FROM chambers WHERE name=:name"), {"name":chamber.replace("_"," ")}).fetchone()
    if not result:
        return None
    else:
        return result

def getchambers():
    get = db.session.execute(text("SELECT name FROM chambers")).fetchall()
    return get

def getthreads():
    get = db.session.execute(text("SELECT * FROM threads")).fetchall()
    return get