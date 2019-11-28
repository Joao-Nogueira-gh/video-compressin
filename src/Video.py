import numpy as np
import cv2

class Video:

    def __init__(self, file_name):
        #play_video
        self.vid = file_name
        self.esc = 'q'
        #read_video
        self.encoding='utf-8'

    def play_video(self):
        cap = cv2.VideoCapture(self.vid)

        while(cap.isOpened()):
            ret, frame = cap.read()
            
            if not ret or cv2.waitKey(1) & 0xFF == ord(self.esc):
                break
                
            cv2.imshow('Video',frame)
            
        cap.release()
        cv2.destroyAllWindows()

    def read_video(self):
        f=open(self.vid,"rb")
        c=1
        for line in f:
            if c==1:
                line=line.decode(self.encoding)
                fields=line.split(" ")
                self.width=int((fields[1])[1:])
                self.height=int((fields[2])[1:])
                self.fps=int((fields[3])[1:3]) #isto pode nem sempre ser correto segundo o site
                self.getColorSpace(fields)
                print(self.width, self.height, self.fps, self.colorSpace, self.frameLength, self.shape, 'line ',1)
            if c>=2:
                frame=f.read(self.frameLength)
                yuv=np.frombuffer(frame, dtype=np.uint8)
                #yuv=yuv.reshape(shape)
                print(yuv, len(yuv),c)
            c+=1
        print('500 = 50fps * 10 SeemsGood')
        f.close

    def getColorSpace(self,fields):
        for x in fields:
            if x[0]=='C':
                c=x[1:4]
                if c=='444':
                    self.colorSpace='4:4:4'
                    self.frameLength=self.width*self.height*3
                    self.shape = (int(self.height*3), self.width)
                    #not sure about this shape stuff
                elif c=='422':
                    self.colorSpace='4:2:2'
                    self.frameLength=self.width*self.height*2
                    self.shape = (int(self.height*2), self.width)
                elif c=='420':
                    self.colorSpace='4:2:0'
                    self.frameLength=self.width*self.height*3/2
                    self.shape = (int(self.height*1.5), self.width)
                break