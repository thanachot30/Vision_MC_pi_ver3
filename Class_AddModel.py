
import cv2
from matplotlib.pyplot import text
import numpy as np
from tkinter import *               #

from tkinter import filedialog

import tkinter.messagebox
from PIL import Image, ImageTk      #

# import class dependency
from Class_learing import Learning
from Class_EachLearning import EachLearning

import os
import sys                   #
from functools import partial       #
import json
import logging

logger = logging.getLogger('ftpuploader')


class AddModel:
    def __init__(self, master):
        self.master_add = master
        self.screen_w = 1200
        self.screen_h = 850
        self.master_add.title("Adding new model")
        # size of windown and position start
        self.master_add.geometry("1920x1080+0+0")

        self.cropping = False
        self.on_cam = False
        self.x_start, self.y_start, self.x_end, self.y_end = 0, 0, 0, 0
        self.oriImage = None
        self.show = None

        # dictionary model
        self.newModel_dict = {
            "name": None,
            "num_pos": None,
            "codi_pos": []
        }
        self.newProcessing_dict = {
            "name": None,
            "num_pos": None,
            "codi_pos": [],
            "threshold": []
        }
        #
        PB_exit_addModel = Button(self.master_add, text="EXIT", fg="red", bg="black",height=3,width=25, command=self.EXIT_AddModel).place(
            x=1350, y=600, width=300, height=100)
        PB_get_master = Button(self.master_add, text="GET MASTER", fg="yellow", bg="red", font=18, command=self.get_master).place(
            x=0, y=0, width=300, height=100)

        PB_processing = Button(self.master_add, text="GET PROCESSING", fg="black", bg="#00FFFF", font=18, command=self.get_processing).place(
            x=300, y=0, width=300, height=100)
        #
        self.frame1 = Frame(
            self.master_add)
        self.frame1.place(x=0, y=100)
        # Opration
        self.read_json_file()
    def read_json_file(self):
        with open('NewData.json') as f:
            self.newModel_dict = json.load(f)
        print("JSON MODEL FILE: ", self.newModel_dict)

        with open('NewDataProcessing.json') as f:
            self.newProcessing_dict = json.load(f)
        print("JSON processing FILE: ", self.newProcessing_dict)
        return

    def save_newJson(self):
        print("save json model: ", self.newModel_dict["codi_pos"])
        with open('NewData.json', 'w') as json_file:
            # เขียน Python Dict ลงในไฟล์ NewData.json
            json.dump(self.newModel_dict, json_file)
    def save_newJson_processing(self):
        print("save json processing: ", self.newProcessing_dict["codi_pos"])
        with open('NewDataProcessing.json', 'w') as json_file_process:
            # เขียน Python Dict ลงในไฟล์ NewDataProcessing.json
            json.dump(self.newProcessing_dict, json_file_process)

        # save image crop
        for index in range(len(self.newProcessing_dict["codi_pos"])):
            pos = self.newProcessing_dict['codi_pos'][index]
            image = self.image_save.copy()
            croping = image[int(pos[1]):int(
                pos[3]), int(pos[0]):int(pos[2])]
            resize_crop = cv2.resize(croping, (50, 50))
            path_to_save = "/home/pi/Documents/Vision_MC_pi/Vision_MC_pi_ver3/data_new_processing/image" + \
                str(index+1)+".jpg"
            print(path_to_save)
            cv2.imwrite(path_to_save, resize_crop)
        return
#function for only Image processing
    def get_processing(self):
        try:
            for widget in self.frame1.winfo_children():
                widget.destroy()
            for widget in self.fram_in_get_master.winfo_children():
                widget.destroy()
            for widget in self.fram_list_pos.winfo_children():
                widget.destroy()
        except:
            pass
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
                    # cv2.imshow("Cropped", roi)
                    # cv2.waitKey(1000)
                    # cv2.destroyWindow("Cropped")
                    self.on_cam = False
                    print("gu crop")            
            return

        def draw_crop_func(pos, img):
            image_croped = img
            for i in pos:
                print(i)
                image_croped = cv2.rectangle(image_croped, (i[0], i[1]),
                                             (i[2], i[3]), (0, 255, 0), 2)
            return image_croped

        def crop_position_operation():            
            # camera config
            self.on_cam = True
            cam = cv2.VideoCapture(0)
            cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
            cam.set(28,180)
            # set mouse call back
            
            if self.newProcessing_dict["name"] == None:
                pass
            else:
                cv2.namedWindow("image")
                cv2.setMouseCallback("image", mouse_crop)
                while True:
                    check, frame = cam.read()
                    frame = cv2.resize(frame,(self.screen_w,self.screen_h))
                    if check:
                        image = frame.copy()
                        self.oriImage = frame.copy()
                        self.image_save = frame.copy()
                        self.image_copy = frame.copy()  
                        if not self.cropping:
                            cv2.imshow("image", image)
                        elif self.cropping:
                            cv2.rectangle(self.image_copy, (self.x_start, self.y_start),
                                          (self.x_end, self.y_end), (0, 0, 255), 2)
                            cv2.imshow("image", self.image_copy)
#fuck
                        k = cv2.waitKey(1)
                        if self.on_cam == False:
                            break
                        elif k == ord('q'):
                            break
                    # add crop position to dict model
                    else:
                        print("check:", check)
                        cam = cv2.VideoCapture(0)
                        cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
                        cam.set(28,200)

                cv2.destroyAllWindows()
                cam.release()
                # save crop codinate position
                self.newProcessing_dict["codi_pos"].append(
                    [self.x_start, self.y_start, self.x_end, self.y_end,70])
                
            # show image croped on GUI
            self.show = draw_crop_func(
                self.newProcessing_dict["codi_pos"], self.image_save.copy())
            # show list for component
            show_list_position()
            resize_image = cv2.resize(self.show, (self.screen_w, self.screen_h))
            resize_image = cv2.cvtColor(resize_image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(resize_image)
            iago = ImageTk.PhotoImage(image)
            show_image.configure(image=iago)
            show_image.image = iago

        def show_list_position():
            list_pos = self.newProcessing_dict["codi_pos"]
            # loop for delete same pos, from click
            for k in list_pos:
                if k[0] == k[2]:
                    self.newProcessing_dict["codi_pos"].remove(k)
                else:
                    pass
            list_pos = self.newProcessing_dict["codi_pos"]
            start_row = 2
            for p in list_pos:
                Button(self.fram_list_pos, text=p, fg="blue", bg="yellow",height=3,width=25).grid(
                    row=start_row, column=0)
                Button(self.fram_list_pos, text=p, fg="blue", bg="red",height=3,width=25,command=lambda p=p: delete_croped(p)).grid(
                    row=start_row, column=1)
                start_row = start_row+1
            PB_saveNewModelJson = Button(self.fram_list_pos, text="SAVE JSON", fg="yellow", bg="green",height=3,width=25, command=self.save_newJson_processing).grid(
                row=start_row, column=0)

        def delete_croped(data):
            print("delete image: ", data)
            self.newProcessing_dict["codi_pos"].remove(data)
            print("joson dict: ", self.newProcessing_dict["codi_pos"])

            # reset GUI
            for widget_list in self.fram_list_pos.winfo_children():
                widget_list.destroy()

            show = draw_crop_func(
                self.newProcessing_dict["codi_pos"], self.image_save.copy())
            # show list for component
            show_list_position()
            # show picture
        
            resize_image = cv2.resize(show, (self.screen_w, self.screen_h))
            resize_image = cv2.cvtColor(resize_image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(resize_image)
            iago = ImageTk.PhotoImage(image)
            show_image.configure(image=iago)
            show_image.image = iago

        data = StringVar()
        self.fram_in_get_master = Frame(self.master_add)
        self.fram_in_get_master.place(x=1350, y=0)
        self.fram_list_pos = Frame(self.master_add)
        self.fram_list_pos.place(x=1350, y=100)

        Button(self.fram_in_get_master, text="POSITION", command=crop_position_operation,
               fg="green", bg="gold",height=3,width=10, font=("Helvetica", 18)).grid(row=1, column=0)
        # ..................
        title_get_master = Label(self.frame1, text="IMAGE", font=(
            "Ariel", 30), fg="yellow", bg="red",)
        title_get_master.pack()
        show_image = Label(self.frame1, width=self.screen_w, height=self.screen_h)
        show_image.pack()

# function for ML crop and save image 
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
                    # cv2.imshow("Cropped", roi)
                    self.on_cam = False
            return

        def draw_crop_func(pos, img):
            image_croped = img
            for i in pos:
                print(i)
                image_croped = cv2.rectangle(image_croped, (i[0], i[1]),
                                             (i[2], i[3]), (0, 255, 0), 2)
            return image_croped

        def crop_position_operation():
            # camera config
            self.on_cam = True
            cam = cv2.VideoCapture(0)
            cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
            cam.set(28,180)
            if self.newModel_dict["name"] == None:
                pass
            else:
                cv2.namedWindow("image")
                cv2.setMouseCallback("image", mouse_crop)
                while True:
                    check, frame = cam.read()
                    frame = cv2.resize(frame,(self.screen_w,self.screen_h))
                    if check:
                        image = frame
                        self.oriImage = frame.copy()
                        self.image_save = frame.copy()
                        self.i = frame.copy()
                        if not self.cropping:
                            cv2.imshow("image", image)
                        elif self.cropping:
                            cv2.rectangle(self.i, (self.x_start, self.y_start),
                                          (self.x_end, self.y_end), (255, 0, 0), 2)
                            cv2.imshow("image", self.i)
                        k = cv2.waitKey(1)
                        if self.on_cam == False:
                            break
                        elif k == ord('q'):
                            break

                    # add crop position to dict model
                    else:
                        print("check:", check)
                # cam.release()
                cv2.destroyAllWindows()
                cam.release()

                self.newModel_dict["codi_pos"].append(
                    [self.x_start, self.y_start, self.x_end, self.y_end])

            # show image croped on GUI
            show = draw_crop_func(
                self.newModel_dict["codi_pos"], self.image_save.copy())
            # show list for component
            show_list_position()

            resize_image = cv2.resize(show, (self.screen_w, self.screen_h))
            resize_image = cv2.cvtColor(resize_image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(resize_image)
            iago = ImageTk.PhotoImage(image)
            show_image.configure(image=iago)
            show_image.image = iago

        def show_list_position():
            list_pos = self.newModel_dict["codi_pos"]
            for k in list_pos:
                if k[0] == k[2]:
                    self.newModel_dict["codi_pos"].remove(k)
                else:
                    pass
            list_pos = self.newModel_dict["codi_pos"]
            start_row = 2
            for p in list_pos:
                Button(self.fram_list_pos, text=p, fg="blue", bg="yellow",height=3,width=25,font=("Helvetica", 18),command=lambda p=p: self.each_learning(p)).grid(
                    row=start_row, column=0)
                Button(self.fram_list_pos, text=p, fg="blue", bg="red",height=3,width=25,font=("Helvetica", 18),command=lambda p=p: delete_croped(p)).grid(
                    row=start_row, column=1)
                start_row = start_row+1
            PB_saveNewModelJson = Button(self.fram_list_pos, text="SAVE JSON", fg="yellow", bg="green",height=3,width=25,command=self.save_newJson).grid(
                row=start_row, column=0)

        def delete_croped(data):
            print("delete image: ", data)
            self.newModel_dict["codi_pos"].remove(data)
            # reset GUI
            for widget_list in self.fram_list_pos.winfo_children():
                widget_list.destroy()
            # .............
            show = draw_crop_func(
                self.newModel_dict["codi_pos"], self.image_save.copy())
            # show list for component
            show_list_position()
            # show picture
            resize_image = cv2.resize(show, (self.screen_w, self.screen_h))
            resize_image = cv2.cvtColor(resize_image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(resize_image)
            iago = ImageTk.PhotoImage(image)
            show_image.configure(image=iago)
            show_image.image = iago

       # entry new name model
        data = StringVar()
        self.fram_in_get_master = Frame(self.master_add)
        self.fram_in_get_master.place(x=1200, y=0)
        self.fram_list_pos = Frame(self.master_add)
        self.fram_list_pos.place(x=1200, y=100)

        
        Button(self.fram_in_get_master, text="POSITION", command=crop_position_operation,
               fg="green", bg="gold",height=3,width=10,font=("Helvetica", 18)).grid(row=1, column=0)

        # ..................

        title_get_master = Label(self.frame1, text="IMAGE", font=(
            "Ariel", 30), fg="yellow", bg="red",)
        title_get_master.pack()
        show_image = Label(self.frame1, width=self.screen_w, height=self.screen_h)
        show_image.pack()

# Buton learning
    
    def each_learning(self,data):
        each_learning = EachLearning(self.master_add,data)
        
    def EXIT_AddModel(self):
        cv2.destroyAllWindows()
        self.master_add.destroy()
