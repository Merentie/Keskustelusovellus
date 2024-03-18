from sqlalchemy.sql import text
from flask import Flask
from flask import redirect, render_template, request, session 
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://"
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

#Frontpage
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/registration",methods=["POST"])
def registration():
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    sql = text("SELECT id, username FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        session["username"] = username
        return redirect("/")
    else:
        return redirect("/testi")
    
@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = text("SELECT id, password, username FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()  
    print(user)
    hash_value = user[1]
    if check_password_hash(hash_value, password):
        session["username"] = username
        return redirect("/")
    else:
        return redirect("/testi")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/testi")
def testi():
    return render_template("testi.html")

if __name__ == "__main__":
    app.run(debug=True)
