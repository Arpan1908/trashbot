import time
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
from smbus import SMBus

PCA9685_I2C_ADDR = 0x40
PCA9685_MODE1 = 0x00
PCA9685_PRESCALE = 0xFE
PCA9685_LED0_ON_L = 0x06

BASE_SERVO_PIN = 0
SECONDARY_SERVO_PIN = 1
# Add pins for additional servos as needed

def set_servo_angle(bus, servo_pin, angle):
    pulse_width = int(2048 + angle * 2.048)  # 2.048 is the conversion factor for 1 degree
    off_time = pulse_width & 0xFF
    on_time = pulse_width >> 8
    # Set off time
    bus.write_byte_data(PCA9685_I2C_ADDR, PCA9685_LED0_ON_L + 4 * servo_pin, off_time)
    bus.write_byte_data(PCA9685_I2C_ADDR, PCA9685_LED0_ON_L + 4 * servo_pin + 1, off_time >> 8)
    # Set on time
    bus.write_byte_data(PCA9685_I2C_ADDR, PCA9685_LED0_ON_L + 4 * servo_pin + 2, on_time)
    bus.write_byte_data(PCA9685_I2C_ADDR, PCA9685_LED0_ON_L + 4 * servo_pin + 3, on_time >> 8)

def detect_objects(frame):
    bbox, label, conf = cv.detect_common_objects(frame)
    output_image = draw_bbox(frame, bbox, label, conf)
    return bbox, output_image

def calculate_object_position(bbox):
    x_center = (bbox[0] + bbox[2]) / 2
    y_center = (bbox[1] + bbox[3]) / 2
    return x_center, y_center

def move_arm(base_angle, secondary_angle, base_speed=1.0, secondary_speed=1.0):
    # Adjust speed
    base_speed = max(min(base_speed, 1.0), 0.1)  # Ensure speed is within range (0.1 to 1.0)
    secondary_speed = max(min(secondary_speed, 1.0), 0.1)
    # Calculate delay based on speed
    base_delay = (1.0 - base_speed) * 0.5
    secondary_delay = (1.0 - secondary_speed) * 0.5

    # Set servo angles with delays
    set_servo_angle(bus, BASE_SERVO_PIN, base_angle)
    time.sleep(base_delay)
    set_servo_angle(bus, SECONDARY_SERVO_PIN, secondary_angle)
    time.sleep(secondary_delay)

def main():
    # Initialize PCA9685
    bus = SMBus(1)
    bus.write_byte_data(PCA9685_I2C_ADDR, PCA9685_MODE1, 0x00)
    prescale_val = int(25e6 / (4096 * 50) - 1)  # 50Hz for servos
    bus.write_byte_data(PCA9685_I2C_ADDR, PCA9685_PRESCALE, prescale_val)
    bus.write_byte_data(PCA9685_I2C_ADDR, PCA9685_MODE1, 0xA0)  # Restart

    video_capture = cv2.VideoCapture(0)

    try:
        while True:
            ret, frame = video_capture.read()

            bbox, output_image = detect_objects(frame)

            cv2.imshow("Real-time object detection", output_image)

            if bbox:
                x_center, y_center = calculate_object_position(bbox)
                
                # Scale angles according to servo range (usually 0-180 degrees)
                base_angle = int(x_center * 180 / frame.shape[1])
                secondary_angle = int(y_center * 180 / frame.shape[0])
                # Adjust the angle values as needed for other servos
                
                # Set servo angles with controlled speed
                move_arm(base_angle, secondary_angle, base_speed=0.5, secondary_speed=0.8)
                # Adjust speeds for other servos as needed

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        bus.close()
        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
