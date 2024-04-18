from picamera import PiCamera
from time import sleep
from datetime import datetime
import numpy as np
import pandas as pd
 
class Detector(object):
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.rotation = 180
        self.threshold = 1000  # Adjust this threshold as needed
        self.previous_frame = None
         
    def start(self):
        while True:
            current_frame = self.capture_frame()
            if self.detect_motion(current_frame):
                print("Motion detected!")
                self.start_camera()
                sleep(5)  # Record video for 5 seconds
                self.camera.stop_recording()
            else:
                print("No motion detected")
         
    def capture_frame(self):
        frame = np.empty((480, 640, 3), dtype=np.uint8)
        self.camera.capture(frame, 'rgb')
        return frame
         
    def detect_motion(self, frame):
        if self.previous_frame is None:
            self.previous_frame = frame
            return False
         
        frame_diff = np.sum(np.abs(frame - self.previous_frame))
        self.previous_frame = frame
        return frame_diff > self.threshold
     
    def start_camera(self):
        datename = "{0:%Y}-{0:%m}-{0:%d}:{0:%H}:{0:%M}:{0:%S}".format(datetime.now())
        filename = str(datename) + "video.h264"
        self.camera.start_recording(filename)
     
def main():
    obj = Detector()
    obj.start()
     
 
if __name__ == "__main__":
    main()
