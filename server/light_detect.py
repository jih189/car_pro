#!/usr/bin/evn python
import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BOARD)

def checkLight(Cpin):
    reading = 0
    GPIO.setup(Cpin, GPIO.OUT)
    GPIO.output(Cpin, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(Cpin, GPIO.IN)
    if (GPIO.input(Cpin) == GPIO.LOW):
        return False 
    else:
        return True 

while True:
    if checkLight(40):
        print "no cup"
    else:
        print "have cup"
