

import mysql.connector


db = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="passwd",
	database = "train_db"
	)


mcurs = db.cursor(buffered = True)

class SQL_tables():
	def __init__(self):
		self.table_names = ['train_routes','car_seating_Tokyo','car_seating_ShinYokohama','car_seating_Mishima','car_seating_Shizuoka','car_seating_Hamatsu','car_seating_Nagoya','car_seating_Maibara','car_seating_Kyoto']


	def create_tables(self):
		train_routes_creation = "CREATE TABLE train_routes (routeID int PRIMARY KEY AUTO_INCREMENT, Date VARCHAR(45) NOT NULL, Dir VARCHAR(45) NOT NULL, TOA_Tokyo VARCHAR(45), TOD_Tokyo VARCHAR(45), TOA_ShinYokohama VARCHAR(45), TOD_ShinYokohama VARCHAR(45), TOA_Mishima VARCHAR(45), TOD_Mishima VARCHAR(45), TOA_Shizuoka VARCHAR(45), TOD_Shizuoka VARCHAR(45), TOA_Hamatsu VARCHAR(45), TOD_Hamatsu VARCHAR(45), TOA_Nagoya VARCHAR(45), TOD_Nagoya VARCHAR(45), TOA_Maibara VARCHAR(45), TOD_Maibara VARCHAR(45), TOA_Kyoto VARCHAR(45), TOD_Kyoto VARCHAR(45))"  
		mcurs.execute(train_routes_creation)
		db.commit()
		columns_car_tables = ['RouteID', 'Car_No', 'Column_number', 'Row_A', 'Row_B', 'Row_C', 'Row_D', 'Row_E', 'Row_F', 'Row_G', 'Row_H']
		stops = ['Tokyo','ShinYokohama','Mishima','Shizuoka','Hamatsu','Nagoya','Maibara','Kyoto']
		for k in range(8):
			tablename = 'car_seating_'+stops[k]		
			create_query = "CREATE TABLE %s (carID int PRIMARY KEY AUTO_INCREMENT, RouteID int NOT NULL, FOREIGN KEY(RouteID) REFERENCES train_routes(routeID) , Car_No VARCHAR(45), Column_number int, Row_A VARCHAR(45), Row_B VARCHAR(45), Row_C VARCHAR(45), Row_D VARCHAR(45), Row_E VARCHAR(45), Row_F VARCHAR(45), Row_G VARCHAR(45), Row_H VARCHAR(45))"
			mcurs.execute(create_query %(tablename,))
			db.commit()

	def empty_tables(self):
		query = "DELETE FROM %s"
		reset_query = "ALTER TABLE %s AUTO_INCREMENT = 0"

		for i in range(8,-1,-1):
			query2 = query % (self.table_names[i])
			r_query = reset_query % (self.table_names[i])
			mcurs.execute(query2)
			mcurs.execute(r_query)

			db.commit()


test = SQL_tables()

test.empty_tables()


