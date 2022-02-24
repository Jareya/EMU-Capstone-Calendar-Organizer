from tkinter import *
from tkcalendar import Calendar
import sqlite3

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
    return None

# function to show events (Query)
def query():
    conn = sqlite3.connect('calendar_events.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM EVENTS")
    events = c.fetchall()
    #print(events) Test to see if it prints from data

    #Loop through events to view on GUI
    show_event = ''
    for event in events:
        show_event += str(event[0]) + ": " + str(event[1]) + "-" + str(event[2]) + " " + str(event[3]) + " ""\n"
    event_label = Label(eventCreation, text=show_event)
    event_label.grid(column=4, row=6, columnspan=2)
    conn.commit()
    conn.close()
    return

def create_event():
    conn = sqlite3.connect('calendar_events.db')
    c = conn.cursor()
    global startDate, endDate, eventName, description, eventData
    eventName = event_name.get()
    description = event_description.get('1.0', 'end-1c')
    eventData = [startDate, endDate, eventName, description]
    # print(eventData)
    
    # Insert into table
    c.execute("INSERT INTO EVENTS VALUES (:event_name, :start_date, :end_date, :description)",
            {
                'event_name': eventName,
                'start_date': startDate,
                'end_date': endDate,
                'description': description
            })
    conn.commit()
    conn.close()
    return eventData


#Button for showing events
Button(eventCreation, text='Show Events', command = query).grid(column=4, row=7)

#Buttons for selecting start/end dates
Button(eventCreation, text='Select Start Date', padx=17, command=start_date).grid(column=0, row=2)
Button(eventCreation, text='Select End Date', padx=18, command=end_date).grid(column=1, row=2)

Label(eventCreation, text="Event Name").grid(column=0, row=3, columnspan=2)
event_name = Entry(eventCreation, borderwidth=5, width=40)
event_name.grid(column=0, row=4, columnspan=2)

Label(eventCreation, text="Event Description").grid(column=0, row=5, columnspan=2)
event_description = Text(eventCreation, borderwidth=5, height=20, width=30)
event_description.grid(column=0, row=6, columnspan=2)

Button(eventCreation, text='Create Event', padx=27, command=create_event).grid(column=0, row=7)
Button(eventCreation, text='Clear', padx=43, command=clear).grid(column=1, row=7)


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
            EVENT_NAME VARCHAR(255) NOT NULL,
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


