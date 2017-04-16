#!/usr/bin/python

# Standard imports
import cv2
import numpy as np;
import math
from pieces import pieces
from result import result 
from matching import matching
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
    #if(i==4):
    #    eachPiece.findingcorners(test=True)
    #else:
    eachPiece.findingcorners()
    eachPiece.side[0].setsideproperty()
    eachPiece.side[1].setsideproperty()
    eachPiece.side[2].setsideproperty()
    eachPiece.side[3].setsideproperty()
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
    eachPiece.setdirection()

    #print("------------------------------------------------------- ")
   # eachPiece.showGraphs()

print("------------------------------------------------------- ")
print(testingi)
print(testingj)
print(testingk)
print("------------------------------------------------------- ")
result = result(jigsawPieces)
result
result.getresult()

#matchingtesting = cornerPieces[0]

##for i in range(0,len(matchingtesting.side)):
##    side = matchingtesting.side[i]
##    if(not side.isStraight):
##        for j in range(0,len(borderPieces)):
##            borderPiece = borderPieces[j]
##            for k in range(0,len(borderPiece.side)):
##                matchSide = borderPiece.side[k]
##                if(not matchSide.isStraight):
##                    doesMatch = object.isMatch(side,matchSide)
##                    if(doesMatch):
##                        print("The match from this algo is = :: ",j)
##                    else:
##                        side.showside("corner side",side.x_axis_PointsApprox)
##                        matchSide.showside("match side",matchSide.x_axis_PointsApprox)
##                        matchingtesting.showImage("corner")
##                        borderPiece.showImage("border")
##                        cv2.waitKey(0)
##
##
##for i in range(0,len(matchingtesting.side)):
##    side = matchingtesting.side[i]
##    nma="corner side "+str(i)
##    side.showside(nma,side.x_axis_Points,testing=True)
##print(side.approxPoints)
##borderPiece = borderPieces[0]
##matchSide = borderPiece.side[2]

##for k in range(0,len(borderPiece.side)):
##                matchSide = borderPiece.side[k]
##                if(not matchSide.isStraight):
##                    doesMatch = object.isMatch(side,matchSide)
##                    if(doesMatch):
##                        print("The match from this algo is = :: ",k)
##                        side.showside("corner side",side.x_axis_PointsApprox,testing=True)
##                        matchSide.showside("match side",matchSide.x_axis_PointsApprox)
##                        matchingtesting.showImage("corner")
##                        borderPiece.showImage("border")
##                        cv2.waitKey(0)
##                    else:
##                        side.showside("corner side",side.x_axis_PointsApprox)
##                        matchSide.showside("match side",matchSide.x_axis_PointsApprox)
##                        matchingtesting.showImage("corner")
##                        borderPiece.showImage("border")
##                        cv2.waitKey(0)
##matchSide = borderPiece.side[0]
##matchSide = borderPiece.side[1]
##matchSide = borderPiece.side[3]

##first corner matches the second border (position is i = 0 side is 2 and j = 2 side is 0)
#First = cornerPieces[2]
#matchLookingFor = 0
#First.showImage("corner pieces")



##object.subsampling(First.side[1],"1 Stuff ")
##object.showsubsample(First.side[2],First.side[2],"subsample")
##First.side[2].showside("approx corner side",First.side[2].x_axis_Points)
#############################################################################


#First.side[matchLookingFor].split()
#First.side[matchLookingFor].setsubsampling(First.side[matchLookingFor])
##First.side[0].printsubsample(First.side[2])
##cv2.waitKey(0)


#border = borderPieces[1]
#border.showImage("border pieces")
#border.side[1].split()

##First.side[2].setsubsampling(First.side[2])

##print("BORDER PRINTING")
#border.side[1].setsubsampling(border.side[3])
##print("----------------------------------------------")
##border.side[3].printsubsample(border.side[3])
#object.canMatch(First.side[matchLookingFor],border.side[1], "Border 3   Piece 1")
##object.aligned(First.side[matchLookingFor],border.side[1],Testing = True)
######################################################################

##border.side[0].showside("Border 6 piece 0",border.side[0].x_axis_Points)

##First.side[2].showTwosplit(First.side[2],border.side[2])

##First.side[0].showside("Border 1 piece 0",First.side[0].x_axis_Points)
##First.side[1].showside("Border 1 piece 1",First.side[1].x_axis_Points)
##First.side[2].showside("Border 1 piece 2",First.side[2].x_axis_Points)
##First.side[3].showside("Border 1 piece 3",First.side[3].x_axis_Points)
##cv2.waitKey(0)

##border.showImage("border pieces")
##cv2.waitKey(0)
##object.subsampling(border.side[0],"2 Stuff ")
##object.doesMatch(First.side[2],border.side[0],True)


##border.side[0].showside("approx border side",border.side[0].x_axis_Points)
##object.subsampling(First.side[2],border.side[3],"Stuff")
##object.subsampling(First.side[2],border.side[1],"Stuff1")
##object.subsampling(First.side[2],border.side[2],"Stuff2")
##object.subsampling(First.side[2],border.side[3],"Stuff3")

##object.isMatchTestingStuff(First.side[2],border.side[0],"Stuff")
##object.isMatchTestingStuff(First.side[2],border.side[1],"Stuff 1")
##object.isMatchTestingStuff(First.side[2],border.side[2],"Stuff 2")
##object.isMatchTestingStuff(First.side[2],border.side[3],"Stuff 3")

    
##for k in range(0,len(borderPieces)):
##    Match = borderPieces[k]
##    First.side[matchLookingFor].showTwoSides(First.side[matchLookingFor],Match.side[0],name="border "+str(k)+"Piece 0")  
##    First.side[matchLookingFor].showTwoSides(First.side[matchLookingFor],Match.side[1],name="border "+str(k)+"Piece 1")  
##    First.side[matchLookingFor].showTwoSides(First.side[matchLookingFor],Match.side[2],name="border "+str(k)+"Piece 2")  
##    First.side[matchLookingFor].showTwoSides(First.side[matchLookingFor],Match.side[3],name="border "+str(k)+"Piece 3") 
##    if(k == len(borderPieces)-1):
##        print("-----------------------------------------------------------------------") 
##    cv2.waitKey(0)




##First.side[0].showside("original corner side",First.side[0].originalPoints)
###First.side[2].showside("apppro corner side",First.side[2].x_axis_PointsApprox)
##cv2.waitKey(0);
##Match.showImage("border piece")
##Match.side[2].showside("approx border side",Match.side[2].x_axis_Points)
##Match.side[2].showside("original border side",Match.side[2].originalPoints)

#for k in range(0,len(cornerPieces)):
#    corner = cornerPieces[k]
#    corner.side[0].split()
#    corner.side[1].split()
#    corner.side[2].split()
#    corner.side[3].split()

#    corner.side[0].setsubsampling(corner.side[0])
#    corner.side[1].setsubsampling(corner.side[1])
#    corner.side[2].setsubsampling(corner.side[2])
#    corner.side[3].setsubsampling(corner.side[3])

    
#for k in range(0,len(borderPieces)):
#    Match = borderPieces[k]
#    #Match.showImage("Border " + str(k))

#    #Match.side[0].showside("Border " + str(k) + " Pieces 0",Match.side[0].x_axis_Points)
#    #Match.side[1].showside("Border " + str(k) + " Pieces 1",Match.side[1].x_axis_Points)
#    #Match.side[2].showside("Border " + str(k) + " Pieces 2",Match.side[2].x_axis_Points)
#    #Match.side[3].showside("Border " + str(k) + " Pieces 3",Match.side[3].x_axis_Points)
    
#    Match.side[0].split()
#    Match.side[1].split()
#    Match.side[2].split()
#    Match.side[3].split()

#    Match.side[0].setsubsampling(Match.side[0])
#    Match.side[1].setsubsampling(Match.side[1])
#    Match.side[2].setsubsampling(Match.side[2])
#    Match.side[3].setsubsampling(Match.side[3])

##    Match.showImage("border piece"+str(k))

##First.side[0].showside("Border " + str(k) + " Pieces 0",First.side[0].x_axis_Points)
##First.side[1].showside("Border " + str(k) + " Pieces 1",First.side[1].x_axis_Points)
##First.side[2].showside("Border " + str(k) + " Pieces 2",First.side[2].x_axis_Points)
##First.side[3].showside("Border " + str(k) + " Pieces 3",First.side[3].x_axis_Points)
   
##cv2.waitKey(0)
#possibleMatches = []
#for k in range(0,len(borderPieces)):
#    Match = borderPieces[k]
##    print("The Border is = ",k)
##    print("The side is = 0")
##    if(k==2):
##        object.showsubsample(First.side[2],Match.side[0],"Testin")
##        object.doesMatch(First.side[2],Match.side[0],True)
##    else:
##        object.doesMatch(First.side[2],Match.side[0])
##    print("The side is = 1")
#    name = str("Border Piece  =  ")+str(k)
#    print(name,"-----------------------------------")
#    test0  = object.canMatch(First.side[matchLookingFor],Match.side[0], str(name)+"   Piece 0")
#    if(test0 and object.aligned(First.side[matchLookingFor],Match.side[0], name= str(name)+"   Piece 0")):
#        possibleMatches.append([Match,0,k])
#        print("border piece = "+str(k) , " : 0 Maybe ")
#    test1  = object.canMatch(First.side[matchLookingFor],Match.side[1], str(name)+"   Piece 1")
#    if(test1 and object.aligned(First.side[matchLookingFor],Match.side[1], name= str(name)+"   Piece 1")):
#        possibleMatches.append([Match,1,k])
#        print("border piece = "+str(k) , " : 1 Maybe ")
#    test2  = object.canMatch(First.side[matchLookingFor],Match.side[2], str(name)+"   Piece 2")
#    if(test2 and object.aligned(First.side[matchLookingFor],Match.side[2], name= str(name)+"   Piece 2")):
#        possibleMatches.append([Match,2,k])
#        print("border piece = "+str(k) , " : 2 Maybe ")
#    test3  = object.canMatch(First.side[matchLookingFor],Match.side[3], str(name)+"   Piece 3")
#    if(test3 and object.aligned(First.side[matchLookingFor],Match.side[3], name= str(name)+"   Piece 3")):
#        possibleMatches.append([Match,3,k])
#        print("border piece = "+str(k) , " : 3 Maybe ")
#    if(k==9):
#        print("========================================================")
#        Match.side[3].printsubsample(Match.side[3])
#        #object.aligned(First.side[matchLookingFor],Match.side[3], name= str(name)+"   Piece 3",Testing=True)
#        print("Dv help me")
#        #Match.showImage("border piece"+str(k))
#        #print("Test 0 = ",test0 , "Test 1 = " ,test1, "Test 2 = " ,test2, "Test 3 = " ,test3)
#        #Match.side[0].showside("Border  Pieces 0",Match.side[0].x_axis_Points)
#        #Match.side[1].showside("Border  Pieces 1",Match.side[1].x_axis_Points)
#        #Match.side[2].showside("Border  Pieces 2",Match.side[2].x_axis_Points)
#        #Match.side[3].showside("Border  Pieces 3",Match.side[3].x_axis_Points)
#        #cv2.waitKey(0);
#newPossiblMatch = []
#for i in range(0,len(possibleMatches)):
#    possibleMatches[i][0].showImage("border piece"+str(possibleMatches[i][2]))
#    print("border piece = ",possibleMatches[i][2]," : ",possibleMatches[i][1])
#    #if(i == 1):
#    #    object.aligned(First.side[1],possibleMatches[i][0].side[possibleMatches[i][1]],Testing = True)
#    #    First.side[1].showTwosplit(First.side[1],possibleMatches[i][0].side[possibleMatches[i][1]])
#    #    First.side[1].showTwoSides(First.side[1],possibleMatches[i][0].side[possibleMatches[i][1]])
#    flag = object.aligned(First.side[matchLookingFor],possibleMatches[i][0].side[possibleMatches[i][1]])
#    #if(flag):
#    #    newPossiblMatch.append
#    object.Match(First.side[matchLookingFor],[possibleMatches[i][0].side[possibleMatches[i][1]]])
#    print("-------------------------------------------------------")
#    #print("Test 0 = ",test0 , "Test 1 = " ,test1, "Test 2 = " ,test2, "Test 3 = " ,test3)
#    #possibleMatches[i].side[possibleMatches[1]].showside("Border  Pieces 0",Match.side[0].x_axis_Points)
     
##First.side[matchLookingFor].showTwoSides(First.side[matchLookingFor],borderPieces[8].side[0],name="dc 2 0")  

##First.side[2].showside("Original Border",First.side[2].originalPoints)
##borderPieces[2].side[0].showside("Original Border",borderPieces[2].side[0].originalPoints)

##First.side[2].showTwoSides(First.side[0],borderPieces[1].side[1],name="Border 2 1") 
#First.side[0].testingthexaiss("PLS dvworkr",borderPieces[1].side[1])

##borderPieces[1].side[1].showside("DvHelp Me  rtrt",borderPieces[1].side[1].originalPoints)

##First.side[matchLookingFor].showside("DvHelp Me2",First.side[matchLookingFor].originalPoints)
##First.side[matchLookingFor].testingthexaiss("come on 2")
##First.side[matchLookingFor].showside("DvHelp Me rtrtr5",First.side[matchLookingFor].x_axis_Points) 
##First.side[2].showTwoSides(First.side[matchLookingFor],borderPieces[3].side[3],name="Border 3 3")  
##First.side[2].showTwoSides(First.side[2],borderPieces[8].side[3],name="Border 8 7")  
#cv2.waitKey(0);


##object.aligned(First.side[2],border.side[0])
##object.Match(First.side[2],[border.side[0]])
##    print("The side is = 2")
##    object.doesMatch(First.side[2],Match.side[2])
##    print("The side is = 3")
##    object.doesMatch(First.side[2],Match.side[3])
##    print("-------------------------------------------------------------------------------------------")

##Match.side[0].showside("original border side",Match.side[0].originalPoints)
##Match.side[0].showside("apppro border side",Match.side[0].x_axis_PointsApprox)
##print("Answer  =  ",object.isMatch(First.side[0],Match.side[2]))
##cv2.imshow("Thks dv for working",img)
cv2.waitKey(0);

