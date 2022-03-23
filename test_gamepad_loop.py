#!/usr/bin/env python

from evdev import InputDevice, categorize, ecodes

gamepad = InputDevice('/dev/input/event2')

for event in gamepad.read_loop():
    print(event)
    if event.type == ecodes.EV_KEY:
        print(categorize(event), "(EV_KEY)")

