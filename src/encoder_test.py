from Video import Video

if __name__ == "__main__":
    v1="../res/ducks_take_off_444_720p50.y4m"
    v2="../res/ducks_take_off_422_720p50.y4m"	
    v3="../res/ducks_take_off_420_720p50.y4m"
    v=Video(v1,'normal')
    v.printPixels()
    m1,m2,m3=v.getStuff()
    v.encode_video('encoded')
    encodVid=Video('encoded','intra_encoding')
    m4,m5,m6=v.getStuff()
    encodVid.printPixels()
    encodVid.play_video(1)

