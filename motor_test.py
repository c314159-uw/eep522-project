import time
import RPi.GPIO as gpio
gpio.setmode(gpio.BCM)

in1 = 17
in2 = 27
en_a = 4

gpio.setup(in1, gpio.OUT)
gpio.setup(in2, gpio.OUT)
gpio.setup(en_a, gpio.OUT)

power_a = gpio.PWM(en_a, 120)  # channel=12 frequency=50Hz
power_a.start(100)

gpio.output(in1, gpio.LOW)
gpio.output(in2, gpio.LOW)

try:
    while True:
        user_input = input()
        
        if user_input == "w":
            gpio.output(in1, gpio.HIGH)
            gpio.output(in2, gpio.LOW)
        elif user_input == "s":
            gpio.output(in1, gpio.LOW)
            gpio.output(in2, gpio.HIGH)

except KeyboardInterrupt:
    pass
power_a.stop()
gpio.cleanup()
print("Exiting gracefully.")