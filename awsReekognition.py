import cv2
from picamera import PiCamera
from time import sleep
from datetime import datetime
import boto3
import os

class ObjectDetector(object):
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.rotation = 180
        self.threshold = 1000  # Adjust this threshold as needed
        self.previous_frame = None
        self.access_key_id = ''
        self.secret_key = ''
        self.region_name = 'us-west-2'  # Change this to your desired AWS region
        self.client = boto3.client('rekognition',
                                   aws_access_key_id=self.access_key_id,
                                   aws_secret_access_key=self.secret_key,
                                   region_name=self.region_name)

    def start(self):
        while True:
            current_frame = self.capture_frame()
            if self.detect_motion(current_frame):
                print("Motion detected!")
                labels = self.detect_objects('photo.jpg')
                self.send_data(labels)
                sleep(5)  # Record video for 5 seconds
            else:
                print("No motion detected")

    def capture_frame(self):
        self.camera.capture('photo.jpg')
        frame = cv2.imread('photo.jpg')
        return frame

    def detect_motion(self, frame):
        if self.previous_frame is None:
            self.previous_frame = frame
            return False

        frame_diff = cv2.absdiff(frame, self.previous_frame).sum()
        self.previous_frame = frame
        return frame_diff > self.threshold

    def detect_objects(self, photo_path):
        with open(photo_path, 'rb') as source_photo:
            source_bytes = source_photo.read()

        response = self.client.detect_labels(Image={'Bytes': source_bytes})
        labels = []
        for label in response['Labels']:
            labels.append(label['Name'])
        return labels

    def send_data(self, labels):
        # Example: Send labels to a database, API, or another service
        print("Detected objects:", labels)

def main():
    obj_detector = ObjectDetector()
    obj_detector.start()

if __name__ == "__main__":
    main()
