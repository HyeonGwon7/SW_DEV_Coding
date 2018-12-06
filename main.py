import RPi.GPIO as GPIO
from picamera.array import PiRGBArray
from picamera import PiCamera
import math
import time
import cv2
import numpy as np
import os, sys

camera = PiCamera()
camera.resolution = (960,540)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size = (960,540))
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format = 'bgr',use_video_port = True):
        image = frame.array
        key = cv2.waitKey(1)&0xff
        rawCapture.truncate(0)
        if key==27:
                break


