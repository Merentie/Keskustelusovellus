from app import app
from flask import redirect, render_template, request, session 
import actions
import userstuff

#Frontpage
@app.route("/")
def index():
    chambers = actions.getchambers()
    links = {}
    for chamber in chambers:
        links[chamber[0]] = str("/c/"+chamber[0]).replace(" ","_")
    return render_template("index.html", chamberlinks = links)

#Registration page, handles the registration, adding user to database unless the username is there already. Also logs the new user in if registration is successful. 
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        user = userstuff.register(username,password)
        if user:
            session["username"] = username
            return redirect("/")
        else:
            return render_template("error.html", message="User already exists", prev="/register")

#Handling of the attempted log in. It will be successful if the username and hashed passwords are in the same relation in the users table
@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = userstuff.login(username,password)
    if user:
        session["username"] = username
        return redirect("/")
    else:
        return render_template("error.html", message="Invalid username or password", prev="/")

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
        chamber = actions.createchamber(name)
        if chamber:
            return redirect("/")
        else:
            return render_template("error.html", message="Chamber already exists", prev="/createchamber")
    else:
        return render_template("createchamber.html")
    
@app.route("/c/<chamber>/")
def chamber(chamber):
    if not actions.chambercheck(chamber):
        return render_template("error.html", message=f"chamber '{chamber}' not found", prev="/")
    else:
        threads = actions.getthreads()
        links = {}
        for thread in threads:
            links[thread[3]] = str("/c/"+thread[3]).replace(" ","_")
        return render_template("chamber.html", threadlinks = links, creator = "/c/"+chamber+"/createthread")

    
@app.route("/c/<chamber>/createthread", methods=["GET","POST"])
def createthread(chamber):
    if request.method == "POST":
        if not actions.chambercheck(chamber):
            return render_template("error.html", message=f"chamber '{chamber}' not found", prev="/")
        chamberid = actions.chambercheck(chamber)[0]
        title = request.form["title"]
        content = request.form["content"]
        print(session["username"])
        user = userstuff.findadude(session["username"])
        userid = user[0]
        username = user[1]
        thread = actions.createthread(userid, chamberid, title, content)
        return render_template("thread.html", createdby = username, threadid = thread)

    else:
        return render_template("createthread.html", where = "/c/"+chamber+"/createthread")