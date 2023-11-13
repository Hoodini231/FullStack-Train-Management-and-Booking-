#New project, Train ticket booker#
import math

from tkinter import *
import tkinter.ttk as tkk
from tkmacosx import *
from tkcalendar import Calendar
from tkcalendar import DateEntry
from datetime import datetime
from Query_trains import Train_Route_Querys
from Query_Seats import book_seats
from Email_Class import Email
from Email_Class import Send_Email

#GUI CODE REGION
class App(Tk):
	def __init__(self, *args, **kwargs):
		super().__init__()
		self.geometry("1280x750")
		self.title("Ticketing Alpha")
		
		self.resizable(False, False)
		self.iconbitmap('Images/ticketingIcon.ico')
		#self.borderlessMode()

		self.container = Frame(self)
		self.container.pack()
		self.container.grid_rowconfigure(0, weight = 1)
		self.container.grid_columnconfigure(0, weight = 1)
		self.x_co1 = 0
		self.y_co1 = 0

		self.frames = {}
		self.frames["home"] = homePage(parent = self.container, controller = self)
		self.frames["home"].grid(row = 0, column = 0, sticky = "S")
		self.frames["trainTimeTable"] = trainTimeTable(parent = self.container, controller = self)
		self.frames["trainTimeTable"].grid(row = 0, column = 0, sticky= "s")
		self.frames["bookingPage"] = bookingPage(parent = self.container, controller = self)
		self.frames["bookingPage"].grid(row = 0, column = 0, sticky = "s")
		self.newPage("home")

	def borderlessMode(self):

		self.overrideredirect(True)
		self.exitButtonImage= PhotoImage(file= "Images/exitButt.png")
		self.titleBarImage = PhotoImage(file= "Images/titlebar.png")

		self.Title_Bar = Canvas(self, bg ="green", relief = "raised", bd = 0)
		self.Title_Bar.bind('<B1-Motion>', self.move_app)
		self.Title_Bar.place(x=0,y=0,width=1280, height=30)

		self.TitleBarDisplay = Label(self.Title_Bar, image = self.titleBarImage)
		self.TitleBarDisplay.bind('<Button-1>', self.mouseClicked)
		self.TitleBarDisplay.bind('<B1-Motion>', self.move_app)
		self.TitleBarDisplay.place(x=0,y=0,height=30)
		self.TitleBarDisplay.image = self.titleBarImage

		self.ExitButton = Button(self.Title_Bar, image = self.exitButtonImage, relief = FLAT, command=lambda:self.destroy())
		self.ExitButton.place(x=1250, y = 3, height = 21, width = 24)
		self.ExitButton.image = self.exitButtonImage

	def move_app(self, e):
		self.geometry(f"+{e.x_root-self.x_co1}+{e.y_root-self.y_co1}")

	def mouseClicked(self, e):
		self.x_co1 = e.x
		self.y_co1 = e.y	

	def generateMap(self):
		frame = Toplevel(self)
		frame.resizable(False, False)
		frame.geometry("900x600")
		frame.title("Map of Central Train line in Japan")
		frame.iconbitmap('Images/ticketingIcon.ico')
		mapImage = PhotoImage(file = "Images/map.png")
		mapImageLabel = Label(frame,image = mapImage, highlightthickness=0)
		mapImageLabel.pack()
		mapImageLabel.image = mapImage

	def newPage(self, page_name):
		frame = self.frames[page_name]
		frame.tkraise()
		self.borderlessMode()

class homePage(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller

		self.wallpaper = PhotoImage(file = "Images/wallpaper4.png")
		self.wallpaperLabel = Label(self, image = self.wallpaper)
		self.wallpaperLabel.image = self.wallpaper
		self.wallpaperLabel.pack(side = BOTTOM, expand = True)
		self.wallpaperLabel.image = self.wallpaper
		self.wallpaperLabel.image = self.wallpaper	

		self.buttonMaker(self, "Images/TrainTablePNG.png", lambda:controller.newPage("trainTimeTable"), 200, 271, 298, 40)
		self.buttonMaker(self, "Images/TicketImage.png", lambda:controller.newPage("bookingPage") , 217, 387,  265,45  )
		self.buttonMaker(self, "Images/MapImage.png", lambda:controller.generateMap(), 308, 500, 83, 43)


 
	def buttonMaker(self, frame, filePath, command, x, y, w, h):
		image = PhotoImage(file = filePath)
		butt = Button(frame, image = image, command = command, relief = FLAT)
		butt.place(x = x, y = y, width = w, height = h)
		butt.image = image


class trainTimeTable(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller
		self.bgPlain = PhotoImage(file = "Images/plain1.PNG")
		self.bg_label = Label(self, image = self.bgPlain)
		self.bg_label.pack()
		self.bg_label.image = self.bgPlain
		self.image = PhotoImage(file = "Images/backer.PNG")
		self.bgi = Button(self, image = self.image, relief = FLAT, command = lambda: self.controller.newPage("home"))
		self.bgi.place(x = 10, y = 40, width = 30, height = 30)
		self.bgi.image = self.image
		
		self.d1 = datetime.now()
		self.today = datetime.now().day
		self.current_month = datetime.now().month
		self.current_year = datetime.now().year

		self.calendar = Calendar(
			self, 
			selectmode = 'day', 
			year = self.current_year, 
			month = self.current_month, 
			day = self.today,
			mindate = self.d1, 
			firstweekday = "sunday", 
			showweeknumbers = False, 
			othermonthbackground = "white" , 
			othermonthforeground = "#999999",
			othermonthwebackground = "white", 
			othermonthweforeground = "#999999" ,
			disableddaybackground = "grey",
			disableddayforeground = "#3a3b3c",

			headersbackground = "#a8aaaa", 
			weekendbackground = "#FFFFFF", 
			bordercolor = "light grey", 
			selectbackground = "light blue", 
			selectforeground = "white",
			date_pattern = 'dd/MM/yyyy'
			)
		self.calendar.place(x = 1280*0.15, y = 720*0.125, width = 1280*0.7, height = 720*0.75)

		Button(self, text = "Show Train Routes", relief = FLAT, command = lambda: self.train_info_popup()).place(x = 610, y = 650)

	def defocus(event):
		event.widget.master.focus_set()

	def show_train_routes_on_date(self):
		return self.get_date()

	def get_date(self):
		return self.calendar.get_date()
		

	def train_info_popup(self):
		win = Frame(self, width = 1280, height = 780)
		win.place(x = -5, y = 30)
		im1 = PhotoImage(file = "Images/plain1.PNG")
		self.bglabel2 = Label(win, image = im1, relief = FLAT)
		self.bglabel2.image = im1
		self.bglabel2.place(x = 0, y = -30)
		bar = Label(self.bglabel2, relief = FLAT)
		bar.place(x = 290, y = 80, width = 700, height = 40)
		add_train_button = Button(bar, text = "Add new Train", relief = FLAT, command = lambda: self.add_new_train()).pack()
		back_button = Button(self.bglabel2, text="back", command=lambda: win.place_forget())
		back_button.place(x=30, y=50)
		self.show_trains()

	def add_new_train(self):
		win = Toplevel(self)
		win.geometry("600x500")
		win.title("New Train")
		frame8 = Frame(win, width = 600, height = 500)
		frame8.pack()
		self.direction = StringVar()
		direction_Entry = tkk.Combobox(frame8, textvariable=self.direction)
		direction_Entry['values'] = ["To Tokyo", "To Kyoto"]
		direction_Entry['state'] = 'readonly'
		direction_Entry.bind("<FocusIn>", self.defocus)
		direction_Entry.pack()
		TOD = StringVar()

		Entry(frame8, textvariable=TOD).pack()
		Button(frame8, text = "Enter TOD", command = lambda: self.SQL_newTrain(TOD, direction_Entry.getvar(),self.get_date() )).pack()

	def SQL_newTrain(self, tod, dir, date):
		a = Train_Route_Querys()
		a.add_route(date,dir, tod)
		self.show_trains()


	def show_trains(self):
		trq = Train_Route_Querys()
		date = self.get_date()
		self.routes = trq.Fetch_Query_Train_by_date(date)
		y_level = 115
		self.trainVar = IntVar()
		for i in range(len(self.routes)):
			if self.routes[i][2] == "To Tokyo":
				output_text = f"route ID: {str(self.routes[i][0])} | Direction: {self.routes[i][2]} | TOD {self.routes[i][18]}"
			else:
				output_text = f"route ID: {str(self.routes[i][0])} | Direction: {self.routes[i][2]} | TOD {self.routes[i][4]}"
			rb = Radiobutton(self.bglabel2, text=output_text, var=self.trainVar, indicator=0, background="light blue",value=i, command = lambda: self.specific_train_page(self.trainVar.get(), self.routes))
			rb.place(x=290, y=y_level, width=700, height=40)
			y_level = y_level + 45

	def specific_train_page(self, trainID, routes):
		frame = Frame(self.bglabel2, width = 1280, height = 780, bg = "#9C9EA3")
		frame.pack()
		id = self.trainVar.get()
		image = PhotoImage(file = "Images/BackIcon.png")
		back_button = Button(frame, image = image, relief = FLAT, command = lambda:frame.pack_forget())
		back_button.image = image
		back_button.place(x = 30, y = 65, width = 40, height = 37)
		Button(frame, text = "Change Time of Dept.", relief = FLAT, bg = "#9C9EA3", command=lambda:self.change_TOD_window()).place(x = 130, y = 65)
		Button(frame, text = "Change Date", relief = FLAT, bg = "#9C9EA3", command = lambda:self.date_popup()).place(x = 280, y = 65)
		Label(frame, text = "Route ID", bg = "#6A77B6").place(x = 30, y = 120, width = 70)
		Label(frame, text = self.routes[id][0]).place(x = 30, y = 144, width = 70 )
		Label(frame, text = "  Date  ", bg = "#6A77B6").place(x = 100, y = 120, width = 115)
		Label(frame, text = self.routes[id][1]).place(x = 100, y = 144, width = 115)
		Label(frame, text = "Direction", bg = "#6A77B6").place(x = 215, y = 120, width = 70)
		Label(frame, text = self.routes[id][2]).place(x = 215, y = 144, width = 70)
		time_info_a = Label(frame, text = "TOA Tokyo | TOD Tokyo | TOA ShinYokohama | TOD ShinYokohama | TOA Mishima | TOD Mishima", bg = "#6A77B6").place(x = 30, y = 173, width = 550)
		string1 = "       %s     |     %s       |              %s               |              %s               |          %s         |           %s       "
		Label(frame, text = (string1 %(self.routes[id][3],self.routes[id][4],self.routes[id][5],self.routes[id][6],self.routes[id][7],self.routes[id][8]))).place(x = 30, y = 198, width = 550)
		time_info_b = Label(frame, text = "TOA Shizuoka | TOD Shizuoka | TOA Hamatsu | TOD Hamatsu | TOA Nagoya |  TOD Nagoya  | TOA Maibara | TOD Maibara |  TOA Kyoto |  TOD Kyoto", bg = "#6A77B6").place(x = 30, y = 228, width = 773)
		string2 = "        %s       |         %s         |          %s         |          %s         |         %s       |         %s        |          %s         |          %s       |       %s     |     %s     "
		Label(frame, text = (string2%(self.routes[id][9],self.routes[id][10],self.routes[id][11],self.routes[id][12],self.routes[id][13],self.routes[id][14], self.routes[id][15],self.routes[id][16],self.routes[id][17], self.routes[id][18]))).place(x = 30, y = 253, width = 773)
		Button(frame, text='Delete Train', relief = FLAT, command=lambda:self.delete_train())

	def delete_train(self):
		trq = Train_Route_Querys()
		trq.delete_route(self.routes[self.trainVar.get()][0])
		#refresh the page

	def change_TOD_window(self):
		win3 = Toplevel(self)
		win3.geometry("300x150")
		win3.title("Change Time of Departure")
		frame4 = Frame(win3, width = 300, height = 400, bg = "blue")
		frame4.pack()
		self.new_tod = StringVar()
		tod_entry = Entry(frame4, textvariable=self.new_tod)
		tod_entry.place(x = 75, y= 30, width = 150)
		butt = Button(frame4, text = "Change TOD now", command = lambda: self.change_TOD_func())
		butt.place(x = 100, y = 50, width = 100)

	def change_TOD_func(self):
		new = int(self.new_tod.get())
		if new < 0 or new > 2359:
			error_popup()
		else:
			trainID = self.routes[self.trainVar.get()][0]
			trq = Train_Route_Querys()
			new_timings = trq.create_timings_fromTOD(self.new_tod.get())
			trq.change_timings_train(new_timings, trainID)
			self.specific_train_page(trainID, self.routes)

	def error_popup(self):
		win = Toplevel(self.pop_up_booking)
		win.geometry("100x50")
		win.title("ERROR")
		frame1 = Frame(win, width = 100, height = 50)
		frame1.pack()
		Label(frame1, text = "ERROR: PLEASE ENTER A CORRECT TIME").pack()

	def date_popup(self):
		win4 = Toplevel(self)
		win4.geometry("300x150")
		win4.title("Change Date")
		frame6 = Frame(win4, width = 300, height = 150, bg = "black")
		frame6.pack()
		min_date = datetime.today()
		self.DE = DateEntry(
			frame6,
			selectmode='day',
			year=self.current_year,
			month=self.current_month,
			day=self.today,
			mindate=min_date,
			firstweekday="sunday",
			showweeknumbers=False,
			othermonthbackground="white",
			othermonthforeground="#999999",
			othermonthwebackground="white",
			othermonthweforeground="#999999",
			disableddaybackground="grey",
			disableddayforeground="#3a3b3c",

			headersbackground="#a8aaaa",
			weekendbackground="#FFFFFF",
			bordercolor="light grey",
			selectbackground="light blue",
			selectforeground="white",
			date_pattern='dd/MM/yyyy'
		)
		self.DE.place(x = 30, y = 30)
		butter = Button(frame6, text = "Change Date Now", command = lambda: self.change_date() ).place(x=30, y= 60)

	def change_date(self):
		date = self.DE.get_date()
		print(date)
		date = date.strftime("%d/%m/%Y")
		trq = Train_Route_Querys()
		trq.change_route_date(date, self.routes[self.trainVar.get()][0])
		#self.specific_train_page(self.trainVar.get(), self.routes)


class bookingPage(Frame):
	def __init__(self, parent, controller):
		
		Frame.__init__(self, parent)
		self.stop_list = ['Tokyo','ShinYokohama','Mishima','Shizuoka','Hamatsu','Nagoya','Maibara','Kyoto']
		self.current_avail_other_endstop_list = ['ShinYokohama','Mishima','Shizuoka','Hamatsu','Nagoya','Maibara','Kyoto']
		self.current_avail_other_startstop_list = ['Tokyo','ShinYokohama','Mishima','Shizuoka','Hamatsu','Nagoya','Maibara','Kyoto']
		self.controller = controller
		self.bgPlain = PhotoImage(file = "Images/plain1.PNG")
		self.bg_label = Label(self, image = self.bgPlain)
		self.bg_label.pack()
		self.image = PhotoImage(file = "Images/backer.PNG")
		self.bgi = Button(self, image = self.image, relief = FLAT, command = lambda: self.controller.newPage("home"))
		self.bgi.place(x = 10, y = 40, width = 30, height = 30)

#search bar
#display port
		self.bar = Label(self, relief = FLAT)
		self.bar.place(x = 250, y = 130, width = 700, height = 30)
		self.start_var = StringVar()
		self.start_var.set("Tokyo")
		self.end_var = StringVar()
		self.end_var.set("Kyoto")
		self.populate_bar()
		self.display_label = Label(self.bg_label, relief = FLAT )
		self.display_label.place(x = 248, y = 160, width = 700, height = 500)
		self.trainVar = IntVar()



		#self.starting_stop = OptionMenu(self, self.start_var, *self.stop_list)
		#self.starting_stop.place(x = 600, y = 130)
	def create_current_avail_other_endstop_list(self, starting_stop):
		self.current_avail_other_endstop_list = self.stop_list.copy()
		self.current_avail_other_endstop_list.remove(starting_stop)
		self.populate_bar()

	def create_current_avail_other_startstop_list(self, ending_stop):
		self.current_avail_other_startstop_list = self.stop_list.copy()
		self.current_avail_other_startstop_list.remove(ending_stop)
		self.populate_bar()


	def onClick_displayRoutes(self, event):
		self.display_routes()

	def populate_bar(self):
		self.bar_date()
		self.bar_stop_choices()
		self.enter_button = Button(self.bar, text = "Show Available Trains", command = lambda: self.display_routes())
		self.enter_button.place( x = 550, y = 0)


	def bar_date(self):
		self.date_label = Label(self.bar, text = "Date:", relief = FLAT)
		self.date_label.place(x = 40, y = 0)

		self.d1 = datetime.now()
		self.min_date = datetime(2023, 2, 17)
		self.today = datetime.now().day
		self.current_month = datetime.now().month
		self.current_year = datetime.now().year
		self.a = DateEntry(
		self.bar, 
		selectmode = 'day', 
		year = self.current_year, 
		month = self.current_month, 
		day = self.today,
		mindate = self.min_date, 
		firstweekday = "sunday", 
		showweeknumbers = False, 
		othermonthbackground = "white" , 
		othermonthforeground = "#999999",
		othermonthwebackground = "white", 
		othermonthweforeground = "#999999" ,
		disableddaybackground = "grey",
		disableddayforeground = "#3a3b3c",

		headersbackground = "#a8aaaa", 
		weekendbackground = "#FFFFFF", 
		bordercolor = "light grey", 
		selectbackground = "light blue", 
		selectforeground = "white",
		date_pattern = 'dd/MM/yyyy'

		)

		self.a.place(x = 80, y =0)
		self.a.bind('<FocusIn>', self.defocus)
	
	def bar_stop_choices(self):
		


		self.start_label = Label(self.bar, text = "From")
		self.start_label.place(x = 200, y = 0)
		self.end_label = Label(self.bar, text = "To")
		self.end_label.place(x = 355, y = 0)

		self.starting_stop = tkk.Combobox(self.bar, textvariable = self.start_var)
		self.starting_stop['values'] = self.current_avail_other_startstop_list
		self.starting_stop['state'] = 'readonly'
		self.starting_stop.bind("<FocusIn>", self.defocus)
		self.starting_stop.bind("<<ComboboxSelected>>", self.onClick_displayRoutes)
		self.starting_stop.place(x = 240, y = 0, width = 105)

		self.ending_stop = tkk.Combobox(self.bar, textvariable = self.end_var)
		self.ending_stop['values'] = self.current_avail_other_endstop_list
		self.ending_stop.bind("<FocusIn>", self.defocus)
		self.ending_stop.bind("<<ComboboxSelected>>", self.onClick_displayRoutes)
		self.ending_stop.place(x = 385, y = 0, width = 105)

	def get_start(self):
		return self.start_var.get()
	def get_end(self):
		return self.end_var.get()
	def selected_date(self):
		date = self.a.get_date()
		return date.strftime("%d/%m/%Y")
		
	def find_dir(self):
		start_index = 0
		start = self.get_start()
		end = self.get_end()
		for i in range(8):
			if self.stop_list[i] == start:
				start_index = i
		for k in range(start_index+1, 8):
			if self.stop_list[k] == end:
				return "To Kyoto"
		return "To Tokyo"

	def defocus(self, event):
		event.widget.master.focus_set()


	def get_routes(self):
		dir = self.find_dir()
		date = self.selected_date()
		trq = Train_Route_Querys()
		current_routes = trq.Fetch_Query_Train(date, dir)
		return current_routes

	def find_index_in_stops(self, stop_name):
		for i in range(8):
			if stop_name == self.stop_list[i]:
				return i
		return 0

	def display_routes(self):
		
		routes = self.get_routes()
		start = self.get_start()
		self.create_current_avail_other_endstop_list(start)
		end = self.get_end()
		self.create_current_avail_other_startstop_list(end)
		start_index = self.find_index_in_stops(start)
		end_index = self.find_index_in_stops(end)
		self.current_seat_button_list = []
		#You want to grab the start TOD and the END TOA TAKE INDEX + 1 TIMES 2 + 1 = TOA THEN + 1 again for TOD
		display_text_list = []
		y_level = 0
		for i in range(len(routes)):
			
			output_text = "ID: " + str(routes[i][0]) + "	|	TOD FROM " + start + " " + routes[i][((start_index+1)*2+2)] + "	|	TOA AT " + end + " " + routes[i][((end_index+1)*2)+1]
			rb = Radiobutton(self.display_label, text = output_text, var = self.trainVar, command = lambda: self.seat_popup_win(), indicator = 0, background = "light blue", value = routes[i][0])
			rb.place(x = 0, y = y_level, width = 700, height = 50 )

			y_level = y_level + 50


	def get_TOD_TOA_for_email(self): #FUNCTION TO TAKE THE TOD AND TOA FOR SENDING IN EMAIL
		routes = self.get_routes()
		routeID = self.trainVar.get()
		start = self.get_start()
		end = self.get_end()
		start_index = self.find_index_in_stops(start)
		end_index = self.find_index_in_stops(end)
		index = 0
		for i in range(len(routes)):
			if routes[i][0] == routeID:
				index = i 
		output = [routes[index][((start_index+1)*2+2)], routes[index][((end_index+1)*2)+1]]
		return output

	# FUNCTINO FOR THE ENTIRE POPUP WINDOW FOR SEAT SELECTION
	def seat_popup_win(self):
		routes = self.get_routes()
		routeID = self.trainVar.get()
		start = self.get_start()
		end = self.get_end()
		dir = self.find_dir()
		self.popup_cars = Toplevel(self)
		self.popup_cars.geometry("1200x700")
		self.popup_cars.resizable(False, False)
		title_str = "Seat listing from %s to %s on route ID:  %s " %(start, end, str(routeID))
		self.popup_cars.title(title_str)
		self.car_var = StringVar()
		self.car_var.set("A")
		self.button_tracker = 1
		self.populate_popup()


	def populate_popup(self):
		#populates the popup window adding all widgets
		self.booking_list = []
		routeID = self.trainVar.get()
		start = self.get_start()
		end = self.get_end()
		dir = self.find_dir()
		
		self.car_bg = PhotoImage(file = "Images/plain1.PNG")
		self.car_bg_label = Label(self.popup_cars, image = self.bgPlain)
		self.car_bg_label.pack()

		self.bar_popup = Label(self.car_bg_label, relief = FLAT)
		self.bar_popup.place(x = 100, y = 50, width = 1000, height = 40)
		self.show_cars = Button(self.bar_popup, relief = FLAT, text = "Show Seats", command = lambda: self.format_seat_buttons())
		self.show_cars.place(x = 20, y = 0)

		self.car_label = Label(self.bar_popup, relief= FLAT, text = "Choose Car: ")
		self.car_label.place(x = 170, y = 0)

		self.choose_car = tkk.Combobox(self.bar_popup, textvariable = self.car_var)
		self.choose_car['values'] =  ["A", "B", "C", "D", "E", "F", "G", "H"]
		self.choose_car['state'] = "readonly"
		self.choose_car.bind("<FocusIn>", self.defocus)
		self.choose_car.bind("<<ComboboxSelected>>", self.onClick_showSeats)
		self.choose_car.place(x = 250, y = 0, width = 50)

		self.display_seat_label = Label(self.car_bg_label, relief = FLAT, background = "#3B3B3B").place(x = 100, y = 100, width = 1000, height = 500)
		self.Seat_button_container = []
		self.Seat_button_information = []
		button_flagger = 0

		selected_seats_text = Button(self.bar_popup, relief = FLAT, text = "Book now", command = lambda: self.confirm_bookings_popup())
		selected_seats_text.place(x = 600, y = 0)

		self.car_rows = ["ROW A", "ROW B", "ROW C", "ROW D", "ROW E", "ROW F", "ROW G", "ROW H"]
		col = ["1", "2", "3", "4"]
		y_level = 150
		photoImage = PhotoImage(file="Images/SeatImage.PNG")

		for i in range(5):
			if i == 0:
				y_level = y_level - 100
			else:
				Label(self.car_bg_label, background = "#3B3B3B", relief = FLAT, font = ("Helvetica", "14"), text = col[i-1]).place(x = 150, y = y_level)

			x_level = 200
			for k in range(8):
				if i == 0:
					Label(self.car_bg_label, background ="#3B3B3B", relief = FLAT, text = self.car_rows[k]).place(x = x_level, y = 100)
					
				else:
					temp_button = Button(self.car_bg_label,  image = photoImage, relief = FLAT, command = lambda j=button_flagger:self.button_clicked(j))
					temp_button.image = photoImage
					temp_button.place(x = x_level, y = y_level, width = 45, height = 45)
					self.Seat_button_container.append(temp_button)
					button_flagger += 1                  #add in the counter, carID, rowName
				x_level = x_level + 100
			y_level = y_level + 100
		self.format_seat_buttons()

	def onClick_showSeats(self, event):
		self.format_seat_buttons()

	def format_seat_buttons(self):
		#when formatting, i create an information list using the index to locate the specific button, this stores the carID, the ROW string and the seat name output string
		self.Seat_button_information = []
		current_route = self.get_current_car_seats()
		output = []
		purchase_completed = False #Flag to change the image from selected to taken after order
		for x in range(4): #for every car
			current_col = current_route[x]

			for i in range(8): #for every seat
				output = []
				#IF THE SEAT IS TAKEN 
				if current_col[i+4] != None:
					purchase_completed = True
					output.append(-1)

					#flagged
				else:
					#give the 'clicked' a 0
					output.append(0)

				output.append(current_col[0])
				row_str = self.car_rows[i]
				output.append(row_str)
				
				car_name = self.car_var.get()
				col_id = x+1
				output_str = f"{row_str[4:5]}{col_id} in car {car_name}"
				output.append(output_str)
				self.Seat_button_information.append(output)
				#adds everything back into the info 32 times
		#IF THE PAGE IS RECALLED SO IF I BOOK ON CAR A THEN GO CAR C AND BOOK THEN GO BACK TO CAR A
		#I WANT TO CHECK IF I HAVE ALR SELECTED SEATS THUS FOR 32 TIMES WE ITERATE TO SEE ANY MATCHES IN THE BOOKING LIST
		for i in range(32):
			button = self.Seat_button_container[i]
			info = self.Seat_button_information[i]
			is_selected = self.check_if_alr_selected(info[1], info[2], i )

			if is_selected == False:
				self.config_image(button, i)
				if info[0] == -1:
					pass
					#button.config(state = DISABLED)
				#per normal
			else:
				#THEN CHANGE IMAGE TO SHOWN SELECTED
				image = PhotoImage(file = "Images/Seat_selected.PNG")
				button.config(image = image)
				button.image = image
				self.Seat_button_information[i][0] += 2
				print("CHANGED", self.Seat_button_information[i][0] )



	def check_if_alr_selected(self, carID, row, index):
		#To do this we just need to check the CARID AND ROW in booking list to the button generated
		length = len(self.booking_list)
		for i in range(length):
			if self.booking_list[i][0] == self.Seat_button_information[index][1] and self.booking_list[i][1] == self.Seat_button_information[index][2]:
				return True
		return False

	def get_current_car_seats(self):
		#GETS THE CURRENT CAR SEATS AND RETURNS THE CURRENT SEATING PLAN FOR THE CHOSEN CAR
		seats = book_seats()
		routeID = self.trainVar.get()
		start = self.get_start()
		end = self.get_end()
		dir = self.find_dir()
		car_name = self.car_var.get()
		self.current_route  = seats.fetch_true_aval_seats(start, end, routeID, dir)
		dict = {
			"A" : self.current_route[0:4],
			"B" : self.current_route[4:8],
			"C" : self.current_route[8:12],
			"D" : self.current_route[12:16],
			"E" : self.current_route[16:20],
			"F" : self.current_route[20:24],
			"G" : self.current_route[24:28],
			"H" : self.current_route[28:32]
		}
		routes = dict.get(car_name)
		return routes

	def is_select_or_unselect_seat(self, button_click_counter, index):
		#FUNCTION TO BASICALLY CHANGE THE IMAGE OF THE SEAT TO SHOW ITS STATE
		if button_click_counter == -1:
			return "Images/Seat_taken.PNG"

		i = button_click_counter % 2

		if button_click_counter == 0:
			self.Seat_button_information[index][0] +=1
			return "Images/SeatImage.PNG"

		elif i == 0:
			self.booking_list.append((self.Seat_button_information[index][1],self.Seat_button_information[index][2], self.Seat_button_information[index][3]))
			return "Images/Seat_selected.PNG"

		else:
			booker_list = list(self.booking_list)
			length = len(self.booking_list)
			for i in range(length):
				if self.booking_list[i][0] == self.Seat_button_information[index][1] and self.booking_list[i][1] == self.Seat_button_information[index][2]:
					self.booking_list.pop(i)
					break
			return "Images/SeatImage.PNG"

	def config_image(self, button, index):
		#FUNCTION ACTS TO CONFIG THE IMAGE OF A BUTTON 
		button_clicker_tracker = self.Seat_button_information[index][0]
		image = self.is_select_or_unselect_seat(button_clicker_tracker, index)
		photo_image = PhotoImage(file = image)
		button.toggleState = 1
		button.config(image = photo_image)
		button.image = photo_image

	def button_clicked(self, index):
		#FUCNTION WHICH ACTS ON THE BUTTON CLICKED
		l = len(self.Seat_button_container)
		print("index: ", index)
		button = self.Seat_button_container[index]
		if self.Seat_button_information[index][0] != -1:
			self.Seat_button_information[index][0] += 1
		self.config_image(button, index)
		print(self.booking_list)
		self.show_selected_seats()

	def show_selected_seats(self):
		text = ""
		for i in range(len(self.booking_list)):
			text += self.booking_list[i][2] + ", "
		return text

	#NEW POP UP WINDOW FOR CART, PRICING, TICKET INFO AND OUTPUT EMAIL
	def confirm_bookings_popup(self):
		self.pop_up_booking = Toplevel(self)
		self.pop_up_booking.geometry("500x600")
		self.pop_up_booking.title("Booking")
		self.pop_up_booking.resizable(False, False)
		bg_im = PhotoImage(file = "Images/plain1.PNG")
		bg = Label(self.pop_up_booking, image = bg_im)
		bg.image = bg_im
		bg.pack()

		#for every index, put a \n and the price, price can be calculated via number of stops
		output_seat_text = self.show_selected_seats()
		self.seats_selected_string = self.format_selected_seats_to_string(output_seat_text)

		Seat_Price_frame = Frame(self.pop_up_booking, bg ="grey", width = 200, height = 300)
		Seat_Price_frame.place(x = 50, y = 50)
		v=Scrollbar(Seat_Price_frame)
		v.pack(side = LEFT, fill = 'y')
		
		text = Text(Seat_Price_frame, font = ("Helvetica, 12"), yscrollcommand = v.set)
		text.insert(END, self.seats_selected_string)
		v.config(command=text.yview)
		text.config(state = DISABLED)
		text.pack()

		Ticket_information_and_email_frame = Frame(self.pop_up_booking, bg = "grey", width = 250, height = 436)
		Ticket_information_and_email_frame.place(x = 275, y = 50)

		l = Label(Ticket_information_and_email_frame, bg = "grey")
		l.place(x=0,y=0, width = 250, height = 500)
		total_cost = self.number_formatting()
		total_cost_label = Label(l, text = f"Total Cost: ¥{total_cost}", font = "Helvetica, 15", bg = "grey",relief = FLAT)
		total_cost_label.place(x = 10, y = 20 )
		stops_label = Label(l, text = f"Going from {self.get_start()} to {self.get_end()}", font = "Helvetica 7 italic", bg = "grey").place(x=10, y=72)
		quantity_label = Label(l, text = f"{len(self.booking_list)} seat(s) choosen", font = "Helvetica 11 italic", bg = "grey").place(x = 10, y = 50)
		date_label = Label(l, text = f"Date: {self.selected_date()}", bg = "grey").place(x=10, y = 110)
		timings = self.get_TOD_TOA_for_email()

		TOD_label = Label(l, text = f"Time of Depterature ({self.get_start()}): {timings[0]}", bg = "grey").place(x = 10, y = 130)
		TOA_label = Label(l, text = f"Time of Arrival ({self.get_end()}): {timings[1]}", bg = "grey").place(x = 10, y = 155)

		email_label = Label(l ,text = "Customer Email:", bg = "grey").place(x = 10, y = 190)
		self.customer_email_var = StringVar()
		email_entry = Entry(l, textvariable = self.customer_email_var)
		email_entry.place(x = 10, y = 220, width = 185)

		Order_button = Button(l, text = "ORDER NOW", command = lambda: self.order_clicked())
		Order_button.place(x = 60, y = 350)
		#display_text = Label(frame1, text = o).place(x = 200, y = 100, width = 200, height = 200)

	def format_selected_seats_to_string(self, text):
		str_list = text.split(", ")
		o_str = ""
		self.seats_noprice_str = ""
		self.price = self.make_price()
		for i in range(len(str_list)-1):
			o_str += f"  {i+1}: {str_list[i]}    |    ¥{self.price} \n"
			self.seats_noprice_str += "\n"+str_list[i]
		return o_str

	def number_formatting(self):
		total_cost = len(self.booking_list) * self.price
		o = f'{total_cost:,}'
		return o

	def find_number_of_stops(self):
		start = self.get_start()
		end = self.get_end()
		stops = ['Kyoto', 'Maibara', 'Nagoya','Hamatsu','Shizuoka','Mishima','ShinYokohama','Tokyo']
		index = [0,0]
		filler = [start, end]
		for k in range(2):
			for i in range(8):
				if filler[k] == stops[i]:
					index[k] = i
		output = abs(index[0]-index[1])
		return output

	def make_price(self):
		stops = self.find_number_of_stops()
		x = pow(stops, 15)
		self.price = (2*(math.log(x)))+20
		self.price = round(self.price*100)
		return self.price

	def order_clicked(self):
		text = "Thank you for purchasing tickets for %s to %s on %s.\nYour assigned seats are: %s" % (self.get_start(),self.get_end(),self.selected_date(), self.seats_noprice_str)
		email = Email(self.customer_email_var.get())
		email_QC_syntax = email.check_valid_syntax()
		email_domain_QC = email.check_valid_address()
		if email_domain_QC == False or email_QC_syntax == False:
			self.error_popup()
		else:
			subject_name = "Tickets Purchased for %s" %(self.selected_date())
			send_req = Send_Email(self.customer_email_var.get(), subject_name, text)
			self.update_SQL()
			self.finish_frame()

		#update_SQL()
	def error_popup(self):
		win = Toplevel(self.pop_up_booking)
		win.geometry("100x50")
		win.title("ERROR")
		frame1 = Frame(win, width = 100, height = 50)
		frame1.pack()
		Label(frame1, text = "ERROR: Email is invalid").pack()

	def update_SQL(self):
		quantity = len(self.booking_list)
		thing = book_seats()
		seats = book_seats()
		routeID = self.trainVar.get()
		start = self.get_start()
		end = self.get_end()
		dir = self.find_dir()
		thing.booking_multiple_seats(quantity, self.booking_list, dir, start, end)
		seats = book_seats()
		print(seats.fetch_true_aval_seats(start, end, routeID, dir))
		self.booking_list = []
		self.format_seat_buttons()



	def finish_frame(self):
		end_display_frame = Frame(self.pop_up_booking, width = 500, height = 600)
		text = Text(end_display_frame, font=("Helvetica, 24"))
		text.insert(END, "ORDER COMPLETED")
		text.config(state=DISABLED)
		text.pack()
		end_display_frame.place(x=0, y=0)






		














		


'''

	def direction(self):
		return self.dir_selection()

	def show_Available_trains(self):
		date = self.selected_date()
		dir = 
		current_trains_routes = Query_trains.Fetch_Query_Train()
		pass
		#runs a SQL script to grab the specified train routes and shows it


	#runs an sql script to input the new data

def showTimeTable():
	ttCanvas = Canvas(root)
	ttCanvas.place(x=0,y=0,relx=1,rely=1)
	
class HomePage(Frame):
	pass

class trainTimeTable_dates(tk.Frame):
	pass
	#popup for the train timetable per date

class mapPage(tk.Frame):
	pass

class bookingPage_search():
	pass
	#pop up for the trains

class hover_button(Button):
	def __init__(self, master, **kw):
		Button.__init__(self, master=master,**kw)
		self.defaultBackground = self["foreground"]
		self.bind("<Enter>", self.on_enter)
		self.bind("<Leave>", self.on_leave)

	def on_enter(self,e):
		self['foreground'] = self['activeforeground'] 

	def on_leave(self, e):
		self['foreground'] = self.defaultBackground

'''
app = App()




app.mainloop()
