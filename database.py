import sqlite3
from sqlite3 import Error

'''Database Outline (as of this commit)
* Users Table
- Username
- Phone no.
- Email
- Password
- Schedule
- Friends
- Pending Friends
- Meetups (IDs)

* Meet Table
- ID
- Users involved in meeting
- Time Period
- Messages
- Comfirmed or not
'''


def testallfunctions():
    con = sqlite3.connect('mydatabase.db')
    cursorObj = con.cursor()
    cursorObj.execute('drop table if exists users')
    cursorObj.execute('drop table if exists meet')
    cursorObj.execute(
        "CREATE TABLE users(username text PRIMARY KEY, phone integer, email text, password text, schedule text, friends text, pfriends text, meetings text)")
    cursorObj.execute(
        "CREATE TABLE meet(id integer PRIMARY KEY autoincrement, users text, time text, messages text, confirmed text)")
    print(register("HTY", 70707070, "lol@lol.com", "pp"))
    print(register("NGMH", 53180080, "imgay@lol.com", "pp"))
    print(register("HTY", 70707070, "lol@lol.com", "pp"))
    print(login("HTY", "passworld123"))
    print(login("HTY", "password123"))
    print(requestfren("HTY", "NGMH"))
    print(confirmfren("NGMH", "HTY", True))
    print(getfren("NGMH"))
    print(getfren("HTY"))
    # print(deletfren("NGMH", "HTY"))
    # print(getfren("NGMH"))
    # print(getfren("HTY"))
    print(editschedule("NGMH", "0"*335+"1"))
    print(editschedule("HTY", "0"*335+"1"))
    print(getschedule("HTY"))
    print(findoverlaps("HTY"))
    print(creatependingmeeting(["NGMH", "HTY"], "0"*335+"1"))
    print(confirmmeeting("HTY", 1))
    print(confirmmeeting("NGMH", 1))
    print(cancelmeeting(1))
    print(creatependingmeeting(["NGMH", "HTY"], "0"*335+"1"))
    print(confirmmeeting("HTY", 2))
    print(confirmmeeting("NGMH", 2))
    print(getpendingmeeting("HTY"))
    print(getconfirmedmeeting("HTY"))
    #cursorObj.execute('drop table if exists users')
    #cursorObj.execute('drop table if exists meet')
    # cursorObj.execute(
    # "CREATE TABLE users(username text PRIMARY KEY, phone integer, email text, password text, schedule text, friends text, pfriends text, meetings text)")
    # cursorObj.execute(
    # "CREATE TABLE meet(id integer PRIMARY KEY autoincrement, users text, time text, messages text, confirmed integer)")
    con.commit()
    con.close()


def register(username, phone, email, password):
    '''add new user
    input: username(must be unique, rest don't need to be for now), phone number, email, password
    output: 1 (success) or 0 (failure)'''
    try:
        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()
        schedule = "0" * 336
        cursorObj.execute(
            "INSERT INTO users VALUES('" + username + "'," + str(phone) + ",'" + email + "','" + password + "','" + schedule + "','','','')")
        con.commit()
        con.close()
        return 1
    except Exception as e:
        print(e)
        return 0


def login(username, password):
    '''check password
    input: username, password
    output: 1 (success) or 0 (failure)'''
    try:
        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()
        cursorObj.execute(
            "SELECT password FROM users where username = '" + username + "'")
        pw = cursorObj.fetchall()[0][0]
        con.close()
        return 1 if password == pw else 0
    except Exception as e:
        print(e)
        return 0


def requestfren(u1, u2):
    ''' making friends pt. 1: requester sends friend request to someone else
    input: username of requester, username of someone else
    output: 1 (success) or 0 (failure)'''
    try:
        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()
        cursorObj.execute(
            "SELECT friends FROM users where username = '" + u2 + "'")
        friends = cursorObj.fetchall()[0][0]
        cursorObj.execute(
            "SELECT pfriends FROM users where username = '" + u2 + "'")
        pfriends = cursorObj.fetchall()[0][0]
        if u1 not in pfriends and u1 not in friends:
            pfriends += "," + u1
        cursorObj.execute("UPDATE users SET pfriends = '" +
                          pfriends + "' where username = '" + u2 + "'")
        con.commit()
        con.close()
        return 1
    except Exception as e:
        print(e)
        return 0


def confirmfren(u2, u1, accepted):
    ''' making friends pt. 2: someone else agrees to be friends, so both now are each other's friends
    input: username of someone else, username of requester, accepted or rejected (1 or 0)
    output: 1 (success) or 0 (failure)'''
    try:
        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()
        if accepted:
            cursorObj.execute(
                "SELECT friends FROM users where username = '" + u2 + "'")

            friends = cursorObj.fetchall()[0][0] + "," + u1

            cursorObj.execute("UPDATE users SET friends = '" +
                              friends + "' where username = '" + u2 + "'")

            cursorObj.execute(
                "SELECT friends FROM users where username = '" + u1 + "'")

            friends = cursorObj.fetchall()[0][0] + "," + u2

            cursorObj.execute("UPDATE users SET friends = '" +
                              friends + "' where username = '" + u1 + "'")

        # u2 is the potentia friend!!
        # u1 is the requester
        cursorObj.execute(
            "SELECT pfriends FROM users where username = '" + u1 + "'")
        pfriends = cursorObj.fetchall()[0][0]
        if u2 in pfriends:
            pfriends = pfriends.replace("," + u2, "")

        # delete that entry in pfwens for the requester
        cursorObj.execute("UPDATE users SET pfriends = '" +
                          pfriends + "' where username = '" + u1 + "'")

        con.commit()
        con.close()
        return 1
    except Exception as e:
        print(e)
        return 0


def deletfren(u1, u2):
    ''' if either side does not want to be friends they will not be friends lol
    input: 2 usernames
    output: 1 (success) or 0 (failure)'''
    try:
        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()
        cursorObj.execute(
            "SELECT friends FROM users where username = '" + u2 + "'")
        friends = cursorObj.fetchall()[0][0].replace("," + u1, "")
        cursorObj.execute("UPDATE users SET friends = '" +
                          friends + "' where username = '" + u2 + "'")

        cursorObj.execute(
            "SELECT friends FROM users where username = '" + u1 + "'")
        friends = cursorObj.fetchall()[0][0].replace("," + u2, "")
        cursorObj.execute("UPDATE users SET friends = '" +
                          friends + "' where username = '" + u1 + "'")

        con.commit()
        con.close()
        return 1
    except Exception as e:
        print(e)
        return 0


def getfren(username):
    ''' returns list of friends
    input: username
    output: list of friends'''
    try:
        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()
        cursorObj.execute(
            "SELECT friends FROM users where username = '" + username + "'")
        frens = cursorObj.fetchall()[0][0].split(",")[1:]
        con.close()
        return frens
    except Exception as e:
        print(e)
        return 0


def getpfren(username):
    ''' returns list of pending friend requests
    input: username
    output: list of pending friends'''
    try:
        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()
        cursorObj.execute(
            "SELECT pfriends FROM users where username = '" + username + "'")
        pfrens = cursorObj.fetchall()[0][0].split(",")[1:]
        con.close()
        return pfrens
    except Exception as e:
        print(e)
        return 0


def editschedule(username, schedule):
    ''' if either side does not want to be friends they will not be friends lol
    input: username, schedule
    output: 1 (success) or 0 (failure)
    '''
    try:
        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()
        cursorObj.execute("UPDATE users SET schedule = '" +
                          schedule + "' where username = '" + username + "'")
        con.commit()
        con.close()
        return 1
    except Exception as e:
        print(e)
        return 0


def getschedule(username):
    ''' returns schedule in binary string format for 1 wk (half hour blocks, 0 is busy and 1 is free time)
    input: username
    output: schedule as binary string'''
    try:
        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()
        cursorObj.execute(
            "SELECT schedule FROM users where username = '" + username + "'")
        sched = cursorObj.fetchall()[0][0]
        con.close()
        return sched
    except Exception as e:
        print(e)
        return 0


def findoverlaps(username):
    '''find scheduling overlaps w all friends of a user
    input: username
    output: [(username, time), ...]
    '''
    try:
        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()
        cursorObj.execute(
            "SELECT friends FROM users where username = '" + username + "'")
        frens = cursorObj.fetchall()[0][0].split(",")[1:]
        cursorObj.execute(
            "SELECT schedule FROM users where username = '" + username + "'")
        schedule = cursorObj.fetchall()[0][0]
        lyst = []
        for f in frens:
            cursorObj.execute(
                "SELECT schedule FROM users where username = '" + f + "'")
            schedule2 = cursorObj.fetchall()[0][0]
            for i in range(336):
                if schedule2[i] == schedule[i] and int(schedule[i]):
                    lyst.append((f, i))
        return lyst
    except Exception as e:
        print(e)
        return 0


def findoverlaps2(usernames):
    '''find scheduling overlaps w all friends of a user
    input: list of usernames
    output: [(username, time), ...]
    '''
    try:
        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()
        schedules = []
        for u in usernames:
            cursorObj.execute(
                "SELECT schedule FROM users where username = '" + username + "'")
            schedules.append(cursorObj.fetchall()[0][0])

        for i in range(336):
            if 0 not in [schedule[i] for schedule in schedules]:
                lyst.append(i)
        return i
    except Exception as e:
        print(e)
        return 0


def creatependingmeeting(usernames, time):
    '''
    input: list of usernames, another giant binary string
    output: 1 (success) or 0 (failure)
    '''
    try:
        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()
        stryng = ",".join(usernames)
        stryng2 = "0"*len(usernames)
        cursorObj.execute(
            "INSERT INTO meet (users, time, messages, confirmed) VALUES('" + stryng + "','" + time + "','','" + stryng2 + "')")
        con.commit()
        cursorObj.execute(
            "SELECT last_insert_rowid()")
        id = cursorObj.fetchall()[0][0]
        for u in usernames:
            cursorObj.execute(
                "SELECT meetings FROM users where username = '" + u + "'")
            meeting = cursorObj.fetchall()[0][0] + "," + str(id)
            cursorObj.execute("UPDATE users SET meetings = '" +
                              meeting + "' where username = '" + u + "'")
        con.commit()
        con.close()
        return 1
    except Exception as e:
        print(e)
        return 0


def confirmmeeting(username, id):
    '''
    sets meeting as confirmed
    input: username, meeting ID
    '''
    try:
        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()
        cursorObj.execute(
            "SELECT users FROM meet where id = " + str(id))
        users = cursorObj.fetchall()[0][0].split(",")
        cursorObj.execute(
            "SELECT confirmed FROM meet where id = " + str(id))
        confirmed = cursorObj.fetchall()[0][0]
        newstring = ""
        for i in range(len(users)):
            if users[i] == username:
                newstring += "1"
            else:
                newstring += confirmed[i]
        cursorObj.execute(
            "UPDATE meet SET confirmed = '" + newstring + "' where id = " + str(id))
        con.commit()
        con.close()
        return 1
    except Exception as e:
        print(e)
        return 0


def cancelmeeting(id):
    '''
    delete meeting from db
    input: meeting ID
    '''
    try:
        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()
        cursorObj.execute(
            "DELETE FROM meet where id = " + str(id))
        con.commit()
        con.close()
        return 1
    except Exception as e:
        print(e)
        return 0


def addmeetingmsg(id, username, message):
    try:
        cursorObj.execute(
            "SELECT messages FROM meet where id =" + id + "'")
        messages = cursorObj.fetchall()[0][0]+","+username+":"+message
        con.commit()
        con.close()
    except Exception as e:
        print(e)
        return 0


def getmeetingmsg(id):
    try:
        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()
        cursorObj.execute(
            "SELECT messages FROM meet where id =" + id)
        messages = cursorObj.fetchall()[0][0]+","+username+":"+message
        return [i.split(":") for i in messages.split(",")]
        con.close()
    except Exception as e:
        print(e)
        return 0


def getpendingmeeting(username):
    try:
        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()
        meetings = []
        cursorObj.execute(
            "SELECT meetings FROM users where username ='" + username + "'")
        a = cursorObj.fetchall()[0][0]
        for id in a.split(",")[1:]:
            cursorObj.execute(
                "SELECT * FROM meet where id = " + id)
            ans = cursorObj.fetchall()
            if ans:
                meetings.append(ans[0])
        final = []
        for meeting in meetings:
            if "0" in meeting[4]:
                final.append([meeting[0], meeting[1].split(","), meeting[2]])
        return final
    except Exception as e:
        print(e)
        return 0


def getconfirmedmeeting(username):
    try:
        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()
        meetings = []
        cursorObj.execute(
            "SELECT meetings FROM users where username ='" + username + "'")
        a = cursorObj.fetchall()[0][0]
        for id in a.split(",")[1:]:
            cursorObj.execute(
                "SELECT * FROM meet where id =" + id)
            ans = cursorObj.fetchall()
            if ans:
                meetings.append(ans[0])
        final = []
        for meeting in meetings:
            if "0" not in meeting[4]:
                final.append([meeting[0], meeting[1].split(","), meeting[2]])
        return final
    except Exception as e:
        print(e)
        return 0


testallfunctions()
