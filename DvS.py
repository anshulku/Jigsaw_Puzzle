#!/usr/bin/python

# Standard imports
import cv2
import numpy as np;
import math
from pieces import pieces
from result import Result 
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
    """
        __init__ creates all the variable needed for the project
    """
    def __init__(self):
        self.win = None
        self.image =[]
        self.filename=None
        self.jigsawpieces = []
        self.resultimage = None
        self.resultvector = None
        self.labelImage = []
        self.logo = []
        self.locationOfImage = 0
        #self.photo = None
    """
        readFile reads the file from the directory and get the image
        then it disaplys on the screan which can be remove or open in a new image
    """
    def readFile(self):
        filename = filedialog.askopenfilename( filetypes = ( ("testing files", "*.*"), ("All Files","*.*") ) )
        # addending all the images in an array
        self.image.append(cv2.imread(filename))

        #displaying the image on the screen
        photo = PhotoImage(file=filename)
        self.logo.append(photo.subsample(20))
        label = Button(self.win, image=self.logo[len(self.logo)-1])

        #Button-1 means right click
        #Button-3 means left click
        label.bind('<Button-1>',self.showImage)
        label.bind('<Button-3>', self.deleteImage)
        label.pack()
        self.labelImage.append(label)
        self.locationOfImage = self.locationOfImage+1
        #updaing the windows
        self.win.update()
    """
        show the image which has been clicked
    """
    def showImage(self,event):  
        i = 0
        # getting which image is been clicked
        for i in range(0,len(self.labelImage)):
            if(event.widget == self.labelImage[i]):
                break
        cv2.imshow("Puzzle ",self.image[i])
    """
        delets the image which has been clicked
    """
    def deleteImage(self,event):  
        i = 0
        # getting which image is been clicked
        for i in range(0,len(self.labelImage)):
            if(event.widget == self.labelImage[i]):
                break
        self.labelImage[i].destroy()
        self.labelImage.pop(i)

        # if the deleted image is the last one the resetting everthing
        # so the user can put a diferent image

        if(len(self.labelImage)==0):
            self.image =[]
            self.filename=None
            self.jigsawpieces = []
            self.resultimage = None
            self.resultvector = None
            self.labelImage = []
            self.logo = []
            self.locationOfImage = 0

        #updating the image
        self.win.update()
    """
        detect each piece in the i th image in the array of the images
        after detecting the piece it add it in the jigsawpiece object
    """
    def detectPieces(self,i):
        #getting the current image
        img = self.image[i]

        #converting the image into grayscale for thresholding the image
        imggry = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        # since contours find white spots so the threshold is been reverse so 
        # it changes the colour
        ret, thresh = cv2.threshold(imggry, 230, 255, cv2.THRESH_BINARY_INV)
        # using the opencv method to find the contours of the image
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # for extracting the pieces
        # we find the minimum points and the maximum points for and contour
        # and then extract it from the image 
        xlow = []
        xhigh = []
        ylow = []
        yhigh = []
        
        # loop in contour to find the pieces
        for cnt in range(0, len(contours)):
            # if the contour size is less than 500 we ignore it
            # since it is not a piece and a noise
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
        for i in range(0, len(ylow)):
            images.append(img[ylow[i]:yhigh[i],xlow[i]:xhigh[i]])
            self.jigsawpieces.append(pieces(images[i]))
    """
        setPropertyOfPeces find the corner for each pieces in jigsaw puzzle
        and then sets the constrants for assembling the puzzle
    """
    def setPropertyOfPieces(self):
        for i in range(0,len(self.jigsawpieces)):
            eachPiece = self.jigsawpieces[i]
            eachPiece.findingcorners()
            #setting the property of each side in the piece
            eachPiece.side[0].setsideproperty()
            eachPiece.side[1].setsideproperty()
            eachPiece.side[2].setsideproperty()
            eachPiece.side[3].setsideproperty()
            #setting the direction of the piece 
            eachPiece.setdirection()
    """
        trys to solve the puzzle using b-tree method 
        it use solve aprroaches to decrease the complexity of the tree
        these approaches are 
    """
    def getResult(self):
        # making the object of result class and sending the pieces
        result = Result(self.jigsawpieces)
        # the result solve the puzzle if the constrants are extracted properly
        # it returns the result image and resultvector
        self.resultimage , self.resultvector = result.getresult()

        #shows the result
        self.showResult()
    """
        shows the assemble puzzle
    """
    def showResult(self):
        print("SHOWING THE RESULTS--------------------------------------------")
        cv2.imshow("The Result is ",self.resultimage)
    """
        creates the window to add image and tell the application to
        solve the puzzle
    """
    def createwindow(self):
        self.win = Tk()
        self.win.title("jIgSAw PuZZlE")
        self.win.geometry("700x700")
        addImage = Button(self.win, text="ADD IMAGE", command=self.addimage)
        #addImage.grid(row=10, column=10)
        addImage.pack()

        startSolver = Button(self.win, text="Solve", command=self.solve)
        startSolver.pack()
        self.win.mainloop()
    """
        adds the image to the solver
    """
    def addimage(self):
        self.readFile()
    """
        solves the puzzle if possible
    """
    def solve(self):
        if(self.resultimage is None):
            print("DETECTING PIECES-----------------------------------------------")
            for i in range(0,len(self.image)):
                self.detectPieces(i)
            print("DETECTING PIECES DONE------------------------------------------")
            print("SETTING THE CONSTRAINTS----------------------------------------")
            self.setPropertyOfPieces()
            print("SETTING THE CONSTRAINTS DONE-----------------------------------")
            print("GETTING THE RESULTS--------------------------------------------")
            self.getResult()
        else:
            self.showResult()
    """
        runs the code
    """
    def run(self):
        self.createwindow()

solver = Main()
solver.run()