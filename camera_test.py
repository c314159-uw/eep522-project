from picamera2 import Picamera2, Preview
from libcamera import controls
import numpy as np
import time
import cv2

# picam2 = Picamera2()
# camera_config = picam2.create_preview_configuration()
# picam2.configure(camera_config)
# picam2.start_preview(Preview.NULL)
# picam2.start()
# picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
# time.sleep(2)
# metadata = picam2.capture_file("test.png")
# print(metadata)

face_detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
cv2.startWindowThread()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

# time.sleep(2)

im = picam2.capture_array()

hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
# low, high = (35, 70, 120), (50, 155, 255)
low, high = (25, 80, 120), (35, 155, 225)
premask = cv2.inRange(hsv, low, high)

element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8,8))
mask = cv2.erode(premask, element, iterations=5)
mask = cv2.dilate(mask, element, iterations=5)

# print(im[:3, :3])

# cv2.rectangle(im, (200, 200), (250, 250), (0,255,0,30), 5)

# cv2.imwrite("base.png", im)
# cv2.imwrite("mask.png", mask)
cv2.imwrite("ballcolortest.png", im)
cv2.imwrite("ballcolormask.png", premask)
cv2.imwrite("ballcolorpost.png", mask)