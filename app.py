import RPi.GPIO as GPIO
from picamera2 import Picamera2, Preview
from libcamera import controls
import numpy as np
import time
import cv2

##### GPIO STUFF #####

GPIO.setmode(GPIO.BOARD)
in1 = 5
in2 = 7
en_a = 3

in3 = 11
in4 = 13
en_b = 15


GPIO.setup([en_a, en_b, in1, in2, in3, in4], GPIO.OUT)

power_a = GPIO.PWM(en_a, 120)
power_a.start(0)
power_b = GPIO.PWM(en_b, 120)
power_b.start(0)

def clamp(value, min_, max_):
    return min(max(value, min_), max_)

def deadband(value, threshold):
    if abs(value) < threshold:
        return 0
    return value

def tank_drive(m1, m2):
    # m1 is right, + is backward
    # m2 is left, + is forward
    m1 = deadband(clamp(m1, -1, 1), 0.2)
    m2 = deadband(clamp(m2, -1, 1), 0.2)
    GPIO.output(in1, GPIO.HIGH if m1 > 0 else GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH if m1 < 0 else GPIO.LOW)
    power_a.ChangeDutyCycle(abs(m1)*100)
    GPIO.output(in3, GPIO.HIGH if m2 > 0 else GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH if m2 < 0 else GPIO.LOW)
    power_b.ChangeDutyCycle(abs(m2)*100)
    
##### CAMERA STUFF #####

cv2.startWindowThread()
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
camera.start()

def find_ball(image, color):
    out = image.copy()
    success = False
    cx, cy, a = None, None, None
    
    # a dictionary would be more effective
    if color == "orange":
        low, high = (5, 170, 150), (15, 255, 255)
    else:
        low, high = (35, 170, 150), (50, 255, 255)
        
    low, high = (25, 70, 110), (35, 155, 225)
            
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, low, high)
    element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8,8))
    mask = cv2.erode(mask, element, iterations=3)
    mask = cv2.dilate(mask, element, iterations=3)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        max_c = max(contours, key=cv2.contourArea)
        if (a := cv2.contourArea(max_c)) > 0:
            cv2.drawContours(out, [max_c], 0, (0,255,0, 255), 2)
            M = cv2.moments(max_c)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            success = True
        
    return success, out, (cx, cy), a

def mainloop():
    im = camera.capture_array()
    success, overlay, center, area = find_ball(im, None)
    print(f"{center=} {area=}")
    if success:
        cx, cy = center
        tank_drive((cx-320)/320 - 20/area**0.5, (cx-320)/320 + 20/area**0.5)
        # tank_drive(0, 50/area**0.5)
    else:
        tank_drive(0, 0)

try:
    while True:
        mainloop()
except KeyboardInterrupt:
    print("Stopping program.")
    
power_b.stop()
power_a.stop()

GPIO.output([in1,in2,in3,in4,en_b], GPIO.LOW)
GPIO.output(en_a, GPIO.HIGH)
# GPIO.cleanup()
print("Exiting gracefully.")