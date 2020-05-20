# sentry_gate

This Python program takes the RFID number read by the connected USB RFID reader and sends it to our lambda function using a Sentinel API call. The response is then parsed to determine if the door control should be unlocked.

## How To Use:
`python3 GateControl.py [GateID]` Note: When left blank the Gate ID defaults to 1

## Hardware Requirements:
* Raspberry Pi running Linux (We used Raspbian) 
  * Door Control on Pin 22
  * Green LED on Pin 17 and Red LED on Pin 27 (Both Optional)
* USB RFID Reader (Set to keyboard emulation mode)
* An adapter to convert the 3.3V on/off signal output from the RPi to the required input logic for the door lock control system
  * In our case this was a relay module that completed the circuit  of our control box's unlock signal line.

### Note:
Since every RFID reader is different some adjustments may need to be made to the code. Such as what key the reader uses as it's “end” key, in our case it was the “E” key, and the input device file location (Line 34). 
