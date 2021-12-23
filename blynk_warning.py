#!/usr/bin/python3

#************************************#
#Script to run a Blynk prigram

import BlynkLib
from sense_hat import SenseHat
import time

#import the main program
import main

BLYNK_AUTH = 'vhNbxWI_0MjRarIMiY51Cd-SJj2rccgb'

# initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

#initialise SenseHAT
sense = SenseHat()
sense.clear()

# register handler for virtual pin V0 write event
@blynk.on("V0")
def v3_write_handler(value):
    red = (255,0,0)
    buttonValue=value[0]
    print(f'Current button value: {buttonValue}')
    if buttonValue=="1":
       sense.show_message("Time UP!", text_colour = red)  
    else:
        sense.clear()

# register handler for virtual pin V1 write event
@blynk.on("V1")
def v3_write_handler(value):
    red = (255,0,0)
    buttonValue=value[0]
    print(f'Current button value: {buttonValue}')
    if buttonValue=="1":
       sense.show_message("Start!", text_colour = red)  
    else:
        sense.clear()        
while True:
    blynk.run()
    time.sleep(1)