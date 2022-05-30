
import cv2
from matplotlib.pyplot import text
import numpy as np
from tkinter import *               #

from tkinter import filedialog
from tkinter import ttk
import tkinter.messagebox
from PIL import Image, ImageTk      #

# import class dependency
from Class_learing import Learning

import os
import sys                   #
from functools import partial       #
import json
import logging

logger = logging.getLogger('ftpuploader')


class AddModel:
    def __init__(self, master):
        self.master_add = master
        self.master_add.title("Adding new model")
        # size of windown and position start
        self.master_add.geometry("1280x720+0+0")

        self.cropping = False
        self.x_start, self.y_start, self.x_end, self.y_end = 0, 0, 0, 0
        self.oriImage = None
        # dictionary model
        self.newModel_dict = {
            "name": None,
            "num_pos": None,
            "codi_pos": []
        }

        #
        PB_exit_addModel = Button(self.master_add, text="EXIT", fg="red", bg="black", command=self.EXIT_AddModel).place(
            x=1000, y=600, width=100, height=35)
        PB_get_master = Button(self.master_add, text="GET MASTER", fg="yellow", bg="red", font=18, command=self.get_master).place(
            x=0, y=0, width=150, height=100)
        PB_learing = Button(self.master_add, text="LEARING", fg="yellow", bg="red", font=18, command=self.learning).place(
            x=170, y=0, width=150, height=100)

        self.frame1 = Frame(
            self.master_add)
        self.frame1.place(x=0, y=150)

    def save_newJson(self):
        print("save json: ", self.newModel_dict["codi_pos"])
        with open('NewData.json', 'w') as json_file:
            # เขียน Python Dict ลงในไฟล์ NewData.json
            json.dump(self.newModel_dict, json_file)

    def get_master(self):
        try:
            for widget in self.frame1.winfo_children():
                widget.destroy()
            for widget in self.fram_in_get_master.winfo_children():
                widget.destroy()
            for widget in self.fram_list_pos.winfo_children():
                widget.destroy()
        except:
            pass

        def save_name_model():
            print("name model: ", data.get())
            self.newModel_dict["name"] = data.get()
            print("from name dict", self.newModel_dict["name"])

        def mouse_crop(event, x, y, flags, param):
            # grab references to the global variables
            # global x_start, y_start, x_end, y_end, cropping
            # if the left mouse button was DOWN, start RECORDING
            # (x, y) coordinates and indicate that cropping is being
            if event == cv2.EVENT_LBUTTONDOWN:
                self.x_start, self.y_start, self.x_end, self.y_end = x, y, x, y
                self.cropping = True
            # Mouse is Moving
            elif event == cv2.EVENT_MOUSEMOVE:
                if self.cropping == True:
                    self.x_end, self.y_end = x, y
            # if the left mouse button was released
            elif event == cv2.EVENT_LBUTTONUP:
                # record the ending (x, y) coordinates
                self.x_end, self.y_end = x, y
                self.cropping = False  # cropping is finished
                refPoint = [(self.x_start, self.y_start),
                            (self.x_end, self.y_end)]
                if len(refPoint) == 2:  # when two points were found
                    roi = self.oriImage[refPoint[0][1]:refPoint[1]
                                        [1], refPoint[0][0]:refPoint[1][0]]
                    cv2.imshow("Cropped", roi)

        def draw_crop_func(pos, img):
            image_croped = img
            for i in pos:
                print(i)
                image_croped = cv2.rectangle(image_croped, (i[0], i[1]),
                                             (i[2], i[3]), (0, 255, 0), 2)
            return image_croped

        def crop_position_operation():
            # camera config
            cam = cv2.VideoCapture(0)
            cam.set(cv2.CAP_PROP_AUTOFOCUS, 1)
            if self.newModel_dict["name"] == None:
                pass
            else:
                cv2.namedWindow("image")
                cv2.setMouseCallback("image", mouse_crop)
                while True:
                    check, frame = cam.read()
                    if check:
                        image = frame
                        self.oriImage = image.copy()
                        self.i = image.copy()
                        if not self.cropping:
                            cv2.imshow("image", image)
                        elif self.cropping:
                            cv2.rectangle(self.i, (self.x_start, self.y_start),
                                          (self.x_end, self.y_end), (255, 0, 0), 2)
                            cv2.imshow("image", self.i)
                        k = cv2.waitKey(1)
                        if k == ord('q'):
                            break

                    # add crop position to dict model
                    else:
                        print("check:", check)
                # cam.release()
                cv2.destroyAllWindows()

                self.newModel_dict["codi_pos"].append(
                    [self.x_start, self.y_start, self.x_end, self.y_end])

            # show image croped on GUI
            show = draw_crop_func(
                self.newModel_dict["codi_pos"], self.i.copy())
            # show list for component
            show_list_position()

            resize_image = cv2.resize(show, (640, 480))
            resize_image = cv2.cvtColor(resize_image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(resize_image)
            iago = ImageTk.PhotoImage(image)
            show_image.configure(image=iago)
            show_image.image = iago

        def show_list_position():
            list_pos = self.newModel_dict["codi_pos"]
            start_row = 2
            for p in list_pos:
                Button(self.fram_list_pos, text=p, fg="blue", bg="yellow").grid(
                    row=start_row, column=0)
                Button(self.fram_list_pos, text=p, fg="blue", bg="red", command=lambda p=p: delete_croped(p)).grid(
                    row=start_row, column=1)
                start_row = start_row+1
            PB_saveNewModelJson = Button(self.fram_list_pos, text="SAVE JSON", fg="yellow", bg="green", command=self.save_newJson).grid(
                row=start_row, column=0)

        def delete_croped(data):
            print("delete image: ", data)
            self.newModel_dict["codi_pos"].remove(data)
            # reset GUI
            for widget_list in self.fram_list_pos.winfo_children():
                widget_list.destroy()
            # .............
            show = draw_crop_func(
                self.newModel_dict["codi_pos"], self.i.copy())
            # show list for component
            show_list_position()
            # show picture
            resize_image = cv2.resize(show, (640, 480))
            resize_image = cv2.cvtColor(resize_image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(resize_image)
            iago = ImageTk.PhotoImage(image)
            show_image.configure(image=iago)
            show_image.image = iago

       # entry new name model
        data = StringVar()
        self.fram_in_get_master = Frame(self.master_add)
        self.fram_in_get_master.place(x=700, y=150)
        self.fram_list_pos = Frame(self.master_add)
        self.fram_list_pos.place(x=700, y=250)

        Label(self.fram_in_get_master, text="New Model: ",
              fg="blue", bg="yellow").grid(row=0, column=0)
        entry1 = Entry(self.fram_in_get_master,
                       textvariable=data).grid(row=0, column=1)
        Button(self.fram_in_get_master, text="save", command=save_name_model,
               fg="blue", bg="green", font=("Helvetica", 10)).grid(row=0, column=2, pady=2)
        Button(self.fram_in_get_master, text="POSITION", command=crop_position_operation,
               fg="green", bg="gold", font=("Helvetica", 10)).grid(row=1, column=0)

        # ..................

        title_get_master = Label(self.frame1, text="IMAGE", font=(
            "Ariel", 11), fg="yellow", bg="red",)
        title_get_master.pack()
        show_image = Label(self.frame1, width=640, height=480)
        show_image.pack()

# Buton learning
    def learning(self):
        for widget in self.frame1.winfo_children():
            widget.destroy()
        for widget in self.fram_in_get_master.winfo_children():
            widget.destroy()
        for widget in self.fram_list_pos.winfo_children():
            widget.destroy()

        learing_ope = Learning(self.master_add)
    # def learning(self):
    #     try:
    #         for widget in self.frame1.winfo_children():
    #             widget.destroy()
    #         for widget in self.fram_in_get_master.winfo_children():
    #             widget.destroy()
    #         for widget in self.fram_list_pos.winfo_children():
    #             widget.destroy()
    #     except:
    #         pass

    #     show_image = Label(self.frame1, width=640, height=480)
    #     show_image.pack()
    #     title_learning = Label(self.frame1, text="IMAGE", font=(
    #         "Ariel", 11), fg="yellow", bg="red",)
    #     title_learning.pack()

    def EXIT_AddModel(self):
        cv2.destroyAllWindows()
        self.master_add.destroy()
