#!/usr/bin/env python


from __future__ import print_function
from evdev import InputDevice, categorize, ecodes
import RPi.GPIO as GPIO
import time

#gamepad = InputDevice('/dev/input/event2')
#gamepad = InputDevice('/dev/input/by-id/usb-Logitech_Wireless_Gamepad_F710_BAB49F2A-event-joystick')

gamepad = InputDevice('/dev/input/by-id/usb-Logitech_Logitech_Cordless_RumblePad_2-event-joystick')

codePinMap = {5 : 21, 1: 13, 16: 26} # map gamepad code -> GPIO pin

pinReversed = {21: True}

class ServoInfo:
    def __init__(self, dutyMin = 3.5, dutyMid = 7.2, dutyMax = 10.5):
        self.dutyMin = dutyMin
        self.dutyMid = dutyMid
        self.dutyMax = dutyMax

servoInfoMap = {}
pwms = {}

def initializeServoInfoMap():
    servoInfoMap[21] = ServoInfo(dutyMid=7.3)
    servoInfoMap[13] = ServoInfo()
    servoInfoMap[26] = ServoInfo()

def initializePWMs():
    GPIO.setmode(GPIO.BCM)
    for pin in set(codePinMap.values()):
        print("initializing pin", pin)
        GPIO.setup(pin, GPIO.OUT)
        pwm = GPIO.PWM(pin, 50)
        pwm.start(servoInfoMap[pin].dutyMid)
        pwms[pin] = pwm



def getAbsInfo(code):
    for c, info in gamepad.capabilities()[3]:
        if c == code:
            return info
    return Null


def translateAbsEventToDuty(event):
    # convert event.value in [eventMin, eventMax] 
    # to duty value in [2.5, 12.5]
    eventMin = float(getAbsInfo(event.code).min)
    eventMax = float(getAbsInfo(event.code).max)
    duty = float(event.value - eventMin)/(eventMax-eventMin)*10 + 2.5

    pin = codePinMap[event.code]
    servoInfo = servoInfoMap[pin]

    if abs(duty-servoInfo.dutyMid) < .5:
         duty = servoInfo.dutyMid
    if duty <= servoInfo.dutyMin: duty = servoInfo.dutyMin
    if duty >= servoInfo.dutyMax: duty = servoInfo.dutyMax

    if pin in pinReversed and pinReversed[pin]:
        duty = 14.4 - duty

    print("abs event:", event.code, event.value, eventMin, eventMax, duty)
    return duty



def cleanup():
    for pwm in pwms:
        print("Cleaning up")
        pwm.ChangeDutyCycle(midpoint)
        pwm.stop()
    GPIO.cleanup()


def main():

    initializeServoInfoMap()
    initializePWMs()

    try:
        for event in gamepad.read_loop():
            if event.type == ecodes.EV_ABS:
                if event.code in codePinMap:
                    pin = codePinMap[event.code]
                    duty = translateAbsEventToDuty(event)
                    pwms[pin].ChangeDutyCycle(duty)
                    print("event: ", event.code, pin, duty)
    except KeyboardInterrupt:
        cleanup()

if __name__ == '__main__':
    main()

