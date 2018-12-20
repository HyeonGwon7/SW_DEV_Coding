import RPi.GPIO as GPIO
from AlphaBot2 import AlphaBot2
from ObstacleDetection  import ObstacleDetection
import time

autoOb = ObstacleDetection
Ab = AlphaBot2()

DR = 16
DL = 19

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

class CarControl:
	slope = 0
	def autoDriving(self,slope,check) :
		if check == 0:
			if(slope > 84  and slope < 98):
				Ab.forward()
				print("Forward")

			elif slope > 98 :
				print("Turn Right")
				Ab.right()
				time.sleep(0.5) 
        
			elif slope < 84 :
				print("Turn LEFT")
				Ab.left()
				time.sleep(0.5)

			else:
				print("STOP")
				Ab.stop()
		elif check == 1:
			DR_status = GPIO.input(DR)
                        DL_status = GPIO.input(DL)
			if((DL_status == 0) or (DR_status==0)):
				print("Detecting Obstacle")
                                Ab.stop()
			else:
                        	if(slope > 84  and slope < 98):
                                	Ab.forward()
                                	print("Forward")

                        	elif slope > 98 :
                                	print("Turn Right")
                                	Ab.right()
                                	time.sleep(0.5) 

                        	elif slope < 84 :
                                	print("Turn LEFT")
                                	Ab.left()
                                	time.sleep(0.5)

                        	else:
                                	print("STOP")
                                	Ab.stop()
