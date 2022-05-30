from ast import Return
import cv2
from matplotlib.pyplot import text
import numpy as np
import tensorflow as tf
from tkinter import *               #

from tkinter import filedialog
from tkinter import ttk
import tkinter.messagebox
from PIL import Image, ImageTk      #

# import class dependency

###
import os
import sys                   #
from functools import partial       #
import time
import json
import logging
import os
from os import listdir


class Operation:
    def __init__(self, master):
        self.master_op = master
        self.master_op.title("Operation page auto")
        # size of windown and position start
        self.master_op.geometry("1280x720+0+0")
        self.frame1 = Frame(self.master_op)
        self.frame1.place(x=0, y=150)
        self.show_image = Label(self.frame1, width=640, height=480)
        self.show_image.pack()
        self.readjson = {}
        self.model_dict = {}

        PB_exit = Button(self.master_op, text="EXIT", fg="red", bg="black", command=self.EXIT_operation).place(
            x=1000, y=600, width=100, height=35)
        ######

        # main operation step
        self.read_json_file()
        self.model_init()
        self.cam_main = cv2.VideoCapture(0)
        self.cam_main.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        self.Loop()

    def model_init(self):
        parent_dir = "/home/pi/Documents/Vision_MC_ver3/Vision_mc_ver3/data_save_ml/"
        file_list = listdir(parent_dir)
        for index_model in range(len(file_list)):
            path_model = parent_dir+"model_pos" + \
                str(index_model+1)+".h5"
            load_model = tf.keras.models.load_model(path_model)
            self.model_dict["pos"+str(index_model+1)] = load_model
            print("init model"+"pos"+str(index_model+1))
        return

    def Loop(self):
        def predict_ok_ng(image_crop, index_pos):
            class_names = ["ng", "ok"]
            batch_size = 32
            img_height = 50
            img_width = 50
            image_actual = image_crop
            model_number = index_pos+1
            model = self.model_dict["pos"+str(model_number)]
            # image and preprocessing,size and type to array
            img_array = tf.keras.utils.img_to_array(image_actual)
            img_array = tf.expand_dims(img_array, 0)  # Create a batch
            # prediction
            predictions = model.predict(img_array)
            score = tf.nn.softmax(predictions[0])

            return class_names[np.argmax(score)], 100 * np.max(score)

            # print(predictions)

            # print(
            #     "This image "+"pos" +
            #     str(model_number) +
            #     " belongs to {} with a {:.2f} percent confidence."
            #     .format(class_names[np.argmax(score)], 100 * np.max(score))
            # )
        def draw_crop_func(img):
            image_actual = img
            for index_pos in range(len(self.readjson["codi_pos"])):
                pos = self.readjson["codi_pos"][index_pos]
                croping = image_actual[int(pos[1]):int(
                    pos[3]), int(pos[0]):int(pos[2])]
                resize_crop = cv2.resize(croping, (50, 50))
                # save actual image
                cv2.imwrite(r"/home/pi/Documents/Vision_MC_ver3/Vision_mc_ver3/data_actual_image/{}.jpg".format(
                    "pos"+str(index_pos+1)), resize_crop)
                predict_result, score_100 = predict_ok_ng(
                    resize_crop, index_pos)

                if predict_result == "ok":
                    image_actual = cv2.rectangle(image_actual, (pos[0], pos[1]),
                                                 (pos[2], pos[3]), (0, 255, 0), 2)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img, str(
                        score_100), (pos[0], pos[1]), font, 1.5, (0, 0, 0), 3, cv2.LINE_AA)

                else:
                    image_actual = cv2.rectangle(image_actual, (pos[0], pos[1]),
                                                 (pos[2], pos[3]), (0, 0, 255), 2)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img, str(
                        score_100), (pos[0], pos[1]), font, 1.5, (0, 0, 0), 3, cv2.LINE_AA)
            return image_actual

        def show_process_image():
            if self.cam_main.isOpened():
                check, self.Frame_raw = self.cam_main.read()
                # print("check1: ", check)
                if check:
                    self.Frame = self.Frame_raw.copy()
                    image_croped = draw_crop_func(
                        self.Frame)

                    image_croped = cv2.resize(image_croped, (640, 480))
                    resize = cv2.cvtColor(image_croped, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(resize)
                    iago = ImageTk.PhotoImage(image)
                    self.show_image.configure(image=iago)
                    self.show_image.image = iago
                else:
                    self.cam_main = cv2.VideoCapture(0)
                    self.cam_main.set(cv2.CAP_PROP_AUTOFOCUS, 1)
                    # check, self.Frame_raw = self.cam_main.read()
                    print("cam read is:", check)
                    pass
            else:
                print("cam open is :", self.cam_main.isOpened())
                # self.master.update()
                self.cam_main = cv2.VideoCapture(0)
                self.cam_main.set(cv2.CAP_PROP_AUTOFOCUS, 1)

        show_process_image()
        self.master_op.after(10, self.Loop)

    def read_json_file(self):
        with open('NewData.json') as f:
            self.readjson = json.load(f)
        print("JSON FILE: ", self.readjson)
        return

    def EXIT_operation(self):
        self.master_op.destroy()
