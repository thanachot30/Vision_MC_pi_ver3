
import cv2
from matplotlib.pyplot import grid, text
from PIL import Image, ImageChops, ImageOps
import math
import numpy as np
import tensorflow as tf
from tkinter import *               #
from tkinter import ttk
from PIL import Image, ImageTk      #

# import class dependency
import time
import json

from os import listdir


class Operation:
    def __init__(self, master):
        self.master_op = master
        self.master_op.title("Operation page auto")
        # size of windown and position start
        self.master_op.geometry("1280x720+0+0")
        self.frame1 = Frame(self.master_op)
        self.frame1.place(x=0, y=150)

        self.frame_bar = Frame(self.master_op)
        self.frame_bar.place(x=700, y=100)

        self.show_image = Label(self.frame1, width=640, height=480)
        self.show_image.pack()
        self.readjson = {}
        self.model_dict = {}
        self.readjson_processing = {}

        Label(self.master_op, text="PROCESSING", fg="red",
              bg="yellow", font=("Arial", 20)).place(x=200, y=110)
        PB_exit = Button(self.master_op, text="EXIT", fg="red", bg="black", command=self.EXIT_operation).place(
            x=1000, y=600, width=100, height=35)
        ######
        # main operation step
        self.read_json_file()
        self.model_init()
        self.show_bar()
        self.cam_main = cv2.VideoCapture(0)
        # self.cam_main.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        self.Loop()

    def model_init(self):
        for ml_list in self.readjson["codi_pos"]:
            data_pos_string = ' '.join(map(str, ml_list))
            parent_dir = "D:/p_ARM/AntVisionSmall_piv3/Vision_MC_pi_ver3/data_save_ml/"
            path_model = parent_dir + data_pos_string + ".h5"
            load_model = tf.keras.models.load_model(path_model)
            self.model_dict[data_pos_string] = load_model
            print("init model: "+str(data_pos_string))

        return

    def rmsdiff(self, im1, im2):
        """Calculates the root mean square error (RSME) between two images"""
        errors = np.asarray(ImageChops.difference(im1, im2)) / 255
        return math.sqrt(np.mean(np.square(errors)))

    def processing_ok_ng(self, image_crop, index_pos, threshold):
        class_names = ["ng", "ok"]
        path_read_image_master = "D:/p_ARM/AntVisionSmall_piv3/Vision_MC_pi_ver3/data_new_processing/"
        #
        image_actual = image_crop
        index = index_pos+1
        threshold_img = threshold
        #
        master_img = Image.open(
            path_read_image_master+"image"+str(index)+".jpg")
        master_img = ImageOps.grayscale(master_img)
        master_img = ImageOps.equalize(master_img, mask=None)
        # master_img.save("/home/pi/Documents/Vision_MC_pi/Vision_MC_pi_ver3/data_new_processing/hist_Master"+str(index)+".jpg")
        # image_actual convert to PIL image"im_pil"==image_actual
        im_pil = Image.fromarray(image_actual)
        im_pil = ImageOps.grayscale(im_pil)
        im_pil = ImageOps.equalize(im_pil, mask=None)
        # im_pil.save("/home/pi/Documents/Vision_MC_pi/Vision_MC_pi_ver3/data_new_processing/hist_actual"+str(index)+".jpg")
        # add rmsdiff root mean sqe error
        result = self.rmsdiff(master_img, im_pil)
        resual = 100 - (result*100)
        return "ok" if resual >= threshold_img else "ng", resual

    def predict_ok_ng(self, image_crop, pos):
        data_pos_string = ' '.join(map(str, pos))
        class_names = ["ng", "ok"]
        batch_size = 32
        img_height = 50
        img_width = 50
        image_actual = image_crop
        model = self.model_dict[data_pos_string]
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
    def draw_crop_func(self, img):
        keep_result = []
        keep_ml = []
        image_actual = img
        # loop for ML
        for index_pos in range(len(self.readjson["codi_pos"])):
            pos = self.readjson["codi_pos"][index_pos]
            croping = image_actual[int(pos[1]):int(
                pos[3]), int(pos[0]):int(pos[2])]
            resize_crop = cv2.resize(croping, (50, 50))
            # save actual image
            cv2.imwrite(r"D:/p_ARM/AntVisionSmall_piv3/Vision_MC_pi_ver3/data_actual_image/{}.jpg".format(
                "pos"+str(index_pos+1)), resize_crop)
            # send to func ML return to (okng,precentage)
            predict_result, score_100 = self.predict_ok_ng(
                resize_crop, pos)

            print(predict_result, score_100)

            if predict_result == "ok":
                image_actual = cv2.rectangle(image_actual, (pos[0], pos[1]),
                                             (pos[2], pos[3]), (0, 255, 0), 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, str(
                    round(score_100, 2)), (pos[0], pos[1]), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
                keep_ml.append("ok")
            else:
                image_actual = cv2.rectangle(image_actual, (pos[0], pos[1]),
                                             (pos[2], pos[3]), (0, 0, 255), 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, str(
                    round(score_100, 2)), (pos[0], pos[1]), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
                keep_ml.append("ng")
        # print("keep ml: ",keep_ml)

        # loop for image processing
        for index in range(len(self.readjson_processing["codi_pos"])):
            pos_pr = self.readjson_processing["codi_pos"][index]
            # index 4 in pos_pr is threshold for ok,ng in iu slidebar adaptive
            pos_threshold = pos_pr[4]
            croping_pr = image_actual[int(pos_pr[1]):int(
                pos_pr[3]), int(pos_pr[0]):int(pos_pr[2])]
            resize_crop_pr = cv2.resize(croping_pr, (50, 50))
            cv2.imwrite(r"D:/p_ARM/AntVisionSmall_piv3/Vision_MC_pi_ver3/data_actual_processing/{}.jpg".format(
                "pos"+str(index+1)), resize_crop_pr)
            # send to processing iamge function
            result_processing, score_pro = self.processing_ok_ng(
                resize_crop_pr, index, pos_threshold)

            if result_processing == "ok":
                image_actual = cv2.rectangle(image_actual, (pos_pr[0], pos_pr[1]),
                                             (pos_pr[2], pos_pr[3]), (0, 255, 0), 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(image_actual, str(
                    round(score_pro, 2)), (pos_pr[0], pos_pr[1]), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
                keep_result.append("ok")
            else:
                image_actual = cv2.rectangle(image_actual, (pos_pr[0], pos_pr[1]),
                                             (pos_pr[2], pos_pr[3]), (0, 0, 255), 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(image_actual, str(
                    round(score_pro, 2)), (pos_pr[0], pos_pr[1]), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
                keep_result.append("ng")
        # print("keep processing: ",keep_result)
        # output GPIO to PLC
        if not(("ng" in keep_ml) or ("ng" in keep_result)):
            pass
        else:
            pass
        return image_actual

    def Loop(self):
        def show_process_image():
            if self.cam_main.isOpened():
                check, self.Frame_raw = self.cam_main.read()
                # print("check1: ", check)
                if check:
                    self.Frame = self.Frame_raw.copy()
                    image_croped = self.draw_crop_func(
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
        # read for NewData.json file
        with open('NewData.json') as f:
            self.readjson = json.load(f)
        print("JSON FILE: ", self.readjson)
        # read for NewDataProcessing.json file

        with open('NewDataProcessing.json') as f_processing:
            self.readjson_processing = json.load(f_processing)
        print("JSON FILE PROCESSING: ", self.readjson_processing)
        return

    def show_bar(self):
        start_row = 2
        list_ml = self.readjson["codi_pos"]
        list_processing = self.readjson_processing["codi_pos"]
        for ml_pos in list_ml:
            tag_ml = Label(self.frame_bar, text=str(ml_pos),
                           fg="black", bg="gray").grid(row=start_row, column=0)
            ml_bar = Scale(self.frame_bar, from_=0, to=100, length=300,
                           orient=HORIZONTAL).grid(row=start_row, column=1)
            # ml_bar.set()
            start_row = start_row + 1
        # add for separate section
        start_row = start_row + 1
        Label(self.frame_bar, text="Processing",
              bg="white").grid(row=start_row, column=0)
        Label(self.frame_bar, text=" ").grid(row=start_row, column=1)

        for process_pos in list_processing:
            start_row = start_row + 1
            tag_process = Button(self.frame_bar, text=process_pos,
                                 fg="black", bg="white").grid(row=start_row, column=0)
            name = str(process_pos)
            self.pro_bar = Scale(
                self.frame_bar, from_=0, to=100, length=300, label=name, orient=HORIZONTAL)
            self.pro_bar.set(process_pos[4])
            self.pro_bar.bind("<ButtonRelease-1>", self.updateValue)

            self.pro_bar.grid(row=start_row, column=1)

    def updateValue(self, event):
        import ast
        w = event.widget
        if isinstance(w, Scale):
            getScale = w.get()
            getScaleLabel = w.cget("label")
            # print(w.get())
            print("slide:", w.cget("label"))
            # change index 4 adjust threshold in self.readjson_processing["codi_pos"]
            # convert string list to int list
            getScaleLabel = ast.literal_eval(getScaleLabel)
            print("getScaleLabel:", getScaleLabel)
            find_index = self.readjson_processing["codi_pos"].index(
                getScaleLabel)
            # print(find_index)
            # next to edit
            listEdit = self.readjson_processing["codi_pos"][find_index]
            listEdit[4] = int(getScale)
            print("listedit: ", listEdit)

        # save json update json file
        with open('NewDataProcessing.json', 'w') as json_file_update:
            # เขียน Python Dict ลงในไฟล์ NewDataProcessing.json
            json.dump(self.readjson_processing, json_file_update)
        # go to read json
        self.read_json_file()
        self.show_bar()
        return

    def EXIT_operation(self):
        self.master_op.destroy()
        self.cam_main.release()
