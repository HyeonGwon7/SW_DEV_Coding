
import cv2
import numpy as np
import os, sys
import math

class LaneDetection(object):
	vp_slope = -1

	def grayscale(self,image):
	        return cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
 
	def canny(self,image,low_thd,high_thd):
        	return cv2.Canny(image,low_thd,high_thd,apertureSize=5)
 
	def gaussianBlur(self,image,kernel_size):
        	return cv2.GaussianBlur(image,(kernel_size,kernel_size),0)
 
	def drawFitline(self,image, lines, color=[0,0,255], thickness=10):
        	cv2.line(image,(lines[0],lines[1]), (lines[2],lines[3]), color, thickness)
 
	def houghLines(self,image,rho,theta,threshold,min_line_len,max_line_gap):
        	lines = cv2.HoughLinesP(image,rho,theta,threshold,np.array([]),minLineLength=min_line_len,maxLineGap = max_line_gap)
        	return lines
 
	def getFitline(self,image,f_lines):
	        lines = np.squeeze(f_lines)
	        lines = lines.reshape(lines.shape[0]*2,2)
	        rows,cols = image.shape[:2]
	        output = cv2.fitLine(lines,cv2.DIST_L2,0,0.01,0.01)
	        vx,vy,x,y = output[0],output[1],output[2],output[3]
	        slope = output[1]/output[0]
	        intercept=output[3]-(slope*output[2])   
	        x1,y1 = int(((image.shape[0]-1)-intercept)/slope),image.shape[0]-1
	        x2,y2 = int(((image.shape[0]-539)-intercept)/slope),image.shape[0]-539
	        result = [x1,y1,x2,y2]
	        return result
 
	def line(self,p1,p2):
	        A = (p1[1] - p2[1])
	        B = (p2[0] - p1[0])
	        C = (p1[0]*p2[1] - p2[0]*p1[1])
	        return A,B,-C
 
	def intersection(self,L1,L2):
	        D = L1[0]*L2[1] - L1[1]*L2[0]
	        Dx = L1[2]*L2[1] - L1[1]*L2[2]
	        Dy = L1[0]*L2[2] - L1[2]*L2[0]
        	if D != 0:
                	x = Dx/D
                	y = Dy/D
                	result = [x,y]
                	return result
        	else:
                	return False

	def lineDetection(self,image,vs,backLeft,backRight):
		global count
		height,width = 960,540
	        ROI = image[200:540,:959]
	        gray_image = self.grayscale(ROI)
	        blur = self.gaussianBlur(gray_image,3)
	        canny_image = self.canny(blur, 600, 800)
	        line_arr = self.houghLines(canny_image, 1, 1*np.pi/180,30,50,20)
	        line_arr = np.squeeze(line_arr)
	        slope_degree = (np.arctan2(line_arr[:, 1]-line_arr[:, 3],line_arr[:, 0]-line_arr[:, 2])*180)/np.pi
	        line_arr = line_arr[np.abs(slope_degree)<160]
	        slope_degree = slope_degree[np.abs(slope_degree)<160]
	        line_arr = line_arr[np.abs(slope_degree)>95]
	        slope_degree = slope_degree[np.abs(slope_degree)>95]
	        L_lines, R_lines = line_arr[(slope_degree>0),:], line_arr[(slope_degree<0),:]
	        temp = np.zeros((image.shape[0], image.shape[1],3), dtype = np.uint8)
	        L_lines, R_lines = L_lines[:,None],R_lines[:,None]
 
	        if L_lines.any(): 
	                if len(L_lines) >= 2 and L_lines[1] != None :
	                        left_fit_line = self.getFitline(ROI,L_lines)
	                        self.drawFitline(ROI, left_fit_line)
		
		else :
			left_fit_line = backLeft
			
 
	        if R_lines.any():
	                if len(R_lines) >= 2 and R_lines[1] != None :
	                        right_fit_line = self.getFitline(ROI,R_lines)
	                        self.drawFitline(ROI,right_fit_line)

		else :
			right_fit_line = backRight

			
	        vp_slope = vs

	        if vp_slope == -1  :    
	                if L_lines.any() and R_lines.any():
				L1 = self.line([left_fit_line[0],left_fit_line[1]],[left_fit_line[2],left_fit_line[3]])
	                        R1 = self.line([right_fit_line[0],right_fit_line[1]],[right_fit_line[2],right_fit_line[3]])
	                        vp = self.intersection(L1,R1)
	                        vp_slope = (np.arctan2(540-vp[1],480-vp[0])*180)/np.pi
	                else : 
				print("err")
	                        vp_slope = np.abs(slope_degree[0])
	        else :

	                  L1 = self.line([left_fit_line[0],left_fit_line[1]],[left_fit_line[2],left_fit_line[3]])
	                  R1 = self.line([right_fit_line[0],right_fit_line[1]],[right_fit_line[2],right_fit_line[3]])
	                  vp = self.intersection(L1,R1)
	                  vp_slope = (np.arctan2(540-vp[1],480-vp[0])*180)/np.pi


		cv2.line(ROI,(480,340),(vp[0],vp[1]),(0,255,0),5)
        	cv2.line(image,(480,540),(480,480),(255,0,0),5)
        	cv2.imshow('r',image)

		ret = [vp_slope,left_fit_line,right_fit_line] 
		return ret
