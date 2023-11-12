import mysql.connector
from Query_dict import booking_seat_dictionary
from Query_trains import Train_Route_Querys
import time
from mysql.connector import RefreshOption

db = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="T@stigers231",
	database = "train_db"
	)
mcurs = db.cursor(buffered = True)

class book_seats():
	def __init__(self):
		pass

	def find_startID(self, stop):
		stops = ['Tokyo','ShinYokohama','Mishima','Shizuoka','Hamatsu','Nagoya','Maibara','Kyoto']
		start_index = 0
		for i in range(8):
			if stops[i] == stop:
				start_index = i 
		return start_index

	def Update_Booking_OneSeat(self, tableName, end, row, carID):
		booking_query = booking_seat_dictionary.return_correct_query(tableName, row)
		mcurs.execute(booking_query, (end, carID))

		db.commit()

	def booking_multiple_stops(self, start, end, dir, carID, row):
		start_index = self.find_startID(start)
		#MAIN IF ELSE STATEMENT
		#IF GOING FROM 0->7
		stops = ['Tokyo','ShinYokohama','Mishima','Shizuoka','Hamatsu','Nagoya','Maibara','Kyoto']
		if dir == "To Kyoto":
			for i in range(start_index+1,8):
				self.Update_Booking_OneSeat(stops[i], end, row, carID) #calls on function
				if stops[i] == end:
					break
		#ELSE GOING 7-> 0
		else:
			end_index = 0
			for i in range(8):
				if stops[i] == end:
					end_index = i

			endingPoint_flag = False #FLAG SO WE KNOW WHEN TO START UPDATING

			#Going through the list of stops, identify the end point, once identified make bookings backwards from end to start
			for i in range(8):
				if stops[i] == end:
					endingPoint_flag = True 

				if endingPoint_flag == True:
					self.Update_Booking_OneSeat(stops[i], end, row, carID) #calls on function
					if stops[i] == start:
						break

	#we use a id and row 2d array as we can have 3 seats all in carID = 1 but in row A B and C
	def booking_multiple_seats(self, quantity, carID_row_list, dir, start, end):
		for i in range(quantity):
			self.booking_multiple_stops(start, end, dir, carID_row_list[i][0], carID_row_list[i][1])

	def fetch_true_aval_seats(self, start, end, trainID, dir):
		start_index = self.find_startID(start)
		if dir == "To_Tokyo":
			stops = ['Kyoto', 'Maibara', 'Nagoya','Hamatsu','Shizuoka','Mishima','ShinYokohama','Tokyo']
		else:
			stops = ['Tokyo','ShinYokohama','Mishima','Shizuoka','Hamatsu','Nagoya','Maibara','Kyoto']
		stop = stops[start_index+1]
		trq = Train_Route_Querys()
		display_seats_tuple = trq.Fetch_Cars(end, trainID)
		display_seats = []
		for item in display_seats_tuple:
			x = list(item)
			display_seats.append(x)

		for x in range(start_index+2,8):
			stop = trq.Fetch_Cars(stops[x], trainID)
			stop = list(stop)
			for i in range(32):
				for k in range(4,12):
					if stop[i][k] != None:
						display_seats[i][k] = stop[i][k]
			if stop[x] == end:
				break

		return display_seats









#FUNCTIONS FOR BOOKING SINGLE SEAT FOR DICT BECAUSE HAVE TO HARD CODE THE FREAKING NAME OF THE TABL







#FIRST FUNCTIONS SHOWS AVAL SEATS FOR THE ENTIRE TRIP

#SECOND MORE ADV METHOD IS SEARCHING FOR PARTIAL SEATS to connect the trip tgt IE CAR A ROW A COL 1 FOR FIRST 3 THEN CAR B ROW C COL 4 for second half



'''
q1 ="""SELECT * FROM car_seating_Kyoto WHERE routeID = 1"""
mcurs.execute(q1)
print(q1)
print(mcurs.fetchall())
a = book_seats()
query = a.Update_Booking_OneSeat("Kyoto", """'Kyoto'""", "ROW C", 3)
print(query)
mcurs.execute(query)
db.commit()
mcurs.execute(q1)
print(mcurs.fetchall())
print("done")
'''
#new_query = """UPDATE car_seating_Kyoto SET ROW_G = 'Kyoto' WHERE carID = 1"""



#d = Update_Booking_OneSeat("Nagoya", "Kyoto", "ROW_A", 1)

#E = booking_multiple_stops("Nagoya", "Kyoto", "To Kyoto", 1, "ROW_A")

#f = booking_multiple_seats(3, [(1,"ROW_B"),(2,"ROW_B"),(1,"ROW_C"),(2,"ROW_C")], "To Kyoto", "Shizuoka","Nagoya")
