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

class match:
    
    
    def __init__(self, pieces):
        self.jigsawpieces=pieces

    #get the angle between the two point send
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

    #checks if the two angle send can have a match for a piece or not
    def samesection(self,anglea,angleb):
        if((0<=anglea<=45 or anglea>=315  or  135<=anglea<=225)  and (0<=angleb<=45 or angleb>=315  or  135<=angleb<=225)):
            return True
        elif((45<anglea<135  or 225<anglea<315)  and (45<angleb<135  or 225<angleb<315)):
            return True
        else:
            return False
    
    #get the distance of two given points

    def getDistance(self,pointA,pointB):
        return ((pointB[0]-pointA[0]) ** 2 + (pointB[1]-pointA[1]) ** 2 ) ** 0.5

    #calculates the length of the side 
    #recieve a side
    def lengthofside(self,side):
        length = 0
        for i in range(0,len(side.axismatchside)-1):
            pointa = side.axismatchside[i]
            pointb = side.axismatchside[i+1]
            length = length + self.getDistance(pointa,pointb)
        return length
    
    #
    #decides if the two side can match or not
    #this is decided on the basics of that the lenght and the angle of the side
    def canmatchAngle(self,sidea,sideb):
        pointa = sidea.axismatchside
        pointb = sideb.axismatchside
        canMatch = True
        anglea = self.getAngle(pointa[0],pointa[len(pointa)-1])
        angleb = self.getAngle(pointb[0],pointb[len(pointb)-1])
        canMatch = self.samesection(anglea,angleb)
        lengtha = self.lengthofside(sidea)
        lengthb = self.lengthofside(sideb)
        if(max(lengtha,lengthb) - min(lengtha,lengtha) > 3):
           canMatch=False

        return canMatch
    def getresult(self):
        corner = []
        border = []
        center = []
        mapresult = []
        possiblebordermacth = []
        for i in range(0,len(self.jigsawpieces)):
            eachPiece = self.jigsawPieces[i]
            if(eachPiece.isCornerPiece):
                corner.append(eachPiece)
            if(eachPiece.isBorderPiece):
                border.append(eachPiece)
                possiblebordermacth.append(eachPiece)
            if(eachPiece.isCenterPiece):
                center.append(eachPiece)
        match = matching()
        
        for i in range(0,len(corner)):
            eachPiece = corner[i]
            print("Corner ",i)
            for j in range(0,len(eachPiece.side)):
                side = eachPiece.side[j]
                if(not side.isStraight):
                    print("Side ",j)
                    possibleMatch = []
                    for k in range(0, len(border)):
                        borderpiece = border[k]
                        print("--------------------------------------------------------------------------")
                        print("Border ",k)
                        for l in range(0, len(borderpiece.side)):
                            sideMatch = borderpiece.side[k]
                            if(not sideMatch.isStraight and ((side.isConvex and sideMatch.isConcave) or (side.isConcave and sideMatch.isConvex))):
                                print("Side ",l)
                                canMatch = self.canmatchAngle(side,sideMatch)
                                if(canMatch):
                                    possibleMatch.append([borderpiece,l,k])
                    for k in range(0,len(possibleMatch)):
                        possibleMatchm = possibleMatch[k][0]
                        possibleMatchm.showImage("Border piece "+str(possibleMatch[k][2])+"  side "+str(possibleMatch[k][1]))
                    cv2.waitKey(0)
                        
                    
                
            