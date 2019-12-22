from IntraCodec import *
from VideoPlayer import *
import sys

if __name__ == "__main__":

    if len(sys.argv)!=2:
        print('\nUsage: python3 intra_codec_test.py <frameNumber>\n\nframeNumber->Number of video frames to encode/decode and show on screen OR \'all\' for all frames in video\n\nWarning: Higher number of frames will take longer to complete!')
        exit(0)
    else:
        fn=sys.argv[1]
        if fn=='all':
            fn=None
        else:
            fn=int(fn)

    v1="../res/ducks_take_off_444_720p50.y4m"
    v2="../res/ducks_take_off_422_720p50.y4m"	
    v3="../res/ducks_take_off_420_720p50.y4m"
    
    v=IntraCodec(v1)

    v.encode_video('../res/intra_encoded', golombparam=4,limitFrames=fn)

    encodVid=IntraCodec('../res/intra_encoded', encoded=True,limitFrames=fn)

    v.verifyData(encodVid,fn)

    vp=VideoPlayer(encodVid,imported=True)

    vp.play_video(frameNumber=fn)

