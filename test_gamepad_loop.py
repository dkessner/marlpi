#!/usr/bin/env python

from evdev import InputDevice, categorize, ecodes

#gamepad = InputDevice('/dev/input/event2')
gamepad = InputDevice('/dev/input/by-id/usb-Logitech_Logitech_Cordless_RumblePad_2-event-joystick')
# gamepad = InputDevice('/dev/input/by-id/usb-Logitech_Wireless_Gamepad_F710_BAB49F2A-event-joystick')

for event in gamepad.read_loop():
    print(event)
    if event.type == ecodes.EV_KEY:
        print(categorize(event), "(EV_KEY)")

