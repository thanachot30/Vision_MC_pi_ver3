# Import the required libraries
from tkinter import *
from tkinter import ttk

# Create an instance of tkinter frame or window
win = Tk()

# Set the size of the window
win.geometry("700x350")


def on_click(text):
    entry.delete(0, END)
    entry.insert(0, text)


# Add an Entry widget
entry = Entry(win, width=25)
entry.pack()

# Add Buttons in the window
b1 = ttk.Button(win, text="A", command=lambda: on_click("A"))
b1.pack()

b2 = ttk.Button(win, text="B", command=lambda: on_click("B"))
b2.pack()

b3 = ttk.Button(win, text="C", command=lambda: on_click("C"))
b3.pack()

win.mainloop()
