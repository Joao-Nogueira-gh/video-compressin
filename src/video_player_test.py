from VideoPlayer import *
import sys

if __name__ == "__main__":

    if len(sys.argv)!=2:
        print('\nUsage: python3 video_player_test.py <frameNumber>\n\nframeNumber->Number of video frames to play OR \'all\' for all frames in video\n\nWarning: Higher number of frames will take longer to complete!')
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

    v=VideoPlayer(v1)

    v.play_video(frameNumber=fn)