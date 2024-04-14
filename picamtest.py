import cv2
import cvlib as cv2
from cvlib.object_detection import draw_bbox
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# Initialize Picamera and grab reference to the raw capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# Allow the camera to warmup
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Grab the raw NumPy array representing the image
    image = frame.array

    bbox, label, conf = cv.detect_common_objects(image)
    output_image = draw_bbox(image, bbox, label, conf)

    # Show the output frame
    cv2.imshow("Real-time object detection", output_image)
    key = cv2.waitKey(1) & 0xFF

    # Clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # If the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# Close the window and release the camera resources
cv2.destroyAllWindows()
