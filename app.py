from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = "shellshock69420"

def get_username():
    if "username" in session: return session["username"]
    return False

@app.route("/")
def index():
    #username = get_username()
    username = True
    if username:
        return render_template("index.html", username=username)
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        
        #user = db_session.query(User).filter_by(name=name).first()
        #if user is None or user.password != hash(password):
        #    return render_template("login.html", error="Invalid Username or Password")

        session["username"] = username
        return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        if username is "":
            return render_template("signup.html", error="No Username Specified")
        if password is "":
            return render_template("signup.html", error="No Password Specified")

        password = hash(password)
        #user = User(type_no, location, name, password)
        #db_session.add(user)
        #db_session.commit()
        return redirect(url_for("login"))

@app.route("/schedule")
def schedule():
    pass

@app.route("/meet")
def meet_new_ppl():
    pass

@app.route("/friends")
def friend_groups():
    pass

@app.route("/profile")
def profile():
    pass

if __name__ == "__main__":
    app.run(debug=True)

