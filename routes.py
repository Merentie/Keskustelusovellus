from app import app
from flask import redirect, render_template, request, session 
import actions
import logreg

#Frontpage
@app.route("/")
def index():
    chambers = actions.fetch()
    return render_template("index.html", chambers=chambers)


#Registration page, handles the registration, adding user to database unless the username is there already. Also logs the new user in if registration is successful. 
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        user = logreg.register(username,password)
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
    user = logreg.login(username,password)
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

@app.route("/createthread")
def createthread():
    pass

if __name__ == "__main__":
    app.run(debug=True)
