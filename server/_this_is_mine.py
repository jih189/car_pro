import numpy as np
import RPi.GPIO as GPIO
import car_dir
import motor
import distance_detect
import lightSense
from time import *
import cv2

busnum = 1 
car_dir.setup(busnum=busnum)
motor.setup(busnum=busnum)
distance_detect.setup()
lightSense.setup( False )
car_dir.home()
motor.setSpeed(30)

video_capture = cv2.VideoCapture(-1)
video_capture.set(3, 160)
video_capture.set(4, 120)
command = 0 
stopCount = 0
stopFound = 0

while(True):
    # Capture the frames
    ret, frame = video_capture.read()

    colorLower = np.array( [0,0,100], dtype='uint8' )
    colorUpper = np.array( [50,50,255], dtype='uint8' )
    colorMask = cv2.inRange( frame, colorLower, colorUpper )
    outMask   = cv2.bitwise_and( frame, frame, mask = colorMask )

    clonedImg = outMask.copy()
    clonedImg = cv2.cvtColor( clonedImg, cv2.COLOR_BGR2GRAY)
    clonedImg = cv2.GaussianBlur(clonedImg,(5,5),0)
    
    cv2.namedWindow( 'Gray color select', cv2.WINDOW_NORMAL )
    cv2.imshow('Gray color select',clonedImg)
    
    circles = cv2.HoughCircles( clonedImg, cv2.cv.CV_HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=15, maxRadius=100 )
    if circles != None:
        if stopFound == 0:
            stopCount += 1
            stopFound = 1

        circles = np.uint16( np.around( circles ))

        for i in circles[0, :]:
            cv2.circle( clonedImg, (i[0],i[1]), i[2], (0,255, 0), 2)
            cv2.circle( clonedImg, (i[0],i[1]), 2, (0,255, 0), 3)
    elif (cv2.countNonZero( clonedImg ) == 0):
      stopFound = 0

    cv2.namedWindow( 'Circles', cv2.WINDOW_NORMAL )
    cv2.imshow( 'Circles', clonedImg)

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

    # detect whether there is thing 
    dis = distance_detect.checkdis()
    cupRem = lightSense.checkOccupied()
    print "distance: ", dis

    # Find the biggest contour (if detected)
    if len(contours) > 0 and dis >=15:
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
        if dis < 15:
            print "something blocking me"
            car_dir.home()
            motor.stop()
        else:
            print "I don't see the line"
            car_dir.home()
            motor.backward()
 
    #Display the resulting frame
    cv2.namedWindow( 'frame', cv2.WINDOW_NORMAL )
    cv2.imshow('frame',crop_img)

    if stopCount == 1 or cupRem or ( cv2.waitKey(1) & 0xFF == ord('q') ):
        motor.stop()
	distance_detect.cleanup()
        lightSense.cleanup()
        break
