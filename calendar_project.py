# Import Required Library
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
 
# Create Object
root = Tk()

root.title("Calendar")
 
# Set geometry
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
 
# Add Calendar
cal = Calendar(root, selectmode = 'day')
               
 
cal.grid(column=2, row=1, sticky=(W,E ))
 
def grad_date():
    date.config(text = "Selected Date is: " + cal.get_date())

def create_event():
    set_date = cal.datetime.today()
    cal.calevent_create(set_date, "Message", 'message')
    cal.tag_config('reminder', background='red', foreground='yellow')
    cal.grid(column=1, row=2, sticky=W)

    #ttk.Label('top', text="Hover over the events.").pack() Causing errors

# Make it light mode
def light_mode():
    cal = Calendar(root,selectmode = 'day')
    cal.grid(column=2, row=1, sticky=(W,E ))
    root.config(background = "lightgrey")
def dark_mode():
    cal = Calendar(root, background="white", disabledbackground="black", bordercolor="white", 
               headersbackground="black", normalbackground="black", foreground='white', 
               normalforeground='white', headersforeground='white')
    cal.config(background = "black")
    root.config(background = "black")
    cal.grid(column=2, row=1, sticky=(W,E ))
# Add Button and Label
Button(root, text = "Get Date",
       command = grad_date).grid(column=2, row=3, sticky=S)

Button(root, text = "Create Event",
       command = create_event).grid(column=1, row=3, sticky= W)

Button(root, text = "☼",
       command = light_mode).grid(column=3,row=1,sticky=(N,E))
Button(root, text = "☽",
       command = dark_mode).grid(column=4,row=1,sticky=(N,E))
date = Label(root, text = "")
date.grid(column=2, row=2, sticky=(W,E))
 
# Execute Tkinter
root.mainloop()
