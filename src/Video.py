import numpy as np
import cv2
import math
from Golomb import *
from Bitstream import *

class Video:

    def __init__(self, file_name, mode, limitFrames=None):

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

        self.encoded=False
        self.cut=False
        self.colorSpace=None

        np.seterr(over='ignore')

        #calls read video on initialization
        self.read_video(mode, limitFrames)

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
                self.cutFactor=int(field[1:])
                self.cut=True
            elif c=='b':
                self.block_size=int(field[1:])
            elif c=='s':
                self.search_area=int(field[1:])
                    
        self.computeShape()
        print('width=',self.width, 'height=',self.height, self.fps, self.colorSpace, self.frameLength)
        if self.encoded:
            print('g=',self.golombParam, 'totalframes=',self.TotalFrames)
        if self.cut:
            print('q=',self.cutFactor)

    def read_video(self, mode, limitFrames=None):
        if mode=='normal':
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
                    
                    # print(y, len(y),c, end='\n\n')
                    # print(u, len(u),c, end='\n\n')
                    # print(v, len(v),c, end='\n\n')

                c+=1

            self.TotalFrames=len(self.frameY)

            f.close()

        elif mode=='intra_encoding':
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

        elif mode=='hybrid_encoding':
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

                if frame==0:
                
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

                else:
                    blocks=self.getBlocks(frame-1,self.block_size)
                    bl,bc=blocks.shape
                    for i1 in range(0,bl):
                        for i2 in range(0,bc):
                            vetor=self.decodeWithBitstream(2,bs,g,bitsResto)
                            v1,v2=vetor
                            #print(vetor)
                            bestBlock=blocks[v1,v2]
                            for l in range(0,self.block_size):
                                for c in range(0,self.block_size):
                                    pixelErro=self.decodeWithBitstream(3,bs,g,bitsResto)
                                    referencePixel=bestBlock[l,c]
                                    pixel=self.sum(pixelErro,referencePixel)

                                    line,column=self.block_size*i1+l,self.block_size*i2+c           
                                    li,co=self.adjustCoord(line,column)

                                    y[line,column]=pixel[0]                        
                                    u[li,co]=pixel[1]
                                    v[li,co]=pixel[2]



                    self.frameY[frame]=y
                    self.frameU[frame]=u
                    self.frameV[frame]=v
            #
            bs.close()
        else:
            print('unknown mode, shutting down')
            exit(0)

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

    
    def convertToRgb(self, frameNumber):

        self.resize()

        #repare bem isto está um bocado hardcoded
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


    def printrgb(self):
        for frame in self.frameRGB:
            print(frame)

    def play_video(self, frameNumber=None):
        if frameNumber==None:
            frameNumber=self.TotalFrames

        self.convertToRgb(frameNumber)

        print('a mostrar',frameNumber, 'imagens/frames,', len(self.frameRGB))

        # woooooooooooo
        for frame in self.frameRGB:
            RGB_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imshow('Video',RGB_img)
            cv2.waitKey(2000)

    def encode_video(self, filename, q=None, limitFrames=None):
        if limitFrames==None:
            l=self.TotalFrames
        else:
            l=limitFrames

        m=4
        g=Golomb(m)

        bs=BitStream(filename,'WRITE')

        header='ENCODED '+self.header+' Golomb'+str(m)+' z'+str(self.TotalFrames)
        if q!=None:
            header+=' q'+str(q)
        headerlen=len(header)
        bs.write_n_bits(headerlen,8)
        bs.writeTxt(header)

        for frame in range(0,l):
            print('encoding frame',frame)
            for line in range(0,self.height):
                for column in range(0,self.width):
                    p=self.getYUVPixel(frame,line,column, resized=False)
                    # if line==0 or column==0:
                    #     for i in range(0,len(p)):
                    #         n=p[i]
                    #         n=g.encode(n)
                    #         #n="{0:b}".format(p[i])
                    #         #print(n,' vs ',sequence)
                    #         bs.writebits(int(n,2),len(n))
                    # else:
                    a=self.getYUVPixel(frame,line,column-1, resized=False)
                    c=self.getYUVPixel(frame,line-1,column-1, resized=False)
                    b=self.getYUVPixel(frame,line-1,column, resized=False)
                    x=self.predict(a,c,b)
                    erro=self.diff(p,x)

                    self.encodeWithBitstream(erro,bs,g,q,pixel=p,frame=frame,line=line,column=column)
        bs.close()
        
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
                x=max(component[0],component[2])
            else:
                x=component[0]+component[2]-component[1]
            ret.append(x)
        return ret

    def diff(self,p,x):
        # ey=p[0]-x[0]
        # eu=p[1]-x[1]
        # ev=p[2]-x[2]

        ey=int(p[0])-int(x[0])
        eu=int(p[1])-int(x[1])
        ev=int(p[2])-int(x[2])
        return(ey,eu,ev)
    def sum(self,p,x):
        ey=p[0]+x[0]
        eu=p[1]+x[1]
        ev=p[2]+x[2]
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

    def getBlock(self,firstPixel,length,frame):
        yuv=np.zeros(shape=(length,length,3), dtype=np.uint8)
        l,c=firstPixel
        fl,fc=l+length,c+length
        c1,c2=0,0
        for line in range(l,fl):
            for col in range(c,fc):
                p=self.getYUVPixel(frame,line,col,resized=False)
                #print(p)
                yuv[c1,c2]=p
                c2+=1
            c1+=1
            c2=0
        

        return yuv

    def getBlocks(self,frame,block_size):
        firstPixel=[0,0]
        p1=int(self.height/block_size)
        p2=int(self.width/block_size)
        blocks=np.zeros(shape=(p1,p2), dtype=object)
        c1,c2=0,0
        while True:
            if firstPixel[0]==self.height:
                break
            yuv=self.getBlock(firstPixel,block_size,frame)
            blocks[c1,c2]=yuv
            firstPixel[1]=firstPixel[1]+block_size
            c2+=1
            if firstPixel[1]==self.width:
                firstPixel[1]=0
                c2=0
                firstPixel[0]=firstPixel[0]+block_size
                c1+=1
        return blocks


    def hybrid_encoding(self, filename,block_size, search_area, q=None, limitFrames=None):
        if limitFrames==None:
            l=self.TotalFrames
        else:
            l=limitFrames

        m=4
        g=Golomb(m)

        bs=BitStream(filename,'WRITE')

        header='ENCODED '+self.header+' Golomb'+str(m)+' z'+str(self.TotalFrames)+' b'+str(block_size)+' s'+str(search_area)
        if q!=None:
            header+=' q'+str(q)
        headerlen=len(header)
        bs.write_n_bits(headerlen,8)
        bs.writeTxt(header)

        for frame in range(0,l):
            print('encoding frame',frame)
            if frame==0:
                for line in range(0,self.height):
                    for column in range(0,self.width):
                        p=self.getYUVPixel(frame,line,column, resized=False)
                        # if line==0 or column==0:
                        #     for i in range(0,len(p)):
                        #         n=p[i]
                        #         n=g.encode(n)
                        #         #n="{0:b}".format(p[i])
                        #         #print(n,' vs ',sequence)
                        #         bs.writebits(int(n,2),len(n))
                        # else:
                        a=self.getYUVPixel(frame,line,column-1, resized=False)
                        c=self.getYUVPixel(frame,line-1,column-1, resized=False)
                        b=self.getYUVPixel(frame,line-1,column, resized=False)
                        x=self.predict(a,c,b)
                        erro=self.diff(p,x)

                        self.encodeWithBitstream(erro,bs,g,q,pixel=p,frame=frame,line=line,column=column)
            else:
                blocks=self.getBlocks(frame,block_size)
                oldBlocks=self.getBlocks(frame-1,block_size)

                bl,bc=blocks.shape
                for l in range(0,bl):
                    for c in range(0,bc):
                        position=l,c
                        block=blocks[l,c]
                        bestblock,vetor=self.findBestBlock(block,oldBlocks,search_area,position)
                        #write vetor
                        self.encodeWithBitstream(vetor,bs,g,q)
                        #write block
                        nl,nc=bestblock.shape[0], bestblock.shape[1]
                        for a in range(0,nl):
                            for b in range(0,nc):
                                self.encodeWithBitstream(bestblock[a,b],bs,g,q)

            
        bs.close()

    def findBestBlock(self,block,oldBlocks,search_area,position):
        vetor=None
        flag=True
        lastDif=None
        ol,oc=position
        bl,bc=oldBlocks.shape
        #print(bl,bc)
        for l in range(0,bl):
            for c in range(0,bc):
                if abs(ol-l)<=search_area and abs(oc-c)<=search_area:
                    candidateBlock=oldBlocks[l,c]
                    dif=self.blockDif(block,candidateBlock)
                    if flag or self.lessError(dif,lastDif):
                        flag=False
                        lastDif=dif
                        vetor=[l,c]
        return lastDif,vetor


    def blockDif(self,block,candidateBlock):
        length=block.shape[0]
        dif=np.zeros(shape=(length,length,3), dtype=np.int8)
        for l in range(0,length):
            for c in range(0,length):
                dif[l,c]=self.diff(block[l,c],candidateBlock[l,c])
        return dif

    def lessError(self,dif,lastDif):
        s1=0
        s2=0
        length=dif.shape[0]
        for l in range(0,length):
            for c in range(0,length):
                p1=dif[l,c]
                s1+=abs(int(p1[0]))+abs(int(p1[1]))+abs(int(p1[2]))
                p2=lastDif[l,c]
                s2+=abs(int(p2[0]))+abs(int(p2[1]))+abs(int(p2[2]))

        if s1==0 or s2==0:
            print('YOOOOOOOOOOOOO')

        if s1<s2:
            return True
        else:
            return False

    def encodeWithBitstream(self, value,bs,g,q, pixel=None, frame=None, line=None, column=None):
        for i in range(0,len(value)):
            if value[i]<0:
                n=value[i]*-1
                bs.writebits(1,1)
            else:
                bs.writebits(0,1)
                n=value[i]
            
            if q!=None:
                n=math.floor(n/q)
                newValue=pixel[i]+(n*q)
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
            if self.cut:
                comp=comp*self.cutFactor
            pixel.append(comp)
        return pixel

