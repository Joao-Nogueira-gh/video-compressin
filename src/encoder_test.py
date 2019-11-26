import numpy as np
import cv2
import Golomb
import Bitstream

#https://wiki.multimedia.cx/index.php/YUV4MPEG2
#https://stackoverflow.com/questions/2231518/how-to-read-a-frame-from-yuv-file-in-opencv
#https://pypi.org/project/y4m/ , hmm thats stupid tho

def getColorSpace(fields,width,height):
    for x in fields:
        if x[0]=='C':
            c=x[1:4]
            if c=='444':
                colorSpace='4:4:4'
                frameLength=width*height*3
                shape = (int(height*3), width)
                #not sure about this shape stuff
            elif c=='422':
                colorSpace='4:2:2'
                frameLength=width*height*2
                shape = (int(height*2), width)
            elif c=='420':
                colorSpace='4:2:0'
                frameLength=width*height*3/2
                shape = (int(height*1.5), width)
            break
    return colorSpace, frameLength, shape

if __name__ == "__main__":
    encoding='utf-8'
    f=open("../res/ducks_take_off_444_720p50.y4m","rb")
    c=1
    for line in f:
        if c==1:
            line=line.decode(encoding)
            fields=line.split(" ")
            width=int((fields[1])[1:])
            height=int((fields[2])[1:])
            fps=int((fields[3])[1:3]) #isto pode nem sempre ser correto segundo o site
            colorSpace, frameLength, shape=getColorSpace(fields,width,height)
            print(width, height, fps, colorSpace, frameLength, shape, 1)
        if c>=2:
            frame=f.read(frameLength)
            yuv=np.frombuffer(frame, dtype=np.uint8)
            #yuv=yuv.reshape(shape)
            print(yuv, len(yuv),c)
        c+=1
    print('500 = 50fps * 10 SeemsGood')
    f.close




