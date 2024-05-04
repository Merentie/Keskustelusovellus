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
    sql = text("INSERT INTO threads (user_id, chamber_id, title, content, echo, created_at) VALUES (:user_id, :chamber_id, :title, :content, 0, NOW())")
    db.session.execute(sql, {"user_id":uid, "chamber_id":cid, "title":title, "content":content})
    db.session.commit()
    return db.session.execute(text("SELECT MAX(id) FROM threads")).fetchone()

def chambercheck(chamber):
    result = db.session.execute(text("SELECT id, name FROM chambers WHERE name=:name"), {"name":chamber.replace("_"," ")}).fetchone()
    if not result:
        return None
    else:
        return result

def getchambers():
    get = db.session.execute(text("SELECT name FROM chambers")).fetchall()
    return get

def getthreads(chamber):
    chamber = chamber.replace("_"," ")
    id = db.session.execute(text("SELECT id FROM chambers WHERE name=:name"),{"name":chamber}).fetchone()
    if not id:
        return 
    id = id[0]
    get = db.session.execute(text("SELECT * FROM threads WHERE chamber_id=:chamber_id"),{"chamber_id":id}).fetchall()
    return get

def openthread(id):
    get = db.session.execute(text("SELECT * FROM threads WHERE id=:id"),{"id":id}).fetchall()
    if not get:
        return
    return get

def getmessages(id):
    get = db.session.execute(text("SELECT * FROM messages where thread_id=:thread_id"),{"thread_id":id}).fetchall()
    if not get:
        return
    return get

def messagehistory(id):
    history = []
    get = db.session.execute(text("SELECT * FROM messages where user_id=:user_id group by id order by id desc"),{"user_id":id}).fetchall()
    if not get:
        return
    for message in get:
        cid = db.session.execute(text("SELECT chamber_id, id, title FROM threads where id=:id"),{"id":message[2]}).fetchall()
        chamber = db.session.execute(text("SELECT * FROM chambers where id=:id"),{"id":cid[0][0]}).fetchall()
        history.append((message[3],cid[0][1],cid[0][2],chamber,chamber[0][1].replace(" ","_"),message[4]))
    return history

def addamessage(uid, tid, message):
    db.session.execute(text("INSERT INTO messages (user_id, thread_id, message, echo, created_at) VALUES (:user_id, :thread_id, :message, 0, NOW())"), {"user_id":uid, "thread_id":tid, "message":message})
    db.session.commit()


def posthistory(id):
    history = []
    get = db.session.execute(text("SELECT * FROM threads where user_id=:user_id group by id order by id desc"),{"user_id":id}).fetchall()
    if not get:
        return
    for post in get:
        chamber = db.session.execute(text("SELECT * FROM chambers where id=:id"),{"id":post[2]}).fetchall()
        history.append((post[0],post[3],post[5],chamber[0][1],chamber[0][1].replace(" ","_"),post[4]))
    return history
