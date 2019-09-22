
'''
building_start_end=[]
dates=[]
infolist = []
classnumber=input("How many classes do you have?")

for n in range(classnumber):

	building,starttime,endtime=input("Enter building location, start time, end time:").split(",")
	building_start_end.append(building)
	building_start_end.append(starttime)
	building_start_end.append(endlist)

	dates=input("Enter the dates for which you have this class")
	dateslist = dates.split(",")
	building_start_end.append(dateslist)
	infolist.append(building_start_end)
	
'''

walkingspeed = 120

infolist2 = [["Thomas Bldg", "09:05", "09:55", ["Mon", "Wed", "Fri"]], ["Westgate Bldg", "13:25" , "15:20", ["Tue"]], ["Boucke Bldg", "10:35", "11:50", ["Tue"]], ["Thomas Bldg", "16:40", "17:30", ["Mon", "Wed", "Fri"]], ["Walker Building", "09:05", "10:20", ["Tue", "Thr"]], ["Earth and Sciences", "13:35", "14:50", ["Thr"]], ["Osmond Lab", "16:40", "18:35", ["Thr"]], ["Osmond Lab", "08:00", "08:50", ["Tue", "Thr"]]]
infolist = [["Forum Bldg", "09:05", "09:55", ["Mon", "Wed", "Fri"]],["Forum Bldg", "10:10", "11:00", ["Mon", "Wed", "Fri"]],["Hammond Bldg", "10:10", "12:05", ["Tue","Thr"]], ["Willard Bldg", "11:15", "12:05",["Mon", "Wed", "Fri"]],["Nursing Sciences Bldg", "12:20", "13:10", ["Thr"]],["Thomas Bldg", "13.35", "14:50", ["Tue", "Thr"]], ["Hammond Bldg", "15:35", "17:30", ["Tue"]], ["Whitmore Lab", "13:25", "17:30", ["Wed"]]]

dorm = "0324 Nelson, University Park, PA 16802"


class Hour_Min:

	def __init__(self,hourminute):
		self.hour = int(hourminute[0:2])
		self.minute = int(hourminute[3:5])
		self.negative = False

	def __str__(self):
		if len(str(self.hour)) == 1:
			self.hour = "0" + str(self.hour) 
		if len(str(self.minute)) == 1:
			self.minute = "0" + str(self.minute) 
		if self.negative == True:
			return "-{}:{}".format(self.hour,self.minute)
		return "{}:{}".format(self.hour,self.minute)


	__repr__=__str__

	def __eq__(self,other):
		if (int(self.hour) == int(other.hour) and int(self.minute) == int(other.minute)):
			return True
		return False

	def __lt__(self,other):
		if self.hour < other.hour:
			return True
		elif self.hour == other.hour:
			if self.minute < other.minute:
				return True
			return False
		return False

	def __gt__(self,other):
		if self.hour > other.hour:
			return True
		elif self.hour == other.hour:
			if self.minute > other.minute:
				return True
			return False
		return False

	def __sub__(self,other):
		toggle = False
		returnhour = self.hour - other.hour
		returnminute = self.minute - other.minute
		if returnhour < 0:
			returnhour = other.hour - self.hour
			returnminute = other.minute - self.minute
			toggle = True

		if returnminute < 0:
			returnhour -= 1
			returnminute += 60
		if len(str(returnhour)) == 1:
			returnhour = "0" + str(returnhour)
		if len(str(returnminute)) == 1:
			returnminute = "0" + str(returnminute)
		if toggle == True:
			returntime = str(returnhour) + ":" + str(returnminute)
			x = Hour_Min(returntime)
			x.negative = True
			return(x)

		returntime = str(returnhour) + ":" + str(returnminute)
		return(Hour_Min(returntime))

	def __add__(self,other):
		returnhour = self.hour + other.hour
		returnminute = self.minute + other.minute
		if returnminute >= 60:
			returnminute -= 60
			returnhour += 1
		if len(str(returnhour)) == 1:
			returnhour = "0" + str(returnhour)
		if len(str(returnminute)) == 1:
			returnminute = "0" + str(returnminute)
		returnstring = str(returnhour) + ":" + str(returnminute) 
		return(Hour_Min(returnstring))


for element in range(len(infolist)):
	infolist[element][1] = Hour_Min(infolist[element][1])
	infolist[element][2] = Hour_Min(infolist[element][2])


classnumber = len(infolist)
mon_classes = []
tues_classes = []
weds_classes = []
thurs_classes = []
fri_classes = []
for singleclass in range(classnumber):
	if "Mon" in infolist[singleclass][3]:
		mon_classes.append(infolist[singleclass])
	if "Tue" in infolist[singleclass][3]:
		tues_classes.append(infolist[singleclass])
	if "Wed" in infolist[singleclass][3]:
		weds_classes.append(infolist[singleclass])
	if "Thr" in infolist[singleclass][3]:
		thurs_classes.append(infolist[singleclass])
	if "Fri" in infolist[singleclass][3]:
		fri_classes.append(infolist[singleclass])				

#SORTING
sortedmon = []
sortedtues = []
sortedweds = []
sortedthurs = [] 
sortedfri = []

def sort(sorteddate,date_classes):
	switch = False
	for oldclass in range(len(date_classes)):
		if switch == True:
			for newclass in range(len(sorteddate)):
				if date_classes[oldclass][1] < sorteddate[newclass][1]:
					sorteddate.insert(newclass,date_classes[oldclass])
					break
			if date_classes[oldclass] not in sorteddate:
				sorteddate.append(date_classes[oldclass])
		elif switch == False:
			sorteddate.append(date_classes[oldclass])
			switch = True
	return(sorteddate)

sortedmon = sort(sortedmon,mon_classes)
sortedtues = sort(sortedtues,tues_classes)
sortedweds = sort(sortedweds,weds_classes)
sortedthurs = sort(sortedthurs,thurs_classes)
sortedfri = sort(sortedfri,fri_classes)

#BREAKS

monbreak = []
tuesbreak = []
wedsbreak = []
thursbreak = []
fribreak = []

def schedbreak(sorteddate,datebreak):
	for element in range(len(sorteddate)-1):
		datebreak.append(sorteddate[element+1][1] - sorteddate[element][2])
	return(datebreak)

monbreak = schedbreak(sortedmon,monbreak)
tuesbreak = schedbreak(sortedtues,tuesbreak)
wedsbreak = schedbreak(sortedweds,wedsbreak)
thursbreak = schedbreak(sortedthurs,thursbreak)
fribreak = schedbreak(sortedfri,fribreak)

#BUILDING DICTIONARY

buildinglocation = {
"Thomas Bldg":"Joab L. Thomas Bldg, 16802, Shortlidge Rd, State College, PA 16802",
"Westgate Bldg":"E397 Westgate Building, University Park, PA 16802",
"Boucke Bldg":"Boucke Building, University Park, PA 16802",
"Walker Building":"Walker Building, 302 N Burrowes Street, University Park, PA 16802",
"Earth and Sciences":"Earth and Engineering Sciences Building, State College, PA 16801",
"Osmond Lab":"Osmond Laboratory, State College, PA 16801",
"library":"107 Pattee library Rd, State College, PA 16801",
"Forum Bldg":"Forum Building University Park, PA 16802",
"Hammond Bldg":"Hammond Building University Park, PA 16802",
"Willard Bldg":"Willard Buiding University Park, PA 16802",
"Nursing Sciences Bldg":"Nursing Sciences Building, University Park, PA 16802",
"Thomas Bldg":"Joab L. Thomas Bldg, 16802, Shortlidge Rd, State College, PA 16802",
"Whitmore Lab":"Whitmore Lab Pollock Road, State College, PA 16801",
"Pollock":"215 Bigler Rd, State College, PA 16801",
"Reddifer":"Reddifer Commons, E College Ave, State College, PA 16801",
"West":"343 Burrowes Rd, State College, PA 16801",
"Warnock" : "115 Warnock Commons, State College, PA 16803",
"Findlay" : "Findlay Commons, State College, PA 16802"
}
	

from googlemaps.client import Client
from googlemaps.distance_matrix import distance_matrix
api_key = "YOUR_API_KEY_HERE"

gmaps = Client(api_key)


#TRAVEL TIME

montravel = []
tuestravel = []
wedstravel = []
thurstravel = []
fritravel = []

def traveltime(sorteddate, datetravel):
	for element in range(len(sorteddate)-1):
		location1 = buildinglocation[sorteddate[element][0]]
		location2 = buildinglocation[sorteddate[element+1][0]]
		if location1 == location2:
			datetravel.append(Hour_Min("00:00"))
		else:
			distance = distance_matrix(gmaps, location1, location2)
			meterstraveled = distance["rows"][0]["elements"][0]["distance"]["value"]
			timetraveling = meterstraveled // walkingspeed
			hours = str(timetraveling // 60)
			minutes = str(timetraveling % 60)
			if len(hours) == 1:
				hours = "0" + hours
			if len(minutes) == 1:
				minutes = "0" + minutes
			totaltime = hours + ":" + minutes
			datetravel.append(Hour_Min(totaltime))
	return(datetravel)

def traveltime2point(location1,location2):
	if location1 == location2:
		datetravel.append(Hour_Min("00:00"))
	else:
		distance = distance_matrix(gmaps, location1, location2,)
		meterstraveled = distance["rows"][0]["elements"][0]["distance"]["value"]
		timetraveling = meterstraveled // walkingspeed
		hours = str(timetraveling // 60)
		minutes = str(timetraveling % 60)
		if len(hours) == 1:
			hours = "0" + hours
		if len(minutes) == 1:
			minutes = "0" + minutes
		totaltime = hours + ":" + minutes
		return(Hour_Min(totaltime))

montravel = traveltime(sortedmon,montravel)
tuestravel = traveltime(sortedtues,tuestravel)
wedstravel = traveltime(sortedweds,wedstravel)
thurstravel = traveltime(sortedthurs,thurstravel)
fritravel = traveltime(sortedfri,fritravel)


#BREAKSPOTS

monbreakspots = []
tuesbreakspots = []
wedsbreakspots = []
thursbreakspots = []
fribreakspots = []

def breakspotsfinder(datebreak,datetravel,datebreakspots):
	for element in range(len(datebreak)):
		datebreakspots.append(datebreak[element] - datetravel[element])
	return(datebreakspots)

monbreakspots = breakspotsfinder(monbreak,montravel,monbreakspots)
tuesbreakspots = breakspotsfinder(tuesbreak,tuestravel,tuesbreakspots)
wedsbreakspots = breakspotsfinder(wedsbreak,wedstravel,wedsbreakspots)
thursbreakspots = breakspotsfinder(thursbreak,thurstravel,thursbreakspots)
fribreakspots = breakspotsfinder(fribreak,fritravel,fribreakspots)

def pitstop(breaktime,location1,location2,dorm):

	v = Hour_Min("00:00")
	w = Hour_Min("00:15")
	x = Hour_Min("00:30")
	y = Hour_Min("00:45")
	z = Hour_Min("01:00")



	if (breaktime < v):
		print ("RUN! Your next class is super far away!")
	elif (w > breaktime > v)  or (breaktime == v):
		print ("You don't have much time. You ought to just head to class.")
	elif (x > breaktime >w) or (breaktime == w):
		print ("_________________ You have [" + str(breaktime) +"] _________________\nYou have a little bit of time between classes \n Perhaps you could go for a quick study break?")
	elif (y > breaktime >x) or (breaktime == x):
		print ("_________________ You have [" + str(breaktime) + "] _________________\nYou have a decent amount of time before you ought to head to class \n Maybe go catch up with your friends?")
	elif (z > breaktime >y) or (breaktime == y):
		print ("_________________ You have [" + str(breaktime) + "] _________________\nYou have a while before you ought to head to class \n Now's a great time to sit down and eat!")

		Reddifer_time = ((traveltime2point(buildinglocation[location1], buildinglocation["Reddifer"])) + (traveltime2point(buildinglocation[location2], buildinglocation["Reddifer"])))
		Findlay_time = ((traveltime2point(buildinglocation[location1], buildinglocation["Findlay"])) + (traveltime2point(buildinglocation[location2], buildinglocation["Findlay"])))
		Warnock_time = ((traveltime2point(buildinglocation[location1], buildinglocation["Warnock"])) + (traveltime2point(buildinglocation[location2], buildinglocation["Warnock"]))) 
		Pollock_time = ((traveltime2point(buildinglocation[location1], buildinglocation["Pollock"])) + (traveltime2point(buildinglocation[location2], buildinglocation["Pollock"])))
		West_time = ((traveltime2point(buildinglocation[location1], buildinglocation["West"])) + (traveltime2point(buildinglocation[location2], buildinglocation["West"])))
		cafetimelist = [[Reddifer_time,"Reddifer"],[Findlay_time,"Findlay"],[Warnock_time,"Warnock"],[Pollock_time,"Pollock"],[West_time,"West"]]
		cafetimereturn = cafetimelist[0][0]
		cafeplacereturn = cafetimelist[0][1]
		for element in range(len(cafetimelist)):
			if cafetimelist[element][0] < cafetimereturn:
				cafetimereturn = cafetimelist[element][0]
				cafeplacereturn = cafetimelist[element][1]
		print(cafeplacereturn, "is closest to you. You'll be able to spend [" + str(cafetimereturn) + "] of time there.")

	elif ((traveltime2point(buildinglocation[location1], dorm) + (traveltime2point(buildinglocation[location2], dorm))) < breaktime) and (breaktime > z):
		totaltraveltime = ((traveltime2point(buildinglocation[location1], dorm) + (traveltime2point(buildinglocation[location2], dorm))))
		print ("_________________ You have [" + str(breaktime-totaltraveltime)+ "] to potentially spend at your dorm" + "_________________\nYou have more than an hour before you ought to head to class\n You can definitely get away with a visit to your dorm.")
		if ((traveltime2point(buildinglocation[location1], buildinglocation["library"]) + (traveltime2point(buildinglocation[location2], buildinglocation["library"]))) < breaktime) and (breaktime > z):
			totaltraveltime = ((traveltime2point(buildinglocation[location1], buildinglocation["library"]) + (traveltime2point(buildinglocation[location2], buildinglocation["library"]))))
			print ("_________________ You have [" + str(breaktime-totaltraveltime)+ "] to potentially spend at the library" + "_________________\nYou have more than an hour before you ought to head to class\n Maybe read a bit?")



def prompt(datebreakspots,sorteddate):
	switch = False
	numberofclasses = int(len(datebreakspots)) + 1
	print("You have " + str(numberofclasses) + " classes today.")
	while switch is False:
		classnumberinput = int(input("After what number class are you curious about your BreakSpot?"))
		if (classnumberinput >= numberofclasses):
			print("Invalid entry")
		if (classnumberinput) < numberofclasses:
			switch = True
	print("That class is between " + sorteddate[classnumberinput-1][0] + " and " + sorteddate[classnumberinput][0])
	pitstop(datebreakspots[classnumberinput - 1],sorteddate[classnumberinput-1][0],sorteddate[classnumberinput][0],dorm)



date = input("What day is it?")
if date == "Monday":
	prompt(monbreakspots,sortedmon)
elif date == "Tuesday":
	prompt(tuesbreakspots,sortedtues)
elif date == "Wednesday":
	prompt(wedsbreakspots,sortedweds)
elif date == "Thursday":
	prompt(thursbreakspots,sortedthurs)
elif date == "Friday":
	prompt(fribreakspots,sortedfri)
else:
	print("Input a full-length weekday.")





