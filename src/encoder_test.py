import numpy as np
import cv2
import Golomb
import Bitstream

#https://wiki.multimedia.cx/index.php/YUV4MPEG2
#https://stackoverflow.com/questions/2231518/how-to-read-a-frame-from-yuv-file-in-opencv
#https://pypi.org/project/y4m/ , hmm thats stupid tho


if __name__ == "__main__":
    f=open("../res/ducks_take_off_444_720p50.y4m","rb")
    c=0
    for line in f:
        if c==2:
            break
        print(line)
        c+=1
    f.close

