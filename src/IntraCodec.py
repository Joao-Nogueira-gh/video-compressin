import numpy as np
import math
from Golomb import *
from Bitstream import *

class IntraCodec:

    def __init__(self, filename, encoded=False, limitFrames=None):

        self.vid = filename

        self.encoding='utf-8'

        # Array of arrays containing each frame's components
        self.frameY=[]
        self.frameV=[]
        self.frameU=[]

        self.encoded=False
        self.quantizationStep=None
        self.colorSpace=None

        np.seterr(over='ignore')

        #calls read video on initialization
        if not encoded:
            self.read_video()
        else:
            self.encoded=True
            self.read_encoded_video(limitFrames=limitFrames)

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

    def read_encoded_video(self,limitFrames=None):
        bs=BitStream(self.vid,'READ')
        headerlen=bs.read_n_bits(8)

        chars=[]
        for i in range(0,headerlen*8):
            chars.append(str(bs._readbit()))

        res=''.join(chars)
        self.header=self.decode_binary_string(res)

        #handle header
        self.handleHeader()
        
        g=Golomb(self.golombParam)
        bitsResto=int(math.log(self.golombParam,2))

        if limitFrames==None:
            l=self.TotalFrames
        else:
            l=limitFrames
        #
        self.frameY=[None]*l
        self.frameU=[None]*l
        self.frameV=[None]*l
        #
        for frame in range(0,l):
            print('decoding frame',frame)

            y=np.zeros(shape=self.shape,dtype=np.uint8)
            u=np.zeros(shape=self.other_shape,dtype=np.uint8)
            v=np.zeros(shape=self.other_shape,dtype=np.uint8)
            
            for line in range(0, self.height):
                for column in range(0,self.width):
                    pixel=self.decodeWithBitstream(3,bs,g,bitsResto)

                    a=self.getYUVPixel(frame,line,column-1, resized=False)
                    c=self.getYUVPixel(frame,line-1,column-1, resized=False)
                    b=self.getYUVPixel(frame,line-1,column, resized=False)
                    x=self.predict(a,c,b)
                    pixel=self.sum(x,pixel)

                    pixel=tuple(pixel)

                    l,c=self.adjustCoord(line,column)

                    y[line,column]=pixel[0]                        
                    u[l,c]=pixel[1]
                    v[l,c]=pixel[2]
                    #
                    self.frameY[frame]=y
                    self.frameU[frame]=u
                    self.frameV[frame]=v

            #por cada frame
            self.frameY+=[y]
            self.frameU+=[u]
            self.frameV+=[v]
        #
        bs.close()

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
            elif c=='G':
                self.golombParam=int(field[-1:])
                self.encoded=True
            elif c=='z':
                self.TotalFrames=int(field[1:])
            elif c=='q':
                self.quantizationStep=int(field[1:])
                    
        self.computeShape()
        print('width=',self.width, 'height=',self.height, self.fps, self.colorSpace, self.frameLength)
        if self.encoded:
            print('g=',self.golombParam, 'totalframes=',self.TotalFrames)
        if self.quantizationStep!=None:
            print('q=',self.quantizationStep)
    
    def adjustCoord(self,line,column):
        if self.colorSpace=='4:2:2':
            c=math.floor((column/2))
            return line,c
        elif self.colorSpace=='4:2:0':
            c=math.floor((column/2))
            l=math.floor((line/2))
            return l,c
        else:
            return line,column


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

    def updateYUVPixel(self,compNumb,frame,line,column,value):
        if compNumb==0:
            rf=self.frameY[frame]
        elif compNumb==1:
            rf=self.frameU[frame]
        else:
            rf=self.frameV[frame]
        rf.setflags(write=1)
        if self.colorSpace=='4:2:2':
            c=math.floor((column/2))
            if compNumb==0:
                rf[line,column]=value
            else:
                rf[line,c]=value
        elif self.colorSpace=='4:2:0':
            c=math.floor((column/2))
            l=math.floor((line/2))
            if compNumb==0:
                rf[line,column]=value
            else:
                rf[l,c]=value
        else:
            rf[line,column]=value

    def encode_video(self, filename, golombparam, q=None, limitFrames=None):
        if limitFrames==None:
            l=self.TotalFrames
        else:
            l=limitFrames

        g=Golomb(golombparam)

        bs=BitStream(filename,'WRITE')

        header='ENCODED '+self.header+' Golomb'+str(golombparam)+' z'+str(self.TotalFrames)
        if q!=None:
            header+=' q'+str(q)
            self.quantizationStep=int(q)
        headerlen=len(header)
        bs.write_n_bits(headerlen,8)
        bs.writeTxt(header)

        for frame in range(0,l):
            print('encoding frame',frame)
            for line in range(0,self.height):
                for column in range(0,self.width):
                    p=self.getYUVPixel(frame,line,column, resized=False)

                    a=self.getYUVPixel(frame,line,column-1, resized=False)
                    c=self.getYUVPixel(frame,line-1,column-1, resized=False)
                    b=self.getYUVPixel(frame,line-1,column, resized=False)
                    x=self.predict(a,c,b)
                    erro=self.diff(p,x)

                    self.encodeWithBitstream(erro,bs,g,pixel=p,frame=frame,line=line,column=column)
        bs.close()
        
    def predict(self,a,c,b):
        y=[int(a[0]),int(c[0]),int(b[0])]
        u=[int(a[1]),int(c[1]),int(b[1])]
        v=[int(a[2]),int(c[2]),int(b[2])]

        l=[y]+[u]+[v]
        ret=[]
        for component in l:
            if component[1]>=max(component[0],component[2]):
                x=min(component[0],component[2])
            elif component[1]<=min(component[0],component[2]):
                x=max(component[0],component[2])
            else:
                x=component[0]+component[2]-component[1]
            ret.append(x)
        return ret

    def diff(self,p,x):
        ey=int(p[0])-int(x[0])
        eu=int(p[1])-int(x[1])
        ev=int(p[2])-int(x[2])

        return(ey,eu,ev)

    def sum(self,p,x):
        ey=p[0]+x[0]
        eu=p[1]+x[1]
        ev=p[2]+x[2]

        return(ey,eu,ev)

    def printPixels(self):
        l=self.TotalFrames
        l=1
        h=self.height
        #h=20
        w=self.width
        #w=20
        for frame in range(0,l):
            #print('processing frame',frame)
            for line in range(0,h):
                for column in range(0,w):
                    if line==0 and w-10<=column<w:
                        p=self.getYUVPixel(frame,line,column, resized=False)
                        print(p, end=';')
                #print('')

    def decode_binary_string(self,s):
        return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

    def getStuff(self):
        return self.frameY, self.frameU,self.frameV

    def encodeWithBitstream(self, value,bs,g, pixel=None, frame=None, line=None, column=None):
        for i in range(0,len(value)):
            if value[i]<0:
                n=value[i]*-1
                bs.writebits(1,1)
            else:
                bs.writebits(0,1)
                n=value[i]
            
            if self.quantizationStep!=None:
                n=math.floor(n/self.quantizationStep)
                newValue=pixel[i]+(n*self.quantizationStep)
                #TODO
                #self.updateYUVPixel(i,frame,line,column,newValue)
            n=g.encode(n)
            bs.writebits(int(n,2),len(n))

    def decodeWithBitstream(self, len,bs,g,bitsResto):
        pixel=[]
        for i in range(0,len):
            ay=bs.read_n_bits(1)
            seq=''
            while True:
                r=str(bs.read_n_bits(1))
                seq+=r
                if r=='0':
                    break
            seq+=str(bs.readbits(bitsResto))
            comp=g.decode(seq)
            if ay==1:
                comp=comp*-1
            if self.quantizationStep!=None:
                comp=comp*self.quantizationStep
            pixel.append(comp)
        return pixel

    def verifyData(self,video,numberoframes):
        m1,m2,m3=self.getStuff()
        m4,m5,m6=video.getStuff()
        for i in range(0,numberoframes):
            if (np.array_equal(m1[i],m4[i])):
                print('Y-',i,'correct')
        for i in range(0,numberoframes):
            if (np.array_equal(m2[i],m5[i])):
                print('U-',i,'correct')
        for i in range(0,numberoframes):
            if (np.array_equal(m3[i],m6[i])):
                print('V-',i,'correct')

