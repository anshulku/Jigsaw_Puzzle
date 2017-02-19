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

class pieces:
    
    def __init__(self, image):
        self.image = image
        self.corners=[]
        self.pointA=[]
        self.pointB=[]
        self.pointC=[]
        self.pointD=[]
        self.isCornerPiece = False
        self.isBorderPiece = False
        self.isCenterPiece = False



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
                
                
    









    def setPropertyOfCorner(self ,approx, contours):
        cornerA = self.corners[0]
        cornerB = self.corners[1]
        cornerC = self.corners[2]
        cornerD = self.corners[3]
        pointBetweenAB =  self.NumberOfPointInBetween(cornerA,cornerB,approx)[2]
        pointBetweenBC =  self.NumberOfPointInBetween(cornerB,cornerC,approx)[2]
        pointBetweenCD =  self.NumberOfPointInBetween(cornerC,cornerD,approx)[2]
        pointBetweenDA =  self.NumberOfPointInBetween(cornerD,cornerA,approx)[2]
        if(pointBetweenAB != 0 and pointBetweenBC != 0 and pointBetweenCD != 0 and pointBetweenDA != 0):
            self.isCenterPiece = True
        elif((pointBetweenAB == 0 and pointBetweenBC != 0 and pointBetweenCD != 0 and pointBetweenDA != 0)
            or (pointBetweenAB != 0 and pointBetweenBC == 0 and pointBetweenCD != 0 and pointBetweenDA != 0)
                or (pointBetweenAB != 0 and pointBetweenBC != 0 and pointBetweenCD == 0 and pointBetweenDA != 0)
                    or (pointBetweenAB != 0 and pointBetweenBC != 0 and pointBetweenCD != 0 and pointBetweenDA == 0)):
            self.isBorderPiece = True
        else:
            self.isCornerPiece = True
        if(pointBetweenAB==0):
            self.pointA.append(cornerA)
            self.pointA.append(cornerB)
        if(pointBetweenBC==0):
            self.pointB.append(cornerB)
            self.pointB.append(cornerC)
        if(pointBetweenCD==0):
            self.pointC.append(cornerC)
            self.pointC.append(cornerD)
        if(pointBetweenDA==0):
            self.pointD.append(cornerD)
            self.pointD.append(cornerA)
        #here we ar trying to find the best match for the corner in the contours
        #-1 indecates if the match is not found
        
        pointA=-1
        pointB=-1
        pointC=-1
        pointD=-1
        var=contours[0]
        epsilon = 0.0000000001*cv2.arcLength(var,True)
        approx = cv2.approxPolyDP(var,epsilon,True)
        #print(approx[0][0])

        for i in range(0,len(approx)):
            x = approx[i][0][0]
            y = approx[i][0][1]
            if(x == cornerA[0] and y == cornerA[1]):
                pointA = i
            if(x == cornerB[0] and y == cornerB[1]):
                pointB = i
            if(x == cornerC[0] and y == cornerC[1]):
                pointC = i
            if(x == cornerD[0] and y == cornerD[1]):
                pointD = i
        if(pointBetweenAB!=0):
            self.setPointOfSides(approx,pointA,pointB,self.pointA)
        if(pointBetweenBC!=0):
            self.setPointOfSides(approx,pointB,pointC,self.pointB)
        if(pointBetweenCD!=0):
            self.setPointOfSides(approx,pointC,pointD,self.pointC)
        if(pointBetweenDA!=0):
            self.setPointOfSides(approx,pointD,pointA,self.pointD)
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
        #self.showGraphs()
    def setPointOfSides(self,approx,start,end,points):
        while(start != end):
            points.append(approx[start][0])
            start = start+1
            if(start >=len(approx)):
                start=0
        points.append(approx[start][0])
    def findingcorners(self):
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
                    if(count == 0 or (count>3)):
                        #if the count is 0 or 3 or bigger then procede
                        vaildPoint = True
                        if(count>3):
                            #check if the point are valid meaning that those two point can be a corner
                            vaildPoint=self.CheckForCurve(startCheck,endCheck,approx)
                            indexI = self.indexOf(cornerOne,approx)
                            indexJ = self.indexOf(cornerTwo,approx)
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
                                returnedpoints = self.NumberOfPointInBetween(cornerTwo,cornerThree,approx)
                                startCheck=returnedpoints[0]
                                endCheck=returnedpoints[1]
                                count=returnedpoints[2]
                                if(count == 0 or (count>3)):
                                    #if the count is 0 or 3 or bigger then procede
                                    vaildPoint = True
                                    if(count>3):
                                        vaildPoint=self.CheckForCurve(startCheck,endCheck,approx)
                                        indexK = self.indexOf(cornerThree,approx)
                                        indexJ = self.indexOf(cornerTwo,approx)
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
                                            returnedpoints = self.NumberOfPointInBetween(cornerThree,cornerFour,approx)
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
                                                    vaildPoint=self.CheckForCurve(startCheck,endCheck,approx)
                                                    indexK = self.indexOf(cornerThree,approx)
                                                    indexL = self.indexOf(cornerFour,approx)
                                                if(vaildPoint):
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
                                                                vaildPoint=self.CheckForCurve(startCheck,endCheck,approx)
                                                                indexI = self.indexOf(cornerOne,approx)
                                                                indexL = self.indexOf(cornerFour,approx)
        
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
            self.setPropertyOfCorner(approx,contoursPi)
    def showImage(self):
            cv2.imshow("Thks dv",self.image)
            cv2.waitKey(0);
    def showGraphs(self):
        newImageAppro1 = np.zeros((500,500,3), np.uint8)
        for i in range(0,len(self.pointA)-1):
            point1 = self.pointA[i]
            point2 = self.pointA[i+1]
            cv2.line(newImageAppro1,(point1[0],point1[1]),(point2[0],point2[1]), (255,255,255), 1)
        cv2.imshow("graph 1",newImageAppro1)

        newImageAppro2 = np.zeros((500,500,3), np.uint8)
        for i in range(0,len(self.pointB)-1):
            point1 = self.pointB[i]
            point2 = self.pointB[i+1]
            cv2.line(newImageAppro2,(point1[0],point1[1]),(point2[0],point2[1]), (255,255,255), 1)
        cv2.imshow("graph 2",newImageAppro2) 
 
        newImageAppro3 = np.zeros((500,500,3), np.uint8) 
        for i in range(0,len(self.pointC)-1):
            point1 = self.pointC[i]
            point2 = self.pointC[i+1]
            cv2.line(newImageAppro3,(point1[0],point1[1]),(point2[0],point2[1]), (255,255,255), 1)
        cv2.imshow("graph 3",newImageAppro3) 
        newImageAppro4 = np.zeros((500,500,3), np.uint8)  
        for i in range(0,len(self.pointD)-1):
            point1 = self.pointD[i]
            point2 = self.pointD[i+1]
            cv2.line(newImageAppro4,(point1[0],point1[1]),(point2[0],point2[1]), (255,255,255), 1)
        cv2.imshow("graph 4",newImageAppro4)