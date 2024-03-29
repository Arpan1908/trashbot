import RPi.GPIO as GPIO
import time
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox


BASE_SERVO_PIN = 17
SECONDARY_SERVO_PIN = 18


GPIO.setmode(GPIO.BCM)

# Set up GPIO pins
GPIO.setup(BASE_SERVO_PIN, GPIO.OUT)
GPIO.setup(SECONDARY_SERVO_PIN, GPIO.OUT)

# Function to control servo angle
def set_servo_angle(pin, angle):
    duty = angle / 18 + 2
    pwm = GPIO.PWM(pin, 50)  # 
    pwm.start(duty)
    time.sleep(1)
    pwm.stop()

# Function to move robotic arm
def move_arm(base_angle, secondary_angle):
    set_servo_angle(BASE_SERVO_PIN, base_angle)
    set_servo_angle(SECONDARY_SERVO_PIN, secondary_angle)

# Function to detect objects
def detect_objects(frame):
    bbox, label, conf = cv.detect_common_objects(frame)
    output_image = draw_bbox(frame, bbox, label, conf)
    return bbox, output_image


def calculate_object_position(bbox):
    
    x_center = (bbox[0] + bbox[2]) / 2
    y_center = (bbox[1] + bbox[3]) / 2
    return x_center, y_center


def main():
    
    video_capture = cv2.VideoCapture(0)

    try:
        while True:
            
            ret, frame = video_capture.read()

            
            bbox, output_image = detect_objects(frame)

            
            cv2.imshow("Real-time object detection", output_image)

            
            if bbox:
                x_center, y_center = calculate_object_position(bbox)
                
                base_angle = int(x_center * 180 / frame.shape[1])
                secondary_angle = int(y_center * 180 / frame.shape[0])
                # Move the arm
                move_arm(base_angle, secondary_angle)

            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        GPIO.cleanup()
        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
