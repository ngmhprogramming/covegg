from database import *

def run():
	con = sqlite3.connect('mydatabase.db')
	cursorObj = con.cursor()

	cursorObj.execute('drop table if exists users')
	cursorObj.execute('drop table if exists meet')
	cursorObj.execute("CREATE TABLE users(username text PRIMARY KEY, phone integer, email text, password text, schedule text, friends text, pfriends text, meetings text)")
	cursorObj.execute("CREATE TABLE meet(id integer PRIMARY KEY autoincrement, users text, time text, messages text, confirmed integer)")


	register("HTY", 70707070, "lol@lol.com", "pp")
	register("NGMH", 53180080, "imgay@lol.com", "pp")
	register("nuode", 53181080, "imgay@lol.com", "pp")
	register("Jeff", 53181080, "imgay@lol.com", "pp")

	print(requestfren("HTY", "NGMH")) #hty request to ngmh, friend request should show on ngmh
	print(confirmfren("HTY", "NGMH", True)) #ngmh accept the friendrequest
	
	print(requestfren("nuode", "NGMH")) #hty request to ngmh, friend request should show on ngmh
	print(confirmfren("nuode", "NGMH", True)) #ngmh accept the friendrequest
	
	print(requestfren("Jeff", "NGMH")) #hty request to ngmh, friend request should show on ngmh

	print(editschedule("NGMH", "0"*334+"11"))
	print(editschedule("HTY", "0"*334+"11"))
	print(editschedule("Jeff", "0"*324+"1"*12))
	print(editschedule("nuode", "0"*333+"111"))


	"""
	print(getschedule("HTY"))
	print(findoverlaps("HTY"))
	print(findoverlaps2(["HTY", "NGMH"]))
	print(creatependingmeeting(["NGMH", "HTY"], 335))
	print(confirmmeeting("HTY", 1))
	print(confirmmeeting("NGMH", 1))
	print(cancelmeeting(1))
	print(creatependingmeeting(["NGMH", "HTY"], 335))
	print(confirmmeeting("HTY", 2))
	print(confirmmeeting("NGMH", 2))
	print(getpendingmeeting("HTY"))
	print(getconfirmedmeeting("HTY"))
	"""

	con.commit()
	con.close()
	print("All test data generated")