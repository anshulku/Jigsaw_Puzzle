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
from sympy import pi,mpmath

class sideOfPieces:
    def __init__(self,right,left):
        self.contourpoints = []
        self.x_axis_Points=[]
        self.x_axis_PointsApprox = []

        self.x_subampledpoints = []
        self.y_subampledpoints = []

        self.pointsStart = []
        self.pointsEnd = []

        #not going to use any more

        self.cornerRight=right
        self.cornerLeft=left
        self.splitstart = []
        self.splitcurve = []
        self.curvecenter = []
        self.splitend = []
        #point iam using now
        self.approxPoints = []
        self.originalPoints=[]
        self.isStraight = False
        self.isConvex = False
        self.isConcave = False
        self.approxmatchside = []
        self.axismatchside = []
        self.axismatchsidereverse = []
        self.whichaxis = ""
        self.lengthofside = 0
        self.aboveorbelow = True
        self.samplept = []
        self.sampleptreverse = []
        self.direction = ""
        
        
    def getmincornerpoint(self):
        if(self.whichaxis == "X"):
            if( self.cornerRight[0] < self.cornerLeft[0]):
                return self.cornerRight
            else:
                return self.cornerLeft
        else:
            if( self.cornerRight[1] < self.cornerLeft[1]):
                return self.cornerRight
            else:
                return self.cornerLeft
    def getmaxcornerpoint(self):
        if(self.whichaxis == "X"):
            if( self.cornerRight[0] < self.cornerLeft[0]):
                return self.cornerLeft
            else:
                return self.cornerRight
        else:
            if( self.cornerRight[1] < self.cornerLeft[1]):
                return self.cornerLeft
            else:
                return self.cornerRight
    def get_line(x1, y1, x2, y2):
        points = []
        issteep = abs(y2-y1) > abs(x2-x1)
        if issteep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        rev = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            rev = True
        deltax = x2 - x1
        deltay = abs(y2-y1)
        error = int(deltax / 2)
        y = y1
        ystep = None
        if y1 < y2:
            ystep = 1
        else:
            ystep = -1
        for x in range(x1, x2 + 1):
            if issteep:
                points.append((y, x))
            else:
                points.append((x, y))
            error -= deltay
            if error < 0:
                y += ystep
                error += deltax
        # Reverse the list if the coordinates were reversed
        if rev:
            points.reverse()
        return points
    

    
    # for getting the break point (initalliy the start and the end of the graph)
    def split(self,name="default",testing=False):
        imageSplit1 = np.zeros((500,500,3), np.uint8) 
        imageSplit2 = np.zeros((500,500,3), np.uint8) 
        imageSplit3 = np.zeros((500,500,3), np.uint8) 
        startpoint = []
        curvepoint = []
        endpoint = []
        if(len(self.x_axis_PointsApprox)<1):
            return
        startpointcurve = [self.x_axis_PointsApprox[1][0],self.x_axis_PointsApprox[1][1]]
        endpointcurve = [self.x_axis_PointsApprox[len(self.x_axis_PointsApprox)-2][0],self.x_axis_PointsApprox[len(self.x_axis_PointsApprox)-2][1]]
        #print("--------------------------------------------------")
        #print(startpointcurve[0],"  ; ",startpointcurve[1])
        #print(endpointcurve[0],"  ; ",endpointcurve[1])
        #print("--------------------------------------------------")
        #print("--------------------------------------------------")
        flag = "Begin"
        for i in range(0, len(self.x_axis_Points)):
            x1 = self.x_axis_Points[i][0]
            y1 = self.x_axis_Points[i][1]
            if(flag == "Begin"):
                startpoint.append([x1,y1])
            elif(flag == "curve"):
                curvepoint.append([x1,y1])
            elif(flag == "End"):
                endpoint.append([x1,y1])

            if(x1==startpointcurve[0] and y1==startpointcurve[1]):
                curvepoint.append([x1,y1])
                flag="curve"
            if(x1==endpointcurve[0] and y1==endpointcurve[1]):
                endpoint.append([x1,y1])
                flag="End"
        for i in range(0,len(startpoint)-1):
            x1 = startpoint[i][0]
            y1 = startpoint[i][1]
            x2 = startpoint[i+1][0]
            y2 = startpoint[i+1][1]
            cv2.line(imageSplit1,(int(x1),int(y1)),(int(x2),int(y2)), (255,255,255), 1)
        for i in range(0,len(curvepoint)-1):
            x1 = curvepoint[i][0]
            y1 = curvepoint[i][1]
            x2 = curvepoint[i+1][0]
            y2 = curvepoint[i+1][1]
            cv2.line(imageSplit2,(int(x1),int(y1)),(int(x2),int(y2)), (255,255,255), 1)
        for i in range(0,len(endpoint)-1):
            x1 = endpoint[i][0]
            y1 = endpoint[i][1]
            x2 = endpoint[i+1][0]
            y2 = endpoint[i+1][1]
            cv2.line(imageSplit3,(int(x1),int(y1)),(int(x2),int(y2)), (255,255,255), 1)
        #cv2.circle(newImageAppro,(int(self.x_axis_PointsApprox[1][0]),int(self.x_axis_PointsApprox[1][1])), 3, (0,0,255), 1)
        #cv2.circle(newImageAppro,(int(self.x_axis_PointsApprox[len(self.x_axis_PointsApprox)-2][0]),int(self.x_axis_PointsApprox[len(self.x_axis_PointsApprox)-2][1])), 3, (0,0,255), 1)
        #cv2.imshow(str(name)+" First",imageSplit1)
        #cv2.imshow(str(name)+" curve",imageSplit2)
        #cv2.imshow(str(name)+" end",imageSplit3)
        self.splitstart = startpoint
        self.splitcurve = curvepoint
        self.splitend = endpoint

        x1 = curvepoint[0][0]
        y1 = curvepoint[0][1]
        x2 = curvepoint[len(curvepoint)-1][0]
        y2 = curvepoint[len(curvepoint)-1][1]
        x = (x1+x2)/2
        y = (y1+y2)/2
        self.curvecenter = [x,y]
        #if(testing):
        #    print("----------------------------------------")
        #    print("----------------------------------------")
        #    print("Start ",startpoint)
        #    print("----------------------------------------")
        #    print("----------------------------------------")
        #    print("Curve ",curvepoint)
        #    print("----------------------------------------")
        #    print("----------------------------------------")
        #    print("End ",endpoint)
        
    
    def appendpoint(self,pointA, pointB, reverseAdd = False):
        start = 0
        end = len(pointA)
        increment = 1
        if(reverseAdd):
            start = len(pointA)-1
            end = -1
            increment = -1
        for i in range(start, end, increment):
            pointB.append(pointA[i])
    def subsampling(self, side, name="Default",testing = False):
        x = []
        y = []
        for i in range(0,len(side)-1):
            x1 = [side[i][0],side[i+1][0]]
            y1 = [side[i][1],side[i+1][1]]
            if(testing):
                print("---------------------------------------------")
                print("X1 of the array")
                print(x1)
                print("Y1 of the array")
                print(y1)
                print("---------------------------------------------")
            eq =np.polyfit(x1,y1,1)
            if(x1[1]<x1[0]):
                newx = []
                start =int(x1[1])
                end = x1[0]
                if(len(x)>=1 and x[len(x)-1] == int(x1[1])):
                    start =int(x1[1]+1)
                    end = x1[0]
                if(start < x1[1]):
                    start = start+1
                newx = np.arange(start,end)  

                newy = newx * eq[0] + eq[1]
                self.appendpoint(newx,x,reverseAdd = True)
                self.appendpoint(newy,y,reverseAdd=True)
            else:
                newx = []
                start =int(x1[0])
                end = x1[1]
                if(len(x)>=1 and x[len(x)-1] == int(x1[0])):
                    start =int(x1[0]+1)
                    end = x1[1]
                if(start < x1[0]):
                    start = start+1
                newx = np.arange(start,end)    
                newy = newx * eq[0] + eq[1]
                self.appendpoint(newx,x)
                self.appendpoint(newy,y)
            
            #if(testing):
            #    newImageAppro1 = np.zeros((500,500,3), np.uint8)
            #    for j in range(0,len(x)-1):
            #        x1 = x[j]
            #        x2 = x[j+1]
            #        y1 = y[j]
            #        y2 = y[j+1]
            #        cv2.line(newImageAppro1,(int(x1),int(y1)),(int(x2),int(y2)), (255,255,255), 1)
            #    for j in range(0,i+1):
            #        pointA = sideA.x_axis_Points[j]
            #        pointB = sideA.x_axis_Points[j+1]
            #        cv2.line(newImageAppro1,(int(pointA[0]),int(pointA[1])),(int(pointB[0]),int(pointB[1])), (0,0,255), 1)
            #    cv2.imshow("Testing image ",newImageAppro1)
            #    cv2.waitKey(0)


            if(testing):
                print("----------------------------------------------------------")
                print("PRINTING X")
                print(x)
                print("PRINTING Y")
                print(y)
                print("-----------------------------------------------------------")
        if(x == []):
            return []
        return [x,y]
    def setsamples(self,sampleside):
        
        for i in range(len(sampleside[0])):
            print(sampleside[0][i],"  ;  ",sampleside[1][i])
    '''
        setting the subsampling and storing them
    '''
    def appedinrightorder(self,ntarrange):
        if(ntarrange == []):
            return []
        #print("----------------------------------------------")
        arrange = []
        for i in range(0,len(ntarrange[0])):
            
            #print("in loop : ",[ntarrange[0][i],ntarrange[1][i]])
            arrange.append([ntarrange[0][i],ntarrange[1][i]])
        #print("the combine x")
        #for i in range(0,len(arrange)):
        #    print(arrange[i][0]," ::  ",arrange[i][1])
        #print("----------------------------------------------")
        return arrange
    def setsubsampling(self,sent):
        sent.splitstart = self.appedinrightorder(sent.subsampling(sent.splitstart))
        #print("-----------Printing--------------",sent.splitstart )
        #print("-----------Printing start--------------")
        #self.setsamples(startcurvesample)
        sent.splitcurve = self.appedinrightorder(sent.subsampling(sent.splitcurve))
        #print("-----------Printing curve--------------")
        #self.setsamples(curvesample)
        sent.splitend = self.appedinrightorder(sent.subsampling(sent.splitend))
        #print("-----------Printing end--------------")
        #self.setsamples(endcurvesample)
        #print("-----------Printing finished--------------")
        

        #sent.showside("CStart 1",sent.splitstart)
        #sent.showside("Ccurve 1",sent.splitcurve)
        #sent.showside("Cend 1",sent.splitend)

        #startcurvesample2 = sent2.subsampling(sent2.splitstart)
        #curvesample2 = sent2.subsampling(sent2.splitcurve)
        #endcurvesample2 = sent2.subsampling(sent2.splitend)
        #sent.showside("BStart 1",sent2.splitstart)
        #sent.showside("Bcurve 1",sent2.splitcurve)
        #sent.showside("Bend 1",sent2.splitend)

        #self.showsubsample("MStart 2",startcurvesample,startcurvesample2)
        #self.showsubsample("Mcurve 2",curvesample,curvesample2)
        #self.showsubsample("Mend 2",endcurvesample,endcurvesample2)
    def showsubsample(self, name, sent, sent2):
        x = sent[0]
        y = sent[1]
        newImageAppro1 = np.zeros((500,500,3), np.uint8)
        for i in range(0,len(x)-1):
            point1 = [x[i],y[i]]
            point2 = [x[i+1],y[i+1]]
            cv2.line(newImageAppro1,(int(point1[0]),int(point1[1])),(int(point2[0]),int(point2[1])), (255,255,255), 1)
        
        x = sent2[0]
        y = sent2[1]
        for i in range(0,len(x)-1):
            point1 = [x[i],y[i]]
            point2 = [x[i+1],y[i+1]]
            cv2.line(newImageAppro1,(int(point1[0]),int(point1[1])),(int(point2[0]),int(point2[1])), (0,0,255), 1)
        cv2.imshow(name,newImageAppro1)

    

    def printsubsample(self,side):
        print("---------------------PRINTING SIDE SUBSAMPLING-----------------------------")
        print("---------------------START-----------------------------")
        
        for i in range(0,len(side.splitstart)):
            x1 = side.splitstart[i][0]
            y1 = side.splitstart[i][1]
            print(side.splitstart[i])
        print("---------------------CURVE-----------------------------")
        for i in range(0,len(side.splitcurve)):
            x1 = side.splitcurve[i][0]
            y1 = side.splitcurve[i][1]
            print(x1," ; ",y1)
        print("---------------------END-----------------------------")
        for i in range(0,len(side.splitend)):
            x1 = side.splitend[i][0]
            y1 = side.splitend[i][1]
            print(x1," ; ",y1)
        
    def showTwosplit(self,sideA,sideB,name="Default"):
        imageSplit1 = np.zeros((500,500,3), np.uint8) 
        imageSplit2 = np.zeros((500,500,3), np.uint8) 
        imageSplit3 = np.zeros((500,500,3), np.uint8) 

        for i in range(0,len(sideB.splitstart)-1):
            x1 = sideB.splitstart[i][0]
            y1 = sideB.splitstart[i][1]
            x2 = sideB.splitstart[i+1][0]
            y2 = sideB.splitstart[i+1][1]
            cv2.line(imageSplit1,(int(x1),int(y1)),(int(x2),int(y2)), (0,0,255), 1)
        for i in range(0,len(sideB.splitcurve)-1):
            x1 = sideB.splitcurve[i][0]
            y1 = sideB.splitcurve[i][1]
            x2 = sideB.splitcurve[i+1][0]
            y2 = sideB.splitcurve[i+1][1]
            cv2.line(imageSplit2,(int(x1),int(y1)),(int(x2),int(y2)), (0,0,255), 1)
        for i in range(0,len(sideB.splitend)-1):
            x1 = sideB.splitend[i][0]
            y1 = sideB.splitend[i][1]
            x2 = sideB.splitend[i+1][0]
            y2 = sideB.splitend[i+1][1]
            cv2.line(imageSplit3,(int(x1),int(y1)),(int(x2),int(y2)), (0,0,255), 1)
        for i in range(0,len(sideA.splitstart)-1):
            x1 = sideA.splitstart[i][0]
            y1 = sideA.splitstart[i][1]
            x2 = sideA.splitstart[i+1][0]
            y2 = sideA.splitstart[i+1][1]
            cv2.line(imageSplit1,(int(x1),int(y1)),(int(x2),int(y2)), (255,255,255), 1)
        for i in range(0,len(sideA.splitcurve)-1):
            x1 = sideA.splitcurve[i][0]
            y1 = sideA.splitcurve[i][1]
            x2 = sideA.splitcurve[i+1][0]
            y2 = sideA.splitcurve[i+1][1]
            cv2.line(imageSplit2,(int(x1),int(y1)),(int(x2),int(y2)), (255,255,255), 1)
        for i in range(0,len(sideA.splitend)-1):
            x1 = sideA.splitend[i][0]
            y1 = sideA.splitend[i][1]
            x2 = sideA.splitend[i+1][0]
            y2 = sideA.splitend[i+1][1]
            cv2.line(imageSplit3,(int(x1),int(y1)),(int(x2),int(y2)), (255,255,255), 1)

        cv2.imshow(str(name)+" First",imageSplit1)
        cv2.imshow(str(name)+" curve",imageSplit2)
        cv2.imshow(str(name)+" end",imageSplit3)



    def showTwoSides(self,sideA,sideB,name):
        image = np.zeros((500,500,3), np.uint8) 
        

        for i in range(0,len(sideA)-1):
            x1 = sideA[i][0]
            y1 = sideA[i][1]
            x2 = sideA[i+1][0]
            y2 = sideA[i+1][1]
            cv2.line(image,(int(x1),int(y1)),(int(x2),int(y2)), (255,255,255), 1)
        for i in range(0,len(sideB)-1):
            x1 = sideB[i][0]
            y1 = sideB[i][1]
            x2 = sideB[i+1][0]
            y2 = sideB[i+1][1]
            cv2.line(image,(int(x1),int(y1)),(int(x2),int(y2)), (0,0,255), 1)
        
        cv2.imshow(name,image)
        


   

    def  showside(self, sent,name):
        #if(testing):
        #    print("----------------************_---------------")
        #    print(sent)
        newImageAppro1 = np.zeros((500,500,3), np.uint8)
        for i in range(0,len(sent)-1):
            point1 = sent[i]
            point2 = sent[i+1]
            #cv2.circle(newImageAppro1,(int(point1[0]),int(point1[1])), 3, (255,255,255), 1)
            #cv2.imshow(name, newImageAppro1)
            #cv2.waitKey(0)
            cv2.line(newImageAppro1,(int(point1[0]),int(point1[1])),(int(point2[0]),int(point2[1])), (255,255,255), 1)
        #for i in range(0,len(sent2)-1):
        #    point1 = sent2[i]
        #    point2 = sent2[i+1]
        #    #cv2.circle(newImageAppro1,(int(point1[0]),int(point1[1])), 3, (255,255,255), 1)
        #    #cv2.imshow(name, newImageAppro1)
        #    #cv2.waitKey(0)
        #    cv2.line(newImageAppro1,(int(point1[0]),int(point1[1])),(int(point2[0]),int(point2[1])), (0,0,255), 1)
        #newImageAppro2 = np.zeros((500,500,3), np.uint8)
        #for i in range(0,len(self.originalPoints)-1):
        #    point1 = self.originalPoints[i]
        #    point2 = self.originalPoints[i+1]
        #    cv2.line(newImageAppro2,(int(point1[0]),int(point1[1])),(int(point2[0]),int(point2[1])), (255,255,255), 1)
      
        
        #dst = cv2.fastNlMeansDenoisingColored(newImageAppro2,None,10,20,7,5)
        #gryPiec = cv2.cvtColor(dst,cv2.COLOR_RGB2GRAY)
        #rows,cols = gryPiec.shape
        #M = cv2.getRotationMatrix2D((20,20),90,1)
        #dst = cv2.warpAffine(newImageAppro2,M,(cols,rows))
        cv2.imshow(name,newImageAppro1)
        #cv2.imshow(name+str(" TEsting"),dst)











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
        return newAngle
    def showXaxisGraph(self,points):
        originAngle = (self.getAngle(points[0],points[len(points)-1]))
        newFirstX = 200
        newFirstY = 200
        newPoints = [[newFirstX,newFirstY]]
        point1 = points[0]
        for i in range(1,len(points)):
            point2 = points[i]
            angle = (self.getAngle(point1,point2))
            distance = self.getDistance(point1,point2)
            newX = newFirstX + (distance * math.cos(math.radians(-angle)))
            newY = newFirstY + (distance * math.sin(math.radians(-angle)))
            newPoints.append([newX,newY])
        return newPoints
    
    def makeX_axisGraphs(self):
            self.axismatchside = self.showXaxisGraph(self.originalPoints)
            point = []
            for i in range(len(self.originalPoints)-1,-1,-1):
                point.append(self.originalPoints[i])
            self.axismatchsidereverse =  self.showXaxisGraph(point)
            self.approxmatchside = self.showXaxisGraph(self.approxPoints)
            
            return self.approxmatchside
    #checks if the two angle send can have a match for a piece or not
    def samesection(self,anglea):
        if((0<=anglea<=45 or anglea>=315  or  135<=anglea<=225)  and (0<=angleb<=45 or angleb>=315  or  135<=angleb<=225)):
            return [True,"X"]
        elif((45<anglea<135  or 225<anglea<315)  and (45<angleb<135  or 225<angleb<315)):
            return [True,"Y"]
        else:
            return [False]
    # make the liner eqution for given two points
    #return an array in which the first position contains the slope         
    # and the second position contains the constant 
    #if the line is on 90 degree then it return 0 and the x cordinate with it 
    def linerEquation(self,pointa,pointb):
        x1 = pointa[0]
        y1 = pointa[1]
        x2 = pointb[0]
        y2 = pointb[1]
        m = 0 
        c = x1
        if(not x1 == x2):
            c = (x2*y1-x1*y2)/(x2-x1)
            m = (y2-c)/x2
            if(m==0):
                c = y1

        return [m,c]
    #
    # return the number between pointa and point b
    #
    def getrange(self,pointa,pointb):
        start = int(min(pointa,pointb))
        end = int(max(pointa,pointb))
        x = []
        for i in range(start,end):
            x.append(i)
        if(start==end):
            return [[start],False]
        return [x,start==pointa]
    # subsamples the data across x axis
    def subsamplingxaxis(self,side):
        x = []
        y = []
        for i in range(0,len(side)-1):
            pointa = side[i]
            pointb = side[i+1]
            eq = self.linerEquation(pointa,pointb)
            rangexside = self.getrange(pointa[0],pointb[0])
            rangex = rangexside[0]
            rangey = []
            if(eq[0]==0):
                if(eq[1]==pointa[1]):  #meaning that the constant is y so the slope is zero
                    for j in range(0,len(rangex)):
                        rangey.append(pointa[1])
                elif(eq[1]==pointa[0]): #meaning that the constant is x so the slope is infinty
                    for j in range(0,len(rangex)):
                        rangey.append(pointa[1])
            else:
                    for j in range(0,len(rangex)):
                        rangey.append(eq[0]*rangex[j] + eq[1])

            if(rangexside[1]):
                 for j in range(0,len(rangex)):
                    x.append(rangex[j])
                    y.append(rangey[j])
            else:
                 for j in range(len(rangex)-1,-1,-1):
                    x.append(rangex[j])
                    y.append(rangey[j])
                
            
        return [x,y]
    # subsamples the data across y axis
    def subsamplingyaxis(self,side):
        x = []
        y = []
        for i in range(0,len(side)-1):
            pointa = side[i]
            pointb = side[i+1]
            eq = self.linerEquation(pointa,pointb)
            rangexside = self.getrange(pointa[1],pointb[1])
            rangey = rangexside[0]
            rangex = []
            if(eq[0]==0):
                if(eq[1]==pointa[1]):  #meaning that the constant is y so the slope is zero
                    for j in range(0,len(rangey)):
                        rangex.append(pointa[0])
                elif(eq[1]==pointa[0]): #meaning that the constant is x so the slope is infinty
                    for j in range(0,len(rangey)):
                        rangex.append(pointa[0])
            else:
                    for j in range(0,len(rangey)):
                        rangex.append((rangey[j]-eq[1])/eq[0])

            if(rangexside[1]):
                 for j in range(0,len(rangey)):
                    x.append(rangex[j])
                    y.append(rangey[j])
            else:
                 for j in range(len(rangey)-1,-1,-1):
                    x.append(rangex[j])
                    y.append(rangey[j])
        return [x,y]
    #get the distance of two given points

    def getDistance(self,pointA,pointB):
        return ((pointB[0]-pointA[0]) ** 2 + (pointB[1]-pointA[1]) ** 2 ) ** 0.5

    #calculates the length of the side 
    #and set it to the variable
    def setlength(self):
        length = 0
        for i in range(0,len(self.axismatchside)-1):
            pointa = self.axismatchside[i]
            pointb = self.axismatchside[i+1]
            length = length + self.getDistance(pointa,pointb)
        self.lengthofside = length

      #checks if the two angle send can have a match for a piece or not
    def setwhichssection(self,anglea):
        
        if((0<=anglea<=45 or anglea>=315  or  135<=anglea<=225) ):
            self.whichaxis = "X"
        elif((45<anglea<135  or 225<anglea<315)):
            self.whichaxis = "Y"
    
    #tell if the graph is going in up direction or in below direction
    def setaboveorbelow(self):
        eq = self.linerEquation(self.approxmatchside[1],self.approxmatchside[len(self.approxmatchside)-2])
        flag = True
        if(self.whichaxis == "X"):
            if(eq[0]==0):
                y = eq[1]
                flag= self.approxmatchside[2][1]<=y
            else:
                y = eq[0]*self.approxmatchside[2][0] + eq[1]
                flag= self.approxmatchside[2][1]<=y
        elif(self.whichaxis == "Y"):
            if(eq[0]==0):
                flag= self.approxmatchside[2][0] < eq[1]
            else:
                x = (self.approxmatchside[2][1]-eq[1])/eq[0]
                flag= self.approxmatchside[2][0] < x
        self.aboveorbelow = flag
    #arranges the point from pointa in the right order
    def arrangethepoints(self,pointa):
        point = []
        for i in range(0,len(pointa[0])):       
            point.append([pointa[0][i],pointa[1][i]])
        return point
    def setsubsampling(self):
        pointo = []
        pointreverse = []
        if(self.whichaxis == "X"):
            pointo=self.subsamplingxaxis(self.axismatchside)
            pointreverse=self.subsamplingxaxis(self.axismatchsidereverse)
        elif(self.whichaxis == "Y"):
            pointo=self.subsamplingyaxis(self.axismatchside)
            pointreverse=self.subsamplingyaxis(self.axismatchsidereverse)
        self.samplept = self.arrangethepoints(pointo)
        self.sampleptreverse = self.arrangethepoints(pointreverse)
        
    #sets the neccesary data for matching the pieces
    def setsideproperty(self):
        if(not self.isStraight):
            #make the graph on a specific points
            self.makeX_axisGraphs()
            pointa = self.axismatchside
            angle = self.getAngle(pointa[0],pointa[len(pointa)-1])
            #sets the section of the graph meaning X-axis or Y-axis
            self.setwhichssection(angle)
            #sets the length of the graph
            self.setlength()
            #sets if the side is convex or concave 
            self.setaboveorbelow()
            # samples the data across the section of the original data
            self.setsubsampling()
        if(self.isStraight):
            angle = self.getAngle(self.cornerRight,self.cornerLeft)
            self.setwhichssection(angle)
            

    def testingthexaiss(self,name="null"):

        newImageAppro1 = np.zeros((500,500,3), np.uint8)
        sent = self.originalPoints
        for i in range(0,len(sent)-1):
            point1 = sent[i]
            point2 = sent[i+1]
            cv2.line(newImageAppro1,(int(point1[0]),int(point1[1])),(int(point2[0]),int(point2[1])), (0,0,255), 1)

        sent = self.makeX_axisGraphs()
        for i in range(0,len(sent)-1):
            point1 = sent[i]
            point2 = sent[i+1]
            cv2.line(newImageAppro1,(int(point1[0]),int(point1[1])),(int(point2[0]),int(point2[1])), (0,0,255), 1)
        cv2.imshow(name+str("corner"), newImageAppro1)