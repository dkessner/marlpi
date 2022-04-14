#!/usr/bin/env python 

from __future__ import print_function
from evdev import InputDevice, categorize, ecodes
import RPi.GPIO as GPIO
import time
import pigpio

#gamepad = InputDevice('/dev/input/event2')

#gamepad = InputDevice('/dev/input/by-id/usb-Logitech_Wireless_Gamepad_F710_BAB49F2A-event-joystick')
#codePinMap = {4 : 21, 1: 13, 16: 26} # map gamepad code -> GPIO pin

gamepad = InputDevice('/dev/input/by-id/usb-Logitech_Logitech_Cordless_RumblePad_2-event-joystick')
codePinMap = {5 : 21, 1: 13, 16: 26} # map gamepad code -> GPIO pin

pinReversed = {21: True}

pipigpio = pigpio.pi()


def initializePIGPIO():
    print("initializePIGPIO")
    #pipigpio = pigpio.pi()
    print("pipigpio: ", pipigpio)
    for pin in set(codePinMap.values()):
        print("initializing pin", pin)
        pipigpio.set_mode(pin, pigpio.OUTPUT)
        pipigpio.set_PWM_frequency(pin, 50)

def getAbsInfo(code):
    for c, info in gamepad.capabilities()[3]:
        if c == code:
            return info
    return Null


# 1500 == stopped

pw_min = 1000
pw_max = 2000


def translateAbsEventToPulsewidth(event):
    # convert event.value in [eventMin, eventMax] 
    # to duty value in [500, 2500]
    eventMin = float(getAbsInfo(event.code).min)
    eventMax = float(getAbsInfo(event.code).max)
    pulsewidth = float(event.value - eventMin)/(eventMax-eventMin)*(pw_max - pw_min) + pw_min

    pin = codePinMap[event.code]

    if pulsewidth <= pw_min: pulsewidth = pw_min
    if pulsewidth >= pw_max: pulsewidth = pw_max

    if pin in pinReversed and pinReversed[pin]:
        pulsewidth = pw_max + pw_min - pulsewidth

    print("abs event:", event.code, event.value, eventMin, eventMax, pulsewidth)
    return pulsewidth



def cleanup():
    for pin in set(codePinMap.values()):
        pipigpio.set_PWM_dutycycle(pin, 0)
        pipigpio.set_PWM_frequency(pin, 0)
    GPIO.cleanup()


def main():

    initializePIGPIO()

    print("pipigpio: ", pipigpio)

    try:
        for event in gamepad.read_loop():
            if event.type == ecodes.EV_ABS:
                if event.code in codePinMap:
                    pin = codePinMap[event.code]
                    pulsewidth = translateAbsEventToPulsewidth(event)
                    pipigpio.set_servo_pulsewidth(pin, pulsewidth)
                    print("event: ", event.code, pin, pulsewidth)
    except KeyboardInterrupt:
        cleanup()

if __name__ == '__main__':
    main()

