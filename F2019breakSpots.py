from googlemaps.client import Client
from googlemaps.distance_matrix import distance_matrix
api_key = "YOUR_API_KEY_HERE"
gmaps = Client(api_key)

#Stores real world addresses of all of the buildings in my schedules
buildingLocation = {
"Thomas Bldg":"Joab L. Thomas Bldg, 16802, Shortlidge Rd, State College, PA 16802",
"Westgate Bldg":"E397 Westgate Building, University Park, PA 16802",
"Boucke Bldg":"Boucke Building, University Park, PA 16802",
"Walker Building":"Walker Building, 302 N Burrowes Street, University Park, PA 16802",
"Earth and Sciences":"Earth and Engineering Sciences Building, State College, PA 16801",
"Osmond Lab":"Osmond Laboratory, State College, PA 16801",
"Library":"107 Pattee library Rd, State College, PA 16801",
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
"Findlay" : "Findlay Commons, State College, PA 16802",
"Dorm" : "Nelson Hall, State College, PA 16801"
}

campusAttractions = ("Pollock", "Reddifer", "West", "Warnock", "Findlay", "Library")

#Comma is essential: Defines a one element tuple
dorm = ("Dorm",)

#Walking speed is in meters per minute
walkingSpeed = 80
#This variable declares the program will only suggest a location for you to visit if you can spend at least minimumTimeToSpend minutes there
minimumTimeToSpend = "00:25"

#I created a schedule class solely for the ability to easily add new schedules.
class StudentSchedule:

	def __init__(self,schedule = []):
		self.schedule = schedule

	def __str__(self):
		return self.schedule

	__repr__ = __str__

	@property
	def buildSchedule(self):
		while eval(input("Add another class? Type None to stop")):
			slot = []
			slot.append(input("What building is this class in?"))
			slot.append(input("What time does this class start at?"))
			slot.append(input("What time does this class end at?"))
			slot.append(eval(input("What dates does this class take place? Answer in a list")))
			self.schedule += [slot]

#Some of my personal preset schedules
schedule1 = StudentSchedule([["Thomas Bldg", "09:05", "09:55", ["Mon", "Wed", "Fri"]], ["Westgate Bldg", "13:25" , "15:20", ["Tue"]], ["Boucke Bldg", "10:35", "11:50", ["Tue"]], ["Thomas Bldg", "16:40", "17:30", ["Mon", "Wed", "Fri"]], ["Walker Building", "09:05", "10:20", ["Tue", "Thr"]], ["Earth and Sciences", "13:35", "14:50", ["Thr"]], ["Osmond Lab", "16:40", "18:35", ["Thr"]], ["Osmond Lab", "08:00", "08:50", ["Tue", "Thr"]]])
schedule2 = StudentSchedule([["Forum Bldg", "09:05", "09:55", ["Mon", "Wed", "Fri"]],["Forum Bldg", "10:10", "11:00", ["Mon", "Wed", "Fri"]],["Hammond Bldg", "10:10", "12:05", ["Tue","Thr"]], ["Willard Bldg", "11:15", "12:05",["Mon", "Wed", "Fri"]],["Nursing Sciences Bldg", "12:20", "13:10", ["Thr"]],["Thomas Bldg", "13:35", "14:50", ["Tue", "Thr"]], ["Hammond Bldg", "15:35", "17:30", ["Tue"]], ["Whitmore Lab", "13:25", "17:30", ["Wed"]]])

#This program uses operations between times, and I preferred to just use my own time class rather than use datetime. This class just allows representation
#and operations between instances of my HourMin class (times)
class HourMin:

	def __init__(self,hourminute): 
		self.hour = int(hourminute[0:2])
		self.minute = int(hourminute[3:5])
		self.negative = False

	def __str__(self):
		reprHour = "0" + str(self.hour) if len(str(self.hour)) == 1 else str(self.hour)
		reprMin = "0" + str(self.minute) if len(str(self.minute)) == 1 else str(self.minute)
		if self.negative == True:
			return f'-{self.hour}:{self.minute}'
		return f'{reprHour}:{reprMin}'

	__repr__ = __str__

	def __hash__(self):
		return hash((self.hour,self.minute))

	def __eq__(self,other):
		if self.hour == other.hour and self.minute == other.minute:
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
		negative = False
		if other > self:
			self,other = other,self
			negative = True

		time1 = [self.hour, self.minute]; time2 = [other.hour, other.minute]

		if self.minute - other.minute < 0:
			time1[0] -= 1
			time1[1] += 60

		returnTime = HourMin(':'.join(['0' + str(x) if len(str(x)) == 1 else str(x) for x in (time1[0] - time2[0], time1[1] - time2[1])]))
		if negative:
			returnTime.negative = True
		return returnTime


	def __add__(self,other):
		returnHour, returnMin = self.hour + other.hour, self.minute + other.minute
		if returnMin >= 60:
			returnMin -= 60
			returnHour += 1
		return HourMin(':'.join(['0' + str(x) if len(str(x)) == 1 else str(x) for x in (returnHour, returnMin)]))

#Converts a nonstandard time to a standard one (1:00 -> 01:00)
def timeConvert(time):
	time = int(time)
	hour = '0' + str(time // 60) if len(str(time // 60)) == 1 else time // 60
	minute = '0' + str(time % 60) if len(str(time % 60)) == 1 else time % 60
	return HourMin(f'{hour}:{time}')

#Creates gramatically proper references to hours and minutes when referencing instances of my HourMin class. 
#Example: if the time has no hour portion, the resulting string will not include a reference to the hours
#Similarly, the string will only include s's (i.e. minutes) if the hour/minute is greater than one.
def formatTime(time):
	hourSyntax = 's' if time.hour > 1 else ''
	minuteSyntax = 's' if time.minute > 1 else ''

	if time.hour == 0 and time.minute == 0 or time.negative:
		return None

	elif time.hour == 0:
		return(f'{time.minute} minute{minuteSyntax}')
	
	elif time.minute == 0:
		return(f'{time.hour} hour{hourSyntax}')	
	
	else:
		return(f'{time.hour} hour{hourSyntax} and {time.minute} minute{minuteSyntax}')	

#Takes in a schedule and date and responds with only the classes on that date
def dateSelect(date, schedule):
	return [x[0:3] for x in schedule if date in x[3]]

#Converts a schedule's times from strings to instances of HourMin
def listTimeConvert(schedule):
	for eachClass in schedule:
		eachClass[:] = [HourMin(x) if x[2] == ':' else x for x in eachClass]
	return schedule

#Sorts the schedules based on starting times
def dateSort(schedule):
	return sorted(schedule,key = lambda x: x[1])

#Takes in two classes and returns the time between the first's end and the second's start
def breakTime(partialSchedule):
	return partialSchedule[1][1] - partialSchedule[0][2]

#Takes in two locations and uses Google Maps' distance matrix API to calculate the distance between them
#Returns approximate time to walk between the two locations
def travelTime(location1, location2):
	distance = float(''.join([x for x in distance_matrix(gmaps, location1, location2, mode = "walking")["rows"][0]["elements"][0]["distance"]["text"] if (x.isdigit() or x == '.')]))
	return timeConvert(distance * 1000 // walkingSpeed)

#Takes in a list of options to visit, a starting location, and an ending location. The code checks the time to walk from the start location to each option to the end location, and
#returns the smallest option and that options total time
def bestOptionToVisit(options, originalLocation, finalLocation):
	travelList = list(map(lambda x,y: x + y, [travelTime(buildingLocation[originalLocation], buildingLocation[x]) for x in options], \
		[travelTime(buildingLocation[finalLocation], buildingLocation[x]) for x in options]))
	minimumTime = min(travelList)
	return options[travelList.index(minimumTime)], minimumTime

def main():
	date = input("What day is it?")
	validDates = ["Mon", "Tue", "Wed", "Thr", "Fri"]
	while date not in validDates:
		date = input(f'Choose a date in {validDates}')

	dateSchedule = dateSort(listTimeConvert(dateSelect(date, schedule2.schedule)))
	breakSpotNumber = int(input(f'You have {len(dateSchedule)} classes today \nAfter what number class are you curious about your BreakSpot?'))
	while not (len(dateSchedule) > breakSpotNumber > 0):
		breakSpotNumber = int(input(f'Invalid input, try again: '))

	breakSpotPair = dateSchedule[breakSpotNumber - 1], dateSchedule[breakSpotNumber]
	trueTimeBetweenClasses = breakTime(breakSpotPair) - travelTime(*[buildingLocation[x[0]] for x in breakSpotPair])

	if not formatTime(trueTimeBetweenClasses):
		print("You have no time for break! You best get a move on!")
		return()
	
	print(f'From {breakSpotPair[0][0]} to {breakSpotPair[1][0]}, you\'ll have about {formatTime(trueTimeBetweenClasses)} of break, excluding walking')
	
#Here is a list that displays a different prompt depending on how much time you'll have on your break. 

	timeList = [(HourMin(x),y) for (x,y) in [("00:00", 'G'), ("00:15", 'G'), ("00:30", 'G'), ("00:45", campusAttractions), ("01:30", dorm)]]
	instructionList = ["You don't have much time. You ought to just head to class",
	"You have a little bit of time between classes \nPerhaps you could go for a quick study break?",
	"You have a decent amount of time before you ought to head to class \nMaybe go catch up with your friends?",
	"You have a while before you ought to head to class \nNow's a great time to sit down and eat or hit the Library!",
	"You have a ton of time before you ought to head to class \nYou can definitely get away with a visit to your dorm."]

	instructionDict = {timeList[i]:instructionList[i] for i in range(len(timeList))}

	for timeVal in timeList[::-1]:
		if trueTimeBetweenClasses < timeVal[0]:
			continue

		if trueTimeBetweenClasses > timeVal[0] and timeVal[1] != 'G':
			bestOption = bestOptionToVisit(timeVal[1], breakSpotPair[0][0], breakSpotPair[1][0])
			timeToSpendAtLocation = breakTime(breakSpotPair) - bestOption[1] 
			if timeToSpendAtLocation < HourMin(minimumTimeToSpend) or timeToSpendAtLocation.negative:
				continue

		print(instructionDict[timeVal])

		if timeVal[1] == campusAttractions:
			
			print(f'The Library is where you want to go. It\`s closest to you.') if bestOption[0] == "Library" \
			else print(f'Visit {bestOption[0]} Commons: it\'s the closest to you.')
			

		if timeVal[1] == campusAttractions or timeVal[1] == dorm:
			print(f'You\'ll be able to spend {formatTime(timeToSpendAtLocation)} there.')
		return()

main()
