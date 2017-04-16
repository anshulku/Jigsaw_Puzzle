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
from pieces import pieces

class matching:
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
    def isMatchTestingStuff(self,sideA,sideB,name, test = False):
        newImageAppro1 = np.zeros((500,500,3), np.uint8)
        B=100
        G=100
        R=100
        if(test):

            for i in range(0,len(sideA.x_axis_Points)):
                point1 = sideA.x_axis_Points[i]
                cv2.circle(newImageAppro1,(int(point1[0]),int(point1[1])),1, (255,255,255), 1)
            for i in range(0,len(sideB.x_axis_Points)):
                point1 = sideB.x_axis_Points[i]
                cv2.circle(newImageAppro1,(int(point1[0]),int(point1[1])),1, (0,0,255), 1)
        
        else:

            for i in range(0,len(sideA.x_axis_Points)-1):
                point1 = sideA.x_axis_Points[i]
                point2 = sideA.x_axis_Points[i+1]
                cv2.line(newImageAppro1,(int(point1[0]),int(point1[1])),(int(point2[0]),int(point2[1])), (255,255,255), 1)
            for i in range(0,len(sideB.x_axis_Points)-1):
                point1 = sideB.x_axis_Points[i]
                point2 = sideB.x_axis_Points[i+1]
                cv2.line(newImageAppro1,(int(point1[0]),int(point1[1])),(int(point2[0]),int(point2[1])), (0,0,255), 1)
        #dst = cv2.fastNlMeansDenoisingColored(newImageAppro1,None,10,20,7,5)
        #    #print("hello")
        ##convertinf it into grayscale image
        #gryPiec = cv2.cvtColor(dst,cv2.COLOR_RGB2GRAY)
        ##making the threshold of the grayscaled image
        #ret, threshPie = cv2.threshold(gryPiec, 127, 255, cv2.THRESH_BINARY)
        ##dectecting the contours of the pieces    
        #im2Pi, contoursPi, hierarchyPi = cv2.findContours(threshPie, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
        ##making the contours of same colour and the background of same colour
        #var=contoursPi[0]
        #epsilon = 0.014*cv2.arcLength(var,True)
        #approx = cv2.approxPolyDP(var,epsilon,True)
        #newImageAppro22 = np.zeros((500,500,3), np.uint8) 
        #for varCo in range(0,len(approx)-1):
        #            varCord = approx[varCo]
        #            varCord2 = approx[varCo+1]
        #            cv2.line(newImageAppro22,(varCord[0][0],varCord[0][1]),(varCord2[0][0],varCord2[0][1]), (255,255,255), 1) 
        #cv2.imshow(str(name)+" t",newImageAppro22)
        cv2.imshow(str(name)+" points",newImageAppro1)
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

    def subsampling(self, sideA, name,testing = False):
        x = []
        y = []
        for i in range(0,len(sideA.x_axis_Points)-1):
            x1 = [sideA.x_axis_Points[i][0],sideA.x_axis_Points[i+1][0]]
            y1 = [sideA.x_axis_Points[i][1],sideA.x_axis_Points[i+1][1]]
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
                self.appendpoint(newx,x,True)
                self.appendpoint(newy,y,True)
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
                if(i==2):
                    print("range [x;y]" , x1[0],"  ;  ",y1[0]," -----  ", x1[1],"   ;  ",y1[1])
                    print("last x",x[len(x)-1])
                    print(newx)
                    print(newy)
                self.appendpoint(newx,x)
                self.appendpoint(newy,y)
            if(testing):
                newImageAppro1 = np.zeros((500,500,3), np.uint8)
                for j in range(0,len(x)-1):
                    x1 = x[j]
                    x2 = x[j+1]
                    y1 = y[j]
                    y2 = y[j+1]
                    cv2.line(newImageAppro1,(int(x1),int(y1)),(int(x2),int(y2)), (255,255,255), 1)
                for j in range(0,i+1):
                    pointA = sideA.x_axis_Points[j]
                    pointB = sideA.x_axis_Points[j+1]
                    cv2.line(newImageAppro1,(int(pointA[0]),int(pointA[1])),(int(pointB[0]),int(pointB[1])), (0,0,255), 1)
                cv2.imshow("Testing image ",newImageAppro1)
                cv2.waitKey(0)
                    
                
        sideA.x_subampledpoints = x
        sideA.y_subampledpoints = y
        



            
    def showsubsample(self,side,side2,name):
        newImageAppro1 = np.zeros((500,500,3), np.uint8)
        for i in range(0,len(side.x_subampledpoints)-1):
                x1 = side.x_subampledpoints[i]
                x2 = side.x_subampledpoints[i+1]
                y1 = side.y_subampledpoints[i]
                y2 = side.y_subampledpoints[i+1]
                cv2.line(newImageAppro1,(int(x1),int(y1)),(int(x2),int(y2)), (255,255,255), 1)



        newImageAppro2 = np.zeros((500,500,3), np.uint8)
        for i in range(0,len(side2.x_subampledpoints)-1):
                x1 = side2.x_subampledpoints[i]
                x2 = side2.x_subampledpoints[i+1]
                y1 = side2.y_subampledpoints[i]
                y2 = side2.y_subampledpoints[i+1]
                cv2.line(newImageAppro1,(int(x1),int(y1)),(int(x2),int(y2)), (0,0,255), 1)
        cv2.imshow(str(name),newImageAppro1)
        cv2.waitKey(0)
            
    def canMatch(self,sideA,sideB,name = "Deafult",test=False):
        begincurveA = sideA.splitstart
        curveA = sideA.splitcurve
        endcurveA = sideA.splitend

        begincurveB = sideB.splitstart
        curveB = sideB.splitcurve
        endcurveB = sideB.splitend
        if(len(begincurveA)<1):
            print(name," no  match  TEST")
            return False
        
        if(len(begincurveB)<1):
            print(name," no  match  TEST")
            return False
        begincurveB[0][0]
    
        begincurveB[len(begincurveB)-1][0]
        begincurveB[0][1]
        begincurveB[len(begincurveB)-1][1]

        
        beginlengthA = 0

        for i in range(0,len(begincurveA)-1):
            length = ((begincurveA[i][0]  -  begincurveA[i+1][0])**2  +(begincurveA[i][1]  -  begincurveA[i+1][1])**2)**0.5
            beginlengthA = beginlengthA + length



        beginlengthB = 0

        for i in range(0,len(begincurveB)-1):
            length = ((begincurveB[i][0]  -  begincurveB[i+1][0])**2  +(begincurveB[i][1]  -  begincurveB[i+1][1])**2)**0.5
            beginlengthB = beginlengthB + length
        
        #print("beginlengthA =  ",beginlengthA)
        #print("beginlengthB =  ",beginlengthB)
        #print("beginlengthA < (beginlengthB)*(3/4) =  ",beginlengthA < (beginlengthB)*(3/4))
        flag = True
        #if(beginlengthA < (beginlengthB)*(3/4)  or beginlengthB < (beginlengthB)*(3/4)):
        #    flag = False
        #    print(name," no  match")
        if(test):   
            print("---------------------------")
            print("---------------------------")
            print(name,"CAME")
            print((max([beginlengthA,beginlengthB]) - min([beginlengthA,beginlengthB])))
            print("beginlengthA =  ",beginlengthA)
            print("beginlengthB =  ",beginlengthB)
            len1 = 0
            for i in range(0,len(begincurveA)-1):
                len1 =  len1 + ((begincurveA[i][0]  -  begincurveA[i+1][0])**2  +(begincurveA[i][1]  -  begincurveA[i+1][1])**2)**0.5
            len2 = 0
            for i in range(0,len(begincurveB)-1):
                len2 =  len2 + ((begincurveB[i][0]  -  begincurveB[i+1][0])**2  +(begincurveB[i][1]  -  begincurveB[i+1][1])**2)**0.5
            print(len1 - len2)
            print("len1 =  ",len1)
            print("len2 =  ",len2)

            print("---------------------------")
            print("---------------------------")
        if((max([beginlengthA,beginlengthB]) - min([beginlengthA,beginlengthB])) > 3):
            flag = False
            
            print(name, "  No match")
            return False



        
        beginlengthA = 0

        for i in range(0,len(endcurveA)-1):
            length = ((endcurveA[i][0]  -  endcurveA[i+1][0])**2  +(endcurveA[i][1]  -  endcurveA[i+1][1])**2)**0.5
            beginlengthA = beginlengthA + length



        beginlengthB = 0

        for i in range(0,len(endcurveB)-1):
            length = ((endcurveB[i][0]  -  endcurveB[i+1][0])**2  +(endcurveB[i][1]  -  endcurveB[i+1][1])**2)**0.5
            beginlengthB = beginlengthB + length


        #beginlengthA = ((endcurveA[0][0]  -  endcurveA[len(endcurveA)-1][0])**2  +(endcurveA[0][1]  -  endcurveA[len(endcurveA)-1][1])**2)**0.5
        #beginlengthB = ((endcurveB[0][0]  -  endcurveB[len(endcurveB)-1][0])**2  +(endcurveB[0][1]  -  endcurveB[len(endcurveB)-1][1])**2)**0.5
       
       
        if((max([beginlengthA,beginlengthB]) - min([beginlengthA,beginlengthB])) > 3):
            flag = False
            print(name, "  No match")
            return False

        if(sideA.isConcave and sideB.isConvex or sideA.isConvex and sideB.isConcave ):
            print(name,"Maybe")
        else:
            flag = False
            print(name, "  No match")
            return False
        return flag
    '''
        grapha is smaller tha graphb
    '''
    def disintotal(self,grapha,graphb):
        dis = 0
        for i in range(0,len(grapha)):
            x1 = grapha[i][0]
            y1 = grapha[i][1]
            distance = []
            for j in range(i-5,i+6):
                if(j>=0 and j < len(graphb)):
                    x2 = graphb[j][0]
                    y2 = graphb[j][1]
                    x = (x1-x2)**2   
                    y = (y1-y2)**2
                    dis = (x + y)**(0.5)
                    distance.append([dis,j])
            smalldis = [30,-1]
            for j in range(0,len(distance)):
                if(distance[j][0]<smalldis[0]):
                    smalldis = distance[j]
            #print(grapha[i][0] , "  ; ",grapha[i][1], "  :  "  ,graphb[i][0] , "  ; ",graphb[i][1])
            #print("Distance = ",smalldis[0], " point match j = ",smalldis[1]," :: the point is ==  ",graphb[smalldis[1]] )
            dis = dis + smalldis[0]
        return dis
    def Match(self,sideA,setsideB):
        begincurveA = sideA.splitstart
        curveA = sideA.splitcurve
        endcurveA = sideA.splitend
        alldis = []
        for d in range(0,len(setsideB)):
            begincurveB = setsideB[d].splitstart
            curveB = setsideB[d].splitcurve
            endcurveB = setsideB[d].splitend
            
            length = 0
            flagwhich = True
            start = curveA
            end = curveB
            if(len(curveA) < len(curveB)):
                length = len(curveA)
                #flagwhich = True
                start = curveA
                end = curveB
            else:
                length = len(curveB)
                #flagwhich = False
                start = curveB
                end = curveA
            dis = self.disintotal(start,end)
            print("curve distance = " , dis)

            start = begincurveA
            end = begincurveB
            if(len(begincurveA) < len(begincurveB)):
                start = begincurveA
                end = begincurveB
            else:
                start = begincurveB
                end = begincurveA

            dis = dis + self.disintotal(start,end)
            print("begin curve distance = " , dis)

            start = endcurveA
            end = endcurveB
            if(len(endcurveA) < len(endcurveB)):
                start = endcurveA
                end = endcurveB
            else:
                start = endcurveB
                end = endcurveA

            dis = dis + self.disintotal(start,end)
            print("end distance = " , dis)
            ####

            alldis.append([dis,d])
            #print("flag :: ",flag)
        print(alldis)
    def aligned(self,sideA,sideB,Testing=False,name="Default"):
        begincurveA = sideA.splitstart
        curveA = sideA.splitcurve
        endcurveA = sideA.splitend

        begincurveB = sideB.splitstart
        curveB = sideB.splitcurve
        endcurveB = sideB.splitend
        
        goon = True
        i = 0
        flag = True
        beginlengthA=0
        while(goon):
            beginlengthA = round(begincurveA[i][1])  -  round(begincurveB[i][1])
            if(Testing):
                print(begincurveA[i][1],"  ::  ",begincurveB[i][1])
                print("beginlengthA  = ",beginlengthA)
                print("begincurveA[i][1]  -  begincurveB[i][1]  = ",begincurveA[i] ,"  :  ",  begincurveB[i])
            '''
        flag is use to know which line is above and which is below line
        if flag is true then a is above B
        if flag is false then a is below B
            '''
            if(beginlengthA<1e-8 and beginlengthA>=0 ):
                goon = True
                i = i+1
            elif(beginlengthA<0):
                flag = True
                goon = False
            elif(beginlengthA>0):
                flag = False
                goon = False
            
        
        length = 0
        if(len(begincurveA) < len(begincurveB)):
            length = len(begincurveA)
        else:
            length = len(begincurveB)
        i = 0
        isamatch = True
        if(Testing):
            print("Flag value = ",flag)
        for i in range(0,length):
            beginlengthA = round(begincurveA[i][1])  -  round(begincurveB[i][1])
            if(Testing):
                print(begincurveA[i][0] , "  ; ",begincurveA[i][1], "  :  "  ,begincurveB[i][0] , "  ; ",begincurveB[i][1])
                print("Disatance :: ",beginlengthA)
                #print("flag :: ",flag)
            if(not flag and beginlengthA<0):
                isamatch=False    
                print(name,"THE END 1  : ",flag)   
                break
            elif(flag and beginlengthA>0):
            
            #if((not beginlengthA<0 or not flag) and (not beginlengthA<0 or  flag) and not beginlengthA==0):
                isamatch=False    
                print(name,"THE END 1  : ",flag)   
                break

        length = 0
        if(len(endcurveA) < len(endcurveB)):
            length = len(endcurveA)
        else:
            length = len(endcurveB)
        i = 0
        for i in range(0,length):
            beginlengthA = round(endcurveA[i][1])  -  round(endcurveB[i][1])
            #print(begincurveA[i][0] , "  ; ",begincurveA[i][1], "  :  "  ,begincurveB[i][0] , "  ; ",begincurveB[i][1])
            #print("Disatance :: ",beginlengthA)
            #print("flag :: ",flag)
            
            if(not flag and beginlengthA<0):
                isamatch=False    
                print(name,"THE END 1  : ",flag)   
                break
            elif(flag and beginlengthA>0):
            
            #if((not beginlengthA<0 or not flag) and (not beginlengthA<0 or  flag) and not beginlengthA==0):
                isamatch=False    
                print(name,"THE END 1  : ",flag)   
                break

        if(isamatch):
            print(name,"MAYBE")
            return True
        else:
            print(name,"not a chance")
            return False


    def doesMatch(self,pieceA, pieceB,testing=False):
        distance = 0
        end = len(pieceB.x_subampledpoints)
        if(len(pieceA.x_subampledpoints) < len(pieceB.x_subampledpoints)):
            end = len(pieceA.x_subampledpoints)
        for i in range(0,end):
            x1 = pieceA.x_subampledpoints[i]
            y1 = pieceA.y_subampledpoints[i]  
            x2 = pieceB.x_subampledpoints[i] 
            y2 = pieceB.y_subampledpoints[i] 
            if(testing):
                print(int(x1),"  ;  ",int(y1),"  -  ",int(x2)," ;  ",int(y2))
            x = (x1-x2)**2   
            y = (y1-y2)**2
            dis = (x + y)**(0.5)
            distance = distance +dis

            newImageAppro1 = np.zeros((500,500,3), np.uint8)
            newImageAppro2 = np.zeros((500,500,3), np.uint8)
            for i in range(0,i+1):
                    x1 = pieceA.x_subampledpoints[i]
                    x2 = pieceA.x_subampledpoints[i+1]
                    y1 = pieceA.y_subampledpoints[i]
                    y2 = pieceA.y_subampledpoints[i+1]
                    cv2.line(newImageAppro1,(int(x1),int(y1)),(int(x2),int(y2)), (255,255,255), 1)
                    x1 = pieceB.x_subampledpoints[i]
                    x2 = pieceB.x_subampledpoints[i+1]
                    y1 = pieceB.y_subampledpoints[i]
                    y2 = pieceB.y_subampledpoints[i+1]
                    cv2.line(newImageAppro2,(int(x1),int(y1)),(int(x2),int(y2)), (0,0,255), 1)
            cv2.imshow("cor",newImageAppro1)
            cv2.imshow("bor 2",newImageAppro2)
            cv2.waitKey(0)
        print("Distance = ",distance)
    def isMatch(self,sideA,sideB):
        j=0
        tempPointA = [sideA.x_axis_Points[0]]
        for i in range(0,len(sideA.x_axis_Points)-1):
            pointA = sideA.x_axis_Points[i]
            pointB = sideA.x_axis_Points[i+1]
           
            while((pointA[0])<(pointB[0]) and not ((pointA[0])+1==(pointB[0])) and not ((pointA[0]))==(pointB[0])):
                Eq = self.LinerEquation(pointA,pointB)
                y = Eq[0][0] * (int(pointA[0])+1)+ Eq[0][1]
                tempPointA.append([int(pointA[0])+1,y])
                pointA=[int(pointA[0])+1,y]
        for i in range(0,len(tempPointA)):
            print(tempPointA[i][0]," ; ",tempPointA[i][1])

        newImageAppro1 = np.zeros((500,500,3), np.uint8)
        for i in range(0,len(tempPointA)-1):
            point1 = tempPointA[i]
            point2 = tempPointA[i+1]
            cv2.line(newImageAppro1,(int(point1[0]),int(point1[1])),(int(point2[0]),int(point2[1])), (255,255,255), 1)
        cv2.imshow("new corner piece now",newImageAppro1)
        print("----------------************_---------------")
        print("----------------************_---------------")
        print("----------------************_---------------")
        print("----------------************_---------------")
        print("----------------************_---------------")

        while(j<len(sideA.x_axis_Points) or j<len(sideB.x_axis_Points)):
            if(j<len(sideA.x_axis_Points)):
                pointA = sideA.x_axis_Points[j]
                print("Point Corner = ",pointA[0]," ; ",pointA[1])
            if(j<len(sideB.x_axis_Points)):
                pointA = sideB.x_axis_Points[j]
                print("Point Border = ",(pointA[0])," ; ",pointA[1])
            print("----------------************_---------------")
            j=j+1
        i = 0
        for i in range(0,len(sideA.x_axis_Points)):
            pointA = sideA.x_axis_Points[i]
            pointB = sideB.x_axis_Points[i]
            if(not (pointA[0] == pointB[0] and pointA[1] == pointB[1])):
                break
        if(len(sideA.x_axis_Points)==len(sideB.x_axis_Points)):
            print("TRUE")
        else:
            print("corner :",len(sideA.x_axis_Points))
            print("border :",len(sideB.x_axis_Points))
        if(i == len(sideA.x_axis_Points)):
            return True
        return False