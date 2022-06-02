
import cv2
from tkinter import *               #
from PIL import Image, ImageTk      #

import os
from os import listdir                  #
from functools import partial       #
import json
# import for tensorflow
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
##########


class Learning:
    def __init__(self, master):
        self.master_add = master
        # self.oldFram1 = canvas1
        # self.oldFram2 = canvas2
        # self.olfFram3 = canvas3
        self.master_add.title("Learning model")

        print("IN Class learing")
        # init fram1 for use
        self.frame1 = Frame(self.master_add)
        self.frame1.place(x=0, y=150)
        # init fram_ok_ng for PB
        self.fram_ok_ng = Frame(self.master_add)
        self.fram_ok_ng.place(x=1000, y=150)
        # init fram_image_ok_ng for image
        self.fram_img_small = Frame(self.master_add)
        self.fram_img_small.place(x=780, y=150)

        # init pack image on fram1
        self.show_image = Label(self.frame1, width=640, height=480)
        self.show_image.pack()

        PB_ok = Button(self.fram_ok_ng, text="ADD OK", fg="black", bg="#9ACD32", command=self.get_ok
                       ).grid(row=0, column=0, ipadx=20, ipady=10)

        Label(self.fram_ok_ng, text="  ").grid(
            row=1, column=0, ipadx=20, ipady=10)
        Label(self.fram_ok_ng, text="  ").grid(
            row=2, column=0, ipadx=20, ipady=10)
        Label(self.fram_ok_ng, text="  ").grid(
            row=3, column=0, ipadx=20, ipady=10)
        PB_ng = Button(self.fram_ok_ng, text="ADD NG", fg="black", bg="#f47c60", command=self.get_ng
                       ).grid(row=4, column=0, ipadx=20, ipady=10)

        Label(self.fram_ok_ng, text="  ").grid(
            row=5, column=0, ipadx=20, ipady=30)

        PB_learing = Button(self.fram_ok_ng, text="Learning", fg="black", bg="#3287cd",
                            command=self.model_learing).grid(row=6, column=0, ipadx=20, ipady=10)

        self.show_ok_capture = Label(self.fram_img_small)
        self.show_ok_capture.pack()
        self.show_ng_capture = Label(self.fram_img_small)
        self.show_ng_capture.pack()

        self.ReadnewModel_dict = {}

        # init read json file for get position crop
        # Operation step
        self.read_json_file()
        self.mkdir_pos()
        self.cam_learning = cv2.VideoCapture(0)
        self.cam_learning.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        self.show_camera()

    def mkdir_pos(self):
        sub_folder = ["ok", "ng"]
        directory = "pos"
        parent_dir = "/home/pi/Documents/Vision_MC_pi/Vision_MC_pi_ver3/data_new_model/"
        for pos in range(len(self.ReadnewModel_dict["codi_pos"])):
            directory_pos = directory+str(pos+1)
            path = os.path.join(parent_dir, directory_pos)
            os.mkdir(path)
            print("Directory '% s' created" % directory_pos)
        # mkdir subfolder ok,ng
        file_list = listdir(parent_dir)
        for j in file_list:
            print(j)
            para = parent_dir + \
                j + "/"
            for p in sub_folder:
                path_sub = os.path.join(para, p)
                print(p)
                os.mkdir(path_sub)

    def model_learing(self):
        parent_dir = "/home/pi/Documents/Vision_MC_pi/Vision_MC_pi_ver3/data_new_model/"
        file_list = listdir(parent_dir)
        print(file_list)
        for j in file_list:
            print(j)
            para = parent_dir + \
                j + "/"
            print("learning........."+str(j))
            batch_size = 32
            img_height = 50
            img_width = 50
            import pathlib
            data_dir = pathlib.Path(para)
            # Create a dataset
            train_ds = tf.keras.utils.image_dataset_from_directory(
                data_dir,
                validation_split=0.2,
                subset="training",
                seed=123,
                image_size=(img_height, img_width),
                batch_size=batch_size)

            val_ds = tf.keras.utils.image_dataset_from_directory(
                data_dir,
                validation_split=0.2,
                subset="validation",
                seed=123,
                image_size=(img_height, img_width),
                batch_size=batch_size)

            class_names = train_ds.class_names
            print(class_names)

            AUTOTUNE = tf.data.AUTOTUNE
            train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
            val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
            # Standardize the data
            # normalization_layer = layers.Rescaling(1./255)
            # normalized_ds = train_ds.map(
            #     lambda x, y: (normalization_layer(x), y))
            # image_batch, labels_batch = next(iter(normalized_ds))

            data_augmentation = keras.Sequential(
                [
                    layers.RandomFlip("horizontal",
                                      input_shape=(img_height,
                                                   img_width,
                                                   3)),
                    layers.RandomRotation(0.1),
                    layers.RandomZoom(0.1),
                ]
            )
            # visualize what a few augmented examples
            plt.figure(figsize=(10, 10))
            for images, _ in train_ds.take(1):
                for i in range(9):
                    augmented_images = data_augmentation(images)
                    ax = plt.subplot(3, 3, i + 1)
                    plt.imshow(augmented_images[0].numpy().astype("uint8"))
                    plt.axis("off")
            ##################

            # Create the model
            num_classes = len(class_names)
            model = Sequential([
                data_augmentation,
                layers.Rescaling(
                    1./255, input_shape=(img_height, img_width, 3)),
                layers.Conv2D(16, 3, padding='same', activation='relu'),
                layers.MaxPooling2D(),
                layers.Conv2D(32, 3, padding='same', activation='relu'),
                layers.MaxPooling2D(),
                # layers.Conv2D(64, 3, padding='same', activation='relu'),
                # layers.MaxPooling2D(),
                layers.Dropout(0.2),
                layers.Flatten(),
                layers.Dense(128, activation='relu'),
                layers.Dense(num_classes)
            ])
            model.compile(optimizer='adam',
                          loss=tf.keras.losses.SparseCategoricalCrossentropy(
                              from_logits=True),
                          metrics=['accuracy'])
            # Train the model
            epochs = 10
            history = model.fit(
                train_ds,
                validation_data=val_ds,
                epochs=epochs
            )
            # Visualize training results
            acc = history.history['accuracy']
            val_acc = history.history['val_accuracy']

            loss = history.history['loss']
            val_loss = history.history['val_loss']

            epochs_range = range(epochs)

            plt.figure(figsize=(8, 8))
            plt.subplot(1, 2, 1)
            plt.plot(epochs_range, acc, label='Training Accuracy')
            plt.plot(epochs_range, val_acc, label='Validation Accuracy')
            plt.legend(loc='lower right')
            plt.title('Training and Validation Accuracy')

            plt.subplot(1, 2, 2)
            plt.plot(epochs_range, loss, label='Training Loss')
            plt.plot(epochs_range, val_loss, label='Validation Loss')
            plt.legend(loc='upper right')
            plt.title('Training and Validation Loss')
            plt.show()
            save_ml_path = "/home/pi/Documents/Vision_MC_pi/Vision_MC_pi_ver3/data_save_ml/model_" + \
                str(j)+".h5"
            model.save(save_ml_path)
            print("finish save model")
            return

    def read_json_file(self):
        with open('NewData.json') as f:
            self.ReadnewModel_dict = json.load(f)
        print("JSON FILE: ", self.ReadnewModel_dict)

    def croping_image(self, img, state):
        image_actual = img
        # parent_dir = "D:/p_ARM\ANTROBOTICS_VISION_MC_SMALL_3/Vision_mc_ver3/data_new_model/"
        # file_list = listdir(parent_dir)
        for index_pos in range(len(self.ReadnewModel_dict["codi_pos"])):
           # part of crop image
            if state == "ok":
                pos = self.ReadnewModel_dict["codi_pos"][index_pos]
                croping = image_actual[int(pos[1]):int(
                    pos[3]), int(pos[0]):int(pos[2])]
                resize_crop = cv2.resize(croping, (50, 50))
                # part of access file
                path_to_pos = "/home/pi/Documents/Vision_MC_pi/Vision_MC_pi_ver3/data_new_model/pos" + \
                    str(index_pos+1)+"/ok/"
                len_actual_image = len(listdir(path_to_pos))
                path_save_image = path_to_pos+"pos" + \
                    str(index_pos+1)+"_ok"+str(len_actual_image+1)+".jpg"
                print(path_save_image)
                cv2.imwrite(path_save_image, resize_crop)
            elif state == "ng":
                pos = self.ReadnewModel_dict["codi_pos"][index_pos]
                croping = image_actual[int(pos[1]):int(
                    pos[3]), int(pos[0]):int(pos[2])]
                resize_crop = cv2.resize(croping, (50, 50))
                # part of access file
                path_to_pos = "/home/pi/Documents/Vision_MC_pi/Vision_MC_pi_ver3/data_new_model/pos" + \
                    str(index_pos+1)+"/ng/"
                len_actual_image = len(listdir(path_to_pos))
                path_save_image = path_to_pos+"pos" + \
                    str(index_pos+1)+"_ng"+str(len_actual_image+1)+".jpg"
                print(path_save_image)
                cv2.imwrite(path_save_image, resize_crop)
            else:
                print("croping_image imahe lose state")

    def get_ok(self):
        # get image from show_camera loop actual
        print("PB get ok")
        ok_image = self.Frame
        # save and cut croping sub image position and pass argumant is raw image from actual image
        self.croping_image(self.Frame_raw, "ok")
        #
        image = cv2.resize(ok_image, (200, 150))
        resize = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(resize)
        iago = ImageTk.PhotoImage(image)
        self.show_ok_capture.configure(image=iago)
        self.show_ok_capture.image = iago

    def get_ng(self):
        # get image from show_camera loop actual
        print("PB get ng")
        ng_image = self.Frame
        # save and cut croping sub image position and pass argumant is raw image from actual image
        self.croping_image(self.Frame_raw, "ng")

        image = cv2.resize(ng_image, (200, 150))
        resize = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(resize)
        iago = ImageTk.PhotoImage(image)
        self.show_ng_capture.configure(image=iago)
        self.show_ng_capture.image = iago

    def show_camera(self):
        def draw_crop_func(img, dict):
            image = img
            codinate_crop = dict
            for i in codinate_crop:
                image = cv2.rectangle(image, (i[0], i[1]),
                                      (i[2], i[3]), (0, 255, 0), 2)
            return image

        if self.cam_learning.isOpened():
            check, self.Frame_raw = self.cam_learning.read()
            self.Frame = self.Frame_raw.copy()
            # croping image position
            image_croped = draw_crop_func(
                self.Frame, self.ReadnewModel_dict["codi_pos"])
            # image resize
            image_croped = cv2.resize(image_croped, (640, 480))
            resize = cv2.cvtColor(image_croped, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(resize)
            iago = ImageTk.PhotoImage(image)
            self.show_image.configure(image=iago)
            self.show_image.image = iago

        else:
            print("cam is not open:", self.cam_learning.isOpened())

        self.master_add.after(10, self.show_camera)

        # for widget in self.oldFram1.winfo_children():
        #     widget.destroy()
        # for widget in self.oldFram2.winfo_children():
        #     widget.destroy()
        # for widget in self.oldFram3.winfo_children():
        #     widget.destroy()
