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

	print(requestfren("HTY", "NGMH"))
	#mun hin request to be tengyi's friend

	#teng yi accepts munhun's friend request
	print(confirmfren("HTY", "NGMH", True))

	print(editschedule("NGMH", "0"*335+"1"))
	print(editschedule("HTY", "0"*335+"1"))

	requestfren("HTY", "nuode")
	requestfren("NGMH", "nuode")

	confirmfren("HTY", "nuode", True)
	confirmfren("NGMH", "nuode", True)

	print(editschedule("nuode", "1"*10+"0"*325+"1"))
	print(editschedule("Jeff", "0"*300+"1"*36))

	#print(getschedule("HTY"))
	
	print(requestfren("HTY", "Jeff"))


	"""
	print(getfren("NGMH"))
	print(getfren("HTY"))

	# print(deletfren("NGMH", "HTY"))
	# print(getfren("NGMH"))
	# print(getfren("HTY"))

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
	"""


	con.commit()
	con.close()
	print("All test data generated")