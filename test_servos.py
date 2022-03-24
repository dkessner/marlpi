#!/usr/bin/env python

import sys

import RPi.GPIO as GPIO
import time

servoPIN = 13

def cleanup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)
    GPIO.cleanup()
    sys.exit(0)


GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) 

#p.start(2.5)
p.start(0)

duty = 6.5

try:
    while True:
        print(duty)
        p.ChangeDutyCycle(duty)
        time.sleep(0.5)
        duty += .1
        if duty > 8.5:
            duty = 6.5

except KeyboardInterrupt:
    print("interrupt")
    print("7")
    p.ChangeDutyCycle(7.2)
    p.stop()
    GPIO.cleanup()


print("0")
p.ChangeDutyCycle(7.2)
p.stop()
GPIO.cleanup()

