from evdev import InputDevice, categorize, ecodes
import requests
import json
import RPi.GPIO as gpio
import time
import sys

# Sets Gate ID based on program args defaults to Gate 1
if len(sys.argv) > 1:
    gateID = sys.argv[1]
else:
    gateID = "1"
    print("Gate ID default to 1")
print("Gate " + gateID + " is ready")
print()

red = 27
green = 17
door = 22

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

gpio.setup(green, gpio.OUT) # Green LED on pin 17
gpio.setup(red, gpio.OUT) # Red LED on pin 27
gpio.setup(door, gpio.OUT) # Door Control on pin 22

gpio.output(green, gpio.LOW) # Init green to off
gpio.output(red, gpio.HIGH) # Init red to on
gpio.output(door, gpio.LOW) # Init door control to off (locked)

# The RFID Reader emulates a usb keyboard, the following code listens and records the inputed keys until "E" (the end symbol) is entered

device = InputDevice("/dev/input/event0") # Grabs instance of RFID Reader
rfid = []
for event in device.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.value == 1:
            key = ecodes.KEY[event.code]
            num = key[4]
            if num != "E":
                rfid.append(num)
            else:
                rfidstring = "".join(rfid)
                if rfidstring != "":
                    print(rfidstring)
                    url="https://kix7tx694g.execute-api.us-east-1.amazonaws.com/dev/authenticate/" + rfidstring #+ "/" + gateID
                    print(url)
                    response = requests.get(url)
                    print(response.text) #TEXT/HTML
                    print()
                    if response.text == "{\"status\":true}":
                        gpio.output(red, gpio.LOW)  # Red LED off
                        gpio.output(green, gpio.HIGH) # Green LED on
                        gpio.output(door, gpio.HIGH) # door set to on (unlocked)
                        time.sleep(4)
                        gpio.output(red, gpio.HIGH) # red LED on
                        gpio.output(green, gpio.LOW)  # Green LED off
                        gpio.output(door, gpio.LOW) # door set to off (unlocked)
                    else:
                        gpio.output(red, gpio.LOW) # Red LED flashes on and off multiple times to indicate denied access
                        time.sleep(.25)
                        gpio.output(red, gpio.HIGH)
                        time.sleep(.25)
                        gpio.output(red, gpio.LOW)
                        time.sleep(.25)
                        gpio.output(red, gpio.HIGH)
                        time.sleep(.25)
                        gpio.output(red, gpio.LOW)
                        time.sleep(.25)
                        gpio.output(red, gpio.HIGH)
                rfid = []
