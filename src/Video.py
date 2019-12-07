import numpy as np
import cv2
from PIL import Image
import math

class Video:

    def __init__(self, file_name):

        # High Level Video Playing
        self.vid = file_name
        self.esc = 'q'

        # Reading video
        self.encoding='utf-8'

        # Array of arrays containing each frame's components
        self.frameY=[]
        self.frameV=[]
        self.frameU=[]
        #
        self.frameRGB=[]

        #calls read video on initialization
        self.read_video()

    #regular video playing from opencv, not used
    def old_play_video(self):
        cap = cv2.VideoCapture(self.vid)

        while(cap.isOpened()):
            ret, frame = cap.read()
            #print(frame)
            
            if not ret or cv2.waitKey(10) & 0xFF == ord(self.esc):
                break
            cv2.imshow('Video',frame)
            
        cap.release()
        cv2.destroyAllWindows()

    def read_video(self):
        f=open(self.vid,"rb")
        c=1

        for line in f:

            # Processing header
            if c==1:
                #print(line)
                line=line.decode(self.encoding)
                fields=line.split(" ")

                self.width=int((fields[1])[1:])
                self.height=int((fields[2])[1:])
                self.fps=int((fields[3])[1:3])

                self.getColorSpace(fields)
                print('width=',self.width, 'height=',self.height, self.fps, self.colorSpace, self.frameLength,'line ',1)
            
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
                
                # print(y, len(y),c, end='\n\n')
                # print(u, len(u),c, end='\n\n')
                # print(v, len(v),c, end='\n\n')

            c+=1

        self.TotalFrames=len(self.frameY)

        f.close()


    def getColorSpace(self,fields):

        for x in fields:

            if x[0]=='C':
                c=x[1:4]
                
                if c=='444':
                    self.colorSpace='4:4:4'
                    self.frameLength=int(self.width*self.height*3)
                    self.yLength=self.uLength=self.vLength=int(self.frameLength/3)
                    self.shape = (int(self.height), self.width)
                    self.other_shape = (int(self.height), self.width)
                    return

                elif c=='422':
                    self.colorSpace='4:2:2'
                    self.frameLength=int(self.width*self.height*2)
                    self.yLength=int(self.frameLength/2)
                    self.vLength=self.uLength=int(self.frameLength/4)
                    self.shape = (int(self.height), self.width)
                    self.other_shape = (int(self.height), int(self.width/2))
                    return
                
                elif c=='420':
                    self.colorSpace='4:2:0'
                    self.frameLength=int(self.width*self.height*3/2)
                    self.yLength=int(self.frameLength*(2/3))
                    self.uLength=self.vLength=int(self.frameLength*(1/6))
                    self.shape = (int(self.height), self.width)
                    self.other_shape = (int(self.height/2), int(self.width/2))
                    return

        # If no condition was fullfilled, assume the default   
        self.colorSpace='4:2:0'
        self.frameLength=int(self.width*self.height*3/2)
        self.yLength=int(self.frameLength*(2/3))
        self.uLength=self.vLength=int(self.frameLength*(1/6))
        self.shape = (int(self.height), self.width)
        self.other_shape = (int(self.height/2), int(self.width/2))

    def print(self):
        c=1
        for x in self.frameY:
            print(x, 'colunas=',len(x[0]),'linhas=',len(x), 'frame=',c,'y' ,end='\n\n')
            if c==1: break
            c+=1
        c=1
        for x in self.frameU:
            print(x,'colunas=',len(x[0]),'linhas=',len(x), 'frame=',c,'u' ,end='\n\n')
            if c==1: break
            c+=1
        c=1
        for x in self.frameV:
            print(x, 'colunas=',len(x[0]),'linhas=',len(x), 'frame=',c,'v' ,end='\n\n')
            if c==1: break
            c+=1

    def resize(self):
        # Resize arrays
        if self.colorSpace != '4:4:4':

            for i in range(0, len(self.frameU)):
                self.frameU[i] = cv2.resize(self.frameU[i], (self.width, self.height))
                self.frameV[i] = cv2.resize(self.frameV[i], (self.width, self.height))

        else:

            print("No resizing needed")


    def getYUVPixel(self, frame, l, c, resized):
        yf=self.frameY[frame]
        uf=self.frameU[frame]
        vf=self.frameV[frame]
        if resized==False:
            if self.colorSpace=='4:2:2':
                c=math.floor((c/2))
            elif self.colorSpace=='4:2:0':
                c=math.floor((c/2))
                l=math.floor((l/2))

        p=yf[l,c], uf[l,c], vf[l,c]
        return p
    
    def convertToRgb(self, frameNumber):

        self.resize()

        #repare bem isto está um bocado hardcoded
        delta=128
        for frame in range(0,frameNumber):
            print('processing frame ',frame)
            rgb=np.zeros(shape=(self.height,self.width,3), dtype=np.uint8)
            for line in range(0,self.height):
                for column in range(0,self.width):
                    p=self.getYUVPixel(frame,line,column, resized=True)
                    r=p[0]+1.403*(p[2]-delta)
                    g=p[0]-0.714*(p[2]-delta)-0.344*(p[1]-delta)
                    b=p[0]+1.773*(p[1]-delta)
                    rgb[line,column] = r,g,b
            self.frameRGB+=[rgb]


    def printrgb(self):
        for frame in self.frameRGB:
            print(frame)

    def play_video(self, frameNumber=None):
        if frameNumber==None:
            frameNumber=self.TotalFrames

        self.convertToRgb(frameNumber)

        print('a mostrar ',frameNumber, ' imagens/frames,', len(self.frameRGB))
        
        # for frame in self.frameRGB:
        #     a=Image.fromarray(frame)
        #     a.show()

        # woooooooooooo
        for frame in self.frameRGB:
            RGB_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imshow('Video',RGB_img)
            cv2.waitKey(2000)

    def encode_video(self):
        print(len(self.frameY),len(self.frameU),len(self.frameV))
        for frame in range(0,self.TotalFrames):
            print('processing frame ',frame)
            for line in range(0,self.height):
                for column in range(0,self.width):
                    #print(frame,line,column)
                    p=self.getYUVPixel(frame,line,column, resized=False)
            #each loop

