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
- Pending or Not
'''


def testallfunctions():
    con = sqlite3.connect('mydatabase.db')
    cursorObj = con.cursor()
    cursorObj.execute('drop table if exists users')
    cursorObj.execute(
        "CREATE TABLE users(username text PRIMARY KEY, phone integer, email text, password text, schedule text, friends text, pfriends text, meetings text)")
    cursorObj.execute(
        "CREATE TABLE meet(id text PRIMARY KEY, users text, time text, messages text, confirmed integer)")
    con.commit()
    con.close()
    print(register("HTY", 70707070, "lol@lol.com", "passworld123"))
    print(register("NGMH", 53180080, "imgay@lol.com", "iloverubikcube"))
    print(register("HTY", 70707070, "lol@lol.com", "passworld123"))
    print(login("HTY", "passworld123"))
    print(login("HTY", "password123"))
    print(requestfren("HTY", "NGMH"))
    print(confirmfren("NGMH", "HTY", True))
    print(getfren("NGMH"))
    print(getfren("HTY"))
    print(deletfren("NGMH", "HTY"))
    print(getfren("NGMH"))
    print(getfren("HTY"))


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
    except Error as e:
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
    except Error as e:
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
            "SELECT pfriends FROM users where username = '" + u2 + "'")
        pfriends = cursorObj.fetchall()[0][0]
        if u1 not in pfriends:
            pfriends += "," + u1
        cursorObj.execute("UPDATE users SET pfriends = '" +
                          pfriends + "' where username = '" + u2 + "'")
        con.commit()
        con.close()
        return 1
    except Error as e:
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

        cursorObj.execute(
            "SELECT pfriends FROM users where username = '" + u2 + "'")
        pfriends = cursorObj.fetchall()[0][0]
        if u1 in pfriends:
            pfriends = pfriends.replace("," + u1, "")

        con.commit()
        con.close()
        return 1
    except Error as e:
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
    except Error as e:
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
    except Error:
        print(Error)
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
        con.close()
        return 1
    except Error as e:
        print(e)
        return 0


def getschedule():
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
    except Error as e:
        print(e)
        return 0


def createmeeting(): return


'''
    input: list of usernames, timeframe (number from 0 to 336)
    output: 1 (success) or 0 (failure)
    '''


def confirmmeeting(): return


def cancelmeeting(): return


def msgmeeting(): return


# testallfunctions()
