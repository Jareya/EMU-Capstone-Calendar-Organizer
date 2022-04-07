from tkinter import *
from tkinter import messagebox
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
        booked += [(appointment[4].split('/')[2], appointment[4].split('/')[0], appointment[4].split('/')[1], appointment[2].split(':')[0], appointment[2].split(':')[1], appointment[4].split('/')[2], appointment[4].split('/')[0], appointment[4].split('/')[1], appointment[3].split(':')[0], appointment[2].split(':')[1])]
    
    #Creates datetime tuple for events on same day as selected start date
    for i in booked:
        if int(i[1]) == int(startDate.split('/')[0]) and int(i[2]) == int(startDate.split('/')[1]):
            all_events.append(tuple((datetime(int(i[0]),int(i[1]),int(i[2]),int(i[3]), int(i[4])), datetime(int(i[5]),int(i[6]),int(i[7]),int(i[8]), int(i[9])))))
        else:
            continue

    
    #The time range to find availabe slots    
    hours = (datetime(int(startDate.split('/')[2]), int(startDate.split('/')[0]), int(startDate.split('/')[1]), 8), (datetime(int(startDate.split('/')[2]), int(startDate.split('/')[0]), int(startDate.split('/')[1]), 18)))
    print(hours)
    #Sorts all events and displays the timeslots available 
    slots = sorted([(hours[0], hours[0])] + all_events + [(hours[1], hours[1])])
    print(slots)
    print("______________")
    
            
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

    if filter_clicked.get() == "Start Date":
        c.execute("SELECT *, oid FROM EVENTS ORDER BY start_date")
        events = c.fetchall()
        #print(events) Test to see if it prints from data

        #Loop through events to view on GUI
        show_event = ''
        for event in events:
            show_event += "[" + str(event[0]) + "] " + str(event[1]) + ": " + str(event[2] + "-" + str(event[3]) + " " + str(event[4])) + "\t" + str(event[7]) + "\n"
        event_label = Label(eventCreation, text=show_event)
        event_label.grid(column=2, row=1)

    if filter_clicked.get() == "Event Name":
        c.execute("SELECT *, oid FROM EVENTS ORDER BY event_name")
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
    c.execute("DELETE from EVENTS WHERE oid = " + select_box.get())
    conn.commit()
    conn.close()


# Function to update a record
def update():
    conn = sqlite3.connect('calendar_events.db')
    c = conn.cursor()
    # Uses oid from the Select ID entry box
    record_id = select_box.get()

    # Update the database with new set of entry
    c.execute("""UPDATE EVENTS SET
            EVENT_OWNER= :owner,
            EVENT_NAME= :eventName,
            START_TIME= :startTime,
            END_TIME= :endTime,
            START_DATE= :startDate,
            END_DATE= :endDate,
            DESCRIPTION= :description
            WHERE oid = :oid""",
              {'owner': owner_name_edit.get(),
               'eventName': event_name_edit.get(),
               'startTime': start_time_edit.get(),
               'endTime': end_time_edit.get(),
               'startDate': startDate_edit,
               'endDate': endDate_edit,
               'description': event_description_edit.get('1.0', 'end-1c'),
               'oid': record_id
               })
    conn.commit()
    conn.close()
    editor.destroy()

# Grab dates in the edit tk
def start_date_edit():
    global startDate_edit
    startDate_edit = cal_edit.get_date()  # returns in m/d/y format
    return None


def end_date_edit():
    global endDate_edit
    endDate_edit = cal_edit.get_date()  # returns in m/d/y format
    return None


# Function to create the edit prompt where you can change/modify a event in the database
def edit():
    global editor
    conn = sqlite3.connect('calendar_events.db')
    c = conn.cursor()
    record_id = select_box.get()
    c.execute("SELECT * FROM EVENTS WHERE oid = " + record_id)
    events = c.fetchall()
    
        
                                                                                  
    editor = Tk()
    editor.title("Edit Event")
    global cal_edit
    cal_edit = Calendar(editor, selectmode='day', borderwidth=3)
    cal_edit.grid(column=0, row=1, columnspan=2, rowspan=1)
    global startDate_edit
    global endDate_edit
    global owner_name_edit
    global event_name_edit
    global start_time_edit
    global end_time_edit
    global event_description_edit

    for event in events:       
        startDate_edit = event[4]
        endDate_edit = event[5]
    print(startDate_edit)
    print(endDate_edit)

    # Remaking the UI in a pop up with same features
    Button(editor, text='Select Start Date', padx=17, command=start_date_edit).grid(column=0, row=2)
    Button(editor, text='Select End Date', padx=18, command=end_date_edit).grid(column=1, row=2)
    
    Label(editor, text="Event Owner").grid(column=0, row=3, columnspan=2)
    owner_name_edit = Entry(editor, borderwidth=5, width=40)
    owner_name_edit.grid(column=0, row=4, columnspan=2)
    
    Label(editor, text="Event Name").grid(column=0, row=5, columnspan=2)
    event_name_edit = Entry(editor, borderwidth=5, width=40)
    event_name_edit.grid(column=0, row=6, columnspan=2)

    Label(editor, text="Start Time").grid(column=0, row=7)
    start_time_edit = Entry(editor, borderwidth=5, width=18)
    start_time_edit.grid(column=1, row=7)

    Label(editor, text="End Time").grid(column=0, row=8)
    end_time_edit = Entry(editor, borderwidth=5, width=18)
    end_time_edit.grid(column=1, row=8)

    Label(editor, text="Event Description").grid(column=0, row=9, columnspan=2)
    event_description_edit = Text(editor, borderwidth=5, height=10, width=30)
    event_description_edit.grid(column=0, row=10, columnspan=2)

    # Inserts the data from an event into the edit tk
    for event in events:    
        owner_name_edit.insert(0, event[0])
        event_name_edit.insert(0, event[1])
        start_time_edit.insert(0, event[2])
        end_time_edit.insert(0, event[3])
        
        event_description_edit.insert(1.0, event[6])
    #Create a Save button
    save_btn = Button(editor, text = "Save", command=update, width=37).grid(column=0, row=11, columnspan=2)
    conn.commit()
    conn.close()
# Function for creating events 
def create_event():
    try:
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
    except ValueError:
        messagebox.showerror(title= "An Error has occurred", message = "Please enter a start and end time in %H:%M format. i.e 3:00, 15:00")
    except sqlite3.IntegrityError:
        messagebox.showerror(title= "An Error has occurred", message = "The following entries cannot be left blank: Start Date, Event Owner, Event Name, Start/End Time")
    return eventData

def ask_help():
    global help_box
    help_box = Tk()
    help_box.title("Help Info")
    help_label = Label(help_box, text = "Help Info")
    

    help_text="""Create and show available times To create an event:
Select a Start and End date using the buttons below the
calendar and fill in the following boxes underneath
The following entries must be completed for an event to be
created: Start Date, Event Owner, Event Name, Start/End Time
Once the event entries have been completed, click the
create event button to store it. You can clear the data using
the clear data
             
Show Events:
To show events entered, click the Show Events button which
will display all events stored. The events can be
filtered using the drop downand clicking Go to apply the filter.
             
Show Available times: To show available times, first
use the calendar to select which date you would like
to view available times by selecting a date
and clicking Select Start Date. Click show available times
to display following timeslots that are available on that day.
             
Remove/Edit Events:
Click show events to display the event ID number (Far right number).
To edit/remove, enter the ID number and select either edit or
remove. If edit, another window will pop up which will allow you to
change the data for that event. Click save to update that event.
            """
    text = Text(help_box, height = 20, width = 70)
    help_label.pack()
    text.pack()
    text.insert(END, help_text)
    
    return

#Button for help box
Button(eventCreation, text='Help', padx=40, command = ask_help).grid(column= 6, row = 11)
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
select_box = Entry(eventCreation, borderwidth=5, width = 20)
select_box.grid(column=2, row=3, columnspan = 2)
Button(eventCreation, text='Remove Event', command = delete).grid(column=2, row=4)

#Button for Editing Records
Button(eventCreation, text='Edit Event', command = edit).grid(column=2, row=5)

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
filter_event_drop = OptionMenu(eventCreation, filter_clicked, "Owner", "Start Date", "Event Name")
filter_event_drop.grid(column=4, row= 0)

#####################################################################################################################
'''
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
'''
#Only run this once to create the database file

#sqlite3 database

connection_obj = sqlite3.connect('calendar_events.db')
 
# cursor object
cursor_obj = connection_obj.cursor()
 
# Drop the GEEK table if already exists.
#cursor_obj.execute("DROP TABLE IF EXISTS EVENTS")
 
# Creating table
table = """ CREATE TABLE IF NOT EXISTS EVENTS (
            EVENT_OWNER VARCHAR(255) NOT NULL,
            EVENT_NAME VARCHAR(255) NOT NULL,
            START_TIME CHAR(25) NOT NULL,
            END_TIME CHAR(25),
            START_DATE CHAR(25) NOT NULL,
            END_DATE CHAR(25),
            DESCRIPTION CHAR(25)
        ); """
 
cursor_obj.execute(table)
 
print("Table is Ready")
 
# Close the connection
connection_obj.close()


eventCreation.mainloop()


