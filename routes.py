from app import app
from flask import redirect, render_template, request, session, flash
import actions
import userstuff
from datetime import datetime

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
    if session:
            return redirect("/")
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
            return render_template("register.html", error="User already exists")

#Handling of the attempted log in. It will be successful if the username and hashed passwords are in the same relation in the users table
@app.route("/login",methods=["POST"])
def login():
    
    if session:
        return redirect("/")

    username = request.form["username"]
    password = request.form["password"]
    user = userstuff.login(username,password)
    if user:
        session["username"] = username
        return redirect("/")
    else:
        return render_template("index.html", error="Invalid username or password", chamberlinks = {})

#Logs the user out
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

#Allows user to make a new chamber
@app.route("/createchamber", methods=["GET","POST"])
def createchamber():
    if not session:
        return redirect("/")
    if request.method == "POST":
        name = request.form["name"]
        chamber = actions.createchamber(name)
        if chamber:
            return redirect("/")
        else:
            return render_template("createchamber.html", error="Chamber already exists")
    else:
        return render_template("createchamber.html")
    
@app.route("/c/<chamber>/")
def chamber(chamber):
    if not session:
        return redirect("/")
    if not actions.chambercheck(chamber):
        return render_template("error.html", message=f"chamber '{chamber}' not found", prev="/")
    else:
        threads = actions.getthreads(chamber)
        links = {}
        if threads:
            for thread in threads:
                links[thread[3]] = str("/c/"+chamber+"/"+str(thread[0])).replace(" ","_")
        return render_template("chamber.html", chamber=chamber.replace("_"," "), threadlinks = links, creator = "/c/"+chamber+"/createthread")

@app.route("/c/<chamber>/createthread", methods=["GET","POST"])
def createthread(chamber):
    if not session:
        return redirect("/")
    if request.method == "POST":
        if not actions.chambercheck(chamber):
            return render_template("error.html", message=f"chamber '{chamber}' not found", prev="/")
        chamberid = actions.chambercheck(chamber)[0]
        title = request.form["title"]
        content = request.form["content"]
        user = userstuff.findadude(session["username"])
        userid = user[0]
        username = user[1]
        thread = actions.createthread(userid, chamberid, title, content)
        return redirect(f"/c/{chamber}/{thread[0]}")
    else:
        return render_template("createthread.html", where = "/c/"+chamber+"/createthread")
    
@app.route("/c/<chamber>/<thread>", methods=["GET","POST"])
def thread(chamber, thread):
    if not session:
        return redirect("/")
    if request.method == "POST":
        user = userstuff.findadude(session["username"])
        actions.addamessage(user[0],thread,request.form["message"])
        return redirect(f"/c/{chamber}/{thread}")
    else:
        rawmessages = actions.getmessages(thread)
        thready = actions.openthread(thread)[0]
        thready = [userstuff.findadudebyid(thready[1]),thready[3],thready[4],thready[5],thready[6].strftime("%Y-%m-%d %H:%M:%S")]
        if not rawmessages:
                return render_template("thread.html", thready = thready, back = chamber)
        messages = []
        for message in rawmessages:
            dude = userstuff.findadudebyid(message[1])
            date = message[5].strftime("%Y-%m-%d %H:%M:%S")
            messages.append([message[3],dude[1],message[4],date])
        return render_template("thread.html", thready = thready, backl = chamber, back = chamber.replace("_"," "), messages=messages, where = "/c/"+chamber+"/"+str(thread))
    
@app.route("/p/<user>")
def profile(user):
        if not session:
            return redirect("/")
        if userstuff.findadude(user):
            user = userstuff.findadude(user)
            if actions.messagehistory(user[0]):
                messages = actions.messagehistory(user[0])
            else:
                messages = []
            echo = userstuff.echosum(user[1])[0]
            if echo == None:
                echo = 0
            return render_template("profile.html", messages=messages, user=user, echo = echo)
        else:
            return render_template("error.html", message="User not found", prev="/")