#!/usr/bin/evn python
import RPi.GPIO as GPIO
import time
import os
import sys

# current pin mapped to photo resistor
RESIS_PIN = 40

def checkLight(Cpin):
    # setup necessary board readings
    GPIO.setmode(GPIO.BOARD)
    reading = 0
    GPIO.setup(Cpin, GPIO.OUT)
    GPIO.output(Cpin, GPIO.LOW)
    time.sleep(0.1)

    # setup input reading and determine if object is present or not
    GPIO.setup(Cpin, GPIO.IN)
    if (GPIO.input(Cpin) == GPIO.LOW):
        return False 
    else:
        return True 

def setup():
    # continue to display message until cup has been placed
    while checkLight( RESIS_PIN ):
        raw_input( "Cups have not been placed!! Press return to retry..." )

def dropoff():
    print "Awaiting customer pick up..."

    # wait until cup has been removed
    while not checkLight( RESIS_PIN ):
        pass
    
    print "Customer has picked up order!! Heading back home..."
    time.sleep( 1.5 )
        
