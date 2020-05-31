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
- Pending friends

Adding soon: requests and chats
'''

con = sqlite3.connect('mydatabase.db')
cursorObj = con.cursor()


def setup():
    cursorObj.execute(
        "CREATE TABLE users(username text PRIMARY KEY, phone integer, email text, password text, schedule text, friends text, pfriends text)")
    con.commit()


def testallfunctions():
    cursorObj.execute('drop table if exists users')
    setup()
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
        schedule = "0" * 336
        cursorObj.execute(
            "INSERT INTO users VALUES('" + username + "'," + str(phone) + ",'" + email + "','" + password + "','" + schedule + "','','')")
        con.commit()
        return 1
    except Error:
        print(Error)
        return 0


def login(username, password):
    '''check password
    input: username(must be unique, rest don't need to be for now), password
    output: 1 (success) or 0 (failure)'''
    try:
        cursorObj.execute(
            "SELECT password FROM users where username = '" + username + "'")
        pw = cursorObj.fetchall()[0][0]
        return 1 if password == pw else 0
    except Error:
        print(Error)
        return 0


def requestfren(u1, u2):
    ''' making friends pt. 1: requester sends friend request to someone else
    input: username of requester, username of someone else
    output: 1 (success) or 0 (failure)'''
    try:
        cursorObj.execute(
            "SELECT pfriends FROM users where username = '" + u2 + "'")
        pfriends = cursorObj.fetchall()[0][0]
        if u1 not in pfriends:
            pfriends += "," + u1
        cursorObj.execute("UPDATE users SET pfriends = '" +
                          pfriends + "' where username = '" + u2 + "'")
        con.commit()
        return 1
    except Error:
        print(Error)
        return 0


def confirmfren(u2, u1, accepted):
    ''' making friends pt. 2: someone else agrees to be friends, so both now are each other's friends
    input: username of someone else, username of requester, accepted or rejected (1 or 0)
    output: 1 (success) or 0 (failure)'''
    try:
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
        return 1
    except Error:
        print(Error)
        return 0


def deletfren(u1, u2):
    ''' if either side does not want to be friends they will not be friends lol
    input: 2 usernames
    output: 1 (success) or 0 (failure)'''
    try:
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
        return 1
    except Error:
        print(Error)
        return 0


def getfren(username):
    ''' returns list of friends
    input: username
    output: list of friends'''
    try:
        cursorObj.execute(
            "SELECT friends FROM users where username = '" + username + "'")
        return cursorObj.fetchall()[0][0].split(",")[1:]
    except Error:
        print(Error)
        return 0


def editschedule(username, schedule):
    ''' if either side does not want to be friends they will not be friends lol
    input: username, schedule
    output: 1 (success) or 0 (failure)
    '''
    try:
        cursorObj.execute("UPDATE users SET schedule = '" +
                          schedule + "' where username = '" + username + "'")
        return 1
    except Error:
        print(Error)
        return 0


def getschedule():
    ''' returns schedule in binary string format for 1 wk (half hour blocks, 0 is busy and 1 is free time)
    input: username
    output: schedule as binary string'''
    try:
        cursorObj.execute(
            "SELECT schedule FROM users where username = '" + username + "'")
        return cursorObj.fetchall()[0][0]
    except Error:
        print(Error)
        return 0


testallfunctions()
