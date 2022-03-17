from tkinter import *
from tkcalendar import Calendar
import sqlite3
from datetime import datetime, timedelta
import time
# Create background
eventCreation = Tk()
#icon = PhotoImage(file="quill.ico")
#eventCreation.iconphoto(False, icon)
eventCreation.title("Calendar")

# Functions to show and hide the date picker
cal = Calendar(eventCreation, selectmode='day', borderwidth=3)
cal.grid(column=0, row=1, columnspan=2, rowspan=1)


def show_cal():
    cal.grid(column=0, row=1, columnspan=2, rowspan=1)


def hide_cal():
    cal.grid_forget()


Button(eventCreation, text='Show Calendar', padx=20, command=show_cal).grid(column=0, row=0)
Button(eventCreation, text='Hide Calendar', padx=21, command=hide_cal).grid(column=1, row=0)

# Event Creation
owner = None
startTime = None
endTime = None
startDate = None  # string
endDate = None  # string
eventName = None  # string
description = None  # string
eventData = None  # string



def start_date():
    global startDate
    startDate = cal.get_date()  # returns in m/d/y format
    return None


def end_date():
    global endDate
    endDate = cal.get_date()  # returns in m/d/y format
    return None


def clear():
    global startDate, endDate
    startDate = None
    endDate = None
    event_name.delete(0, END)
    event_description.delete(1.0, END)
    owner_name.delete(0,END)
    start_time.delete(0, END)
    end_time.delete(0, END)
    return None

# function to show events (Query)
def query():
    conn = sqlite3.connect('calendar_events.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM EVENTS")
    events = c.fetchall()
    
    print(events) #Test to see if it prints from data

    #Loop through events to view on GUI
    show_event = ''
    for event in events:
        show_event += "[" + str(event[0]) + "] " + str(event[1]) + ": " + str(event[2] + "-" + str(event[3]) + " " + str(event[4])) + "\t" + str(event[7]) + "\n"
    event_label = Label(eventCreation, text=show_event)
    event_label.grid(column=2, row=1)
    conn.commit()
    conn.close()
    return

# Function to show available times

def get_available_times(duration=timedelta(hours=1)):
    conn = sqlite3.connect('calendar_events.db') #connect to database
    c = conn.cursor()
    c.execute("SELECT *, oid FROM EVENTS")
    appointments = c.fetchall()

    booked = []
    all_events = []

    #Grabs specific data needed for datetime format (Year, Month, Day, Time)
    for appointment in appointments:
        booked += [(appointment[4].split('/')[2], appointment[4].split('/')[0], appointment[4].split('/')[1], appointment[2].split(':')[0], appointment[4].split('/')[2], appointment[4].split('/')[0], appointment[4].split('/')[1], appointment[3].split(':')[0])]
    #Creates datetime tuple 
    for i in booked:
        all_events.append(tuple((datetime(int(i[0]),int(i[1]),int(i[2]),int(i[3])), datetime(int(i[4]),int(i[5]),int(i[6]),int(i[7])))))


    #The time range to find availabe slots
    hours = (datetime(int(appointment[4].split('/')[2]), int(appointment[4].split('/')[0]), int(appointment[4].split('/')[1]), 9), (datetime(int(appointment[4].split('/')[2]), int(appointment[4].split('/')[0]), int(appointment[4].split('/')[1]), 18)))

    #Sorts all events and displays the timeslots available 
    slots = sorted([(hours[0], hours[0])] + all_events + [(hours[1], hours[1])])
    show_available_slots=''
    available_label = Label(eventCreation, text = show_available_slots)
    for start, end in ((slots[i][1], slots[i+1][0]) for i in range(len(slots)-1)):
        assert start <= end, "Cannot attend all apointments"
        while start + duration <= end:
            show_available_slots += "{:%H:%M} - {:%H:%M}".format(start, start + duration) + "\n"
            print( "{:%H:%M} - {:%H:%M}".format(start, start + duration) + "\n")
            start+= duration
    
    available_label = Label(eventCreation, text = show_available_slots)
    available_label.grid(column=6, row=1)
    conn.commit()
    conn.close()
    return

# Function to filter the events shown based off of what drop option is selected
filter_clicked = StringVar()
def filter_event():
    conn = sqlite3.connect('calendar_events.db')
    c = conn.cursor()
    if filter_clicked.get() == "Owner":
        c.execute("SELECT *, oid FROM EVENTS ORDER BY event_owner") 
        events = c.fetchall()
        #print(events) Test to see if it prints from data

        #Loop through events to view on GUI
        show_event = ''
        for event in events:
            show_event += "[" + str(event[0]) + "] " + str(event[1]) + ": " + str(event[2] + "-" + str(event[3]) + " " + str(event[4])) + "\t" + str(event[7]) + "\n"
        event_label = Label(eventCreation, text=show_event)
        event_label.grid(column=2, row=1)
    conn.commit()
    conn.close()
    return

# Function to delete a record
def delete():
    conn = sqlite3.connect('calendar_events.db')
    c = conn.cursor()
    #Delete a record
    c.execute("DELETE from EVENTS WHERE oid = " + delete_box.get())
    conn.commit()
    conn.close()
    
# Function for creating events 
def create_event():
    conn = sqlite3.connect('calendar_events.db')
    c = conn.cursor()
    global owner, startTime, endTime, startDate, endDate, eventName, description, eventData
    eventName = event_name.get()
    description = event_description.get('1.0', 'end-1c')
    owner = owner_name.get()
    startTime = start_time.get()
    if not time.strptime(startTime, "%H:%M"):
        return           
    endTime = end_time.get()
    if not time.strptime(endTime, "%H:%M"):
        return  
    eventData = [owner, startDate, endDate, eventName, startTime, endTime, description]
    print(eventData)
    
    
    # Insert into table
    c.execute("INSERT INTO EVENTS VALUES (:event_owner, :event_name, :start_time, :end_time, :start_date, :end_date, :description)",
            {
                'event_owner': owner,
                'event_name': eventName,
                'start_time': startTime,
                'end_time' : endTime,
                'start_date': startDate,
                'end_date': endDate,
                'description': description
            })
    conn.commit()
    conn.close()
    clear()
    return eventData


#Button for showing events
Button(eventCreation, text='Show Events',padx=10, command = query).grid(column=2, row=0)

#Button to select filter for events
filter_label= Label(eventCreation, text = "Filter by:").grid(column=3, row = 0)
filter_event_button = Button(eventCreation, text='Go', command = filter_event)
filter_event_button.grid(column=5, row=0)

#Button for showing available times
available_time_button = Button(eventCreation, text="Show available times", command=get_available_times).grid(column=6, row=0)

#Button for Deleting records/event
Label(eventCreation, text = "Select ID Number").grid(column=2, row=2)
delete_box = Entry(eventCreation, borderwidth=5, width = 20)
delete_box.grid(column=2, row=3, columnspan = 2)
Button(eventCreation, text='Remove Event', command = delete).grid(column=2, row=4)

#Buttons for selecting start/end dates
Button(eventCreation, text='Select Start Date', padx=17, command=start_date).grid(column=0, row=2)
Button(eventCreation, text='Select End Date', padx=18, command=end_date).grid(column=1, row=2)

#Button for event owner
Label(eventCreation, text="Event Owner").grid(column=0, row=3, columnspan=2)
owner_name = Entry(eventCreation, borderwidth=5, width=40)
owner_name.grid(column=0, row=4, columnspan=2)

#Widgets for event name
Label(eventCreation, text="Event Name").grid(column=0, row=5, columnspan=2)
event_name = Entry(eventCreation, borderwidth=5, width=40)
event_name.grid(column=0, row=6, columnspan=2)

#Widgets for time
Label(eventCreation, text="Start Time").grid(column=0, row=7)
start_time = Entry(eventCreation, borderwidth=5, width=18)
start_time.grid(column=1, row=7)

Label(eventCreation, text="End Time").grid(column=0, row=8)
end_time = Entry(eventCreation, borderwidth=5, width=18)
end_time.grid(column=1, row=8)

#Widgets for description
Label(eventCreation, text="Event Description").grid(column=0, row=9, columnspan=2)
event_description = Text(eventCreation, borderwidth=5, height=10, width=30)
event_description.grid(column=0, row=10, columnspan=2)

#Widgets for create event and clear entries
Button(eventCreation, text='Create Event', padx=27, command=create_event).grid(column=0, row=11)
Button(eventCreation, text='Clear', padx=43, command=clear).grid(column=1, row=11)

#Filter widgets
filter_event_drop = OptionMenu(eventCreation, filter_clicked, "Owner", "Start Date")
filter_event_drop.grid(column=4, row= 0)

#####################################################################################################################

# Code to generate the month view of the calendar
months = (("January", 31), ("February", 28), ("March", 31), ("April", 30), ("May", 31), ("June", 30),
          ("July", 31), ("August", 31), ("September", 30), ("October", 31), ("November", 30), ("December", 31))
monthNum = 0  # tracks what month the month view is on, starting with 0 which is january
monthTuple = months[monthNum]  # To store the pairing of month and number of days for use in create_view()
monthView = Tk()
monthView.title("Calendar")
gridList = []  # Tracks anything placed onto the month grid, so it can be removed when selecting another month


def month_up():  # executed when the > Button is pressed in the app
    global monthNum, monthTuple
    clear_grid()
    monthNum = (monthNum + 1) % 12  # so that the list keeps cycling when you get to december
    monthTuple = months[monthNum]
    create_view()


def month_down():  # executed when the < Button is pressed in the app
    global monthNum, monthTuple
    clear_grid()
    monthNum = (monthNum - 1) % 12
    monthTuple = months[monthNum]
    create_view()


def clear_grid():  # Clears out anything created and placed on the grid so that the next month can be placed
    for i in gridList:
        i.grid_forget()


def create_view():  # fills the month view grid with the number of dates based on the current month
    Label(monthView, text=monthTuple[0], padx=20).grid(column=1, row=0, columnspan=4)
    day = 1  # no comment
    column = 0
    row = 1
    while day <= monthTuple[1]:  # Example monthTuple = ("January", 31) | so prevents having too many days in month
        if column <= 5:  # Keep doing this chunk until it reaches 6 wide
            date = Label(monthView, text=day, padx=53, pady=50)
            date.grid(column=column, row=row)
            gridList.append(date)  # Store the created object in the list, so it can be removed later
            column += 1
            day += 1
            continue
        row += 1  # Move to next row
        column = 0  # Reset column counter
        day += 1


Button(monthView, text='<', padx=20, command=month_down).grid(column=0, row=0)
Button(monthView, text='>', padx=20, command=month_up).grid(column=5, row=0)
create_view()  # Create the first month

#Only run this once to create the database file
'''
#sqlite3 database

connection_obj = sqlite3.connect('calendar_events.db')
 
# cursor object
cursor_obj = connection_obj.cursor()
 
# Drop the GEEK table if already exists.
cursor_obj.execute("DROP TABLE IF EXISTS EVENTS")
 
# Creating table
table = """ CREATE TABLE EVENTS (
            EVENT_OWNER VARCHAR(255) NOT NULL,
            EVENT_NAME VARCHAR(255) NOT NULL,
            START_TIME CHAR(25),
            END_TIME CHAR(25),
            START_DATE CHAR(25) NOT NULL,
            END_DATE CHAR(25),
            DESCRIPTION CHAR(25)
        ); """
 
cursor_obj.execute(table)
 
print("Table is Ready")
 
# Close the connection
connection_obj.close()
'''

eventCreation.mainloop()




