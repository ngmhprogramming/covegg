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
        
        if db.login(username, hash(password)):
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

    days = ["Monday","Tuesday", "Wednesday", "Thursday", "Friday","Saturday","Sunday"]
    
    amhourlist = ["0000-0030","0030-0100","0100-0130","0130-0200","0200-0230","0230-0300","0300-0330","0330-0400","0400-0430","0430-0500","0500-0530","0530-0600","0600-0630","0630-0700","0700-0730","0730-0800","0800-0830","0830-0900","0900-0930","0930-1000","1000-1030","1030-1100","1100-1130","1130-1200"]

    pmhourlist = ["1200-1230","1230-1300","1300-1330","1330-1400","1400-1430","1430-1500","1500-1530","1530-1600","1600-1630","1630-1700","1700-1730","1730-1800","1800-1830","1830-1900","1900-1930","1930-2000","2000-2030","2030-2100","2100-2130","2130-2200","2200-2230","2230-2300","2300-2330","2330-0000"]

    if request.method == "GET":  
        schedule_string = db.getschedule(username)
        return render_template("schedule.html",days = days, amhourlist = amhourlist, pmhourlist = pmhourlist,schedule_string = schedule_string)
    else:
        #post
        sched_data = request.form.getlist('scheduledata')
    
        s = ["0" for i in range(336)]
        for item in sched_data:
            s[int(item)] = "1"
        s = "".join(s)
        
        db.editschedule(username,s)
        return render_template("schedule.html",days = days, amhourlist = amhourlist, pmhourlist = pmhourlist,schedule_string =s)


@app.route("/meetings", methods=["GET", "POST"])
def meetings():
    username = get_username()
    if not username:
        return redirect(url_for("login"))

    #pmeetings = db.getpendingmeeting(username)
    #cmeetings = db.getconfirmedmeeting(username)
    pmeetings = [["1", ["a", "b"], "0am"], ["2", ["c", "d"], "1am"]]
    cmeetings = [["3", ["a", "b"], "0am"], ["4", ["c", "d"], "1am"]]
    if request.method == "GET":
        return render_template("meetings.html", pmeetings=pmeetings, cmeetings=cmeetings, username=username)
    else:
        meetingid = request.form["meetingid"]
        db.confirmmeeting(meetingid)
        return render_template("meetings.html", pmeetings=pmeetings, cmeetings=cmeetings, username=username)

@app.route("/create_meeting", methods=["GET", "POST"])
def create_meeting():
    username = get_username()
    if not username:
        return redirect(url_for("login"))

    #over = db.findoverlaps(username)
    over = [["a", "1am"], ["b", "2am"], ["c", "3am"]]
    if request.method == "GET":
        return render_template("create_meeting.html", over=over, username=username)
    else:
        user = request.form["user"]
        time = request.form["time"]
        #db.creatependingmeeting(user, time)
        return render_template("create_meeting.html", over=over, username=username)

@app.route("/friends", methods=["GET", "POST"])
def friends():
    username = get_username()
    if not username:
        return redirect(url_for("login"))

    friendl = db.getfren(username)
    rfriendl = db.getpfren(username)
    if request.method == "GET":
        return render_template("friends.html", friendl=friendl, rfriendl=rfriendl, username=username)
    else:
        if 'username' in request.form:
            friendreq = request.form["username"]
            db.requestfren(username, friendreq)
        else:
            friendreq = request.form["rusername"]
            db.confirmfren(friendreq, username, True)
        return render_template("friends.html", friendl=friendl, rfriendl=rfriendl, username=username)

db.testallfunctions()
if __name__ == "__main__":
    app.run(debug=True)
