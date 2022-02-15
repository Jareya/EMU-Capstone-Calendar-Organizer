from tkinter import *
from tkcalendar import Calendar

# Create background
root = Tk()
icon = PhotoImage(file="quill.ico")
root.iconphoto(False, icon)
root.title("Calendar")

# Functions to show and hide the date picker
cal = Calendar(root, selectmode='day', borderwidth=3)
cal.grid(column=0, row=1, columnspan=2, rowspan=1)


def show_cal():
    cal.grid(column=0, row=1, columnspan=2, rowspan=1)


def hide_cal():
    cal.grid_forget()


Button(root, text='Show Calendar', padx=20, command=show_cal).grid(column=0, row=0)
Button(root, text='Hide Calendar', padx=21, command=hide_cal).grid(column=1, row=0)

# Month view
months = (("January", 31), ("February", 28), ("March", 31), ("April", 30), ("May", 31), ("June", 30),
          ("July", 31), ("August", 31), ("September", 30), ("October", 31), ("November", 30), ("December", 31))
monthNum = 0
monthTuple = months[monthNum]
monthView = Tk()


def monthUp():
    global monthNum, monthTuple
    monthNum = (monthNum + 1) % 12
    monthTuple = months[monthNum]
    createView()
    print(monthNum)


def monthDown():
    global monthNum, monthTuple
    monthNum = (monthNum - 1) % 12
    monthTuple = months[monthNum]
    createView()
    print(monthNum)


def createView():
    monthView.title("Calendar")
    Button(monthView, text='<', padx=20, command=monthDown).grid(column=0, row=0)
    Button(monthView, text='>', padx=20, command=monthUp).grid(column=5, row=0)
    Label(monthView, text=monthTuple[0], padx=20).grid(column=0, row=0, columnspan=6)
    i = 1
    column = 0
    row = 1
    while i <= monthTuple[1]:
        if column <= 5:
            if i < 10:
                date = Label(monthView, text=i, padx=53, pady=50)
                date.grid(column=column, row=row)
                column += 1
                i += 1
                continue
            date = Label(monthView, text=i, padx=53, pady=50)
            date.grid(column=column, row=row)
            column += 1
            i += 1
            continue
        row += 1
        column = 0
        i += 1


createView()

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
    print(eventData)
    return eventData


Button(root, text='Select Start Date', padx=17, command=start_date).grid(column=0, row=2)
Button(root, text='Select End Date', padx=18, command=end_date).grid(column=1, row=2)

Label(root, text="Event Name").grid(column=0, row=3, columnspan=2)
event_name = Entry(root, borderwidth=5, width=40)
event_name.grid(column=0, row=4, columnspan=2)

Label(root, text="Event Description").grid(column=0, row=5, columnspan=2)
event_description = Text(root, borderwidth=5, height=20, width=30)
event_description.grid(column=0, row=6, columnspan=2)

Button(root, text='Create Event', padx=27, command=create_event).grid(column=0, row=7)
Button(root, text='Clear', padx=43, command=clear).grid(column=1, row=7)

root.mainloop()
