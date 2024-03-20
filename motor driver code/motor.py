import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins
ENA = 18
IN1 = 23
IN2 = 24
ENB = 25
IN3 = 5
IN4 = 6

# Setup GPIO pins
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Set ENA and ENB to HIGH to enable motor driver outputs
GPIO.output(ENA, GPIO.HIGH)
GPIO.output(ENB, GPIO.HIGH)

# Define motor control functions
def forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

# Move motors forward for 2 seconds
forward()
time.sleep(2)

# Stop motors for 1 second
stop()
time.sleep(1)

# Move motors backward for 2 seconds
backward()
time.sleep(2)

# Stop motors
stop()

# Clean up GPIO
GPIO.cleanup()
