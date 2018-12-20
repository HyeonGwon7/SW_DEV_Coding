import numpy as np
import cv2 as cv

width = 960
height = 540
bpp = 3

red = (0, 0, 255)
green = (0, 255, 0)
blue = (255, 0, 0)
white = (255, 255, 255)
yellow = (0, 255, 255)
cyan = (255, 255, 0)
magenta = (255, 0, 255)




class ModeView:
    def displayMenu(self,img2):
        thickness = 2 

        font = cv.FONT_HERSHEY_COMPLEX  
        fontScale = 2.0
        cv.putText(img2, 'Team CJGCoding CAR', (125,150), font, fontScale, yellow, thickness, cv.LINE_AA)



        font = cv.FONT_HERSHEY_COMPLEX  
        fontScale = 1.0
        cv.putText(img2, 'Camera Mode', (350,280), font, fontScale, red, thickness, cv.LINE_AA)
    


        font = cv.FONT_HERSHEY_COMPLEX  
        fontScale = 1.0
        cv.putText(img2, 'Obstacle Mode', (350,350), font, fontScale, blue, thickness, cv.LINE_AA)



        font = cv.FONT_HERSHEY_COMPLEX  
        fontScale = 1.0
        cv.putText(img2, 'Straight Driving Mode', (350,420),font, fontScale, green, thickness, cv.LINE_AA)


        font = cv.FONT_HERSHEY_COMPLEX  
        fontScale = 1.0
        cv.putText(img2, 'Integrated Mode', (350,490),font, fontScale, white, thickness, cv.LINE_AA)

	cv.namedWindow('drawing')
	cv.setMouseCallback('drawing',self.mouse_callback)

	
    def Display_Control(self,m):
        img2 = np.zeros((height, width, bpp), np.uint8)
        img_h = img2.shape[0]
        img_w = img2.shape[1]
        img_bpp = img2.shape[2]
        thickness = 2 
        font = cv.FONT_HERSHEY_COMPLEX  
        fontScale = 2.0
        cv.putText(img2, 'Do you want to Run it', (100,150), font, fontScale, yellow, thickness, cv.LINE_AA)


        font = cv.FONT_HERSHEY_COMPLEX  
        fontScale = 1.3
        cv.putText(img2, 'Yes', (350,350), font, fontScale, red, thickness, cv.LINE_AA)
    

        font = cv.FONT_HERSHEY_COMPLEX  
        fontScale = 1.3
        cv.putText(img2, 'No', (550,350), font, fontScale, blue, thickness, cv.LINE_AA)


    def mouse_callback(self,event, x, y, flags, param):

        if(event == cv.EVENT_LBUTTONUP and (x >= 340 and x < 590) and (y > 255 and y < 280)):
            self.Display_Control(1)
            print("Canny Cammer MODE")
	    
    
        elif(event == cv.EVENT_LBUTTONUP and (x> 340 and x < 600 ) and (y > 330 and y < 350)):
            self.Display_Control(2)
            print("Detecting Obstacle MODE")

        elif(event == cv.EVENT_LBUTTONUP and (x> 340 and x <730 ) and (y > 400 and y <420)):
            self.Display_Control(3)
            print("Straight Driving MODE")

        elif(event == cv.EVENT_LBUTTONUP and (x>340 and x < 640 ) and (y> 470 and y <490)):
            self.Display_Control(4)
            print("Auto Driving MODE")

        if(event == cv.EVENT_LBUTTONUP):
	    print(str(x),str(y))


    def mouse_callback2(self,event,x,y,flags,param):
        if(event == cv.EVENT_LBUTTONUP and (x >= 350 and x < 425 ) and (y > 320 and y < 350)):
	    print("yes")	    
	elif(event == cv.EVENT_LBUTTONUP and(x>=550 and x<610) and (y >325 and y < 350)):	
	    print("No")



