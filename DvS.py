#!/usr/bin/python

# Standard imports
import cv2
import numpy as np;
import math
from pieces import pieces
from result import Result 
from matching import matching
# read the image throught an window frame 
#imports for that
from tkinter import *
import generatePuzzle as gen
from tkinter import filedialog
from matplotlib import pyplot as plt
from matplotlib import path
from tkinter import messagebox
import tkinter as tk
from tkinter import *


class Main:
    def __init__(self):
        self.win = None
        self.image =[]
        self.filename=None
        self.jigsawpieces = []
        self.resultimage = None
        self.resultvector = None
        self.labelImage = []
        self.logo = []
        #self.photo = None
    def readFile(self):
        filename = filedialog.askopenfilename( filetypes = ( ("testing files", "*.*"), ("All Files","*.*") ) )
        self.image.append(cv2.imread(filename))
        
        #image = pilImage.open(self.filename)
        #photo = ImageTk.PhotoImage(image)
        
        #filename = filedialog.askopenfilename( filetypes = ( ("testing files", "*.*"), ("All Files","*.*") ) )
        self.logo.append(PhotoImage(file=filename))
        self.logo.append(self.logo[len(self.logo)-1].subsample(10))
        self.labelImage.append(Label(self.win, image=self.logo[len(self.logo)-1]).pack())
        #lb.grid(row=50, column=50)
    def detectPieces(self,i):
        img = self.image[i]
        dst = cv2.fastNlMeansDenoisingColored(img,None,1,1,10,5)
        imggry2 = cv2.cvtColor(dst,cv2.COLOR_RGB2GRAY)
        ret, thresh12 = cv2.threshold(imggry2, 230, 255, cv2.THRESH_BINARY_INV)

        imggry = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        ret, thresh = cv2.threshold(imggry, 230, 255, cv2.THRESH_BINARY_INV)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(img, contours, -1, (0,255,0), 3)
        #cv2.imshow("The Image",img)
        xlow = []
        xhigh = []
        ylow = []
        yhigh = []
        
        for cnt in range(0, len(contours)):
            
            if(cv2.contourArea(contours[cnt])<=500) :
                continue
            point=contours[cnt]
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
            if(txlow == txhigh or txhigh==tyhigh):
                continue
            xlow.append(txlow-2)
            xhigh.append(txhigh+2)
            ylow.append(tylow-2)
            yhigh.append(tyhigh+2)
        images = []
        jigsawPieces = []
        #extracting each piece from the image given in the system Part 1
        #------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------
        for i in range(0, len(ylow)):
            images.append(img[ylow[i]:yhigh[i],xlow[i]:xhigh[i]])
            self.jigsawpieces.append(pieces(images[i]))
            #cv2.imshow("Thks dv",images[i])
            #cv2.waitKey(0);
    def setPropertyOfPieces(self):
        for i in range(0,len(self.jigsawpieces)):
            eachPiece = self.jigsawpieces[i]
            print("------------------------------------------------------- = " , i)
            print("eachPiece = " , i)
            #if(i==4):
            #    eachPiece.findingcorners(test=True)
            #else:
            eachPiece.findingcorners()

            eachPiece.side[0].setsideproperty()
            eachPiece.side[1].setsideproperty()
            eachPiece.side[2].setsideproperty()
            eachPiece.side[3].setsideproperty()
            eachPiece.setdirection()
    def getResult(self):
        result = Result(self.jigsawpieces)
        self.resultimage , self.resultvector = result.getresult()
        cv2.imshow("The Result is ",self.resultimage)
        cv2.waitKey(0)
    def createwindow(self):
        self.win = Tk()
        self.win.title("jIgSAw PuZZlE")
        self.win.geometry("700x700")
        addImage = Button(self.win, text="ADD IMAGE", command=self.addimage)
        #addImage.grid(row=10, column=10)
        addImage.pack()
        #root = Tk()

        startSolver = Button(self.win, text="Solve", command=self.solve)
        #startSolver.grid(row=20, column=10)
        startSolver.pack()
        #filename = filedialog.askopenfilename( filetypes = ( ("testing files", "*.*"), ("All Files","*.*") ) )
        #logo = PhotoImage(file=filename)
        #w1 = Label(self.win, image=logo).pack(side="right")
        #addImage.pack()
        self.win.mainloop()
    def addimage(self):
        self.readFile()
    def solve(self):
        for i in range(0,len(self.image)):
            self.detectPieces(i)
        self.setPropertyOfPieces()
        self.getResult()
    def run(self):
        self.createwindow()


        self.detectPieces()
        self.setPropertyOfPieces()
        self.getResult()

#root = Tk()
#filename = filedialog.askopenfilename( filetypes = ( ("testing files", "*.*"), ("All Files","*.*") ) )
#logo = PhotoImage(file=filename)
#w1 = Label(root, image=logo).pack(side="right")
#explanation = """At present, only GIF and PPM/PGM
#formats are supported, but an interface 
#exists to allow additional image file
#formats to be added easily."""
#w2 = Label(root, 
#           justify=LEFT,
#           padx = 10, 
#           text=explanation).pack(side="left")
#root.mainloop()

solver = Main()
solver.run()
# Read image
root = Tk()

root.title("jigsaw Puzzle")
root.geometry("700x700")

#def helloCallBack():
#   tk.messagebox.showinfo( "Hello Python", "Hello World")

#B = Button(root, text ="AddImage", command = helloCallBack)

#B.pack()
#root.mainloop()
filename = filedialog.askopenfilename( filetypes = ( ("testing files", "*.*"), ("All Files","*.*") ) )

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
result = Result(jigsawPieces)
resultimage , resultvector = result.getresult()
cv2.imshow("The Result is ",resultimage)
cv2.waitKey(0);

