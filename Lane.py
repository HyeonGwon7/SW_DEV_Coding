import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from itertools import chain
from copy import deepcopy
from picamera.array import PiRGBArray
from picamera import PiCamera
from AlphaBot2 import AlphaBot2
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


class Lane(object):	
	CRITICAL_SLOPE_CHANGE = 0.1
    	MOSTLY_HORIZONTAL_SLOPE = 0.4
    	MAX_SLOPE_DIFFERENCE = 0.8
    	MAX_DISTANCE_FROM_LINE = 20
    	BUFFER_FRAMES = 10
    	COLORS = {
    	    'lane_color': (255,0,0),
    	    'region_stable': (0,80,60),
    	    'region_unstable': (255,80,60),
    	    'left_line': (60,40,220),
    	    'right_line': (255,0,255)
    	}

	THICKNESS = 5
    	FIRST_FRAME_LINE_RANGES = {'left_line': range(480),'right_line': range(480,960)}
    
    # A decision matrix for updating a lane line in order to keep it steady.
    # A weighted average of average lane position from buffer and from the current frame.
    # 0.1 * frame position + 0.9 * avg from buffer: in case of unstable lane.
    # 1 * frame position + 0 * buffer: in case of stable lane.
    	DECISION_MAT = [[.1,.9],[1,0]]
    
    	left_line = None
    	right_line = None

	def lines_exist():
        	return all([Lane.left_line, Lane.right_line])
    
    
    	def fit_lane_line(segments):
       	#"""
       	#Lines interpolation using a linear regression.
        #Any order of polynomial can be used, but we limit ourselves with 1st order for now.
	#"""
        	x, y = [], []
    
		for line in segments:
        		if line.candidate:
        	        	x_coords = list(range(line.x1, line.x2, 1))
        	        	y_coords = list(map(line.get_y_coord, x_coords))
        	        	x.extend(x_coords)
        	        	y.extend(y_coords)
                
        # Assisted lane lines detection for the 1st video frame
        # This can be definitely improved
        	if x != [] and not Lane.lines_exist():
        		lane_line = segments[0].lane_line
            		coords = np.array([[x, y] for x,y in zip(x, y)
                        	if x in Lane.FIRST_FRAME_LINE_RANGES[lane_line]])
            		x = coords[:,0]
            		y = coords[:,1]
        	if x != []:
            		poly_coeffs = np.polyfit(x, y, 1)
            		return poly_coeffs, list(zip(x, y))
        	else: return None, None
    
    #staticmethod
    	def update_vanishing_point(left, right):
        	equation = left.coeffs - right.coeffs
        	x = -equation[1] / equation[0]
        	y = np.poly1d(left.coeffs)(x)
        	x, y = map(int, [x, y])
        	left.vanishing_point = [x, y]
        	right.vanishing_point = [x, y]
        
    #staticmethod
    	def purge():
        	Lane.left_line = None
        	Lane.right_line = None
    
    	def __init__(self, segments):
        	#"""
        	#Since lane line can be any order polynomial, I keep all poly coefficients
        	#in an array -- this is mostly for the future.
        	#"""
        	buffer_frames = Lane.BUFFER_FRAMES
        
        	# Lane coefficients from the current image
        	self.current_lane_line_coeffs, self.points = Lane.fit_lane_line(segments)
        
        	if self.current_lane_line_coeffs is None: 
        		raise Exception('Cannot initialize lane. No lines detected.')
        
        	# Buffer for lane line smoothing
        	self.buffer = np.array(buffer_frames * [self.current_lane_line_coeffs])
        
        	# Publicly available coefficients of lane line
        	self.coeffs = self.buffer[0]
        
        	# Stability flag. Set to False if the slope changes too rapidly
        	self.stable = True
        
        	# Hough lines which belong to this lane line
        	self.segments = None
        
        	# List of points which belong to this lane line. Transformed from segments
        	self.points = None
        	
        	# Coordinates for drawing this lane line
        	self.x1, self.x2, self.y1, self.y2 = 0,0,0,0
        
    #property
    	def a(self):
        	#"""
        	#Slope of the lane line. Not intended for higher order polynomials.
        	#"""
        	if len(self.coeffs) > 2: 
            		return Exception("You have a higher order polynomial for Lane, but you treat it as a line.")
        	return self.coeffs[0]
    
    #property
    	def b(self):
        	#"""
        	#Intercept of the lane line. Not intended for higher order polynomials.
        	#"""
        	if len(self.coeffs) > 2: 
            		return Exception("You have a higher order polynomial for Lane, but you treat it as a line.")
        	return self.coeffs[1]
    
    # The main client method for dealing with lane updates
    	def update_lane_line(self, segments):
        	average_buffer = np.average(self.buffer, axis=0)
        	self.coeffs = np.average(self.buffer, axis=0)
        	self.update_current_lane_line_coeffs(segments)
        	weights = Lane.DECISION_MAT[self.stable]
        	current_buffer_coeffs = np.dot(weights, np.vstack([self.current_lane_line_coeffs, average_buffer]))
        	self.buffer = np.insert(self.buffer, 0, current_buffer_coeffs, axis=0)[:-1]
        	self.update_lane_line_coords()
    
    	def update_current_lane_line_coeffs(self, segments):
        	lane_line_coeffs, points = Lane.fit_lane_line(segments)
        	if lane_line_coeffs is None:
            		lane_line_coeffs = np.average(self.buffer, axis=0)
        	if points is not None:
            		self.points = points
        	average_buffer = np.average(self.buffer, axis=0)
        	buffer_slope = average_buffer[0]
        	current_slope = lane_line_coeffs[0]
        	self.current_lane_line_coeffs = lane_line_coeffs
        	if abs(current_slope - buffer_slope) > Lane.CRITICAL_SLOPE_CHANGE:
        	   	 self.stable = False
        	else: self.stable = True
            
    	def update_segments_list(self, segments):
        	self.segments = segments
    
    	def get_x_coord(self, y):
        	return int((y - self.coeffs[1]) / self.coeffs[0])
    
    	def update_lane_line_coords(self):
        	# Offset to distinguish lines
        	visual_offset = 20
        	self.y1 = image.shape[1]
        	self.x1 = self.get_x_coord(self.y1)
        	self.y2 = self.vanishing_point[1] + visual_offset
        	self.x2 = self.get_x_coord(self.y2)
