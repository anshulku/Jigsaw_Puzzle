#!/usr/bin/python

# Standard imports
import cv2
import numpy as np;
import math
from pieces import pieces
# read the image throught an window frame 
#imports for that
from tkinter import *
import generatePuzzle as gen
from tkinter import filedialog
from matplotlib import pyplot as plt
from matplotlib import path
def LinerEquation(point1,point2):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    if(x1==x2):
        return [[0,x1]]
    else:   
        b=(x2*y1-x1*y2)/(x2-x1)
        a = (y2-b)/x2
        return [[a,b]]
def LineEquation(point1,point2):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    A = -(y2 - y1)
    B = x2 - x1
    C = -(A * x1 + B * y1)
    return[A,B,C]
    
def NumberOfPointInBetween(startpoint,endpoint,approx):
    startIndex = 0
    endIndex = 0 
    count=0
    for check in range(0,len(approx)):
        startPoint=approx[check]
        if(startPoint[0][0] == startpoint[0]  and startPoint[0][1] == startpoint[1]):
            startIndex = check
    for check in range(0,len(approx)):
        startPoint=approx[check]
        if(startPoint[0][0] == endpoint[0]  and startPoint[0][1] == endpoint[1]):
            endIndex=check
            break
    startIndex = startIndex+1
    startCheck = startIndex
    endCheck = endIndex-1
    if(endCheck<0):
        endCheck=len(approx)-1
    if(startIndex>=len(approx)):
        startIndex = 0
    startCheck = startIndex
    while(startIndex!=endIndex):
        count=count+1
        startIndex=startIndex+1
        if(startIndex>=len(approx)):
            startIndex=0
    return [startCheck,endCheck,count]


def pointsInBetween(startIndex,endIndex,approx):
    count=0
    startIndex=startIndex+1
    if(startIndex>=len(approx)):
        startIndex=0
    while(startIndex!=endIndex):
        count=count+1
        startIndex=startIndex+1
        if(startIndex>=len(approx)):
            startIndex=0
    return count


def indexOf(point,approx):
    index = 0
    for check in range(0,len(approx)):
        startPoint=approx[check]
        if(startPoint[0][0] == point[0]  and startPoint[0][1] == point[1]):
            index = check
            break
    return index
def checkForCorner(startCheck,endCheck,approx):
    print("Incompleted")

def CheckForCurve(startCheck,endCheck,approx,Test=False, opsite=False):
    #check if the point are valid meaning that those two point can be a corner
    #startCheck= rightPoints(startCheck, approx, True, Test)
    #endCheck=rightPoints(endCheck, approx, False)
    Eq = LinerEquation([ approx[startCheck][0][0] , approx[startCheck][0][1] ] , [ approx[endCheck][0][0] , approx[endCheck][0][1] ])
    nextPointCheck=0
    if(startCheck+1< len(approx)):
        nextPointCheck = approx[startCheck+1]
    else:
        nextPointCheck = approx[0]
    y = Eq[0][0] * nextPointCheck[0][0]+ Eq[0][1]
    angle = math.atan2(approx[endCheck][0][1] - approx[startCheck][0][1], approx[endCheck][0][0] - approx[startCheck][0][0]) * 180.0 / math.pi
    isY = True
    if((-135<=angle and angle<=-45) or (45<=angle and angle<=135)):
        isY = False

    above = False   
    x=0    
    if(y<nextPointCheck[0][1] and isY):
        above = False   
    else:
        if(not isY):
            x=0
            if(Eq[0][0]==0):
                x = approx[endCheck][0][0]
            else:
                x = (nextPointCheck[0][1]-Eq[0][1])/Eq[0][0] 
            if(x>nextPointCheck[0][0]):
                above = True   
            else:
                above = False
        else:
            above = True
    #if(Test):
    #    if(isY):
    #        print("Y")
    #    else:
    #        print("X")
    #    print("above = ",above)
    #    print("start point = ",startCheck)
    #    print("end point = ",endCheck)
    #    print("equation we got   = ",Eq)
    #    print("x = ",x)
    #    print("nextPointCheck = ",nextPointCheck)
    startIndex = startCheck 
    endIndex = endCheck
    if(opsite):
        vaildPoint = False
    else:
        vaildPoint = True
    while(startIndex!=endIndex):
        while(endIndex!=startIndex):
            Eq = LinerEquation([ approx[startIndex][0][0] , approx[startIndex][0][1] ] , [ approx[endIndex][0][0] , approx[endIndex][0][1] ])
            check = startIndex+1
            if(check>=len(approx)):
                check=0
            while(check!=endIndex):
                nextPointCheck = approx[check]
                y = Eq[0][0] * nextPointCheck[0][0]+ Eq[0][1]
                x = 0
                if(Eq[0][0]!=0):
                    x = (nextPointCheck[0][1]-Eq[0][1])/Eq[0][0] 
                else:
                    x = approx[startIndex][0][0]
                if(not isY):
                    if(above and nextPointCheck[0][0]>x):
                        if(opsite):
                            vaildPoint = True
                        else:
                            vaildPoint = False
                    if(not above and nextPointCheck[0][0]<x):
                        if(opsite):
                            vaildPoint = True
                        else:
                            vaildPoint = False
                if(above and nextPointCheck[0][1]>y and isY):
                        #if(Test):
                        #    print("checks = ",check)
                        #    print("start point = ",startCheck)
                        #    print("points where it is = ",nextPointCheck)
                        #    print("cam x on line = ",x)
                        #    print("end point = ",endCheck)
                        if(opsite):
                            vaildPoint = True
                            if(Test):
                                print("checks = ",check)
                                print("start = ",startIndex)
                                print("end = ",endIndex)
                        else:
                            vaildPoint = False
                if(not above and nextPointCheck[0][1]<y and isY):
                            #print("points = ",nextPointCheck)
                            #print("x = ",x)
                        if(opsite):
                            vaildPoint = True
                            if(Test):
                                print("checks = ",check)
                                print("start = ",startIndex)
                                print("end = ",endIndex)
                        else:
                            vaildPoint = False
                check=check+1
                
                if(check>=len(approx)):
                    check=0
            endIndex=endIndex-1
            if(endIndex<0):
                endIndex=len(approx)-1
        startIndex=startIndex+1
        if(startIndex>=len(approx)):
            startIndex=0
        endIndex=endCheck

    return vaildPoint

#def checkDirections(Start,End,approx):
#    vaildPoint = True
#    prvPoint = Start-1
#    if(prvPoint<0):
#        prvPoint = len(approx)-1
#    nextPoint = End+1
#    if(nextPoint>=len(approx)):
#        nextPoint=0
#    angleStart = math.atan2(approx[Start][0][1] - approx[prvPoint][0][1], approx[Start][0][0] - approx[prvPoint][0][0]) * 180.0 / math.pi
#    angleEnd = math.atan2(approx[nextPoint][0][1] - approx[End][0][1], approx[nextPoint][0][0] - approx[End][0][0]) * 180.0 / math.pi
#    n.jn.kn.kllkdsmol
#    return vaildPoint
def changestartandendpoints(point, approx):
    start=0
    end=0
    if(not (point==0 and point==len(approx)-1)):
        for i in range(0, len(approx)):
            if(i==point):
                end=i+1
                break
            start = i
            
    if(point==0):
        start = len(approx)-1
        end = 1
    if(point==len(approx)-1):
        start = len(approx)-2
        end = 0
    return [start,end]
def rightPoints(point, approx, forward, testing=False):
    points = changestartandendpoints(point,approx)
    start=points[0]
    end=points[1]
    #print("start of the point  =  ",start)
    #print("current point of the point = ",point)
    #print("end of the point =  ",end)
    
    while True:
        startpointX = approx[start][0][0]
        startpointY = approx[start][0][1]
        currentX = approx[point][0][0]
        currentY = approx[point][0][1]
        endpointX = approx[end][0][0]
        endpointY = approx[end][0][1]
        angle = math.atan2(currentY - startpointY, currentX - startpointX) * 180.0 / math.pi
        angle2 = math.atan2(endpointY - currentY, endpointX - currentX) * 180.0 / math.pi
        if(testing):
            print("---------------ANGLE  one  = ",angle)
            print("---------------ANGLE  two  = ",angle2)
        #print("angle  =  ",angle)
        #print("point first (x,y)  =  (",startpointX," , ",startpointY,")")
        #print("current first (x,y)  =  (",currentX," , ",currentY,")")
        #print("angle  2  =  ",angle2)
        if(angle-45 <= angle2 and angle2<=angle+45):
            if(forward):
                point=end
            else:
                point=start
                
            points = changestartandendpoints(point,approx)
            start=points[0]
            end=points[1]
        else:
            break
    return point
            
            
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



jigsawPieces = []
#extracting each piece from the image given in teh system Part 1
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
for i in range(0, len(ylow)):
    images.append(img[ylow[i]:yhigh[i],xlow[i]:xhigh[i]])
    jigsawPieces.append(pieces(images[i]))
    #cv2.imshow("Thks dv",images[i])
    #cv2.waitKey(0);

#finding the corner of each pieces
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
cornerPieces = []
borderPieces = []
centerPieces = []
testingi = []
testingj = []
testingk = []
for i in range(0,len(jigsawPieces)):
    eachPiece = jigsawPieces[i]
    eachPiece.findingcorners()
    #print("is corner = ",eachPiece.isCornerPiece)
    #print("is border = ",eachPiece.isBorderPiece)
    #print("is center = ",eachPiece.isCenterPiece)
    if(eachPiece.isCornerPiece):
        cornerPieces.append(eachPiece)
        testingi.append(i)
    if(eachPiece.isBorderPiece):
        borderPieces.append(eachPiece)
        testingj.append(i)
    if(eachPiece.isCenterPiece):
        centerPieces.append(eachPiece)
        testingk.append(i)
    #print("------------------------------------------------------- ")
    eachPiece.showImage()
print("------------------------------------------------------- ")
print(testingi)
print(testingj)
print(testingk)
print("------------------------------------------------------- ")
cv2.imshow("Thks dv for working",img)
cv2.waitKey(0);

