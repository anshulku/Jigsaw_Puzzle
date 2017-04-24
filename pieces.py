import cv2
import numpy as np;
import math
# read the image throught an window frame 
#imports for that
from tkinter import *
import generatePuzzle as gen
from tkinter import filedialog
from matplotlib import pyplot as plt
from matplotlib import path
from sideOfPieces import sideOfPieces

class pieces:
    
    # init for the class pieces
    def __init__(self, image):
        self.image = image
        self.corners = []
        self.side = []
        self.center = []
        self.isCornerPiece = False
        self.isBorderPiece = False
        self.isCenterPiece = False

        self.pointA = []
        self.pointB = []
        self.pointC = []
        self.pointD = []
        self.name = ""

    # returns the linear equation for given two points
    def LinerEquation(self,point1,point2):
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
    def LineEquation(self,point1,point2):
        x1 = point1[0]
        y1 = point1[1]
        x2 = point2[0]
        y2 = point2[1]
        A = -(y2 - y1)
        B = x2 - x1
        C = -(A * x1 + B * y1)
        return[A,B,C]
        
    def NumberOfPointInBetween(self,startpoint,endpoint,approx):
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
    
    
    def pointsInBetween(self,startIndex,endIndex,approx):
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
    
    
    def indexOf(self,point,approx):
        index = 0
        for check in range(0,len(approx)):
            startPoint=approx[check]
            if(startPoint[0][0] == point[0]  and startPoint[0][1] == point[1]):
                index = check
                break
        return index
    
    def CheckForCurve(self,startCheck,endCheck,approx,Test=False, opsite=False):
        #check if the point are valid meaning that those two point can be a corner
        #startCheck= rightPoints(startCheck, approx, True, Test)
        #endCheck=rightPoints(endCheck, approx, False)
        Eq = self.LinerEquation([ approx[startCheck][0][0] , approx[startCheck][0][1] ] , [ approx[endCheck][0][0] , approx[endCheck][0][1] ])
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
        startIndex = startCheck 
        endIndex = endCheck
        if(opsite):
            vaildPoint = False
        else:
            vaildPoint = True
        while(startIndex!=endIndex):
            while(endIndex!=startIndex):
                Eq = self.LinerEquation([ approx[startIndex][0][0] , approx[startIndex][0][1] ] , [ approx[endIndex][0][0] , approx[endIndex][0][1] ])
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
                            if(opsite):
                                vaildPoint = True
                                if(Test):
                                    print("checks = ",check)
                                    print("start = ",startIndex)
                                    print("end = ",endIndex)
                            else:
                                vaildPoint = False
                    if(not above and nextPointCheck[0][1]<y and isY):
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
    
    def changestartandendpoints(self,point, approx):
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
    def rightPoints(self,point, approx, forward, testing=False):
        points = changestartandendpoints(point,approx)
        start=points[0]
        end=points[1]
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
                
                
    








    def checkforcontourcurve(self,cornera,pointa,pointb,cornerb,test=False):
        #var=contour[0]
        #epsilon = 0.0000000001*cv2.arcLength(var,True)
        #allPoints = cv2.approxPolyDP(var,epsilon,True)
        ##print(approx[0][0])
        #startCheck = 0
        #endCheck = 0
        #for i in range(0, len(allPoints)):
        #    x = allPoints[i][0][0]
        #    y = allPoints[i][0][1]
        #    if(x == pointa[0] and y == pointa[1]):
        #        startcheck = i
        #    if(x == pointb[0] and y == pointb[1]):
        #        endcheck = i
        #if(test):
        #    print("startCheck  = ",startCheck)
        #    print("endCheck  = ",endCheck)
        #return self.CheckForCurve(startCheck,endCheck,allPoints)
        anglea = self.getAngle(cornera,pointa)
        angleb = self.getAngle(cornera,pointb)
        maxangle = max(anglea,angleb)
        flag = True
        if((0<=anglea<=45 or anglea>=315  or  135<=anglea<=225)  and (0<=angleb<=45 or angleb>=315  or  135<=angleb<=225)):
            flag= True
        elif((45<anglea<135  or 225<anglea<315)  and (45<angleb<135  or 225<angleb<315)):
            flag= True
        else:
            flag= False
        anglea = self.getAngle(cornerb,pointa)
        angleb = self.getAngle(cornerb,pointb)
        if((0<=anglea<=45 or anglea>=315  or  135<=anglea<=225)  and (0<=angleb<=45 or angleb>=315  or  135<=angleb<=225)):
            flag= True
        elif((45<anglea<135  or 225<anglea<315)  and (45<angleb<135  or 225<angleb<315)):
            flag= True
        else:
            flag= False
        return flag
    def findingcorners(self,test=False):
#getting the pieces of jigsaw
            tmpim=self.image
#denosing the image of each piece (Actually one piece)
            dst = cv2.fastNlMeansDenoisingColored(tmpim,None,10,20,7,5)
            #print("hello")
        #convertinf it into grayscale image
            gryPiec = cv2.cvtColor(dst,cv2.COLOR_RGB2GRAY)
        #making the threshold of the grayscaled image
            ret, threshPie = cv2.threshold(gryPiec, 230, 255, cv2.THRESH_BINARY_INV)
        #dectecting the contours of the pieces    
            im2Pi, contoursPi, hierarchyPi = cv2.findContours(threshPie, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
        #making the contours of same colour and the background of same colour
            newImageAppro = np.zeros((500,500,3), np.uint8)  
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
                
            im_with_keypoints = cv2.drawKeypoints(tmpim, keypoints, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
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
                #print(x," , ",y," ,",s)
           
        #getting all the set of possible corner points        
            Possible_Corners=[]
            cornerFound = False
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
            testing=False
            #print(Possible_Corners)
            #if(test):
            #    newImageAppro1 = np.zeros((500,500,3), np.uint8)
            #    for i in range(0,len(Possible_Corners)):
            #        point1 = Possible_Corners[i]
            #        cv2.circle(tmpim,(point1[0],point1[1]), 3, (0,255,0), 1)
            #        cv2.imshow("Possible corner", newImageAppro1)
            #        cv2.imshow("Piece image",self.image)
            #        cv2.waitKey(0)
        #finding all corners
            for i in range(0,len(Possible_Corners)):
                if(testing):
                    print("i = ",i)
                if(cornerFound):
                    break
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
                    returnedpoints = self.NumberOfPointInBetween(cornerOne,cornerTwo,approx)
                    startCheck=returnedpoints[0]
                    endCheck=returnedpoints[1]
                    count=returnedpoints[2]
                    if(count == 0 or (count>2)):
                        #if the count is 0 or 3 or bigger then procede
                        vaildPoint = True
                        if(count>2):
                            #check if the point are valid meaning that those two point can be a corner
                            vaildPoint=self.CheckForCurve(startCheck,endCheck,approx)
                            #if(count == 3  and vaildPoint and vaildPoint):
                            #    vaildPoint = self.checkforcontourcurve(cornerOne, approx[startCheck][0],approx[endCheck][0],cornerTwo)
                            indexI = self.indexOf(cornerOne,approx)
                            indexJ = self.indexOf(cornerTwo,approx)
                        if(vaildPoint and self.isCorner(cornerOne, approx[startCheck][0],approx[endCheck][0],cornerTwo)):
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
                                if(test):
                                    print("i = ",i,"j = ",j,"k = ",k)
                                cornerThree=Possible_Corners[k]
                                returnedpoints = self.NumberOfPointInBetween(cornerTwo,cornerThree,approx)
                                startCheck=returnedpoints[0]
                                endCheck=returnedpoints[1]
                                count=returnedpoints[2]
                                if(count == 0 or (count>2)):
                                    #if the count is 0 or 3 or bigger then procede
                                    vaildPoint = True
                                    if(count>2):
                                        vaildPoint=self.CheckForCurve(startCheck,endCheck,approx)
                                        # if cornerone and corner two had 3 number of point then try to find a point between j and k which make be a cornertwo
                                        if( self.NumberOfPointInBetween(cornerOne,cornerTwo,approx)[2] == 3  and vaildPoint):
                                                                    flag=True
                                                                    dvi = j+1
                                                                    while(dvi !=k ):
                                                                        if(dvi >= len(Possible_Corners)):
                                                                            dvi = 0
                                                                        possibleCornerthree = Possible_Corners[dvi]
                                                                        posreturnedpoints = self.NumberOfPointInBetween(cornerOne,possibleCornerthree,approx)
                                                                        posstartCheck=returnedpoints[0]
                                                                        posendCheck=returnedpoints[1]
                                                                        poscount=returnedpoints[2]
                                                                        posvaildPoint=self.CheckForCurve(posstartCheck,posendCheck,approx)
                                                                        if(posvaildPoint):
                                                                            flag = False
                                                                        dvi=dvi+1
                                                                        if(dvi >= len(Possible_Corners)):
                                                                            dvi = 0
                                                                    vaildPoint = flag

                                        indexK = self.indexOf(cornerThree,approx)
                                        indexJ = self.indexOf(cornerTwo,approx)
                                    if(vaildPoint and self.isCorner(cornerTwo, approx[startCheck][0],approx[endCheck][0],cornerThree)):
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
                                            if(test):
                                                print("i = ",i,"j = ",j,"k = ",k,"l = ",l)
                                            #cv2.imshow("Thks dsadvakcndlkadlc",newImageAppro)
                                            #cv2.imshow("Thks dv",img)
                                            #print("------------------------------------------------------------------------------------------------------------------------------------------------------------")
                                            #cv2.waitKey(0);
                                            cornerFour = Possible_Corners[l]
                                            returnedpoints = self.NumberOfPointInBetween(cornerThree,cornerFour,approx)
                                            startCheck=returnedpoints[0]
                                            endCheck=returnedpoints[1]
                                            count=returnedpoints[2]
        
        
        
                                            if(count==0 or (count>2)):
                                                #print("count detected = ",count)
                                                #got four point which are valid for corner but not for sure
                                                #need to do futher investegation
                                                #if the count is 0 or 3 or bigger then procede
                                                vaildPoint = True
                                                if(count>2):
                                                    #check if the point are valid meaning that those two point can be a corner
                                                    vaildPoint=self.CheckForCurve(startCheck,endCheck,approx)
                                                    # if cornerone and corner two had 3 number of point then try to find a point between j and k which make be a cornertwo
                                                    if( self.NumberOfPointInBetween(cornerTwo,cornerThree,approx)[2] == 3  and vaildPoint):
                                                                    flag=True
                                                                    dvi = k+1
                                                                    if(test):
                                                                        print("dvi" ,dvi)
                                                                        print("l" ,l)
                                                                        print("k" ,k)
                                                                    while(dvi !=l ):
                                                                        if(test):
                                                                            print("dvi increment" ,dvi)
                                                                            cv2.imshow("Thks dv",tmpim)
                                                                            cv2.waitKey(0);
                                                                        if(dvi >= len(Possible_Corners)):
                                                                            dvi = 0
                                                                        possibleCornerthree = Possible_Corners[dvi]
                                                                        posreturnedpoints = self.NumberOfPointInBetween(cornerTwo,possibleCornerthree,approx)
                                                                        posstartCheck=returnedpoints[0]
                                                                        posendCheck=returnedpoints[1]
                                                                        poscount=returnedpoints[2]
                                                                        posvaildPoint=self.CheckForCurve(posstartCheck,posendCheck,approx)
                                                                        if(posvaildPoint):
                                                                            flag = False
                                                                        dvi=dvi+1
                                                                        if(dvi >= len(Possible_Corners)):
                                                                            dvi = 0
                                                                    vaildPoint = flag
                                                    indexK = self.indexOf(cornerThree,approx)
                                                    indexL = self.indexOf(cornerFour,approx)
                                                if(vaildPoint and self.isCorner(cornerThree, approx[startCheck][0],approx[endCheck][0],cornerFour)):
                                                    vaildPoint = True
                                                    
                                                    if(vaildPoint):

                                                
                                                        returnedpoints = self.NumberOfPointInBetween(cornerFour,cornerOne,approx)
                                                        startCheck=returnedpoints[0]
                                                        endCheck=returnedpoints[1]
                                                        count=returnedpoints[2]
                                                        #print("-------------------------------------------------")
                                                        #print("corners For",l)
                                                        #print("corners Fir",i)
                                                        #print("end check  = ",endCheck)
                                                        #print("countout = ",count)
                                                        if(count == 0 or (count>2)):
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
                                                            if(count>2):
                                                                #check if the point are valid meaning that those two point can be a corner
                                                                vaildPoint=self.CheckForCurve(startCheck,endCheck,approx)
                                                                if( self.NumberOfPointInBetween(cornerThree,cornerFour,approx)[2] == 3  and vaildPoint):
                                                                    flag=True
                                                                    dvi = l+1
                                                                    while(dvi !=i ):
                                                                        if(dvi >= len(Possible_Corners)):
                                                                            dvi = 0
                                                                        possibleCornertwo = Possible_Corners[dvi]
                                                                        posreturnedpoints = self.NumberOfPointInBetween(cornerThree,possibleCornertwo,approx)
                                                                        posstartCheck=returnedpoints[0]
                                                                        posendCheck=returnedpoints[1]
                                                                        poscount=returnedpoints[2]
                                                                        posvaildPoint=self.CheckForCurve(posstartCheck,posendCheck,approx)
                                                                        if(posvaildPoint):
                                                                            flag = False
                                                                        dvi=dvi+1
                                                                        if(dvi >= len(Possible_Corners)):
                                                                            dvi = 0
                                                                    vaildPoint = flag
                                                                indexI = self.indexOf(cornerOne,approx)
                                                                indexL = self.indexOf(cornerFour,approx)
        
                                                            if(vaildPoint and self.isCorner(cornerFour, approx[startCheck][0],approx[endCheck][0],cornerOne)):
                                                                #angle and the last validation?????
                                                                
                                                                p = path.Path([(cornerOne[0],cornerOne[1])
                                                                                        , (cornerTwo[0], cornerTwo[1]), (cornerThree[0], cornerThree[1]), (cornerFour[0], cornerFour[1])])
                                                                result = p.contains_points([(centerX, centerY)])
                                                                if(result[0]):
                                                                    #cv2.circle(tmpim,(cornerOne[0],cornerOne[1]), 3, (0,0,0), 1)
                                                                    #cv2.circle(tmpim,(cornerTwo[0],cornerTwo[1]), 3, (0,0,0), 1)
                                                                    #cv2.circle(tmpim,(cornerThree[0],cornerThree[1]), 3, (0,0,0), 1)
                                                                    #cv2.circle(tmpim,(cornerFour[0],cornerFour[1]), 3, (0,0,0), 1)
                                                                    self.corners.append(cornerOne)
                                                                    self.corners.append(cornerTwo)
                                                                    self.corners.append(cornerThree)
                                                                    self.corners.append(cornerFour)
                                                                    cornerFound = True
                                                                    #if(testing):
                                                                    #    cv2.imshow("Thks dsadvakcndlkadlc",newImageAppro)
                                                                    #    cv2.imshow("Thks dv",img)
                                                                    #    cv2.waitKey(0);
                                                                  #  print("----------------------------********************************************--------------------------------------")
                                                                
                                            if(cornerFound):
                                                break    
                                            l=l+1
                                if(cornerFound):
                                    break   
                                k=k+1
                    if(cornerFound):
                        break
                    j=j+1
            #cv2.imshow("Thks dsadvakcndlkadlc",newImageAppro)
            #cv2.imshow("Thks dv",tmpim)
            #cv2.waitKey(0);
            

            
            self.center.append(centerX)
            self.center.append(centerY)
#giving contour here 
           
            self.setPropertyOfCorner(approx,contoursPi,test)





        

    #
    #   approx -- all the approx rectanguler points
    #   contours -- contains all the points in the pieces
    #   pointA -- one corner in this side on approx array
    #   pointB -- second corner in this side on approx array
    #   startPoint -- one corner in this side on allpoints array
    #   endPoint -- second corner in this side on allpoints array
    #   allpoints -- contains all the points on the side of this piece
    def getSide(self, approx, contours, pointA, pointB, startPoint, endPoint,allPoints,test=False):
        side=sideOfPieces(pointA,pointB)
        pointBetweenAB =  self.NumberOfPointInBetween(pointA,pointB,approx)[2]
        indexI = self.indexOf(pointA,approx)
        indexJ = self.indexOf(pointB,approx)
        points=[]
        if(pointBetweenAB==0):
            points.append(pointA)
            points.append(pointB)
            side.isStraight = True
        if(pointBetweenAB!=0):
            self.setPointOfSides(allPoints,startPoint,endPoint,points)
            nextPoint = indexI+1
            if(nextPoint>=len(approx)):
                nextPoint = 0
            previousPoint = indexJ-1
            if(previousPoint < 0):
                previousPoint = len(approx)-1
            
            Eq = self.LinerEquation([ approx[nextPoint][0][0] , approx[nextPoint][0][1] ] , [ approx[previousPoint][0][0] , approx[previousPoint][0][1] ])
            nextPointCheck=0
            if(nextPoint+1< len(approx)):
                nextPointCheck = approx[nextPoint+1]
            else:
                nextPointCheck = approx[0]
            y = Eq[0][0] * nextPointCheck[0][0]+ Eq[0][1]
            angle = math.atan2(approx[previousPoint][0][1] - approx[nextPoint][0][1], approx[previousPoint][0][0] - approx[nextPoint][0][0]) * 180.0 / math.pi
            # Weare lookin into y because y is different on the equation and different for the actual points
            # thus we look in to y when the degree is between 
            #
            #
            isY = True
            if((-135<=angle and angle<=-45) or (45<=angle and angle<=135)):
                isY = False
            #    print("XXX")   
            #else:
            #    print("YYY")   
            above = False   
            x=0    
            if(y<nextPointCheck[0][1] and isY):
                above = False  
                #print("above ",above)  
            else:
                if(not isY):
                    x=0
                    if(Eq[0][0]==0):
                        x = approx[previousPoint][0][0]
                    else:
                        x = (nextPointCheck[0][1]-Eq[0][1])/Eq[0][0] 
                    if(x>nextPointCheck[0][0]):
                        above = True  
                        #print("above ",above)    
                    else:
                        above = False
                        #print("above ",above)  
                else:
                    above = True
                    #print("above ",above)  
            if(isY):
                y = Eq[0][0] * self.center[0]+ Eq[0][1]
                if(y<self.center[1] and  not above):
                    side.isConvex=True
                    #print("inside false ",above)  
                elif(y>self.center[1] and above):
                    side.isConvex=True
                    #print("inside true ",above)  
                else:
                    side.isConcave=True
                    #print("outside ",above)  
            else:
                x=0
                if(Eq[0][0]==0):
                    x = approx[previousPoint][0][0]
                else:
                    x = (self.center[1]-Eq[0][1])/Eq[0][0]

                if(x<self.center[0] and  not above):
                    side.isConvex=True
                    #print("inside false ",above)  
                elif(x>self.center[0] and above):
                    side.isConvex=True
                    #print("inside true ",above)  
                else:
                    side.isConcave=True
                    #print("outside ",above)  
                
        side.originalPoints = points
        #if(test):
            
        #    newImageAppro1 = np.zeros((500,500,3), np.uint8)
        #    for i in range(0,len(points)):
        #        point1 = points[i]
        #        cv2.circle(newImageAppro1,(int(point1[0]),int(point1[1])), 3, (255,255,255), 1)
        #        cv2.imshow("Lets goos", newImageAppro1)
        #        print("side.isConcave",side.isConcave)
        #        print("side.isConvex",side.isConvex)
        #        print("side.isStraight",side.isStraight)
        #        cv2.waitKey(0)
            
        return side
    def getPointsForApprox(self, approx, startPoint, endPoint):
        points = []
        cordinate = approx[startPoint]
        points.append([cordinate[0][0],cordinate[0][1]])
        while(startPoint != endPoint):
            ipoint = startPoint + 1
            if(ipoint != endPoint and not ipoint>=len(approx)):
                cordinate = approx[ipoint]
                points.append([cordinate[0][0],cordinate[0][1]])
            if(ipoint>=len(approx)):
                startPoint = 0
            else:
                startPoint = ipoint
        cordinate = approx[endPoint]
        points.append([cordinate[0][0],cordinate[0][1]])
        return points 
        
    def setPropertyOfCorner(self ,approx, contours,test=False):
        cornerA = self.corners[0]
        cornerB = self.corners[1]
        cornerC = self.corners[2]
        cornerD = self.corners[3]
        pointBetweenAB =  self.NumberOfPointInBetween(cornerA,cornerB,approx)[2]
        pointBetweenBC =  self.NumberOfPointInBetween(cornerB,cornerC,approx)[2]
        pointBetweenCD =  self.NumberOfPointInBetween(cornerC,cornerD,approx)[2]
        pointBetweenDA =  self.NumberOfPointInBetween(cornerD,cornerA,approx)[2]
        #getting the position of the corner in approx
        pointi = self.indexOf(cornerA,approx)
        pointj = self.indexOf(cornerB,approx)
        pointk = self.indexOf(cornerC,approx)
        pointl = self.indexOf(cornerD,approx)
        #all the points betweent the corners in approx
        approxPointA = self.getPointsForApprox(approx,pointi,pointj)
        approxPointB = self.getPointsForApprox(approx,pointj,pointk)
        approxPointC = self.getPointsForApprox(approx,pointk,pointl)
        approxPointD = self.getPointsForApprox(approx,pointl,pointi)
        
        #decideing if the pieces is a corner, border or an center piece
        if(pointBetweenAB != 0 and pointBetweenBC != 0 and pointBetweenCD != 0 and pointBetweenDA != 0):
            self.isCenterPiece = True
        elif((pointBetweenAB == 0 and pointBetweenBC != 0 and pointBetweenCD != 0 and pointBetweenDA != 0)
            or (pointBetweenAB != 0 and pointBetweenBC == 0 and pointBetweenCD != 0 and pointBetweenDA != 0)
                or (pointBetweenAB != 0 and pointBetweenBC != 0 and pointBetweenCD == 0 and pointBetweenDA != 0)
                    or (pointBetweenAB != 0 and pointBetweenBC != 0 and pointBetweenCD != 0 and pointBetweenDA == 0)):
            self.isBorderPiece = True
        else:
            self.isCornerPiece = True
        #if(pointBetweenAB==0):
        #    print(approx)   
        #    print("come on")
        #here we are trying to find the best match for the corner in the contours
        #-1 indecates if the match is not found
        
        pointA=-1
        pointB=-1
        pointC=-1
        pointD=-1
        var=contours[0]
        epsilon = 0.0000000001*cv2.arcLength(var,True)
        allPoints = cv2.approxPolyDP(var,epsilon,True)
        #print(approx[0][0])

        for i in range(0,len(allPoints)):
            x = allPoints[i][0][0]
            y = allPoints[i][0][1]
            if(x == cornerA[0] and y == cornerA[1]):
                pointA = i
            if(x == cornerB[0] and y == cornerB[1]):
                pointB = i
            if(x == cornerC[0] and y == cornerC[1]):
                pointC = i
            if(x == cornerD[0] and y == cornerD[1]):
                pointD = i
        #decides if the side is a straight , convex or concave 
        #also store the original point of the graph in the side object
        self.side.append(self.getSide(approx,contours,cornerA,cornerB,pointA,pointB,allPoints))
        self.side.append(self.getSide(approx,contours,cornerB,cornerC,pointB,pointC,allPoints,test))
        self.side.append(self.getSide(approx,contours,cornerC,cornerD,pointC,pointD,allPoints))
        self.side.append(self.getSide(approx,contours,cornerD,cornerA,pointD,pointA,allPoints))
        #store the approximate point of the graph in the side
        self.side[0].approxPoints = approxPointA
        self.side[1].approxPoints = approxPointB
        self.side[2].approxPoints = approxPointC
        self.side[3].approxPoints = approxPointD
        #if(test):
            
        #    newImageAppro1 = np.zeros((500,500,3), np.uint8)
        #    for i in range(0,len(approxPointB)):
        #        point1 = approxPointB[i]
        #        cv2.circle(newImageAppro1,(int(point1[0]),int(point1[1])), 3, (255,255,255), 1)
        #        cv2.imshow("Lets goos", newImageAppro1)
        #        cv2.waitKey(0)
        #print(self.pointA)
        #print("------------------------------------------------------- ")
        #print(self.pointB)
        #print("------------------------------------------------------- ")
        #print(self.pointB[0])
        #print("------------------------------------------------------- ")
        #print(self.pointC)
        #print("------------------------------------------------------- ")
        #print(self.pointD)
        #print("------------------------------------------------------- ")
        #coverting the original point on the x-aixsi
        self.showGraphs()
    '''
        sets the defination of the side 
        meaning that if the side is on the top 
        it is named TOP if it is at the bottom it is named BOTTOM
        so thi funcition set direction of a side same thing with right and left
    '''
    def setdirection(self):
        axis = self.side[0].whichaxis
        if(axis=="X"):
            y1 = self.side[0].cornerRight[1]
            y2 = self.side[2].cornerRight[1]
            if(y1<y2):
                self.side[0].direction = "TOP"
                self.side[2].direction = "BOTTOM"
            else:
                self.side[0].direction = "BOTTOM"
                self.side[2].direction = "TOP"

            x1 = self.side[1].cornerRight[0]
            x2 = self.side[3].cornerRight[0]
            if(x1<x2):
                self.side[1].direction = "LEFT"
                self.side[3].direction = "RIGHT"
            
            else:
                self.side[1].direction = "RIGHT"
                self.side[3].direction = "LEFT"
        else:
            x1 = self.side[0].cornerRight[0]
            x2 = self.side[2].cornerRight[0]
            if(x1<x2):
                self.side[0].direction = "LEFT"
                self.side[2].direction = "RIGHT"
            
            else:
                self.side[0].direction = "RIGHT"
                self.side[2].direction = "LEFT"

            y1 = self.side[1].cornerRight[1]
            y2 = self.side[3].cornerRight[1]
            if(y1<y2):
                self.side[1].direction = "TOP"
                self.side[3].direction = "BOTTOM"
            
            else:
                self.side[1].direction = "BOTTOM"
                self.side[3].direction = "TOP"
        sidea = self.side[0]
        sideb = self.side[1]
        sidec = self.side[2]
        sided = self.side[3]

        if(((sidea.isStraight and sidea.direction=="TOP") or (sidec.isStraight and sidec.direction=="TOP") 
                or (sideb.isStraight and sideb.direction=="TOP") or (sided.isStraight and sided.direction=="TOP"))
    
                and ((sidea.isStraight and sidea.direction=="LEFT") or (sidec.isStraight and sidec.direction=="LEFT") 
                or (sideb.isStraight and sideb.direction=="LEFT") or (sided.isStraight and sided.direction=="LEFT"))):
            self.name = "TL"
        elif(((sidea.isStraight and sidea.direction=="TOP") or (sidec.isStraight and sidec.direction=="TOP") 
                or (sideb.isStraight and sideb.direction=="TOP") or (sided.isStraight and sided.direction=="TOP"))
    
                and ((sidea.isStraight and sidea.direction=="RIGHT") or (sidec.isStraight and sidec.direction=="RIGHT") 
                or (sideb.isStraight and sideb.direction=="RIGHT") or (sided.isStraight and sided.direction=="RIGHT"))):
            self.name = "TR"
        elif(((sidea.isStraight and sidea.direction=="BOTTOM") or (sidec.isStraight and sidec.direction=="BOTTOM") 
                or (sideb.isStraight and sideb.direction=="BOTTOM") or (sided.isStraight and sided.direction=="BOTTOM"))

                and ((sidea.isStraight and sidea.direction=="LEFT") or (sidec.isStraight and sidec.direction=="LEFT") 
                or (sideb.isStraight and sideb.direction=="LEFT") or (sided.isStraight and sided.direction=="LEFT"))):
            self.name = "BL"
        elif(((sidea.isStraight and sidea.direction=="BOTTOM") or (sidec.isStraight and sidec.direction=="BOTTOM") 
                or (sideb.isStraight and sideb.direction=="BOTTOM") or (sided.isStraight and sided.direction=="BOTTOM"))
    
                and ((sidea.isStraight and sidea.direction=="RIGHT") or (sidec.isStraight and sidec.direction=="RIGHT") 
                or (sideb.isStraight and sideb.direction=="RIGHT") or (sided.isStraight and sided.direction=="RIGHT"))):
            self.name = "BR"
        else:
            self.name = "N"
            
    def setPointOfSides(self,approx,start,end,points):
        while(start != end):
            points.append(approx[start][0])
            start = start+1
            if(start >=len(approx)):
                start=0
        points.append(approx[start][0])

    def showXaxisGraph(self,points,opsiteSides = False , testing=False ):
        originAngle = self.getAngle(points[0],points[len(points)-1])
        newFirstX = 10
        newFirstY = 60
        newPoints = [[newFirstX,newFirstY]]
        #if(opsiteSides):
        #    startI = len(points)-2
        #    while(startI>=0):
        #        point1 = points[len(points)-1]
        #        point2 = points[startI]
        #        angle = self.getAngle(point2,point1)
        #        diffAngle = originAngle - angle
        #        distance = self.getDistance(point2,point1)
        #        newX = newFirstX + (distance * math.cos(math.radians(diffAngle)))
        #        newY = newFirstY + (distance * math.sin(math.radians(diffAngle)))
        #        newPoints.append([newX,newY])
        #        startI = startI-1
        #    return newPoints
            
        for i in range(1,len(points)):
            point1 = points[0]
            point2 = points[i]
            angle = self.getAngle(point1,point2)
            diffAngle=0
            if(opsiteSides):
                diffAngle = angle-originAngle 
            else:
                diffAngle = originAngle-angle 
            distance = self.getDistance(point1,point2)
            newX = newFirstX + (distance * math.cos(math.radians(diffAngle)))
            newY = newFirstY + (distance * math.sin(math.radians(diffAngle)))
            newPoints.append([newX,newY])
            if(testing):
                newImageAppro1 = np.zeros((500,500,3), np.uint8)
                ts = False
                for j in range(0,len(newPoints)-1):
                    nex1 = newPoints[j]
                    nex2 = newPoints[j+1]
                    cv2.line(newImageAppro1,(int(nex1[0]),int(nex1[1])),(int(nex2[0]),int(nex2[1])), (255,255,255), 1)
                   
                #if(ts):
                    
                print("originAngle  ::  ",originAngle)
                print("angle  ::  ",angle)
                print("diffAngle  ::  ",diffAngle)
                print("distance  ::  ",distance)
                print("new the distance is  ::  ",self.getDistance([newFirstX,newFirstY],[newX,newY]))
                print("j =   ::  ",j)
                print("j+1 =   ::  ",j+1)
                if(i==26 or i==27):
                    print("Angle In Real : = ",math.atan2(point2[1] - point1[1], point2[0] - point1[0]) * 180.0 / math.pi)
                    print("real points : = ",newX," ; ",newY)
                    print("shown points : = ",int(newX)," ; ",int(newY))
                ts = True
                print("------------------------------------------------------------------------------------------  ::  ")

                newImageAppro2 = np.zeros((500,500,3), np.uint8)
                cv2.imshow("testing stuff",newImageAppro1) 
                for j in range(0,len(newPoints)-1):
                        point1 = points[j]
                        point2 = points[j+1]
                        cv2.line(newImageAppro2,(int(point1[0]),int(point1[1])),(int(point2[0]),int(point2[1])), (255,255,255), 1)
                cv2.imshow("real stuff",newImageAppro2) 
                cv2.waitKey(0)
            #X = Cx + (r * cosine(angle))  
            #Y = Cy + (r * sine(angle))
            #/_(x2-x1^2)+(y2-y1^2)
        
        return newPoints

    def makeX_axisGraphs(self,side):
        newPoints = self.showXaxisGraph(side.approxPoints)
        start = newPoints[1] # 1 since we need the next point and not the first one
        end = newPoints[len(newPoints)-2] # same we don't need the 
        if(2>=len(newPoints)):
            return []
        nextCheck = newPoints[2]
        Eq = self.LinerEquation([ start[0] , start[1] ] , [ end[0] , end[1] ])
        y = Eq[0][0] * nextCheck[0]+ Eq[0][1]
        '''
        *we will be looking only in y since all is in x-axis
        '''
        above = False   
        x=0    
        if(y<nextCheck[1]):
            above = False  #this below the line
        else:
            above = True   #this is above the line
        #concave is outside
        #convex is inside
        if(above):
            newPoints = self.showXaxisGraph(side.originalPoints,testing=False)
            side.x_axis_Points = newPoints
            newPoints = self.showXaxisGraph(side.approxPoints)
            side.x_axis_PointsApprox = newPoints
        else:
            newPoints = self.showXaxisGraph(side.originalPoints,opsiteSides=True,testing=False)
            side.x_axis_Points = newPoints
            newPoints = self.showXaxisGraph(side.approxPoints,opsiteSides=True)
            side.x_axis_PointsApprox = newPoints





    def getDistance(self,pointA,pointB):
        return ((pointB[0]-pointA[0]) ** 2 + (pointB[1]-pointA[1]) ** 2 ) ** 0.5
    #
    # gets two point and then calclutes the angle between them
    # and returns the angle in 0 -360
    #
    def getAngle(self,pointA,pointB):
        angle = math.atan2(pointB[1] - pointA[1], pointB[0] - pointA[0]) * 180.0 / math.pi
        newAngle = angle
        if(angle<0):
            newAngle = angle *-1
        elif(angle != 0):
            newAngle = 360 -angle
        else:
            if(pointB[0]<pointA[0]):
                newAngle = 180
            else:
                newAngle = 0
        #print("angle (old , new ) = ( ",angle," ; ", newAngle)
        return newAngle
    def isCorner(self,pointa,nextpoint,prevpoint,pointb):
        #print("pointa = ",pointa)
        #print("nextpoint = ",nextpoint)
        #print("prevpoint = ",prevpoint)
        #print("pointb = ",pointb)
        anglea = self.getAngle(pointa,nextpoint)
        angleb = self.getAngle(prevpoint,pointb)
        if((0<=anglea<=45 or anglea>=315  or  135<=anglea<=225)  and (0<=angleb<=45 or angleb>=315  or  135<=angleb<=225)):
            return True
        elif((45<anglea<135  or 225<anglea<315)  and (45<angleb<135  or 225<angleb<315)):
            return True
        else:
            return False
        #minangle = min(anglea,angleb)
        #maxangle = max(anglea,angleb)
        #if(maxangle - minangle <60):
        #    return True 
        #return False
    def showGraphs(self):
        #print("------------------------------------------------------- ")
        #newImageAppro1 = np.zeros((500,500,3), np.uint8)
        #for i in range(0,len(self.side[0].originalPoints)-1):
        #    point1 = self.side[0].originalPoints[i]
        #    point2 = self.side[0].originalPoints[i+1]
        #    print("------------------------------------------------------- ")
        #    print(point1)
        #    print(point2)
        #    print("------------------------------------------------------- ")
            
        #    cv2.line(newImageAppro1,(point1[0],point1[1]),(point2[0],point2[1]), (255,255,255), 1)
        #print("------------------------------------------------------- ")
        #cv2.imshow("graph 1",newImageAppro1)
        #print("---------------------------------")

        #print("this is ir  0 ",self.side[0].contourpoints)
        #print("---------------------------------")
        #print("---------------------------------")
        self.makeX_axisGraphs(self.side[0])
        #self.side[0].showside("side 0",self.side[0].x_axis_Points)
        #print("--------------------------------------")
        #print("above  ",self.side[0].isConcave)
        #print("below  ",self.side[0].isConvex)
        #print("stragit  ",self.side[0].isStraight)
        #print("1111111111111111111 ")
        #cv2.waitKey(0);
        #newImageAppro2 = np.zeros((500,500,3), np.uint8)
        #for i in range(0,len(self.side[1].originalPoints)-1):
        #    point1 = self.side[1].originalPoints[i]
        #    point2 = self.side[1].originalPoints[i+1]
        #    cv2.line(newImageAppro2,(point1[0],point1[1]),(point2[0],point2[1]), (255,255,255), 1)
        #print("------------------------------------------------------- ")
        #cv2.imshow("graph 2",newImageAppro2) 
        self.makeX_axisGraphs(self.side[1])
        #self.side[1].showside("side 1",self.side[1].x_axis_Points)
        #cv2.waitKey(0);
        #print("--------------------------------------")
        #print("above  ",self.side[1].isConcave)
        #print("below  ",self.side[1].isConvex)
        #print("stragit  ",self.side[1].isStraight)
        #print("2222222222222222222222 ")
        #cv2.waitKey(0);
 
        #newImageAppro3 = np.zeros((500,500,3), np.uint8) 
        #for i in range(0,len(self.side[2].originalPoints)-1):
        #    point1 = self.side[2].originalPoints[i]
        #    point2 = self.side[2].originalPoints[i+1]
        #    cv2.line(newImageAppro3,(point1[0],point1[1]),(point2[0],point2[1]), (255,255,255), 1)
        #print("------------------------------------------------------- ")
        #cv2.imshow("graph 3",newImageAppro3) 
        self.makeX_axisGraphs(self.side[2])
        #self.side[2].showside("side 2",self.side[2].x_axis_Points)
        #print("--------------------------------------")
        #print("above  ",self.side[2].isConcave)
        #print("below  ",self.side[2].isConvex)
        #print("stragit  ",self.side[2].isStraight)
        #print("33333333333333333333333  ")
        #cv2.waitKey(0);
        #newImageAppro4 = np.zeros((500,500,3), np.uint8)  
        #for i in range(0,len(self.side[3].originalPoints)-1):
        #    point1 = self.side[3].originalPoints[i]
        #    point2 = self.side[3].originalPoints[i+1]
        #    cv2.line(newImageAppro4,(point1[0],point1[1]),(point2[0],point2[1]), (255,255,255), 1)
        #print("------------------------------------------------------- ")
        #cv2.imshow("graph 4",newImageAppro4)
        self.makeX_axisGraphs(self.side[3])
        #self.side[3].showside("side 3",self.side[3].x_axis_Points)
        #print("--------------------------------------")
        #print("above  ",self.side[3].isConcave)
        #print("below  ",self.side[3].isConvex)
        #print("stragit  ",self.side[3].isStraight)
        #print("44444444444444444444444 ")
        #cv2.waitKey(0);

    def showImage(self,name):
            #for i in range(0,len(self.side)):
            #    strj = "Original Pice" +str(i)
            #    self.side[i].showside(strj,self.side[i].originalPoints) 
            #    strj = "approx Pice" +str(i)
            #    self.side[i].showside(strj,self.side[i].x_axis_Points) 
              #  print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"    ,  i)  
    
#getting the pieces of jigsaw
            tmpim=self.image
#denosing the image of each piece (Actually one piece)
        #    dst = cv2.fastNlMeansDenoisingColored(tmpim,None,10,20,7,5)
        #    #print("hello")
        ##convertinf it into grayscale image
        #    gryPiec = cv2.cvtColor(dst,cv2.COLOR_RGB2GRAY)
        ##making the threshold of the grayscaled image
        #    ret, threshPie = cv2.threshold(gryPiec, 230, 255, cv2.THRESH_BINARY_INV)
        ##dectecting the contours of the pieces    
        #    cv2.imshow("Threshold "+str(name),threshPie)
        #    median = cv2.medianBlur(tmpim,5)
        #    gryPiec = cv2.cvtColor(median,cv2.COLOR_RGB2GRAY)
        ##making the threshold of the grayscaled image
        #    ret, threshPie = cv2.threshold(gryPiec, 230, 255, cv2.THRESH_BINARY_INV)
        #    cv2.imshow("Threshold Median "+str(name),threshPie)
        #    newBlur = cv2.blur(tmpim,(5,5))
        #    gryPiec = cv2.cvtColor(newBlur,cv2.COLOR_RGB2GRAY)
        ##making the threshold of the grayscaled image
        #    ret, threshPie = cv2.threshold(gryPiec, 230, 255, cv2.THRESH_BINARY_INV)
        #    cv2.imshow("new Median "+str(name),threshPie)

            cv2.imshow(name,tmpim)

    #testing contour and approx gives the samepoints
    def showApproxAndContour(self):
            print("i came")
#getting the pieces of jigsaw
            tmpim=self.image
#denosing the image of each piece (Actually one piece)
            dst = cv2.fastNlMeansDenoisingColored(tmpim,None,10,20,7,5)
            #print("hello")
        #convertinf it into grayscale image
            gryPiec = cv2.cvtColor(dst,cv2.COLOR_RGB2GRAY)
        #making the threshold of the grayscaled image
            ret, threshPie = cv2.threshold(gryPiec, 230, 255, cv2.THRESH_BINARY_INV)
        #dectecting the contours of the pieces    
            im2Pi, contoursPi, hierarchyPi = cv2.findContours(threshPie, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
        #making the contours of same colour and the background of same colour
            newImageAppro = np.zeros((500,500,3), np.uint8)  
            Directions=[]
            var=contoursPi[0]
            epsilon = 0.00000000000000000001*cv2.arcLength(var,True)
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
        # the above part as well since it is for visuals 
            
            cv2.line(newImageAppro,(approx[0][0][0],approx[0][0][1]),(approx[len(approx)-1][0][0],approx[len(approx)-1][0][1]), (255,255,255))
            contourImage = np.zeros((500,500,3), np.uint8)  
            print(contoursPi[0][0])
            for varCo in range(0,len(contoursPi[0])-1):
                    
                    varCord=contoursPi[0][varCo]
                    varCord2=contoursPi[0][varCo+1]
                    cv2.line(contourImage,(varCord[0][0],varCord[0][1]),(varCord2[0][0],varCord2[0][1]), (255,255,255), 1)
            compare = True
            for varCo in range(0,len(contoursPi[0])):
                    
                    varCord=contoursPi[0][varCo]
                    varCordCompa = approx[varCo]
                    if(varCord[0][0] != varCordCompa[0][0] or varCordCompa[0][1]!=varCord[0][1]):
                        compare=False
            if(compare):
                print("True")
            else:
                print("False")
            cv2.imshow("approx",newImageAppro)
            cv2.imshow("contourImage",contourImage)
            cv2.waitKey(0)
        