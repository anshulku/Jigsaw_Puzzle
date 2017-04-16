#!/usr/bin/python
#####backup file 02/02/2017
#obs

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

#extracting each piece from the image given in teh system Part 1
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
for i in range(0, len(ylow)):
    images.append(img[ylow[i]:yhigh[i],xlow[i]:xhigh[i]])
    #cv2.imshow("Thks dv",images[i])
    #cv2.waitKey(0);
    
k=0
ster = "Piece "
titles = []

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------


#CORNER DETECTION
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
for pointpossible in range(0, len(images)):
    print("loop i")
#getting the pieces of jigsaw
    tmpim=images[pointpossible] 
#denosing the image of each piece (Actually one piece)
    dst = cv2.fastNlMeansDenoisingColored(tmpim,None,10,20,7,5)
    print("hello")
#convertinf it into grayscale image
    gryPiec = cv2.cvtColor(dst,cv2.COLOR_RGB2GRAY)
#making the threshold of the grayscaled image
    ret, threshPie = cv2.threshold(gryPiec, 230, 255, cv2.THRESH_BINARY_INV)
#dectecting the contours of the pieces    
    im2Pi, contoursPi, hierarchyPi = cv2.findContours(threshPie, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
#making the contours of same colour and the background of same colour
    newImageAppro = np.zeros((500,500,3), np.uint8)  
    newImageAppro2 = np.zeros((500,500,3), np.uint8)  
    Directions=[]
    var=contoursPi[0]
    epsilon = 0.014*cv2.arcLength(var,True)
    approx = cv2.approxPolyDP(var,epsilon,True)
#### don't need to be done now
    for varCo in range(0,len(approx)-1):
            varCordP=approx[0]
            if(varCo==0):
                varCordP=approx[len(approx)-1]
            else:
                varCordP=approx[varCo-1]
            varCord = approx[varCo]
            varCord2 = approx[varCo+1]
            cv2.line(newImageAppro,(varCord[0][0],varCord[0][1]),(varCord2[0][0],varCord2[0][1]), (255,255,255), 1)
            angleP = math.atan2(varCordP[0][1] - varCord[0][1], varCordP[0][0] - varCord[0][0]) * 180.0 / math.pi
            angleN = math.atan2(varCord2[0][1] - varCord[0][1], varCord2[0][0] - varCord[0][0]) * 180.0 / math.pi
# the above part as well since it is for visuals 
            
    cv2.line(newImageAppro,(approx[0][0][0],approx[0][0][1]),(approx[len(approx)-1][0][0],approx[len(approx)-1][0][1]), (255,255,255), 1)
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
    params.filterByInertia = False
    params.minInertiaRatio = 0.01
        
        ## Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)
        ## Detect blobs.
    keypoints = detector.detect(newImageAppro)

        ## Draw detected blobs as red circles.
        ## cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
        ## the size of the circle corresponds to the size of blob
        
    im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    centerX=0
    centerY=0
    for keyPoint in keypoints:
        x = keyPoint.pt[0]
        y = keyPoint.pt[1]
        centerX = x
        centerY = y
        s = keyPoint.size
        cv2.circle(newImageAppro,(int(x),int(y)), 3, (0,255,0), 1)
        #cv2.circle(newImageAppro,(int(x),int(y)), int(s/2), (0,255,0), 1)
        print(x," , ",y," ,",s)
   
#getting all the set of possible corner points        
    Possible_Corners=[]
    for point in range(0,len(approx)):    
        isPointCorner = approx[point]
        startPoint = point+1
        UppperR = False
        UppperL = False
        LowwerR = False
        LowwerL = False
        while point!=startPoint:       
            if(startPoint>=len(approx)):
                startPoint = 0
            nextPoint = approx[startPoint]
            if(point!=startPoint):
                angle = math.atan2(nextPoint[0][1] - isPointCorner[0][1], nextPoint[0][0] - isPointCorner[0][0]) * 180.0 / math.pi
                if(angle>=0 and angle <=90):
                    UppperR = True
                if(angle>90 and angle <=180):
                    UppperL = True
                if(angle<0 and angle >=-90):
                    LowwerR = True
                if(angle<-90 and angle >=-180):
                    LowwerL = True
                startPoint=startPoint+1
        if((UppperR and UppperL and LowwerR and LowwerL)==False):
            Possible_Corners.append([isPointCorner[0][0],isPointCorner[0][1]])
  
    allCorners = []
    #for i in range(0,len(approx)):    
    #    checkpoint1 = approx[i]
    #    j = i+1
    #    if(j>=len(approx)):
    #        j=0
    #    while(i!=j):  
    #        checkpoint2 = approx[j]
    #        pointCount = pointsInBetween(i,j,approx)  
    #        if(pointcount>3):
    #            vaildPointTesting1=CheckForCurve(i,j,approx)
    #            if(vaildPointTesting1 and pointpossible==1):
    #                allCorners.append(checkpoint1)
    #                allCorners.append(checkpoint2)
    #                cv2.circle(newImageAppro,(checkpoint1[0][0],checkpoint1[0][1]), 3, (0,255,255), 1)
    #                cv2.circle(newImageAppro,(checkpoint2[0][0],checkpoint2[0][1]), 3, (0,255,255), 1)
    #                print("I   = ",i)
    #                print("J   = ",j)
    #                print("Point = ",pointCount)
    #                cv2.imshow("Thks dsadvakcndlkadlc",newImageAppro)
    #                cv2.imshow("Thks dv",img)
    #                cv2.waitKey(0);
    #        j=j+1
    #        if(j>=len(approx)):
    #            j=0
            
    testing=False
#finding all corners
    for i in range(0,len(Possible_Corners)):
        if(testing):
            print("i = ",i)
        cornerOne = Possible_Corners[i]
#--------------------------------------
#second corner point finding
        j=i+1
            
        if(j>=len(Possible_Corners)):
            j=0
        while(j!=i):
            if(j >= len(Possible_Corners)):
                j=0
            if(j == i):
                break
            if(testing):
                print("i = ",i,"j = ",j)
            cornerTwo = Possible_Corners[j]
            #checking if the point between the two corners are 0 or at least 3
            returnedpoints = NumberOfPointInBetween(cornerOne,cornerTwo,approx)
            startCheck=returnedpoints[0]
            endCheck=returnedpoints[1]
            count=returnedpoints[2]
            if(count == 0 or (count>3)):
                #if the count is 0 or 3 or bigger then procede
                vaildPoint = True
                if(count>3):
                    #check if the point are valid meaning that those two point can be a corner
                    vaildPoint=CheckForCurve(startCheck,endCheck,approx)
                    indexI = indexOf(cornerOne,approx)
                    indexJ = indexOf(cornerTwo,approx)
                if(vaildPoint):
                    #if it is vaild then go find points
#----------------------------------------------------
#Third corner point finding
                    k=j+1
                    if(k>=len(Possible_Corners)):
                        k=0
                    while(k!=i):
                        
                        if(k >= len(Possible_Corners)):
                            k=0
                        if(k == i):
                            break
                        if(testing):
                            print("i = ",i,"j = ",j,"k = ",k)
                        cornerThree=Possible_Corners[k]
                        returnedpoints = NumberOfPointInBetween(cornerTwo,cornerThree,approx)
                        startCheck=returnedpoints[0]
                        endCheck=returnedpoints[1]
                        count=returnedpoints[2]
                        if(count == 0 or (count>3)):
                            #if the count is 0 or 3 or bigger then procede
                            vaildPoint = True
                            if(count>3):
                                vaildPoint=CheckForCurve(startCheck,endCheck,approx)
                                indexK = indexOf(cornerThree,approx)
                                indexJ = indexOf(cornerTwo,approx)
                            if(vaildPoint):
#-------------------------------------------------------------------------------------------------------
#fourth point corner dectection
                                l=k+1
                                if(l >= len(Possible_Corners)):
                                    l=0
                                while(l!=i):
                                    if(l >= len(Possible_Corners)):
                                        l=0
                                    if(l == i):
                                        break
                                    if(testing):
                                        print("i = ",i,"j = ",j,"k = ",k,"l = ",l)
                                    #cv2.imshow("Thks dsadvakcndlkadlc",newImageAppro)
                                    #cv2.imshow("Thks dv",img)
                                    #print("------------------------------------------------------------------------------------------------------------------------------------------------------------")
                                    #cv2.waitKey(0);
                                    cornerFour = Possible_Corners[l]
                                    returnedpoints = NumberOfPointInBetween(cornerThree,cornerFour,approx)
                                    startCheck=returnedpoints[0]
                                    endCheck=returnedpoints[1]
                                    count=returnedpoints[2]



                                    if(count==0 or (count>3)):
                                        #print("count detected = ",count)
                                        #got four point which are valid for corner but not for sure
                                        #need to do futher investegation
                                        #if the count is 0 or 3 or bigger then procede
                                        vaildPoint = True
                                        if(count>3):
                                            #check if the point are valid meaning that those two point can be a corner
                                            vaildPoint=CheckForCurve(startCheck,endCheck,approx)
                                            indexK = indexOf(cornerThree,approx)
                                            indexL = indexOf(cornerFour,approx)
                                        if(vaildPoint):
                                            vaildPoint = True
                                            
                                            if(vaildPoint):

                                                
                                                returnedpoints = NumberOfPointInBetween(cornerFour,cornerOne,approx)
                                                startCheck=returnedpoints[0]
                                                endCheck=returnedpoints[1]
                                                count=returnedpoints[2]
                                                #print("-------------------------------------------------")
                                                #print("corners For",l)
                                                #print("corners Fir",i)
                                                #print("end check  = ",endCheck)
                                                #print("countout = ",count)
                                                if(count == 0 or (count>3)):
                                                    #print("-------------------------------------------------")
                                                    #print("i = ",i)
                                                    #print("j = ",j)
                                                    #print("k = ",k)
                                                    #print("l = ",l)
                                                    #print("count = ",count)
                                                    #print("end check check 2 = ",endCheck)
                                                   
                                                    
                                                    vaildPoint = True
                                                    angle5=0
                                                    angle6=0
                                                    if(count>3):
                                                        #check if the point are valid meaning that those two point can be a corner
                                                        vaildPoint=CheckForCurve(startCheck,endCheck,approx)
                                                        indexI = indexOf(cornerOne,approx)
                                                        indexL = indexOf(cornerFour,approx)

                                                    if(vaildPoint):
                                                        #angle and the last validation?????
                                                        
                                                        p = path.Path([(cornerOne[0],cornerOne[1])
                                                                                , (cornerTwo[0], cornerTwo[1]), (cornerThree[0], cornerThree[1]), (cornerFour[0], cornerFour[1])])
                                                        result = p.contains_points([(centerX, centerY)])
                                                        if(result[0]):
                                                            cv2.circle(tmpim,(cornerOne[0],cornerOne[1]), 3, (0,0,0), 1)
                                                            cv2.circle(tmpim,(cornerTwo[0],cornerTwo[1]), 3, (0,0,0), 1)
                                                            cv2.circle(tmpim,(cornerThree[0],cornerThree[1]), 3, (0,0,0), 1)
                                                            cv2.circle(tmpim,(cornerFour[0],cornerFour[1]), 3, (0,0,0), 1)
                                                            cv2.circle(newImageAppro,(cornerOne[0],cornerOne[1]), 3, (0,255,0), 1)
                                                            cv2.circle(newImageAppro,(cornerTwo[0],cornerTwo[1]), 3, (0,255,0), 1)
                                                            cv2.circle(newImageAppro,(cornerThree[0],cornerThree[1]), 3, (0,255,0), 1)
                                                            cv2.circle(newImageAppro,(cornerFour[0],cornerFour[1]), 3, (0,255,0), 1)
                                                            #if(testing):
                                                            #    cv2.imshow("Thks dsadvakcndlkadlc",newImageAppro)
                                                            #    cv2.imshow("Thks dv",img)
                                                            #    cv2.waitKey(0);
                                                            print("----------------------------********************************************--------------------------------------")
                                                        
                                                           
                                    l=l+1
                        k=k+1
            j=j+1
    cv2.imshow("Thks dsadvakcndlkadlc",newImageAppro)
    cv2.imshow("Thks dv",tmpim)
    cv2.waitKey(0);
cv2.imshow("Thks dv for working",img)
cv2.waitKey(0);

#dst = cv2.fastNlMeansDenoisingColored(im1,None,15,20,7,5)
#im2 = cv2.cvtColor(dst,cv2.COLOR_RGB2GRAY)
'''
#threshold testing 
ret, timg = cv2.threshold(im2,230,255,cv2.THRESH_BINARY)
cv2.imshow("thre", timg)

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 230
params.maxThreshold = 255


# Filter by Area.
params.filterByArea = False
params.minArea = 1500

# Filter by Circularity
params.filterByCircularity = False
params.minCircularity = 0.1

# Filter by Convexity
params.filterByConvexity = False
params.minConvexity = 0.87

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01

# Create a detector with the parameters
detector = cv2.SimpleBlobDetector_create(params)


# Detect blobs.
keypoints = detector.detect(timg)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
# the size of the circle corresponds to the size of blob

im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

for keypoint in keypoints:
    print(keypoint.angle)
'''

# Show blobs