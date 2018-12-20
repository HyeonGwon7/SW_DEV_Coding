import RPi.GPIO as GPIO
import time
from motor_control import AlphaBot2

Ab = AlphaBot2()

DR = 16
DL = 19

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)
class ObstacleDetection:
	def obstacleDetect(self):
		try:
			while True:
				DR_status = GPIO.input(DR)
				DL_status = GPIO.input(DL)
				print(DR_status,DL_status)
				if((DL_status == 0) or (DR_status == 0)):
					print("Detecting Obstacle")
					Ab.stop()
					time.sleep(0.002)
				else:
					Ab.forward()
					print("forward")

		except KeyboardInterrupt:
			GPIO.cleanup();

