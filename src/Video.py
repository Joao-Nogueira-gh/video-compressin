import numpy as np
import cv2
from PIL import Image
import math
from Golomb import *
from Bitstream import *

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
                self.header=line.strip()

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

    def encode_video(self, filename):
        l=self.TotalFrames
        l=1
        m=4
        g=Golomb(4)
        #b=BitStream()
        f=open(filename,'w')
        f.write('ENCODED '+self.header+' '+str(m)+'\n')
        for frame in range(0,l):
            print('processing frame ',frame)
            for line in range(0,self.height):
                for column in range(0,self.width):
                    p=self.getYUVPixel(frame,line,column, resized=False)
                    if line==0 or column==0:
                        newP=''
                        for pp in p:
                            newP+=g.encode(pp)+','
                        f.write(newP[:-1]+';')
                    else:
                        a=self.getYUVPixel(frame,line,column-1, resized=False)
                        c=self.getYUVPixel(frame,line-1,column-1, resized=False)
                        b=self.getYUVPixel(frame,line-1,column, resized=False)
                        x=self.predict(a,c,b)
                        erro=self.diff(p,x)
                        #print(p,x,erro)
                        newP=''
                        for pp in erro:
                            newP+=g.encode(pp)+','
                        f.write(newP[:-1]+';')
                f.write('\n')
        
    def predict(self,a,c,b):
        y=[int(a[0]),int(c[0]),int(b[0])]
        u=[int(a[1]),int(c[1]),int(b[1])]
        v=[int(a[2]),int(c[2]),int(b[2])]
        # y=[a[0],c[0],b[0]]
        # u=[a[1],c[1],b[1]]
        # v=[a[2],c[2],b[2]]
        l=[y]+[u]+[v]
        ret=[]
        for component in l:
            if component[1]>=max(component[0],component[2]):
                x=min(component[0],component[2])
            elif component[1]<=min(component[0],component[2]):
                x=min(component[0],component[2])
            else:
                x=component[0]+component[2]-component[1]
            ret.append(x)
        return ret

    def diff(self,p,x):
        ey=p[0]-x[0]
        eu=p[1]-x[1]
        ev=p[2]-x[2]
        # ey=p[0]-x[0]
        # eu=p[1]-x[1]
        # ev=p[2]-x[2]
        # ey=int(p[0])-int(x[0])
        # eu=int(p[1])-int(x[1])
        # ev=int(p[2])-int(x[2])
        return(ey,eu,ev)

    def printPixels(self):
        l=self.TotalFrames
        l=1
        h=self.height
        h=2
        w=self.width
        #w=2
        for frame in range(0,l):
            print('processing frame ',frame)
            for line in range(0,h):
                for column in range(0,w):
                    p=self.getYUVPixel(frame,line,column, resized=False)
                    print(p, end=';')
                print('\n\n')

