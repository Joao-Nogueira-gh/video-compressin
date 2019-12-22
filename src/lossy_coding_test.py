from Video import Video
from numpy import *

if __name__ == "__main__":
    numberoframes=2

    v1="../res/ducks_take_off_444_720p50.y4m"
    v2="../res/ducks_take_off_422_720p50.y4m"	
    v3="../res/ducks_take_off_420_720p50.y4m"
    v=Video(v1,'normal')

    m1,m2,m3=v.getStuff()

    v.encode_video('../res/lossy_encoded', q=2, limitFrames=numberoframes)

    encodVid=Video('../res/lossy_encoded','intra_encoding', limitFrames=numberoframes)
    m4,m5,m6=encodVid.getStuff()
    
    for i in range(0,numberoframes):
        if (array_equal(m1[i],m4[i])):
            print('aoi')
    for i in range(0,numberoframes):
        if (array_equal(m2[i],m5[i])):
            print('boi')
    for i in range(0,numberoframes):
        if (array_equal(m3[i],m6[i])):
            print('coi')

    encodVid.play_video(numberoframes)

