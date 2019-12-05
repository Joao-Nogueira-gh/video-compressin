import numpy as np
import cv2

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

    def play_video(self):
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
                print(line)
                line=line.decode(self.encoding)
                fields=line.split(" ")

                self.width=int((fields[1])[1:])
                self.height=int((fields[2])[1:])
                self.fps=int((fields[3])[1:3])

                self.getColorSpace(fields)
                print(self.width, self.height, self.fps, self.colorSpace, self.frameLength, self.shape, 'line ',1)
            
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
                
                print(y, len(y),c, end='\n\n')
                print(u, len(u),c, end='\n\n')
                print(v, len(v),c, end='\n\n')

            c+=1

        print('500 = 50fps * 10 SeemsGood')
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
            print(x, len(x), c,'y' ,end='\n\n')
            c+=1
        c=1
        for x in self.frameU:
            print(x, len(x),c, 'u', end='\n\n')
            c+=1
        c=1
        for x in self.frameV:
            print(x, len(x),c, 'v', end='\n\n')
            c+=1

    def resize(self):
        # Resize arrays
        if self.colorSpace != '4:4:4':

            self.frameU = cv2.resize(self.frameU, (len(self.frameY), len(self.frameY[0])))
            self.frameV = cv2.resize(self.frameV, (len(self.frameY), len(self.frameY[0])))

        else:

            print("No resizing needed")
