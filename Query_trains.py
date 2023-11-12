import mysql.connector
from Insert_Script import ensure_proper_time
from Insert_Script import strFromatTime
db = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="passwd",
	database = "train_db"
	)

mcurs = db.cursor(buffered = True)


class Train_Route_Querys():
	def __init__(self):
		pass



	def Fetch_Query_Train_by_date(self, date):

		fetch_query_t = """SELECT * FROM train_routes WHERE Date = %s"""
		output = mcurs.execute(fetch_query_t,(date,))
		output = mcurs.fetchall()

		return output

	def Fetch_Query_Train(self, date, dir):
		if dir == "To Tokyo":
			fetch_query = """SELECT * FROM train_routes WHERE Date = %s and Dir = %s ORDER BY TOD_KYOTO"""
		else:
			fetch_query = """SELECT * FROM train_routes WHERE Date = %s and Dir = %s ORDER BY TOD_KYOTO"""
		output = mcurs.execute(fetch_query,(date,dir))
		output = mcurs.fetchall()
		return output

	def Fetch_Cars(self, end, trainID):
		fetch_query = "SELECT * FROM %s WHERE routeID = %s"
		table_name = "car_seating_" + end
		print(fetch_query%(table_name, trainID))
		mycursor = mcurs.execute(fetch_query % (table_name, trainID))
		output = mcurs.fetchall()
		db.commit()
		return output

	def change_route_date(self, date, routeid):
		date = f"'{date}'"
		query = """UPDATE train_routes SET Date = %s WHERE routeID = %s""" %(date, routeid)
		print(query)
		mcurs.execute(query)
		db.commit()

	def add_route(self, date, dir, tod):
		list_of_times = self.create_timing_fromTOD(tod)
		add_query = f"""INSERT INTO train_routes VALUES ({date, dir, list_of_times})"""
		mcurs.execute(add_query)
		db.commit()

	def delete_route(self, routeID):
		query = "DELETE FROM train_routes WHERE routeID = %s"
		mcurs.execute(query,(routeID,))
		db.commit()

	def create_timings_fromTOD(self, tod):
		timing_list = []
		int_time = int(tod)
		timing_list.append("NULL")
		timing_list.append(tod)
		for i in range(7):
			int_time += 100
			int_time = ensure_proper_time(int_time)
			output_time = strFromatTime(int_time)
			timing_list.append(output_time)
			if i != 6:
				int_time += 15
				int_time = ensure_proper_time(int_time)
				output_time = strFromatTime(int_time)
				timing_list.append(output_time)
			else:
				timing_list.append("NULL")
		return timing_list

	def change_timings_train(self, todlist, id):
		col_names = ["TOA_Tokyo","TOD_Tokyo","TOA_ShinYokohama", "TOD_ShinYokohama","TOA_Mishima","TOD_Mishima","TOA_Shizuoka","TOD_Shizuoka","TOA_Hamatsu","TOD_Hamatsu","TOA_Nagoya"," TOD_Nagoya ","TOA_Maibara","TOD_Maibara"," TOA_Kyoto"," TOD_Kyoto"]
		print(todlist)
		print(len(todlist))
		for i in range(16):
			time = f"'{todlist[i]}'"
			query = "UPDATE train_routes SET %s = %s WHERE routeID = %s" % (col_names[i], time, id)
			print(query)


			mcurs.execute(query)
			db.commit()


