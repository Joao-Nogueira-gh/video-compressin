from Video import Video
from numpy import *

if __name__ == "__main__":
    v1="../res/ducks_take_off_444_720p50.y4m"
    v2="../res/ducks_take_off_422_720p50.y4m"	
    v3="../res/ducks_take_off_420_720p50.y4m"
    v=Video(v3,'normal')
    b=v.getBlocks(0,80)#mdc
    #wowwwwwwwwwwwwwww
    #the thing is, it returns
    # 80,80 80,80 80,80
    # 80,80 80,40 80,40
    # 80,80 40,40 40,40
    # which is 'right', but, not really
    for i in b:
        #print(i)
        #i has len1, tuple of 3 arrays, y u v
        #print(len(i),i)
        y=i[0]
        u=i[1]
        v=i[2]
        print(y.shape,u.shape,v.shape)

    exit(0)
    m1,m2,m3=v.getStuff()

    v.encode_video('encoded')

    encodVid=Video('encoded','intra_encoding')
    m4,m5,m6=encodVid.getStuff()
    
    for i in range(0,1):
        if (array_equal(m1[i],m4[i])):
            print('aoi')
        print(m1[i].shape, m4[i].shape)
    for i in range(0,1):
        if (array_equal(m2[i],m5[i])):
            print('boi')
        print(m2[i].shape, m5[i].shape)
    for i in range(0,1):
        if (array_equal(m3[i],m6[i])):
            print('coi')
        print(m3[i].shape, m6[i].shape)

    for i in range(0,len(m1[0])):
        if not array_equal(m1[0][i], m4[0][i]):
            print(i)
            for xd in range(0,len(m1[0][i])):
                if m1[0][i][xd]!=m4[0][i][xd]:
                    print(xd, m1[0][i][xd], m4[0][i][xd])
            break

    encodVid.play_video(1)

