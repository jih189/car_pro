import numpy as np
import RPi.GPIO as GPIO
import car_dir
import motor
import distance_detect
from time import *
import cv2 

def drive( stops ):
    # setup all devices and initialize values
    busnum = 1 
    car_dir.setup(busnum=busnum)
    motor.setup(busnum=busnum)
    distance_detect.setup()
    car_dir.home()
    motor.setSpeed(23)

    video_capture = cv2.VideoCapture(-1)
    video_capture.set(3, 160)
    video_capture.set(4, 120)
    command = 0
    stopCount = 0
    stopFound = 0
    
    #drive until passed certain amount of stops
    while True:
        # capture video frames
        ret, frame = video_capture.read()

        # set color masking boundaries for red and mask image
        colorLower = np.array( [0,0,100], dtype='uint8' )
        colorUpper = np.array( [50,50,255], dtype='uint8' )
        colorMask = cv2.inRange( frame, colorLower, colorUpper )
        outMask   = cv2.bitwise_and( frame, frame, mask = colorMask )

        # create mask image, convert to grayscale, and blur 
        clonedImg = outMask.copy()
        clonedImg = cv2.cvtColor( clonedImg, cv2.COLOR_BGR2GRAY)
        clonedImg = cv2.GaussianBlur(clonedImg,(5,5),0)

        # show current image
        cv2.namedWindow( 'Gray color select', cv2.WINDOW_NORMAL )
        cv2.imshow('Gray color select',clonedImg)

        # set whenever a red area has been recognized and passed a stop
        if cv2.countNonZero( clonedImg ) and stopFound == 0:
            stopFound = 1
        elif cv2.countNonZero( clonedImg ) == 0 and stopFound == 1:
            stopFound = 0
            stopCount += 1
        else:
            pass
            
        # crop the image
        crop_img = frame[60:120, 0:160]

        # convert to grayscale
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

        # gaussian blur
        blur = cv2.GaussianBlur(gray,(5,5),0)

        # color thresholding
        ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

        # find the contours of the frame
        contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

        # detect distance to closes object
        dis = distance_detect.checkdis()
        print "distance: ", dis

        # find the biggest contour (if detected)
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
 
        # display the resulting frame
        cv2.namedWindow( 'frame', cv2.WINDOW_NORMAL )
        cv2.imshow('frame',crop_img)

        # exit condition after passing certain amount of stops or 'q' is pressed
        if stopCount == stops or ( cv2.waitKey(1) & 0xFF == ord('q') ):
            # clean up
            motor.stop()
	    distance_detect.cleanup()
            cv2.destroyAllWindows()
            break
