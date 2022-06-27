from turtle import color
import cv2
import numpy as np
from tkinter import *               #
from tkinter import filedialog
from tkinter import ttk
import tkinter.font as font
from PIL import Image, ImageTk      #
# import class dependency.      
from Class_AddModel import AddModel 
from Class_operation import Operation
from functools import partial       #


class App: 
    def __init__(self, master):
        self.master = master
        self.master.title("ANTROBOTICS IMG")
        # size of windown and position start
        # self.master.geometry("100x100+0+0")
        self.value_start = 20
        self.num_comp = 0                                                                 
        self.width = 10
        self.height= 2
        myFont = font.Font(family='Courier',size=20,weight='bold')
        # Button Add and seting
        PB_add_model = Button(self.master, text="ADD", fg="black",width=self.width,height=self.height, bg="yellow", command=self.add_model)
        PB_add_model['font'] = myFont
        PB_add_model.pack()
        
        PB_operation = Button(self.master, text="OPERATION", fg="black", font=100,width=self.width,height=self.height, bg="yellow", command=self.operation)
        PB_operation['font'] = myFont
        PB_operation.pack()

        PB_exit= Button(self.master, text="EXIT", fg="red", bg="black",font=100,width=self.width,height=self.height, command=self.exit)
        PB_exit['font'] = myFont
        PB_exit.pack()

        # Operation home page# for Auto Mode
        
        # operation = Operation(Toplevel(self.master))

    def show_process_bar(self, get):
        # show component bar and percent of true
        get_model = get
        if get_model == "Selact an Model":
            print(get_model)
            self.num_comp = 0
        elif get_model == "antoo1":
            print(get_model)
            self.num_comp = 1
        elif get_model == "antoo2":
            print(get_model)
            self.num_comp = 2
        start = 100
        for i in range(int(self.num_comp)):
            print(i)
            ttk.Progressbar(self.master, orient=HORIZONTAL,
                            length=200, value=self.value_start).place(x=800, y=start)
            start = start + 100
            self.value_start = self.value_start + 15
        return

    def add_model(self):
        print("add_model")
        add_model = Toplevel(self.master)
        add_mode = AddModel(add_model)

    def operation(self):
        print("start Operation")
        operation = Operation(Toplevel(self.master))

    def setting(self):
        print("seting")

    def exit(self):
        cv2.destroyAllWindows()
        self.master.destroy()

def main():
    root = Tk()
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
