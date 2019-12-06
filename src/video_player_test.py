from Video import Video


if __name__ == "__main__":
    v1="../res/ducks_take_off_444_720p50.y4m"
    v2="../res/ducks_take_off_422_720p50.y4m"
    v3="../res/ducks_take_off_420_720p50.y4m"
    v=Video(v2)
    #number of video frames to play
    v.play_video(3)