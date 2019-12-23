## @class VideoPlayer 
# Module designed for reading video information and displaying it on screen using Python's opencv
# Since the video format is YUV it has to be converted to RGB
# @author Tiago Melo 89005
# @author João Nogueira 89262

import numpy as np
import cv2
import math

class VideoPlayer:
    ## Initialization function
    # @param[in] filename Path of the file to read
    # @param[in] imported A flag used to indicate if we are reading a saved video from a file, or importing the structures of one of our Codecs
    # Initializing and setting up some useful parameters and flags
    def __init__(self, filename, imported=False):
        if not imported:
            self.vid = filename

            self.esc = 'q'

            self.encoding='utf-8'

            # Array of arrays containing each frame's components
            self.frameY=[]
            self.frameV=[]
            self.frameU=[]
            #
            self.frameRGB=[]

            self.colorSpace=None

            np.seterr(over='ignore')

            #calls read video on initialization
            self.read_video()
        else:
            self.TotalFrames=filename.TotalFrames
            self.frameRGB=[]
            self.colorSpace=filename.colorSpace
            self.frameY=filename.frameY
            self.frameV=filename.frameV
            self.frameU=filename.frameU
            self.width=filename.width
            self.height=filename.height

    ## read_video function
    # Reads YUV video information from file, storing all its data in our structures, calculating different components lengths and shapes
    def read_video(self):
        f=open(self.vid,"rb")
        c=1

        for line in f:

            # Processing header
            if c==1:
                line=line.decode(self.encoding)
                self.header=line.strip()
                self.handleHeader()
            
            # Rest of the video
            if c>=2:

                frameY=f.read(self.yLength)
                frameU=f.read(self.uLength)
                frameV=f.read(self.vLength)

                y=np.frombuffer(frameY, dtype=np.uint8)
                u=np.frombuffer(frameU, dtype=np.uint8)
                v=np.frombuffer(frameV, dtype=np.uint8)

                y=y.reshape(self.shape)
                u=u.reshape(self.other_shape)
                v=v.reshape(self.other_shape)

                self.frameY+=[y]
                self.frameU+=[u]
                self.frameV+=[v]

            c+=1

        self.TotalFrames=len(self.frameY)

        f.close()

    ## handleHeader function
    # Interpreting the header of the file, containing width, height, frames per second and color space, assigning them to class variables
    def handleHeader(self):
        print(self.header)
        fields=self.header.split(" ")

        for field in fields:
            c=field[0]
            if c=='W':
                self.width=int(field[1:])
            elif c=='H':
                self.height=int(field[1:])
            elif c=='F':
                self.fps=int(field[1:3])
            elif c=='C':
                self.colorSpace=int(field[1:])
                    
        self.computeShape()
        print('width=',self.width, 'height=',self.height, self.fps, self.colorSpace, self.frameLength)

    ## computeShape function
    # Calculating array shapes for YUV components based on the color space
    def computeShape(self):      
        if self.colorSpace==444:
            self.colorSpace='4:4:4'
            self.frameLength=int(self.width*self.height*3)
            self.yLength=self.uLength=self.vLength=int(self.frameLength/3)
            self.shape = (int(self.height), self.width)
            self.other_shape = (int(self.height), self.width)

        elif self.colorSpace==422:
            self.colorSpace='4:2:2'
            self.frameLength=int(self.width*self.height*2)
            self.yLength=int(self.frameLength/2)
            self.vLength=self.uLength=int(self.frameLength/4)
            self.shape = (int(self.height), self.width)
            self.other_shape = (int(self.height), int(self.width/2))
        else: 
            self.colorSpace='4:2:0'
            self.frameLength=int(self.width*self.height*3/2)
            self.yLength=int(self.frameLength*(2/3))
            self.uLength=self.vLength=int(self.frameLength*(1/6))
            self.shape = (int(self.height), self.width)
            self.other_shape = (int(self.height/2), int(self.width/2))

    ## resize function
    # Resizing arrays so that they all share the same shape in 422 and 420 formats
    # Makes use of Python's opencv method 'resize'
    def resize(self):
        # Resize arrays
        if self.colorSpace != '4:4:4':
            print('Resizing arrays')

            for i in range(0, len(self.frameU)):
                self.frameU[i] = cv2.resize(self.frameU[i], (self.width, self.height))
                self.frameV[i] = cv2.resize(self.frameV[i], (self.width, self.height))

        else:

            print("No resizing needed")


    ## getYUVPixel function
    # @param[in] frame Number of the frame from which to read the pixel from
    # @param[in] line Line in which the pixel is located
    # @param[in] column Column in which the pixel is located
    # @param[in] resized A flag used to indicate if the arrays have been resized or not
    # @param[out] p The pixel tuple in YUV format
    # Returns 0,0,0 for non existent pixels, useful for the Codecs
    # Adjust line and column numbers based on the color space (and array shapes)
    def getYUVPixel(self, frame, line, column, resized):
        yf=self.frameY[frame]
        uf=self.frameU[frame]
        vf=self.frameV[frame]

        if resized==False:
            if self.colorSpace=='4:2:2':
                c=math.floor((column/2))
                if line<0 or column<0 or c<0:
                    return 0,0,0
                p=yf[line,column], uf[line,c], vf[line,c]
            elif self.colorSpace=='4:2:0':
                c=math.floor((column/2))
                l=math.floor((line/2))
                if line<0 or column<0 or c<0 or l<0:
                    return 0,0,0
                p=yf[line,column], uf[l,c], vf[l,c]
            else:
                if line<0 or column<0:
                    return 0,0,0
                p=yf[line,column], uf[line,column], vf[line,column]
        else:
            if line<0 or column<0:
                return 0,0,0
            p=yf[line,column], uf[line,column], vf[line,column]
        return p
    
    ## getYUVPixel function
    # @param[in] frameNumber Number of the frame to be converted to RGB
    # Converts all the pixels in the desired frame to RGB format
    def convertToRgb(self, frameNumber):

        self.resize()

        delta=128
        
        for frame in range(0,frameNumber):
            print('converting frame',frame,'to rgb')
            rgb=np.zeros(shape=(self.height,self.width,3), dtype=np.uint8)
            for line in range(0,self.height):
                for column in range(0,self.width):
                    p=self.getYUVPixel(frame,line,column, resized=True)
                    r=p[0]+1.403*(p[2]-delta)
                    g=p[0]-0.714*(p[2]-delta)-0.344*(p[1]-delta)
                    b=p[0]+1.773*(p[1]-delta)
                    rgb[line,column] = r,g,b
            self.frameRGB+=[rgb]

    ## getYUVPixel function
    # @param[in] frameNumber Optional parameter to limit the number of frames to be shown (and converted)
    # Currently showing frames with 1 second delay between each one for development purposes
    # Can be altered be changing the value in 'cv2.waitKey(x)'
    def play_video(self, frameNumber=None):
        if frameNumber==None:
            frameNumber=self.TotalFrames

        self.convertToRgb(frameNumber)

        print('a mostrar',frameNumber, 'imagens/frames (delay de 1s entre cada frame!)')

        for frame in self.frameRGB:
            RGB_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imshow('Video',RGB_img)
            cv2.waitKey(1000)
