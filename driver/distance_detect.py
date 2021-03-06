#!/usr/bin/evn python
import RPi.GPIO as GPIO
import PCA9685 as p
import time

TRIG = 16 
ECHO = 18 

def setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	print "distance measurement in progress"

	GPIO.setup(TRIG, GPIO.OUT)
	GPIO.setup(ECHO, GPIO.IN)

	GPIO.output(TRIG, False)
	print "waiting for sensor to settle"
	time.sleep(2)

def checkdis():
	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)

	while GPIO.input(ECHO)==0:
		pulse_start = time.time()

	while GPIO.input(ECHO)==1:
		pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start

	distance = pulse_duration * 17150
	distance = round(distance, 2)

	return distance

def cleanup():
	GPIO.cleanup()
