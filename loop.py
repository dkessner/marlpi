#!/usr/bin/env python

# marlpi 

from evdev import InputDevice, categorize, ecodes
import RPi.GPIO as GPIO
import time


gamepad = InputDevice('/dev/input/event2')
#gamepad = InputDevice('/dev/input/by-id/usb-Logitech_Wireless_Gamepad_F710_BAB49F2A-event-joystick')

# GPIO servo initialization

servoPIN = 21

dutyMin = 3.5
dutyMid = 7.1
dutyMax = 10.5


GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
pwm = GPIO.PWM(servoPIN, 50)
pwm.start(dutyMid)


def getAbsInfo(code):
    return gamepad.capabilities()[3][code][1]

def translateAbsEventToDuty(event):
    # convert event.value in [eventMin, eventMax] 
    # to duty value in [2.5, 12.5]
    eventMin = float(getAbsInfo(event.code).min)
    eventMax = float(getAbsInfo(event.code).max)
    duty = float(event.value - eventMin)/(eventMax-eventMin)*10 + 2.5

    if abs(duty-dutyMid) < .5:
         duty = dutyMid
    if duty <= dutyMin: duty = dutyMin
    if duty >= dutyMax: duty = dutyMax

    print("abs event:", event.code, event.value, eventMin, eventMax, duty)
    return duty


def main():

    try:
        for event in gamepad.read_loop():
            #print(event)
            if event.type == ecodes.EV_ABS:
                if event.code == 0:
                    duty = translateAbsEventToDuty(event)
                    print("duty returned: ", duty)
                    pwm.ChangeDutyCycle(duty)

    except KeyboardInterrupt:
        print("Cleaning up")
        pwm.ChangeDutyCycle(midpoint)
        pwm.stop()
        GPIO.cleanup()


if __name__ == '__main__':
    main()

