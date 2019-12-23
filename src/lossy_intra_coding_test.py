## @brief
# Module for testing of the lossy component of the IntraCodec class
#

from IntraCodec import *
from VideoPlayer import *
import sys

if __name__ == "__main__":

    if len(sys.argv)!=6:
        print('\nUsage: python3 lossy_intra_coding.py <frameNumber> <golombFactor> <qs1> <qs2> <qs3>\n\nframeNumber->Number of video frames to encode/decode and show on screen OR \'all\' for all frames in video\ngolombFactor->Golomb\'s parameter M (ex: 4)\nqsX-> Quantization steps for each color component (YUV) (ex:2)\n\nWarning: Higher number of frames will take longer to complete!')
        exit(0)
    else:
        fn=sys.argv[1]
        gol=int(sys.argv[2])
        qs1=int(sys.argv[3])
        qs2=int(sys.argv[4])
        qs3=int(sys.argv[5])

        if fn=='all':
            fn=None
        else:
            fn=int(fn)

    v1="../res/ducks_take_off_444_720p50.y4m"
    v2="../res/ducks_take_off_422_720p50.y4m"
    v3="../res/ducks_take_off_420_720p50.y4m"

    ans=input('There are 3 videos in our repository,\n1)ducks_take_off_444\n2)ducks_take_off_422\n3)ducks_take_off_420\nEach in the respective format, choose the desired one (1,2,3) :  ')
    if ans=='1':
        video=v1
    elif ans=='2':
        video=v2
    elif ans=='3':
        video=v3
    else:
        print('Invalid answer')
        exit(0)
    
    v=IntraCodec(video)

    v.encode_video('../res/intra_encoded', golombparam=gol,q=[qs1,qs2,qs3],limitFrames=fn)

    encodVid=IntraCodec('../res/intra_encoded', encoded=True,limitFrames=fn)

    vp=VideoPlayer(encodVid,imported=True)

    v.verifyData(encodVid,fn)

    vp.play_video(frameNumber=fn)

