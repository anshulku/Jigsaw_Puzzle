#**********************************************************************************
# traget to achieve
# ** remove noise get the blob fix it and threshold it....
#date 5/11/2016 : 16:58 DV
#**********************************************************************************
#imports
import cv2
import numpy as np;

# read the image throught an window frame 
#imports for that
from tkinter import *
import generatePuzzle as gen
from tkinter import filedialog
from matplotlib import pyplot as plt
 
#getting the file
print("running")
root = Tk()
root.title("jigsaw")
root.geometry("600x600")
filename = filedialog.askopenfilename( filetypes = ( ("testing files", "*.*"), ("All Files","*.*") ) )
im = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

## Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

## Change thresholds
params.minThreshold = 230
params.maxThreshold = 255


## Filter by Area.
params.filterByArea = False
params.minArea = 1500

## Filter by Circularity
params.filterByCircularity = False
params.minCircularity = 0.1

## Filter by Convexity
params.filterByConvexity = False
params.minConvexity = 0.87

## Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01

## Create a detector with the parameters
detector = cv2.SimpleBlobDetector_create(params)


## Detect blobs.
keypoints = detector.detect(im)

## Draw detected blobs as red circles.
## cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
## the size of the circle corresponds to the size of blob

im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
for keyPoint in keypoints:
    x = keyPoint.pt[0]
    y = keyPoint.pt[1]
    s = keyPoint.size
    print(x," , ",y," ,",s)


## Show blobs
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)

'''

#imports
import cv2
import numpy as np;

# read the image throught an window frame 
#imports for that
from tkinter import *
import generatePuzzle as gen
from tkinter import filedialog
from matplotlib import pyplot as plt

#getting the file
root = Tk()
root.title("jigsaw")
root.geometry("600x600")
filename = filedialog.askopenfilename( filetypes = ( ("testing files", "*.*"), ("All Files","*.*") ) )

#reading the image 
image = cv2.imread(filename, 0)

p = cv2.SimpleBlobDetector_Params()
p.minCircularity = 0.8
p.maxCircularity = 1.2
p.filterByCircularity = True
det = cv2.SimpleBlobDetector_create(p)
blobs = det.detect(image)
ret, imth = cv2.threshold(image,230,255,cv2.THRESH_BINARY)
im_with_ke = cv2.drawKeypoints(imth, blobs, np.array([]), (100,10,200), cv2.DRAW_MATCHES_FLAGS_DEFAULT)
cv2.imshow("Keypoints", im_with_ke)

gray= cv2.imread(filename,0)

# Threshold to detect rectangles independent from background illumination
ret2,th3 = cv2.threshold(gray,220,255,cv2.THRESH_BINARY_INV)

# Detect contours
_, contours, hierarchy = cv2.findContours( th3.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Draw contours
h, w = th3.shape[:2]
vis = np.zeros((h, w, 3), np.uint8)
cv2.drawContours( vis, contours, -1, (128,255,255), -1)

# Print Features of each contour and select some contours
contours2=[]
for i, cnt in enumerate(contours):
    cnt=contours[i]
    M = cv2.moments(cnt)

    if M['m00'] != 0:
        # for definition of features cf http://docs.opencv.org/3.1.0/d1/d32/tutorial_py_contour_properties.html#gsc.tab=0
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        area = cv2.contourArea(cnt)
        x,y,w,h = cv2.boundingRect(cnt)
        aspect_ratio = float(w)/h
        rect_area = w*h
        extent = float(area)/rect_area        

        print (i, cx, cy, area, aspect_ratio, rect_area, extent)

        if area < 80 and area > 10:
            contours2.append(cnt)

# Detect Harris corners
dst = cv2.cornerHarris(th3,2,3,0.04)

#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None, iterations=5)

# Threshold for an optimal value, it may vary depending on the image.
harris=image.copy()
print (harris.shape)
harris[dst>0.4*dst.max()]=[255,0,0]

titles = ['Original Image', 'Thresholding', 'Contours', "Harris corners"]
images = [image, th3, vis, harris]
for i in range(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()
'''
cv2.waitKey(0)