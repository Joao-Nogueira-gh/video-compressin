import numpy as np
import cv2
import Golomb
import Bitstream
from Video import Video

#https://wiki.multimedia.cx/index.php/YUV4MPEG2
#https://stackoverflow.com/questions/2231518/how-to-read-a-frame-from-yuv-file-in-opencv
#https://pypi.org/project/y4m/ , hmm thats stupid tho

if __name__ == "__main__":
    v=Video("../res/ducks_take_off_444_720p50.y4m")
    v.read_video()




