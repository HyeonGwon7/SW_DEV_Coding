import RPi.GPIO as GPIO
from picamera.array import PiRGBArray
from picamera import PiCamera
import math
import time
import cv2
import numpy as np
import os, sys
from LaneDetection import LaneDetection
from CarControl import CarControl
from ObstacleDetection import ObstacleDetection
from ModeView import ModeView

camera = PiCamera()
camera.resolution = (960,540)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size = (960,540))
time.sleep(0.1)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


laneDetection = LaneDetection()
carControl = CarControl()
modeView = ModeView()
obstacleDetection = ObstacleDetection()

backLeft = [0,0,0,0]
backRight = [0,0,0,0]
vp_slope = [-1,backLeft,backRight]

img2 = np.zeros((540, 960, 3), np.uint8)
check = 0
click = 0

def mouse_callback(event, x, y, flags, param):
	global check
	global click
	if(event == cv2.EVENT_LBUTTONUP and (x >= 340 and x < 590) and (y > 255 and y < 280)):
            check = 1
	    click = 1 
            print("Line Detecting Camera MODE")
	    cv2.destroyAllWindows()	
    
        elif(event == cv2.EVENT_LBUTTONUP and (x> 340 and x < 600 ) and (y > 330 and y < 350)):
            check = 2
            print("Detecting Obstacle MODE")
	    cv2.destroyAllWindows()	

        elif(event == cv2.EVENT_LBUTTONUP and (x> 340 and x <730 ) and (y > 400 and y <420)):
            check = 3
            print("Straight Driving MODE")
	    cv2.destroyAllWindows()

        elif(event == cv2.EVENT_LBUTTONUP and (x>340 and x < 640 ) and (y> 470 and y <490)):
            check = 4
            print("Auto Driving MODE")
	    cv2.destroyAllWindows()







modeView.displayMenu(img2)
cv2.namedWindow('drawing')
cv2.setMouseCallback('drawing',mouse_callback)

cv2.imshow("drawing",img2)
cv2.waitKey(0)
 

for frame in camera.capture_continuous(rawCapture, format = 'bgr',use_video_port = True):
        image = frame.array
        key = cv2.waitKey(1)&0xff
        rawCapture.truncate(0)
#        if key==27:
#                break

	if check == 1:
		vp_slope = laneDetection.lineDetection(image,vp_slope[0],backLeft,backRight)
		backLeft = vp_slope[1]
                backRight = vp_slope[2]

		if key == ord('q'):
			break
	elif check == 2:
		obstacleDetection.obstacleDetect()
		if key == ord('q'):
			break
	elif check == 3:
                vp_slope = laneDetection.lineDetection(image,vp_slope[0],backLeft,backRight)
                backLeft = vp_slope[1]
                backRight = vp_slope[2]
                print("vp",vp_slope)
                carControl.autoDriving(vp_slope[0],0)
		if key == ord('q'):
			break

	elif check == 4:
                vp_slope = laneDetection.lineDetection(image,vp_slope[0],backLeft,backRight)
                backLeft = vp_slope[1]
                backRight = vp_slope[2]
                print("vp",vp_slope)
                carControl.autoDriving(vp_slope[0],1)
		if key == ord('q'):
			break

	

