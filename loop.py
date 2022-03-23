#!/usr/bin/env python


from __future__ import print_function
from evdev import InputDevice, categorize, ecodes
import RPi.GPIO as GPIO
import time


codePinMap = {1 : 21, 4: 21, 16: 21}


#gamepad = InputDevice('/dev/input/event2')
gamepad = InputDevice('/dev/input/by-id/usb-Logitech_Wireless_Gamepad_F710_BAB49F2A-event-joystick')

# GPIO servo initialization

dutyMin = 3.5
dutyMid = 7.1
dutyMax = 10.5

pwms = {}

def initializePWMs():
    GPIO.setmode(GPIO.BCM)
    for pin in set(codePinMap.values()):
        print("initializing pin", pin)
        GPIO.setup(pin, GPIO.OUT)
        pwm = GPIO.PWM(pin, 50)
        pwm.start(dutyMid)
        pwms[pin] = pwm

initializePWMs()


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

    if abs(duty-dutyMid) < .5:
         duty = dutyMid
    if duty <= dutyMin: duty = dutyMin
    if duty >= dutyMax: duty = dutyMax

    #print("abs event:", event.code, event.value, eventMin, eventMax, duty)
    return duty



def cleanup():
    for pwm in pwms:
        print("Cleaning up")
        pwm.ChangeDutyCycle(midpoint)
        pwm.stop()
    GPIO.cleanup()


def main():
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

