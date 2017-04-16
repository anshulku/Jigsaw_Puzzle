import cv2
import numpy as np;

# read the image throught an window frame 
#imports for that
from tkinter import *
import generatePuzzle as gen
from tkinter import filedialog
from matplotlib import pyplot as plt

# Read image
root = Tk()
root.title("jigsaw")
root.geometry("600x600")
filename = filedialog.askopenfilename( filetypes = ( ("testing files", "*.*"), ("All Files","*.*") ) )

img = cv2.imread(filename)
imggry2 = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
ret, thresh = cv2.threshold(imggry2,230,255, cv2.THRESH_BINARY_INV)
im2, contours, hierarchy = cv2.findContours(thresh, 1, 2)


for var in contours:
    epsilon = 0.1*cv2.arcLength(var,True)
    approx = cv2.approxPolyDP(var,epsilon,True)
    for var in approx:
        cv2.circle(img,(var[0][0],var[0][1]), 3, (0,255,0), 1)
cv2.imshow("kvmsomv",img)





























#dst = cv2.fastNlMeansDenoisingColored(img,None,10,20,7,5)
#gryPiec = cv2.cvtColor(dst,cv2.COLOR_RGB2GRAY)

#ret, threshPie = cv2.threshold(gryPiec, 230, 255, cv2.THRESH_BINARY_INV)
#im2Pi, contoursPi, hierarchyPi = cv2.findContours(threshPie, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
#h, w = threshPie.shape[:2]
#vis = np.zeros((h, w, 3), np.uint8)
#cv2.drawContours( vis, contoursPi, -1, (128,255,255), -1)
#ret, fthreshPie = cv2.threshold(vis, 0, 255, cv2.THRESH_BINARY_INV)
#gryPiec2 = cv2.cvtColor(fthreshPie,cv2.COLOR_RGB2GRAY)
#timg3 = cv2.adaptiveThreshold(gryPiec2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)



#edges = cv2.Canny(timg3,230,255,apertureSize = 5)
#cv2.imshow("edge image", timg3);
#cv2.imshow("edge using", edges);
#minLineLength = 4
#maxLineGap = 0

#lines = cv2.HoughLinesP(timg3,1,np.pi/180,minLineLength,maxLineGap)
#print(lines)#465.            1.57079637
#imgtest = np.zeros((600,600,3), np.uint8)  
#for r in lines:
#    for t2  in r:
#        #a = np.cos(theta)
#        #b = np.sin(theta)
#        #x0 = a*rho
#        #y0 = b*rho
#        #x1 = int(x0 + 1000*(-b))
#        #y1 = int(y0 + 1000*(a))
#        #x2 = int(x0 - 1000*(-b))
#        #y2 = int(y0 - 1000*(a))
#        #print(t2)
#        x1 = t2[0]
#        y1 = t2[1]
#        x2 = t2[2]
#        y2 = t2[3]
#        #print(x1," : ",y1," and  ",x2," : ",y2)
#        #print(x0," ; ",y0)
#        #print(x1," ; ",y1)
#        ###print(x2," ; ",y2)
#        #cv2.circle(imgtest,(x1,y1), 3, (0,0,255), 0)
#        #cv2.circle(imgtest,(x2,y2), 3, (0,0,255), 0)
#        cv2.circle(img,(x1,y1), 3, (0,0,255), 0)
#        cv2.circle(img,(x2,y2), 3, (0,0,255), 0)
#        cv2.line(imgtest,(x1,y1),(x2,y2), (0,255,0), 1)
#    #cv2.imshow("testing image", imgtest);
#    #cv2.waitKey(0) & 0xff == 27
#cv2.imshow("final image", imgtest)
#cv2.imshow("final edges", edges);
cv2.waitKey(0) & 0xff == 27