import numpy as np
import cv2

class VideoPlayer:

    def __init__(self, file_name, escape='q'):
        self.vid = file_name
        self.esc = escape

    def play_video(self):
        cap = cv2.VideoCapture(self.vid)

        while(cap.isOpened()):
            ret, frame = cap.read()
            
            if not ret or cv2.waitKey(1) & 0xFF == ord(self.esc):
                break
                
            cv2.imshow('Video',frame)
            
        cap.release()
        cv2.destroyAllWindows()