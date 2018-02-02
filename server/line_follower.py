import numpy as np
import RPi.GPIO as GPIO
import car_dir
import motor
import distance_detect
from time import *
import cv2

busnum = 1 
car_dir.setup(busnum=busnum)
motor.setup(busnum=busnum)
distance_detect.setup()
car_dir.home()
motor.setSpeed(20)

video_capture = cv2.VideoCapture(-1)

video_capture.set(3, 160)

video_capture.set(4, 120)

command = 0 

while(True):

 

    # Capture the frames

    ret, frame = video_capture.read()

 

    # Crop the image

    crop_img = frame[60:120, 0:160]

 

    # Convert to grayscale

    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

 

    # Gaussian blur

    blur = cv2.GaussianBlur(gray,(5,5),0)

 

    # Color thresholding

    ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

 

    # Find the contours of the frame

    contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

 

    # Find the biggest contour (if detected)

    if len(contours) > 0:

        c = max(contours, key=cv2.contourArea)

        M = cv2.moments(c)

 
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

 

        cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)

        cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

 

        cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)

        if cx >= 120:

            print "Turn Right ", cx
            car_dir.turn_right()
            motor.forward()
 

        if cx < 120 and cx > 50:

            print "On Track! ", cx
            car_dir.home()
            motor.forward()
 

        if cx <= 50:

            print "Turn Left! ", cx
            car_dir.turn_left()
            motor.forward()

    else:

        print "I don't see the line"
        car_dir.home()
        motor.backward()
 

    #Display the resulting frame

    cv2.imshow('frame',crop_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
	distance_detect.cleanup()
        motor.stop()
        break
