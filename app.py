from flask import Flask, render_template, session, redirect, url_for, request
from hash import *
import database as db

app = Flask(__name__)
app.secret_key = "shellshock69420"

def get_username():
    if "username" in session: return session["username"]
    return False

get_bin = lambda x, n: format(x, 'b').zfill(n)

def parse_time(string):
    day = 0
    hour = 0
    half = 0
    prev = -1
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    times = []
    for i in range(len(string)):
        if i and i % 48 == 0: day += 1
        if i and i % 2 == 0: hour += 1
        hour %= 24
        half += 1
        half %= 2

        if string[i] == '1':
            time = ""
            f = hour*100+half*30
            f = str(f)
            while len(f) < 4: f = "0"+f

            if half:
                s = (hour+1)*100
            else:
                s = hour*100+30
            s = str(s)
            while len(s) < 4: s = "0"+s

            time = " "+f+"-"+s
            if day != prev: time = days[day]+time
            times.append(time)

            prev = day
    return times

def parse_stime(num):
    day = int(num / 48)
    hour = int(num % 24)
    half = int(num % 2)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    bruh = str(hour*100+half*30)
    while len(bruh) < 4: bruh = "0"+bruh
    time = days[day]+" "+bruh+" - "
    pday = day
    half += 1
    if half == 2:
        half = 0
        hour += 1
        if hour == 24:
            hour = 0
            day += 1
            if day == 7:
                day = 0
    if pday != day: time += days[day]
    bruh = str(hour*100+half*30)
    while len(bruh) < 4: bruh = "0"+bruh
    time += " "+bruh
    return time


@app.route("/")
def index():
    username = get_username()
    if username:
        cmeetings = db.getconfirmedmeeting(username)

        if cmeetings != 0:
            for i in range(len(cmeetings)):
                cmeetings[i][2] = ", ".join(parse_time(cmeetings[i][2]))

        return render_template("index.html", cmeetings=cmeetings, username=username)
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

    pmeetings = db.getpendingmeeting(username)
    cmeetings = db.getconfirmedmeeting(username)
    if pmeetings != 0:
        for i in range(len(pmeetings)):
            pmeetings[i][2] = ", ".join(parse_time(pmeetings[i][2]))

    if cmeetings != 0:
        for i in range(len(cmeetings)):
            cmeetings[i][2] = ", ".join(parse_time(cmeetings[i][2]))

    if request.method == "GET":
        return render_template("meetings.html", pmeetings=pmeetings, cmeetings=cmeetings, username=username)
    else:
        meetingid = request.form["meetingid"]
        db.confirmmeeting(username, meetingid)
        return render_template("meetings.html", pmeetings=pmeetings, cmeetings=cmeetings, username=username)

@app.route("/create_meeting", methods=["GET", "POST"])
def create_meeting():
    username = get_username()
    if not username:
        return redirect(url_for("login"))

    over = db.findoverlaps(username)
    if over == 0:
        return render_template("create_meeting.html", olength=0, username=username)

    overs = []
    for i in range(len(over)):
        overs.append(list(over[i]))
        overs[i][1] = parse_stime(over[i][1])

    olength = len(over)
    if request.method == "GET":
        return render_template("create_meeting.html", overs=overs, over=over, olength=olength, username=username)
    else:
        if "user" in request.form:
            user = request.form["user"]
            time = request.form["time"]
            db.creatependingmeeting([user], int(time))
            return render_template("create_meeting.html", overs=overs, over=over, olength=olength, username=username)
        else:
            if "users" in request.form:
                users = request.form["users"].split(",")
                gtime = request.form["gtime"]
                for i in range(len(users)): users[i] = users[i].strip(" ")

                db.creatependingmeeting(users, int(gtime))                

                gover = db.findoverlaps2(users)
                govers = []
                for i in range(len(gover)):
                    govers.append(parse_stime(gover[i]))
            
                glength = len(govers)
                return render_template("create_meeting.html", overs=overs, over=over, olength=olength, gover=gover, govers=govers, username=username, glength=glength, users=request.form["users"])
            else:
                users = request.form["usernames"].split(",")
                for i in range(len(users)): users[i] = users[i].strip(" ")

                gover = db.findoverlaps2(users)
                govers = []
                for i in range(len(gover)):
                    govers.append(parse_stime(gover[i]))
            
                glength = len(govers)
                return render_template("create_meeting.html", overs=overs, over=over, olength=olength, gover=gover, govers=govers, username=username, glength=glength, users=request.form["usernames"])


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
        error = None

        if 'username' in request.form:
            friendreq = request.form["username"]
            if not db.requestfren(username, friendreq): error = "Cannot send friend request"

        else:
            friendreq = request.form["rusername"]
            if not db.confirmfren(friendreq, username, True): error = "Cannot accept friend request"
       
        friendl = db.getfren(username)
        rfriendl = db.getpfren(username)
        return render_template("friends.html", friendl=friendl, rfriendl=rfriendl, username=username, error=error)

#db.testallfunctions()

if __name__ == "__main__":
    import generate_test_data as gtd
    gtd.run()
    app.run(debug=True)
