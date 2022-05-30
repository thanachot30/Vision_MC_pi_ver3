# import cv2
# import numpy as np
# cropping = False
# x_start, y_start, x_end, y_end = 0, 0, 0, 0
# image = cv2.imread(
#     'D:\p_ARM\ANTROBOTICS_VISION_MC_SMALL_3\Vision_mc_ver3\logo-removebg-preview.png')
# oriImage = image.copy()


# def mouse_crop(event, x, y, flags, param):
#     # grab references to the global variables
#     global x_start, y_start, x_end, y_end, cropping
#     # if the left mouse button was DOWN, start RECORDING
#     # (x, y) coordinates and indicate that cropping is being
#     if event == cv2.EVENT_LBUTTONDOWN:
#         x_start, y_start, x_end, y_end = x, y, x, y
#         cropping = True
#     # Mouse is Moving
#     elif event == cv2.EVENT_MOUSEMOVE:
#         if cropping == True:
#             x_end, y_end = x, y
#     # if the left mouse button was released
#     elif event == cv2.EVENT_LBUTTONUP:
#         # record the ending (x, y) coordinates
#         x_end, y_end = x, y
#         cropping = False  # cropping is finished
#         refPoint = [(x_start, y_start), (x_end, y_end)]
#         if len(refPoint) == 2:  # when two points were found
#             roi = oriImage[refPoint[0][1]:refPoint[1]
#                            [1], refPoint[0][0]:refPoint[1][0]]
#             cv2.imshow("Cropped", roi)


# cv2.namedWindow("image")
# cv2.setMouseCallback("image", mouse_crop)
# while True:
#     i = image.copy()
#     if not cropping:
#         cv2.imshow("image", image)
#     elif cropping:
#         cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
#         cv2.imshow("image", i)
#     cv2.waitKey(1)
# # close all open windows
# cv2.destroyAllWindows()
import cv2
import time

# Resizes a image and maintains aspect ratio


def maintain_aspect_ratio_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # Grab the image size and initialize dimensions
    dim = None
    (h, w) = image.shape[:2]

    # Return original image if no need to resize
    if width is None and height is None:
        return image

    # We are resizing height if width is none
    if width is None:
        # Calculate the ratio of the height and construct the dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    # We are resizing width if height is none
    else:
        # Calculate the ratio of the 0idth and construct the dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # Return the resized image
    return cv2.resize(image, dim, interpolation=inter)


def main(args):

    CAMERA_PORT = 0

    IMAGEWIDTH = 3840
    IMAGEHEIGHT = 2160

    # Propriedades de configuracao da camera
    # 3 = width da camera, 4 = height da camera
    CAMERA_PROP_WIDTH = 3
    CAMERA_PROP_HEIGHT = 4

    camera = cv2.VideoCapture(CAMERA_PORT)
    camera.set(CAMERA_PROP_WIDTH, IMAGEWIDTH)
    camera.set(CAMERA_PROP_HEIGHT, IMAGEHEIGHT)

    imagePath = "D:/p_ARM\ANTROBOTICS_VISION_MC_SMALL_3/Vision_mc_ver3/data_new_model/test_save/image.jpg"

    while(True):

        retval, image = camera.read()
        cv2.imshow('Foto', image)

        k = cv2.waitKey(100)

        if k == 27:
            break

        elif k == ord('s'):
            image = maintain_aspect_ratio_resize(image, width=640)
            cv2.imwrite(imagePath, image)
            break

    cv2.destroyAllWindows()
    camera.release()
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
