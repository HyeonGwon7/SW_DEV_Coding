
import RPi.GPIO as GPIO
from picamera.array import PiRGBArray
from picamera import PiCamera
from motor_control import AlphaBot2
import math
import time
import cv2
import numpy as np
import sys


camera = PiCamera()
camera.resolution = (480,320)
camera.framerate = 40
rawCapture = PiRGBArray(camera, size = (480,320))
time.sleep(0.1)


if __name__=='__main__':
    
        
    DR=16
    DL=19

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
    GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)
        
    Ab=AlphaBot2()
    Ab.forward()	
    for frame in camera.capture_continuous(rawCapture, format = 'bgr', use_video_port = True):
        
        image = frame.array
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print("g")


        gblur = cv2.GaussianBlur(gray,(3,3),0)
        print("gb")


        edge = cv2.Canny(gblur,150,200,apertureSize=5)
        print("eg")


        lines = cv2.HoughLinesP(edge,1,math.pi/180.0,40,np.array([]),100,3)
            
        print("ln")
        
        if lines is not None:
            a,b,c = lines.shape
            
            for i in range(a):
                cv2.line(image, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2],lines[i][0][3]),(0,255,0),2,cv2.LINE_AA)
        
        else :
            pass
             
        #cv2.imshow('f',image)
        cv2.imshow('frame',image)
                
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2.destroyAllWindows()


		

	 #     rawCapture.truncate(0)
	#      if key == 27:
	#	    break
#	print("aaaa")
#	Ab.stop()
#	time.sleep(10)






