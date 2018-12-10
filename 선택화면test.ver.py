import numpy as np
import cv2 as cv

width = 960
height = 540
bpp = 3

img2 = np.zeros((height, width, bpp), np.uint8)

img_h = img2.shape[0]
img_w = img2.shape[1]
img_bpp = img2.shape[2]

print(img_h, img_w, img_bpp)


red = (0, 0, 255)
green = (0, 255, 0)
blue = (255, 0, 0)
white = (255, 255, 255)
yellow = (0, 255, 255)
cyan = (255, 255, 0)
magenta = (255, 0, 255)




thickness = 2 

org = ((int)(img_w / 2) - 200, (int)(img_h / 2) - 100)
font = cv.FONT_HERSHEY_COMPLEX  # hand-writing style font
fontScale = 3.0
cv.putText(img2, 'Choding JoongDing Goding Coding', (180,100), font, fontScale, yellow, thickness, cv.LINE_AA)



org = ((int)(img_w / 2) - 150, (int)(img_h / 2) + 20)
font = cv.FONT_ITALIC  # italic font
fontScale = 1.5
cv.putText(img2, 'Test1', (300,270), font, fontScale, red, thickness, cv.LINE_AA)



org = ((int)(img_w / 2) - 250, (int)(img_h / 2) + 100)
font = cv.FONT_HERSHEY_SIMPLEX  # normal size sans-serif font
fontScale = 1.5
cv.putText(img2, 'Test2', (300,370), font, fontScale, blue, thickness, cv.LINE_AA)



org = ((int)(img_w / 2) - 130, (int)(img_h / 2) + 150)
ont = cv.FONT_HERSHEY_COMPLEX  # normal size serif font
fontScale = 1.5
cv.putText(img2, 'Test3', (300,470),font, fontScale, green, thickness, cv.LINE_AA)




cv.imshow("drawing", img2)
cv.waitKey(0);
