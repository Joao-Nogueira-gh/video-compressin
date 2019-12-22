from Video import Video
from numpy import *

if __name__ == "__main__":
    numberoframes=2
    v1="../res/ducks_take_off_444_720p50.y4m"
    v2="../res/ducks_take_off_422_720p50.y4m"	
    v3="../res/ducks_take_off_420_720p50.y4m"
    v=Video(v1,'normal')
    v.hybrid_encoding('../res/hybrid_encoded',block_size=8,search_area=1, limitFrames=numberoframes)
    m1,m2,m3=v.getStuff()


    encodVid=Video('../res/hybrid_encoded','hybrid_encoding', limitFrames=numberoframes)
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

