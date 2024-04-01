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
    result = db.session.execute(text("SELECT id, name FROM chambers"))
    chambers = result.fetchall()
    return render_template("index.html", chambers=chambers)


#Registration page, handles the registration, adding user to database unless the username is there already. Also logs the new user in if registration is successful. 
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
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
            return render_template("error.html", message="User already exists", prev="/register")



#Handling of the attempted log in. It will be successful if the username and hashed passwords are in the same relation in the users table
@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = text("SELECT id, password, username FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user:
        hash_value = user[1]
        if check_password_hash(hash_value, password):
            session["username"] = username
            return redirect("/")
        else:
            return render_template("error.html", message="Wrong password", prev="/")
    else:
        return render_template("error.html", message="User not found", prev="/")


#Logs the user out
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

#Allows user to make a new chamber
@app.route("/createchamber", methods=["GET","POST"])
def createchamber():
    if request.method == "POST":
        name = request.form["name"]
        sql = text("SELECT name FROM chambers WHERE name=:name")
        result = db.session.execute(sql, {"name":name})
        chamber = result.fetchone()
        if not chamber:
            sql = text("INSERT INTO chambers (name) VALUES (:name)")
            db.session.execute(sql, {"name":name})
            db.session.commit()
            return redirect("/")
        else:
            return render_template("error.html", message="Chamber already exists", prev="/createchamber")
    else:
        return render_template("createchamber.html")

@app.route("/createthread")
def createthread():
    pass

if __name__ == "__main__":
    app.run(debug=True)
