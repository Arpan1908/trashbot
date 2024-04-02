from picamera import PiCamera
from time import sleep
import numpy as np
import cv2
import board
import busio
from adafruit_servokit import ServoKit

# Initialize PCA9685 and servo kit
i2c_bus = busio.I2C(board.SCL, board.SDA)
kit = ServoKit(channels=16, i2c=i2c_bus)

# Define servo indices
# Adjust these indices based on your servo connections to PCA9685
m_index = 0
u_index = 1
d_index = 2
# Add indices for the additional servos
servo_4_index = 3
servo_5_index = 4

# Define servo angles
M_ANGLE_PICKUP = 90
M_ANGLE_DROP = 15
U_ANGLE_PICKUP = 0
U_ANGLE_DROP = 45
D_ANGLE_PICKUP = 45
D_ANGLE_DROP = 0
# Add angles for additional servos
SERVO_4_ANGLE = 0
SERVO_5_ANGLE = 90

# Initialize the camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30

# Warm-up time for camera
sleep(2)

def detect_color(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Add color detection logic here
    low_yellow = np.array([20, 50, 100], dtype=np.uint8)
    high_yellow = np.array([42, 255, 255], dtype=np.uint8)
    mask_yellow = cv2.inRange(hsv, low_yellow, high_yellow)
    count_yellow = cv2.countNonZero(mask_yellow)

    # Blue color range
    low_blue = np.array([110, 130, 50], dtype=np.uint8)
    high_blue = np.array([130, 255, 255], dtype=np.uint8)
    mask_blue = cv2.inRange(hsv, low_blue, high_blue)
    count_blue = cv2.countNonZero(mask_blue)

    # Green color range
    low_green = np.array([44, 54, 63], dtype=np.uint8)
    high_green = np.array([90, 255, 255], dtype=np.uint8)
    mask_green = cv2.inRange(hsv, low_green, high_green)
    count_green = cv2.countNonZero(mask_green)

    return count_yellow, count_blue, count_green
    pass

def move_servos_pickup():
    kit.servo[m_index].angle = M_ANGLE_PICKUP
    kit.servo[u_index].angle = U_ANGLE_PICKUP
    kit.servo[d_index].angle = D_ANGLE_PICKUP
    kit.servo[servo_4_index].angle = SERVO_4_ANGLE
    kit.servo[servo_5_index].angle = SERVO_5_ANGLE
    sleep(1)

def move_servos_drop():
    kit.servo[m_index].angle = M_ANGLE_DROP
    kit.servo[u_index].angle = U_ANGLE_DROP
    kit.servo[d_index].angle = D_ANGLE_DROP
    kit.servo[servo_4_index].angle = SERVO_4_ANGLE
    kit.servo[servo_5_index].angle = SERVO_5_ANGLE
    sleep(1)

try:
    while True:
        # Capture frame from the camera
        frame = np.empty((480, 640, 3), dtype=np.uint8)
        camera.capture(frame, 'bgr')
        
        # Detect colors
        detect_color(frame)

        # Example logic for color detection
        # if blue_count > 4000:
        #     print('Blue detected')
        #     move_servos_pickup()  # Move servos to pick up position
        #     sleep(2)  # Wait for the object to be picked up
        #     move_servos_drop()  # Move servos to drop position
        #     sleep(2)  # Wait for the object to be dropped
        # elif green_count > 4000:
        #     print('Green detected')
        #     move_servos_pickup()  # Move servos to pick up position
        #     sleep(2)  # Wait for the object to be picked up
        #     move_servos_drop()  # Move servos to drop position
        #     sleep(2)  # Wait for the object to be dropped
        # elif yellow_count > 8000:
        #     print('Yellow detected')
        #     move_servos_pickup()  # Move servos to pick up position
        #     sleep(2)  # Wait for the object to be picked up
        #     move_servos_drop()  # Move servos to drop position
        #     sleep(2)  # Wait for the object to be dropped
        if blue_count > 4000:
            print('Blue detected')
            move_servos_pickup()  # Move servos to pick up position
            sleep(2)  # Wait for the object to be picked up
            move_servos_drop()  # Move servos to drop position
            sleep(2)  # Wait for the object to be dropped
        elif green_count > 4000:
            print('Green detected')
            move_servos_pickup()  # Move servos to pick up position
            sleep(2)  # Wait for the object to be picked up
            move_servos_drop()  # Move servos to drop position
            sleep(2)  # Wait for the object to be dropped
        elif yellow_count > 8000:
            print('Yellow detected')
            move_servos_pickup()  # Move servos to pick up position
            sleep(2)  # Wait for the object to be picked up
            move_servos_drop()  # Move servos to drop position
            sleep(2)  # Wait for the object to be dropped


except KeyboardInterrupt:
    pass

finally:
    camera.close()
