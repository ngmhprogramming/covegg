import sqlite3

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


def register(): return

'''add new user
    input: username(must be unique, rest don't need to be for now), phone number, email, password
    output: 1 (success) or 0 (failure)'''


def login(): return


'''check password
    input: username(must be unique, rest don't need to be for now), password
    output: 1 (success) or 0 (failure)'''


def requestfren(): return


''' making friends pt. 1: requester sends friend request to someone else
    input: username of requester, username of someone else
    output: 1 (success) or 0 (failure)'''


def confirmfren(): return


''' making friends pt. 2: someone else agrees to be friends, so both now are each other's friends
    input: username of someone else, username of requester
    output: 1 (success) or 0 (failure)'''


def deletfren(): return


''' if either side does not want to be friends they will not be friends lol
    input: 2 usernames
    output: 1 (success) or 0 (failure)'''


def getfren(): return


''' returns list of friends
    input: username
    output: list of friends'''


def editschedule(): return

''' if either side does not want to be friends they will not be friends lol
    input: username, schedule
    output: 1 (success) or 0 (failure)
    '''


def getschedule(): return

''' returns schedule in binary string format for 1 wk (half hour blocks, 0 is busy and 1 is free time)
    input: username
    output: schedule as binary string'''
