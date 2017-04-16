#finding blob for the jigsaw
# blob is a group of grayscale in the image

#**********************************************************************************
# traget to achieve
# ** remove noise get the blob fix it and threshold it....
#date 5/11/2016 : 16:58 DV
#**********************************************************************************


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
import matplotlib.lines as lines

#colormaps_fig = plt.figure()

#num_plots = 2


## Plot several different functions...
#x = np.arange(10)
#labels = []
#plt.plot([0,50,90,60,40])
#plt.show()


#fig, ax = plt.subplots()

#fig.set_size_inches(6,6)          # Make graph square
#scatter([-0.1],[-0.1],s=0.01)     # Move graph window a little left and down

#line1 = [(0,0), (1,0)]
#line2 = [(0,0), (0,1)]

## Note that the Line2D takes a list of x values and a list of y values,
## not 2 points as one might expect.  So we have to convert our points
## an x-list and a y-list.
#(line1_xs, line1_ys) = zip(*line1)
#(line2_xs, line2_ys) = zip(*line2)

#ax.add_line(Line2D(line1_xs, line1_ys, linewidth=2, color='blue'))
#ax.add_line(Line2D(line2_xs, line2_ys, linewidth=2, color='red'))
#plot()
#show()
## read image
#root = tk()
#root.title("jigsaw")
#root.geometry("600x600")
##filename = filedialog.askopenfilename( filetypes = ( ("testing files", "*.*"), ("all files","*.*") ) )
#imgtest = np.zeros((512,512,3), np.uint8) 
#cv2.line(imgtest,(0,0),(511,511),(255,0,0),5)
#cv2.imshow("im show",imgtest)
#cv2.waitKey(0) & 0xff == 27

#img = cv2.imread(filename)
#gray = cv2.cvtcolor(img,cv2.color_bgr2gray)
#_,thresh = cv2.threshold(gray,1,255,cv2.thresh_binary)

#contours,hierarchy = cv2.findcontours(thresh,cv2.retr_external,cv2.chain_approx_simple)
#cnt = contours[0]
#x,y,w,h = cv2.boundingrect(cnt)

#crop = img[y:y+h,x:x+w]
#cv2.imwrite('filenamecopy.png',crop)
#from tkinter import *
#import generatePuzzle as gen
#from tkinter import filedialog
#import cv2
#from matplotlib import pyplot as plt
#import numpy as np
#class generatePuzzle:
    #root = NONE
    #def __init__(self):
    #  global root 
    #   root = Tk()
#def extract():
#    root = tk()
#    root.title("jigsaw")
#    root.geometry("600x600")
#    filename = filedialog.askopenfilename( filetypes = ( ("testing files", "*.*"), ("all files","*.*") ) )
#    img = cv2.imread(filename,0)
#    ret, timg = cv2.threshold(img,230,255,cv2.thresh_binary)
#    timg2 = cv2.adaptivethreshold(timg,230,cv2.adaptive_thresh_mean_c,cv2.thresh_binary,11,2)
#    timg3 = cv2.adaptivethreshold(timg,230,cv2.adaptive_thresh_gaussian_c,cv2.thresh_binary,11,2)
#    im2, contours, hierarchy = cv2.findcontours(timg3,cv2.retr_tree,cv2.chain_approx_simple)
#   # cv2.drawcontours(im2, constants, -1, (0,255,0),3)
#    cv2.imshow("original",img)
#    cv2.imshow("binary",timg)
#    cv2.imshow("mean",timg2)
#    cv2.imshow("adaptive",im2)
#    dectector = cv2.simpleblobdetector_create() # setting the dectector up for version 3.0 ^
#    keypoint = dectector.detect(img)
#    im_with_keypoints = cv2.drawkeypoints(img, keypoint, np.array([]), (0,0,255), cv2.draw_matches_flags_draw_rich_keypoints)
#    cv2.imshow("dectection" ,im_with_keypoints )
#    cv2.waitkey(0)
#   # plt.imshow(timg,'gray')
#    #plt.title("testing")
#    #plt.show()
#    # def inputfile(self):
#    #    global root

#if __name__ == "__main__" :
#    extract()