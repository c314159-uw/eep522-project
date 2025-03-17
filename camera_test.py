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
mask = cv2.inRange(hsv, (0,70,60), (80,255,255))

# print(im[:3, :3])

# cv2.rectangle(im, (200, 200), (250, 250), (0,255,0,30), 5)

# cv2.imwrite("base.png", im)
# cv2.imwrite("mask.png", mask)
cv2.imwrite("ballcolortest.png", im)