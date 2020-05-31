from flask import Flask, render_template, session, redirect, url_for, request
from hash import *
import database as db

app = Flask(__name__)
app.secret_key = "shellshock69420"

def get_username():
    if "username" in session: return session["username"]
    return False

@app.route("/")
def index():
    username = get_username()
    if username:
        return render_template("index.html", username=username)
    else:
        return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    username = get_username()
    if username:
        return redirect(url_for("index"))

    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        
        if db.login(username, password):
            session["username"] = username
            return redirect(url_for("index"))
        return render_template("login.html", error="Invalid Username or Password")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    username = get_username()
    if username:
        return redirect(url_for("index"))

    if request.method == "GET":
        return render_template("signup.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        pnumber = request.form["pnumber"]
        email = request.form["email"]

        password = hash(password)
        if db.register(username, pnumber, email, password):
            return redirect(url_for("login"))
        return render_template("signup.html", error="Username taken!")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    username = get_username()
    if not username:
        return redirect(url_for("login"))

    if request.method == "GET":
        return render_template("profile.html")
    else:
        return render_template("profile.html")

@app.route("/schedule", methods=["GET", "POST"])
def schedule():
    username = get_username()
    if not username:
        return redirect(url_for("login"))

    if request.method == "GET":
        return render_template("schedule.html")
    else:
        return render_template("schedule.html")

@app.route("/meetings", methods=["GET", "POST"])
def meetings():
    username = get_username()
    if not username:
        return redirect(url_for("login"))

    if request.method == "GET":
        return render_template("meetings.html")
    else:
        return render_template("meetings.html")

@app.route("/friends", methods=["GET", "POST"])
def friends():
    username = get_username()
    if not username:
        return redirect(url_for("login"))

    if request.method == "GET":
        return render_template("friends.html")
    else:
        return render_template("friends.html")

if __name__ == "__main__":
    app.run(debug=True)
