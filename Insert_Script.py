#Python script for inserting new data

import datetime
from datetime import datetime as dt

import mysql.connector
import random

db = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="T@stigers231",
	database = "train_db"
	)


mcurs = db.cursor(buffered = True)

#Functions for creating test data for each train route

def input_New_Train(DateofTrain, Dir, TOA, TOD, TOAB, TODB, TOAC, TODC, TOAD, TODD, TOAE, TODE, TOAF, TODF, TOAG, TODG, TOAH, TODH):
	Query_for_New_Train = """INSERT INTO train_routes VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s)"""
	mcurs.execute(Query_for_New_Train , (DateofTrain, Dir, TOA, TOD, TOAB, TODB, TOAC, TODC, TOAD, TODD, TOAE, TODE, TOAF, TODF, TOAG, TODG, TOAH, TODH))
	lastID = mcurs.lastrowid
	make_SQL_Car_query(lastID)

def make_SQL_Car_query(trainID):
	SQL_table_names = ['Tokyo','ShinYokohama','Mishima','Shizuoka','Hamatsu','Nagoya','Maibara','Kyoto']
	car_name = ["'A'","'B'","'C'","'D'","'E'","'F'","'G'","'H'"]
	for i in range(8):
		stop = "car_seating_" + SQL_table_names[i]
		Query_for_new_car = "INSERT INTO %s (carID, RouteID, Car_No, Column_number, Row_A, Row_B, Row_C, Row_D, Row_E, Row_F, Row_G, Row_H) VALUES (DEFAULT, %s, %s, %s, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)"
		for k in range(8):
			Car_No = car_name[k]
			for l in range(1,5):
				col = l
				mcurs.execute(Query_for_new_car %(stop, trainID, Car_No, col))
				db.commit()

def random_time():
	Start_time = random.randint(6,13)
	Start_time = Start_time * 100
	return Start_time

def strFromatTime(time):
	zeroing = False
	Start_time = time

	if Start_time < 1000:
		zeroing = True

	Start_time_str = str(Start_time)

	if zeroing == True:
		Start_time_str = "0" + Start_time_str
	return Start_time_str

def random_dir():
	coin = random.randint(1,2)
	if coin == 1:
		dir = 'To Kyoto'
	else:
		dir = 'To Tokyo'
	return dir

def check_train_route_dup(list):
	#check
	train_routes = list
	for k in range(len(train_routes)-1):
		for i in range(k+1, len(train_routes)):
			if train_routes[k][1] == train_routes[i][1] and train_routes[k][3] == train_routes[i][3]:
					return False
	return True

def ensure_proper_time(time_int):
	#IF THE TENS IS ABOVE 59 SO 60 AND ABOVE THEN + 100 TO THE TIME (WITHOUT MINUTES) THEN ADD THE SURPLUS OF MINUTES ABOVE 60
	if (time_int % 100) > 59:
		time_int = (time_int - (time_int % 100) + 100) + ((time_int % 100) % 60)
	return time_int


def draft_test_day(date):
	d = date
	outputList = []
	numberOfTrains = random.randint(5,9)

	for i in range(numberOfTrains):
			date_string = d.strftime('%d/%m/%Y')
			numberOfTrains = random.randint(5,8)	
			time = random_time()
			dir = random_dir()
			formating_list = [date_string, dir ]

			for k in range(8):
				time = ensure_proper_time(time)
				#produce TOD FOR FIRST BUT NOT TOA
				#PRODUCE TOA FOR LAST BUT NOT TOD
				if k == 0:
					#PRODUCE NULL FOR TOA AND THEN TOD
					formating_list.append("NULL")
					outputTime = strFromatTime(time)
					formating_list.append(outputTime)
					
				elif k == 7:
					#ADD TOA THEN A NULL FOR TOD
					outputTime = strFromatTime(time)
					
					formating_list.append(outputTime)
					formating_list.append("NULL")
				else:
					#GIVE TOA THEN TOD WHICH IS +15 MIN
					outputTime = strFromatTime(time)
					formating_list.append(outputTime)
					time = time + 15
					time = ensure_proper_time(time)
					outputTime = strFromatTime(time)
					formating_list.append(outputTime)

				time = time + 100 #EVERY STOP IS 1 HOUR DISTANCE AWAY, 15 MIN DEPT TIME

			outputList.append(formating_list)
	return outputList

def TOD_arrangement(train_route, dir):
	tod_list = train_route
	outputList = [tod_list[0], tod_list[1]]
	if dir == 'To Tokyo': #opposite way
		for i in range(17,1,-2):
			outputList.append(tod_list[i-1])
			outputList.append(tod_list[i])
	else:
		outputList = tod_list
	return outputList


def create_test_day(date):
	today = date
	while(True):
		draft_test_data = draft_test_day(today) #drafts the test data incase of dups
		quality_check = check_train_route_dup(draft_test_data) 
		if quality_check == True:
			break
		print('failed:', date)
	print('passed: ', date)

	for i in range(len(draft_test_data)):
		draft_test_data[i] = TOD_arrangement(draft_test_data[i], draft_test_data[i][1])
		print(draft_test_data[i])
		input_New_Train(draft_test_data[i][0],draft_test_data[i][1], draft_test_data[i][2], draft_test_data[i][3], draft_test_data[i][4], draft_test_data[i][5], draft_test_data[i][6], draft_test_data[i][7], draft_test_data[i][8], draft_test_data[i][9], draft_test_data[i][10], draft_test_data[i][11], draft_test_data[i][12], draft_test_data[i][13], draft_test_data[i][14], draft_test_data[i][15], draft_test_data[i][16], draft_test_data[i][17])

	return draft_test_data

def create_all_test_data_trains():
	today = dt.today()
	overall_test_data_trains = []
	for i in range(20):
		day_data = create_test_day(today)
		for i in range(len(day_data)):
			overall_test_data_trains.append(day_data)

		today = today+datetime.timedelta(days=1)
	return overall_test_data_trains

#CREATE MULTIPLE SEAT BOOKING FOR RANDOM STARTS AND RANDOM END WHERE AVAIL


def create_test_bookings_for_traincars_singleSeatBooking(trainID):
	start_index = random.randint(0,6)
	start = stops[start_index]
	end_index = random.randint(start_index,7)
	end = stops[end_index]
	dir_query = """SELECT Dir FROM train_routes WHERE trainID = %s"""
	dir = mcurs.execute(dir_query, (trainID,))
	mcurs.commit()
	seats = fetch_true_aval_seats(start, end, trainID, dir)
	booking_multiple_stops()


def choose_random_seat():
	pass


#create SQL Query for each train made
stops = ['Tokyo','Shin-Yokohama','Mishima','Shizuoka','Hamatsu','Nagoya','Maibara','Kyoto']
#create_all_test_data_trains()
#creates test data for train routes
#test_data = create_all_test_data_trains()

