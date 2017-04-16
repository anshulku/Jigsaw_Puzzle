#!/usr/bin/python

# Standard imports
import cv2
import numpy as np;

# read the image throught an window frame 
#imports for that
from tkinter import *
import generatePuzzle as gen
from tkinter import filedialog
from matplotlib import pyplot as plt
import math
# Read image
root = Tk()
root.title("jigsaw")
root.geometry("600x600")
filename = filedialog.askopenfilename( filetypes = ( ("testing files", "*.*"), ("All Files","*.*") ) )

im = cv2.imread(filename,0)
#removing noise
img = cv2.imread(filename)
dst = cv2.fastNlMeansDenoisingColored(img,None,1,1,10,5)
imggry2 = cv2.cvtColor(dst,cv2.COLOR_RGB2GRAY)
ret, thresh12 = cv2.threshold(imggry2, 230, 255, cv2.THRESH_BINARY_INV)

#cv2.imshow("thresh sup ", thresh12) 

imggry = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)


#finding contour for the binary images
ret, thresh = cv2.threshold(imggry, 230, 255, cv2.THRESH_BINARY_INV)
#cv2.imshow("thresh using", thresh) 
#cv2.imshow('threshold ',thresh)         
#cv2.imshow("removed noise", dst) 

#im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS) was before
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


       

#maxArea = cv2.contourArea(contours[0])
xlow = []
xhigh = []
ylow = []
yhigh = []

#finding the low and high x,y point for each piece in the image
for cnt in range(0, len(contours)):
    
    if(cv2.contourArea(contours[cnt])<=500) :
        continue
    #print(contours[cnt])
    point=contours[cnt]
    #leftmost = tuple(point[point[:,:,0].argmin()][0])
    #rightmost = tuple(point[point[:,:,0].argmax()][0])
    #topmost = tuple(point[point[:,:,1].argmin()][0])
    #bottommost = tuple(point[point[:,:,1].argmax()][0])
    
    #cv2.circle(img,(leftmost), 3, (127,255,0), 0)
    #cv2.circle(img,(rightmost), 3, (0,0,0), 0)
    #cv2.circle(img,(topmost), 3, (67,255,12), -1)
    #cv2.circle(img,(bottommost), 3, (255,255,255), -1)
    #cv2.imshow("DV ", img)
    #b=cv2.waitKey(0) & 0xff == 27 
    txlow = contours[cnt][0][0][0]
    tyhigh = contours[cnt][0][0][1]
    tylow = contours[cnt][0][0][1]
    txhigh = contours[cnt][0][0][0]
    for pt in point:
        if(txlow>pt[0][0]):
            txlow = pt[0][0]
        if(tylow>pt[0][1]):
            tylow = pt[0][1]
        if(txhigh<pt[0][0]):
            txhigh = pt[0][0]
        if(tyhigh<pt[0][1]):
            tyhigh = pt[0][1]
        
       # cv2.circle(img,(pt[0][0],pt[0][1]), 3, (127,255,0), 0)
    #print("low x in it ",txlow)  
    #print("low y in it ",tylow)  
    #print("high x in it ",txhigh)   
    #print("high y in it ",tyhigh)  
    if(txlow == txhigh or txhigh==tyhigh):
        continue
    xlow.append(txlow-2)
    xhigh.append(txhigh+2)
    ylow.append(tylow-2)
    yhigh.append(tyhigh+2)
                
    #cv2.imshow("DV ", img)
    #if cv2.waitKey(0) & 0xff == 27:
    #    continue;
    
    
images = []
#cv2.imshow("as", image[0][0])

#extracting each piece from the image given in teh system
for i in range(0, len(ylow)):
    images.append(img[ylow[i]:yhigh[i],xlow[i]:xhigh[i]])
    
k=0
ster = "Piece "
titles = []
for i in range(0, len(images)):
    tmpim=images[i]
    tmpim2=tmpim.copy()
    dst = cv2.fastNlMeansDenoisingColored(tmpim,None,10,20,7,5)
    gryPiec = cv2.cvtColor(dst,cv2.COLOR_RGB2GRAY)

    ret, threshPie = cv2.threshold(gryPiec, 230, 255, cv2.THRESH_BINARY_INV)
    im2Pi, contoursPi, hierarchyPi = cv2.findContours(threshPie, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
    #h, w = threshPie.shape[:2]
    #vis = np.zeros((h, w, 3), np.uint8)
    #cv2.drawContours( vis, contoursPi, -1, (128,255,255), -1)

    #ret, fthreshPie = cv2.threshold(vis, 0, 255, cv2.THRESH_BINARY_INV)
    #gryPiec = cv2.cvtColor(fthreshPie,cv2.COLOR_RGB2GRAY)
    #timg3 = cv2.adaptiveThreshold(gryPiec,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    imgtest2 = np.zeros((500,500,3), np.uint8)   
    xinital = 0 
    yinital = 0 
    xfinal = 0 
    yfinal = 0 
    for  cntP in range(0, len(contoursPi)):
        point = contoursPi[cntP]
        for pt in range(0, len(point)-1):
            ptPi = point[pt]
            ptPi2 = point[1+pt]
            x = ptPi[0][0]
            y = ptPi[0][1]
            x1= ptPi2[0][0]
            y1= ptPi2[0][1]
            rho = math.atan()
            if(pt==0):
                xinital = x
                yinital = y 
                print(x,"  ,.  ",y)
                print(xinital,"  ,intial.  ",yinital)
            if(pt==len(point)-2):
                xfinal = x1
                yfinal = y1 
                print(x1,"  ,.  ",y1)
                print(xfinal,"  ,final.  ",yfinal)
            cv2.line(imgtest2,(x,y),(x1,y1), (0,255,0), 1)
    cv2.line(imgtest2,(xinital,yinital), (xfinal,yfinal),(0,255,0), 1)
    #for i in range(0,500):
    #    for j in range(0,500):
    #        print(imgtest2[i][j])      
    #cv2.imshow("DV nicht com  2", imgtest2)
    cv2.imshow("testing image", imgtest2);
    if cv2.waitKey(0) & 0xff == 27:
          continue;
    
##############################################################################################################################
#plt.show()







    
#cv2.drawContours(img, contours, -1, (127,255,0), 3)
cv2.imshow("corner detection", img);
cv2.waitKey(0);
