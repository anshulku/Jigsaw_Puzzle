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

# Read image
root = Tk()
root.title("jigsaw")
root.geometry("600x600")
filename = filedialog.askopenfilename( filetypes = ( ("testing files", "*.*"), ("All Files","*.*") ) )

im = cv2.imread(filename,0)
##removing noise
im1 = cv2.imread(filename)
dst = cv2.fastNlMeansDenoisingColored(im1,None,15,20,7,5)
im2 = cv2.cvtColor(dst,cv2.COLOR_RGB2GRAY)

#threshold testing 
ret, timg = cv2.threshold(im2,230,255,cv2.THRESH_BINARY)

imgage = cv2.imread(filename,0)
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, timg = cv2.threshold(gray,230,255,cv2.THRESH_BINARY_INV)
timg2 = cv2.adaptiveThreshold(timg,230,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
timg3 = cv2.adaptiveThreshold(timg,230,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)



im2Pi, contoursPi, hierarchyPi = cv2.findContours(timg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
h, w = timg.shape[:2]
vis = np.zeros((h, w, 3), np.uint8)
cv2.drawContours( vis, contoursPi, -1, (128,255,255), -1)

ret, fthreshPie = cv2.threshold(vis, 0, 255, cv2.THRESH_BINARY_INV)
gryPiec = cv2.cvtColor(fthreshPie,cv2.COLOR_RGB2GRAY)
timg3 = cv2.adaptiveThreshold(gryPiec,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

cv2.imshow('threshold ',fthreshPie)



#dectecting corner in haris dectection way
gray = np.float32(timg3)
dst = cv2.cornerHarris(gray,3,3,0.05)

#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)




# Threshold for an optimal value, it may vary depending on the image.
im1[dst>0.1*dst.max()]=[0,0,255]
##print(dst[0][0]>0.5*dst.max())
#height, width, channels = im1.shape
#for y in range(0, height):
# for x in range(0, width):
#    if(dst[y][x]>0.5*dst.max()):
#        cv2.circle(im1,(x,y), 3, (127,255,0), 0)

cv2.imshow('corner dectection',im1)
#cv2.imshow('H timg3',timg3)






#corners = cv2.goodFeaturesToTrack(timg3,25,0.01,10)
#corners = np.int0(corners)
#print(corners)
#for i in corners:
#    x,y = i.ravel()
#    cv2.circle(img,(x,y),10,10,0)

#plt.imshow(img),plt.show()

#gray = np.float32(gray)
#dst = cv2.cornerHarris(gray,2,3,0.1,3)

###result is dilated for marking the corners, not important
#dst = cv2.dilate(dst,None)

### Threshold for an optimal value, it may vary depending on the image.
#img[dst>0.01*dst.max()]=[127,255,0]

#cv2.imshow('dst',img)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()


## Setup SimpleBlobDetector parameters.
#params = cv2.SimpleBlobDetector_Params()

## Change thresholds
#params.minThreshold = 230
#params.maxThreshold = 255


## Filter by Area.
#params.filterByArea = False
#params.minArea = 1500

## Filter by Circularity
#params.filterByCircularity = False
#params.minCircularity = 0.1

## Filter by Convexity
#params.filterByConvexity = False
#params.minConvexity = 0.87

## Filter by Inertia
#params.filterByInertia = True
#params.minInertiaRatio = 0.01

## Create a detector with the parameters
#detector = cv2.SimpleBlobDetector_create(params)


## Detect blobs.
#keypoints = detector.detect(timg)

## Draw detected blobs as red circles.
## cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
## the size of the circle corresponds to the size of blob

#im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#for keyPoint in keypoints:
#    x = keyPoint.pt[0]
#    y = keyPoint.pt[1]
#    s = keyPoint.size
#    print(x," , ",y," ,",s)


## Show blobs
#cv2.imshow("Keypoints", im_with_keypoints)
#cv2.waitKey(0)