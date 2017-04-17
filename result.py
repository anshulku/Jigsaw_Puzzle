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
from pieces import pieces
from matching import matching
from PIL import Image


class result:

    def __init__(self, pieces):
        self.jigsawpieces=pieces
        self.upperleftcorner = None
        self.upperrightcorner = None
        self.lowwerleftcorner = None
        self.lowwerrightcorner = None

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
            return [True,"X"]
        elif((45<anglea<135  or 225<anglea<315)  and (45<angleb<135  or 225<angleb<315)):
            return [True,"Y"]
        else:
            return [False]
    
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

    #tell if the graph is going in up direction or in below direction
    def aboveorbelow(self,approx,whichside,test=False):
        eq = self.linerEquation(approx[1],approx[len(approx)-2])
        #print("eq  ",eq)
        flag = True
        #if(test):
            #print("corner side")
        if(whichside == "X"):
            if(eq[0]==0):
                y = eq[1]
                flag= approx[2][1]<=y
            else:
                y = eq[0]*approx[2][0] + eq[1]
                flag= approx[2][1]<=y
            #print("approx[2] = ",approx[2])
            #print("approx[len(approx)-2] = ",approx[len(approx)-2])
            #print("approx[1] = ",approx[1])
            #print("y = ",y)
            #print("flag = ",flag)
        elif(whichside == "Y"):
            if(eq[0]==0):
                flag= approx[2][0] < eq[1]
            else:
                x = (approx[2][1]-eq[1])/eq[0]
                flag= approx[2][0] < x
        #newImageAppro2 = np.zeros((500,500,3), np.uint8)
        #for i in range(0,len(approx)-1):
        #    point1 = approx[i]
        #    point2 = approx[i+1]
        #    cv2.line(newImageAppro2,(int(point1[0]),int(point1[1])),(int(point2[0]),int(point2[1])), (255,255,255), 1)
        #cv2.circle(newImageAppro2,(int(approx[1][0]),int(approx[1][1])), 3, (255,255,255), 1)
        #cv2.circle(newImageAppro2,(int(approx[len(approx)-2][0]),int(approx[len(approx)-2][1])), 3, (255,255,255), 1)
        #cv2.imshow("PLS dv", newImageAppro2)
        #cv2.waitKey(0)
        return flag
            
    #
    #decides if the two side can match or not
    #this is decided on the basics of that the lenght and the angle of the side
    def canmatchAngle(self,sidea,sideb):
        pointa = sidea.axismatchside
        pointb = sideb.axismatchside
        canMatch = True
        anglea = self.getAngle(pointa[0],pointa[len(pointa)-1])
        angleb = self.getAngle(pointb[0],pointb[len(pointb)-1])
        section = self.samesection(anglea,angleb)
        canMatch = section[0]
        #print("PASS OR FAIL FOR WHICHAXIS =",canMatch)
        
        #checking the length of the sides
        lengtha = self.lengthofside(sidea)
        lengthb = self.lengthofside(sideb)
        test1 =max(lengtha,lengthb)
        test2 =min(lengtha,lengthb)
        if(test1 - test2 > 4):
           canMatch=False
        
        #print("PASS OR FAIL FOR LENGTH =",canMatch)
        #print("lengtha =",lengtha)
        #print("lengthb =",lengthb)
        #print("max(lengtha,lengthb) =",max(lengtha,lengthb))
        #print("min(lengtha,lengthb) =",min(lengtha,lengthb))
        #print("test1-test2 =",test1-test2)
        #print("max(lengtha,lengthb) - min(lengtha,lengtha) =",(max(lengtha,lengthb) - min(lengtha,lengtha)))
        approxa = sidea.approxmatchside
        approxb = sideb.approxmatchside
        if(section[0]):
            #print(" :: section[0] ; ",section[1])
            flaga = self.aboveorbelow(approxa,section[1],test=True)
            flagb = self.aboveorbelow(approxb,section[1])
            #print(" :: flaga ; ",flaga," :: flagb ; ",flagb)
            if(not flaga==flagb):
                canMatch=False
        #print("PASS OR FAIL FOR ABOVEORBELOW =",canMatch)
        if(section[0]):
            return [canMatch,section[1]]
        else:
            return [canMatch]
    #returns the side with the direction of given direction
    def getside(self,piece,direction):
        sidea = piece.side[0]
        sideb = piece.side[1]
        sidec = piece.side[2]
        sided = piece.side[3]
        #print(direction)
        #print(sidea.direction )
        #print(sideb.direction )
        #print(sidec.direction )
        #print(sided.direction )
        #print(sided.direction  == "TOP")
        #print(sided.direction  == direction)
        if(sidea.direction == direction):  
            return [sidea,0]
        if(sideb.direction == direction):  
            return [sideb,1]
        if(sidec.direction == direction): 
            return [sidec,2]
        if(sided.direction == direction): 
            return [sided,3]
        
    def getresult(self):
        corner = []
        border = []
        center = []
        possiblebordermacth = []
        for i in range(0,len(self.jigsawpieces)):
            eachPiece = self.jigsawpieces[i]

                
            if(eachPiece.isCornerPiece):
                if(eachPiece.name == "TL"): self.upperleftcorner = eachPiece
                if(eachPiece.name == "TR"):self.upperrightcorner = eachPiece
                if(eachPiece.name == "BL"):self.lowwerleftcorner = eachPiece
                if(eachPiece.name == "BR"):self.lowwerrightcorner = eachPiece
                corner.append(eachPiece)
            if(eachPiece.isBorderPiece):
                border.append(eachPiece)
                possiblebordermacth.append(eachPiece)
            if(eachPiece.isCenterPiece):
                center.append(eachPiece)
        #match = matching()
        #for i in range(0,len(corner)):
        #    eachPiece = corner[i]
        #    sidea = eachPiece.side[0]
        #    sideb = eachPiece.side[1]
        #    sidec = eachPiece.side[2]
        #    sided = eachPiece.side[3]
        #    print("sidea.direction = ",sidea.direction,"  sidea.isStraight=",sidea.isStraight)
        #    print("sideb.direction = ",sideb.direction,"  sidea.isStraight=",sideb.isStraight)
        #    print("sidec.direction = ",sidec.direction,"  sidea.isStraight=",sidec.isStraight)
        #    print("sided.direction = ",sided.direction,"  sidea.isStraight=",sided.isStraight)

        #    eachPiece.showImage("corner piece "+str(i))
            
        #    cv2.waitKey(0)
        
        #self.upperleftcorner.showImage("upperleftcorner")
        #self.upperrightcorner.showImage("upperrightcorner")
        #self.lowwerleftcorner.showImage("lowwerleftcorner")
        #self.lowwerrightcorner.showImage("lowwerrightcorner")
        #cv2.waitKey(0)
        mapresult = []
        flag = True 
        cornermatch = [self.upperleftcorner,
                        self.lowwerleftcorner,
                        self.lowwerrightcorner,
                        self.upperrightcorner]
        start = 0
        end = 1
        matchvector = []
        while(flag):
            #getting the start of the side of the puzzle
            if(end==4):
                end=0
            complete = False
            cornerstart = cornermatch[start]
            strsidea = cornerstart.side[0]
            strsideb = cornerstart.side[1]
            strsidec = cornerstart.side[2]
            strsided = cornerstart.side[3]

            #getting the end of the side of the puzzle
            cornerend = cornermatch[end]
            endsidea = cornerend.side[0]
            endsideb = cornerend.side[1]
            endsidec = cornerend.side[2]
            endsided = cornerend.side[3]

            matchside = None
            endmatchside = None
            matchsidei = 0
            endsidei = 0
            if(cornerstart.name=="TL"):
                sideachieved = self.getside(cornerstart,"BOTTOM")
                matchside = sideachieved[0]
                matchsidei = sideachieved[1]
                sideachieved = self.getside(cornerend,"TOP")
                endmatchside = sideachieved[0]
                endsidei = sideachieved[1]
            if(cornerstart.name=="BL"):
                sideachieved = self.getside(cornerstart,"RIGHT")
                matchside = sideachieved[0]
                matchsidei = sideachieved[1]
                sideachieved = self.getside(cornerend,"LEFT")
                endmatchside = sideachieved[0]
                endsidei = sideachieved[1]
            if(cornerstart.name=="BR"):
                sideachieved = self.getside(cornerstart,"TOP")
                matchside = sideachieved[0]
                matchsidei = sideachieved[1]
                sideachieved = self.getside(cornerend,"BOTTOM")
                endmatchside = sideachieved[0]
                endsidei = sideachieved[1]
            if(cornerstart.name=="TR"):
                sideachieved = self.getside(cornerstart,"LEFT")
                matchside = sideachieved[0]
                matchsidei = sideachieved[1]
                sideachieved = self.getside(cornerend,"RIGHT")
                endmatchside = sideachieved[0]
                endsidei = sideachieved[1]
            
            #getting the end corner
            piecematch = cornerstart
            rowvector = []
            while(not complete):
                #print("***********************************************************************************")
                possibleMatch = []
                for k in range(0, len(border)):
                    #print("--------------------------------------------------------------------------")
                    #print("Border ",k)
                    borderpiece = border[k]
                    for l in range(0, len(borderpiece.side)):
                        #print("Side ",l)
                        sideMatch = borderpiece.side[l]
                        if((not sideMatch.isStraight) and ((matchside.isConvex and sideMatch.isConcave) or (matchside.isConcave and sideMatch.isConvex))):
                            canMatch = self.canmatchAngle(matchside,sideMatch)
                            if(cornerstart.name == "TL" and not self.getside(borderpiece,"LEFT")[0].isStraight):
                                canMatch[0] = False
                            if(cornerstart.name == "BL" and not self.getside(borderpiece,"BOTTOM")[0].isStraight):
                                canMatch[0] = False
                            if(cornerstart.name == "BR" and not self.getside(borderpiece,"RIGHT")[0].isStraight):
                                canMatch[0] = False
                            if(cornerstart.name == "TR"and not self.getside(borderpiece,"TOP")[0].isStraight):
                                canMatch[0] = False
                            if(canMatch[0]):
                                possibleMatch.append([borderpiece,l])
                                #print("MAYBE ")
                #piecematch.showImage("piecematch end")
                #endmatchside.showside(cornerend.side[3].axismatchside,"love")
                canMatch=False
                if((not endmatchside.isStraight) and ((matchside.isConvex and endmatchside.isConcave) or (matchside.isConcave and endmatchside.isConvex))):
                    canMatch = self.canmatchAngle(matchside,endmatchside)
                    
                if(canMatch):
                    print("CORNER MAYBE")
                    possibleMatch.append([cornerend,endsidei])


                #for i in range(0,len(possibleMatch)):
                #    possibleMatchm = possibleMatch[i][0]
                #    possibleMatchm.showImage("possi piece "+str(i))
                    #matchside.showTwoSides(matchside.axismatchsidereverse,possibleMatchm.side[possibleMatch[i][1]].axismatchside,"Match two sides "+str(i))
                    #matchside.showTwoSides(matchside.sampleptreverse,possibleMatchm.side[possibleMatch[i][1]].samplept,"Match two sides "+str(i))

                if(len(possibleMatch) == 1):
                    rowvector.append([piecematch,matchside.direction,possibleMatch[0][0],possibleMatch[0][0].side[possibleMatch[0][1]].direction])
                    #possibleMatch[0][0].showImage("Matched piece ")
                    piecematch = possibleMatch[0][0]
                    if(cornerstart.name == "TL"):  
                        matchside = self.getside(piecematch,"BOTTOM")[0]
                        if(end == 0): flag=False
                        if(matchside.isStraight):
                            matchvector.append(rowvector)
                            complete = True
                            start = start+1
                            end = end+1

                    elif(cornerstart.name == "BL"):
                        matchside = self.getside(piecematch,"RIGHT")[0]
                        if(end == 0): flag=False
                        if(matchside.isStraight):
                            complete = True
                            start = start+1
                            end = end+1
                            matchvector.append(rowvector)

                    elif(cornerstart.name == "BR"):
                        matchside = self.getside(piecematch,"TOP")[0]
                        if(end == 0): flag=False
                        if(matchside.isStraight):
                            complete = True
                            start = start+1
                            end = end+1
                            matchvector.append(rowvector)

                    elif(cornerstart.name == "TR"):
                        matchside = self.getside(piecematch,"LEFT")[0]
                        if(end == 0): flag=False
                        if(matchside.isStraight):
                            complete = True
                            start = start+1
                            end = end+1
                            matchvector.append(rowvector)
                else:
                    distance = []
                    for i in range(0,len(possibleMatch)):
                        startpos = []
                        endpos = []
                        if(len(matchside.sampleptreverse) < len(possibleMatch[i][0].side[possibleMatch[i][1]].samplept)):
                            startpos = matchside.sampleptreverse
                            endpos = possibleMatch[i][0].side[possibleMatch[i][1]].samplept
    
                        else:
                            endpos = matchside.sampleptreverse
                            startpos = possibleMatch[i][0].side[possibleMatch[i][1]].samplept
                        diss =  self.disintotal(startpos,endpos)
                        #print(diss)
                        possibleMatch[i].append(diss)
                    match = self.smallerdistance(possibleMatch)

                    rowvector.append([piecematch,matchside.direction,match[0],match[0].side[match[1]].direction])
                    #match[0].showImage("Matched piece ")
                    
                    piecematch = match[0]
                    if(cornerstart.name == "TL"):  
                        matchside = self.getside(piecematch,"BOTTOM")[0]
                        if(end == 0): flag=False
                        if(matchside.isStraight):
                            matchvector.append(rowvector)
                            complete = True
                            start = start+1
                            end = end+1

                    elif(cornerstart.name == "BL"):
                        matchside = self.getside(piecematch,"RIGHT")[0]
                        if(end == 0): flag=False
                        if(matchside.isStraight):
                            matchvector.append(rowvector)
                            complete = True
                            start = start+1
                            end = end+1

                    elif(cornerstart.name == "BR"):
                        matchside = self.getside(piecematch,"TOP")[0]
                        if(end == 0): flag=False
                        if(matchside.isStraight):
                            matchvector.append(rowvector)
                            complete = True
                            start = start+1
                            end = end+1

                    elif(cornerstart.name == "TR"):
                        matchside = self.getside(piecematch,"LEFT")[0]
                        if(end == 0): flag=False
                        if(matchside.isStraight):
                            matchvector.append(rowvector)
                            complete = True
                            start = start+1
                            end = end+1
                    #disintotal
                #self.showresult(rowvector)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()
        #print(matchvector[0])
        #print("-----------------------------------------")
        #print("-----------------------------------------")
        #print(matchvector[1])
        #print("-----------------------------------------")
        #print("-----------------------------------------")
        #print("-----------------------------------------")
        #print("-----------------------------------------")")
        resultvector = []
        resultvector.append([matchvector[0][0][0]])
        for i in range(0,len(matchvector[0])):
            resultvector.append([matchvector[0][i][2]])

        for i in range(len(matchvector[3])-1,-1,-1):
            resultvector[0].append(matchvector[3][i][0])

        for i in range(0,len(matchvector[1])):
            resultvector[len(resultvector)-1].append(matchvector[1][i][2])
        print("-----------------------------------------------")
        print("MAtch vecote")
        print(matchvector)
        print("-----------------------------------------------")
        print("resultvector")
        print(resultvector)
        

        for dv in range(1,len(resultvector)-1):
            matchpiece = resultvector[dv][0]
            matchside = self.getside(matchpiece,"RIGHT")[0]
        
            print("-----------------------------------------------")
            
            for k in range(0,len(resultvector[0])-2):
                toppiece = resultvector[dv-1][k+1]
                possiblepiece = []
                matchpiece.showImage("piecseto be matched "+str(k))
                print("-----------------------------------------------")
                for i in range(0,len(center)):
                    print(" center = ",i)
                    centerpieces = center[i]
                    for j in range(0,len(centerpieces.side)):
                        print(" side = ",j)
                        sideMatch = centerpieces.side[j]
                        if(not sideMatch.isStraight and ((matchside.isConvex and sideMatch.isConcave) or (matchside.isConcave and sideMatch.isConvex))):
                            canMatch = self.canmatchAngle(matchside,sideMatch)
                            canMatch2 = self.canmatchAngle(self.getside(toppiece,"BOTTOM")[0],self.getside(centerpieces,"TOP")[0])
                            if(canMatch[0] and canMatch2[0]):
                                centerpieces.showImage("may be a match "+str(i))
                                possiblepiece.append([i,j])
                #for i in range(0,len(possiblepiece)):
                #        possibleMatchm = possiblepiece[i][0]
                #        possibleMatchm.showImage("possi piece "+str(i))
                #        startpos = []
                #        endpos = []
                #        if(len(matchside.sampleptreverse) < len(possiblepiece[i][1].samplept)):
                #            startpos = matchside.sampleptreverse
                #            endpos = possiblepiece[i][1].samplept
            
                #        else:
                #            endpos = matchside.sampleptreverse
                #            startpos = possiblepiece[i][1].samplept
                #        diss =  self.disintotal(startpos,endpos)
                #        print("possi piece "+str(i)+"  = ",diss)
                if(len(possiblepiece)==0):
                    for i in range(0,len(center)):
                                center[i].showImage("may be a match the only left pieec"+str(i))    
                cv2.waitKey(0)

                if(len(possiblepiece)==1):
                    resultvector[1].append(center[possiblepiece[0][0]])
                    matchpiece = center[possiblepiece[0][0]]
                    matchside = self.getside(center[possiblepiece[0][0]],"RIGHT")[0]
                    center[possiblepiece[0][0]].showImage("perfect match piece "+str(i))
                    center.pop(possiblepiece[0][0])
                    
                else:
                    distance = []
                    for j in range(0,len(possiblepiece)):
                        possibleMatchm = center[possiblepiece[j][0]]
                        startpos = []
                        endpos = []
                        if(len(matchside.sampleptreverse) < len(center[possiblepiece[j][0]].side[possiblepiece[j][1]].samplept)):
                            startpos = matchside.sampleptreverse
                            endpos = center[possiblepiece[j][0]].side[possiblepiece[j][1]].samplept
            
                        else:
                            endpos = matchside.sampleptreverse
                            startpos = center[possiblepiece[j][0]].side[possiblepiece[j][1]].samplept
                        diss =  self.disintotal(startpos,endpos)  
                        possiblepiece[j].append(diss)
        
                    match = self.smallerdistance(possiblepiece)
    
                    center[match[0]].showImage("perfect match piece "+str(i))
                    resultvector[1].append(center[match[0]])
                    matchpiece = center[match[0]]
                    matchside = self.getside(center[match[0]],"RIGHT")[0]

                    center.pop(match[0])
                        #match[0].showImage("Matched piece ")
                

                    #matchside.showTwoSides(matchside.axismatchsidereverse,possiblepiece[i][1].axismatchside,"Match Origin two sides "+str(i))
                    #matchside.showTwoSides(matchside.sampleptreverse,possiblepiece[i][1].samplept,"Match two sides "+str(i))
                cv2.waitKey(0)
                cv2.destroyAllWindows()
    def imcopy(self,image,target,x=0,y=0,extra = 0,change = False):
        height, width, channels = target.shape 
        height2, width2, channels2 = image.shape  
        for i in range(int(x),height2+int(x)):
            for j in range(int(y),width2+int(y)):
                test = image[i-x][j-y]
                b = test[0]
                g = test[1]
                r = test[2]
                if(b>230 and g>230 and r>230):
                    if(change):
                        test = [0,0,0]
                    else:
                        test = target[i][j]
                target[i][j] = test
        return [x,y]
    def showresult(self,rowvector):
        newImageAppro = np.zeros((700,700,3), np.uint8)  
        Oheight = 0
        l = rowvector[0]
        b = rowvector[1]
        r = rowvector[2]
        t = rowvector[3]  
        point = []
        for i in range(0,len(l)):  
            imagetesting = l[i][0].image
            height, width, channels = imagetesting.shape  
            if(i == len(l)-1):
                imagetesting2 = l[i][2].image
                height2, width2, channels2 = imagetesting2.shape
            if(i==0):
                point = self.imcopy(imagetesting,newImageAppro,x=Oheight,change=True)
                leftside = self.getside(l[i][0],"LEFT")[0]
                minpoint = leftside.getmincornerpoint()
                extra = round(self.getDistance([minpoint[0],0],minpoint) )
                Oheight=extra +round( self.getDistance(leftside.cornerRight,leftside.cornerLeft) )
            else: 
                leftside = self.getside(l[i][0],"LEFT")[0]
                minpoint = leftside.getmincornerpoint()
                extra = round(self.getDistance([minpoint[0],0],minpoint) )
                cutting = extra
                point = self.imcopy(imagetesting,newImageAppro,x=Oheight-cutting)
                leftside = self.getside(l[i][0],"LEFT")[0]
                Oheight=Oheight + round(self.getDistance(leftside.cornerRight,leftside.cornerLeft) )
            if(i == len(l)-1):
                leftside = self.getside(l[i][2],"LEFT")[0]
                minpoint = leftside.getmincornerpoint()
                extra = round(self.getDistance([minpoint[0],0],minpoint) )
                cutting = extra
                point = self.imcopy(imagetesting2,newImageAppro,x=Oheight-cutting)
            

        bottomside = self.getside(l[len(l)-1][2],"BOTTOM")[0]
        minpoint = bottomside.getmincornerpoint()
        extra = round(self.getDistance([0,minpoint[1]],minpoint) )

        Owidth= extra +round( self.getDistance(bottomside.cornerRight,bottomside.cornerLeft) )
        Oheight = point[0]
 
        print("  L  = ",l) 
        print("-----------------------------------------")
        print("  B  = ",r)
        for i in range(0,len(b)):   
            imagetesting = b[i][2].image
            height, width, channels = imagetesting.shape 

            bottomside = self.getside(b[i][2],"BOTTOM")[0]
            minpoint = bottomside.getmincornerpoint()
            extra = round(self.getDistance([minpoint[0],0],minpoint) )
            cutting = extra
            point = self.imcopy(imagetesting,newImageAppro,x=Oheight,y=Owidth-cutting) 
            Owidth=Owidth + round(self.getDistance(bottomside.cornerRight,bottomside.cornerLeft) )
            
            
            #for i in range(Oheight,500):
            #    for j in range(0,500):
            #        copy = [0,0,0]
            #        if(i<height and j<width):
            #            copy=imagetesting[i-Oheight][j]

            #        if(i>=height and flag):
            #            Oheight = Oheight + height
            #            flag = False

            #        if(i == len(rowvector)-1):
            #            if(i>=height and (i-Oheight)<height2 and j<width2):
            #                copy=imagetesting2[i-Oheight][j]
            #        newImageAppro[i][j] = copy
        cv2.imshow("testing",newImageAppro)
        #til = Image.new("RGB",(500,500))
        #til.paste(rowvector[0][0].image)
        #til.save("testtiles.png")
        #for i in range(0,len(corner)):
        #    eachPiece = corner[i]
        #    print("Corner ",i)
        #    for j in range(0,len(eachPiece.side)):
        #        side = eachPiece.side[j]
        #        if(not side.isStraight):
        #            print("Side ",j)
        #            possibleMatch = []
        #            for k in range(0, len(border)):
        #                borderpiece = border[k]
        #                print("--------------------------------------------------------------------------")
        #                print("Border ",k)
        #                for l in range(0, len(borderpiece.side)):
        #                    sideMatch = borderpiece.side[l]
        #                    if((not sideMatch.isStraight) and ((side.isConvex and sideMatch.isConcave) or (side.isConcave and sideMatch.isConvex))):
        #                        print("Side ",l)
        #                        print("sideMatch.isStraight ",sideMatch.isStraight)
        #                        canMatch = self.canmatchAngle(side,sideMatch)
        #                        if(canMatch[0]):
        #                            possibleMatch.append([borderpiece,l,k])

        #            eachPiece.showImage("corner piece "+str(i)+"  side "+str(j))
        #            for k in range(0,len(possibleMatch)):
        #                possibleMatchm = possibleMatch[k][0]

        #                possibleMatchm.showImage("Border piece "+str(possibleMatch[k][2])+"  side "+str(possibleMatch[k][1]))
        #            cv2.waitKey(0)
        #            cv2.destroyAllWindows()

    def smallerdistance(self,possibleoutcome):
        smallindex = 0
        smallDis = possibleoutcome[0][2]
        for i in range(0,len(possibleoutcome)):
            if(possibleoutcome[i][2] < smallDis):
                smallindex = i
        return possibleoutcome[smallindex]
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
            smalldis = [99999,-1]
            for j in range(0,len(distance)):
                if(distance[j][0]<smalldis[0]):
                    smalldis = distance[j]
            #print(grapha[i][0] , "  ; ",grapha[i][1], "  :  "  ,graphb[i][0] , "  ; ",graphb[i][1])
            #print("Distance = ",smalldis[0], " point match j = ",smalldis[1]," :: the point is ==  ",graphb[smalldis[1]] )
            dis = dis + smalldis[0]
        return dis
    def showSubsample(self,point,pointb,name):
        newImageAppro1 = np.zeros((500,500,3), np.uint8)
        for i in range(0,len(point[0])-1):
            x1 = point[0][i]
            y1 = point[1][i]
            x2 = point[0][i+1]
            y2 = point[1][i+1]
            print(x1,"   :   " ,y1)
            print(x2,"   :   " ,y2)
            cv2.line(newImageAppro1,(int(x1),int(y1)),(int(x2),int(y2)), (255,255,255), 1)
        for i in range(0,len(pointb[0])-1):
            x1 = pointb[0][i]
            y1 = pointb[1][i]
            x2 = pointb[0][i+1]
            y2 = pointb[1][i+1]
            cv2.line(newImageAppro1,(int(x1),int(y1)),(int(x2),int(y2)), (0,0,255), 1)
        cv2.imshow(name,newImageAppro1)
                    
                
            
