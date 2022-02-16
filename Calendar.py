from tkinter import *
from tkcalendar import Calendar

# Create background
eventCreation = Tk()
icon = PhotoImage(file="quill.ico")
eventCreation.iconphoto(False, icon)
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


def create_event():
    global startDate, endDate, eventName, description, eventData
    eventName = event_name.get()
    description = event_description.get('1.0', 'end-1c')
    eventData = [startDate, endDate, eventName, description]
    # print(eventData)
    # TODO - Store the event data in sqlite 3 database
    return eventData


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

eventCreation.mainloop()
