import RPi.GPIO as GPIO
import time
from motor_control import AlphaBot2

class detecting_obstacle(object):


    def __init__(self,DR=16,DL=19):
	self.DR=DR
	self.DL=DL

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.DR,GPIO.IN,GPIO.PUD_UP)
        GPIO.setup(self.DL,GPIO.IN,GPIO.PUD_UP)

    def printa(self):
        print("obstacle gogogogogo")
        
    def detect_front(self):
        Ab=AlphaBot2()
        
        try:
                DR_status = GPIO.input(self.DR)
                DL_status = GPIO.input(self.DL)
                print(DR_status,DL_status)
                if((DL_status == 0) or (DR_status == 0)):
		    Ab.stop()
		    print("object")
		else:
		    Ab.forward()
		    print("forward")

        except KeyboardInterrupt:
                GPIO.cleanup();

if __name__=='__main__':
        a=detecting_obstacle()
        a.detect_front()
