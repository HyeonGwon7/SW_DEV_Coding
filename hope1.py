import RPi.GPIO as GPIO
from picamera.array import PiRGBArray
from picamera import PiCamera
from motor_control import AlphaBot2
import math
import time
import cv2
import numpy as np
import os, sys

camera = PiCamera()
camera.resolution = (480,320)
camera.framerate = 40
rawCapture = PiRGBArray(camera, size = (480,320))
time.sleep(0.1)

DR = 16
DL = 19

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

Ab=AlphaBot2()
#Ab.forward()

def grayscale(image):
        return cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

def canny(image,low_thd,high_thd):
        return cv2.Canny(image,low_thd,high_thd,apertureSize=5)

def gaussian_blur(image,kernel_size):
        return cv2.GaussianBlur(image,(kernel_size,kernel_size),0)

def region_of_interest(image, vertices, color3=(255,255,25), color1 = 255):
        mask = np.zeros_like(image)
        if len(image.shape)>2:
                color = color3
        else:
                color = color1
        cv2.fillPoly(mask,vertices,color)
        ROI_image = cv2.bitwise_and(image,mask)
        return ROI_image

#def draw_lines(image, lines, color=[255,0,0], thickness=2):
#        for line in lines:
#        	for x1,y1,x2,y2 in line:
#        		cv2.line(image, (x1,y1),(x2,y2),color,thickness)

def draw_fit_line(image, lines, color=[255,0,0], thickness=10):
        cv2.line(image,(lines[0],lines[1]), (lines[2],lines[3]), color, thickness)

def hough_lines(image,rho,theta,threshold,min_line_len,max_line_gap):
        lines = cv2.HoughLinesP(image,rho,theta,threshold,np.array([]),minLineLength=min_line_len,maxLineGap = max_line_gap)
        return lines

def weighted_img(image,initial_img,a=1,b=1.,r=0.):
        return cv2.addWeighted(initial_img,a,image,b,r)

def get_fitline(image,f_lines):
        lines = np.squeeze(f_lines)
	print("re")
        lines = lines.reshape(lines.shape[0]*2,2)
#	print(type(lines))
#	print(lines)
#	if lines != lines or lines == lines:
#		result = []
#		return result
        rows,cols = image.shape[:2]
        output = cv2.fitLine(lines,cv2.DIST_L2,0,0.01,0.01)
        vx,vy,x,y = output[0],output[1],output[2],output[3]
        x1,y1 = int(((image.shape[0]-1)-y)/vy*vx + x), image.shape[0]-1
        x2,y2 = int(((image.shape[0]/2+100)-y)/vy*vx+x), int(image.shape[0]/2+100)
        result = [x1,y1,x2,y2]
        return result


for frame in camera.capture_continuous(rawCapture, format = 'bgr',use_video_port = True):
	DR_status = GPIO.input(DR)
	DL_status = GPIO.input(DL)
	
	print(DR_status,DL_status)
	if((DL_status == 0) or (DR_status == 0)):
		Ab.stop()
		print("object")
	else:
#		Ab.forward()
		print("forward")

	image = frame.array
	key = cv2.waitKey(1)&0xff
        rawCapture.truncate(0)
        if key==27:
                break
	height,width = 480,320
	gray_image = grayscale(image)
	print("gray")
	print(gray_image)

	blur = gaussian_blur(gray_image,3)
	print("blur")
	print(blur)

	canny_image = canny(blur, 600, 800)
	print("canny")
	print(canny_image)

	ROI = canny_image[160:,:]
	print("ROI")
	print(ROI)	
	



#	vertices = np.array([[(50,height),(width/2-45,height/2+60),(width/2+45,height/2+60),(width-50,height)]],dtype=np.int32)
#	print("vertices")
#	print(vertices)
#	ROI_image = region_of_interest(canny_image, vertices)
#	print("ROI_image")
#	print(ROI_image)
#ROI_image
#	line_arr = hough_lines(ROI, 1, 1*np.pi/180,30,10,20)
	line_arr = hough_lines(ROI, 1, 1*np.pi/180,10,70,10)
	print("line_arr")
	print(line_arr)
#        if line_arr is not None:
#                a,b,c = line_arr.shape
#                for i in range(a):
#                        cv2.line(ROI, (line_arr[i][0][0], line_arr[i][0][1]), (line_arr[i][0][2],line_arr[i][0][3]),(255,0,0),2,cv2.LINE_AA)
#        else:
#                print("non")
#                pass



	
	line_arr = np.squeeze(line_arr)
	print("line_arr sq")
	print(line_arr)
	slope_degree = (np.arctan2(line_arr[:, 1]-line_arr[:, 3],line_arr[:, 0]-line_arr[:, 2])*180)/np.pi
	#slope_degree = (np.arctan2(line_arr[:]-line_arr[:],line_arr[:]-line_arr[:])*180)/np.pi

	line_arr = line_arr[np.abs(slope_degree)<160]
	slope_degree = slope_degree[np.abs(slope_degree)<160]

	line_arr = line_arr[np.abs(slope_degree)>75]
	slope_degree = slope_degree[np.abs(slope_degree)>75]

	L_lines, R_lines = line_arr[(slope_degree>0),:], line_arr[(slope_degree<0),:]
	temp = np.zeros((image.shape[0], image.shape[1],3), dtype = np.uint8)
	L_lines, R_lines = L_lines[:,None],R_lines[:,None]
	print("lfl")
	left_fit_line = get_fitline(image,L_lines)
	print("lfl result")
	print(left_fit_line)
	print("rfl")
	right_fit_line = get_fitline(image,R_lines)

	draw_fit_line(temp, left_fit_line)
	draw_fit_line(temp, right_fit_line)
	
#	result = weighted_img(line_arr, image)
	

	cv2.imshow('r',line_arr)
#	cv2.imshow('r',ROI)
#	cv2.imshow('r',line_arr)
#	cv2.waitKey(0)

