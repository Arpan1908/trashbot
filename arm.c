#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define SERVOMIN  150 // Minimum pulse length in microseconds
#define SERVOMAX  600 // Maximum pulse length in microseconds
#define MAX_DISTANCE 200 // Maximum distance in centimeters

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

int trigPin = 2; // Trigger pin for ultrasonic sensor
int echoPin = 3; // Echo pin for ultrasonic sensor
int servoPins[] = {0, 1, 4, 5, 6}; // PWM pins connected to servos
int servoAngles[] = {90, 90, 90, 90, 90}; // Initial angles for servos

void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  // Read distance from ultrasonic sensor
  long duration, distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;

  // If object detected within range, pick up object
  if (distance > 0 && distance < MAX_DISTANCE) {
    pickObject();
  }
}

void pickObject() {
  // Move servos to pick up object
  setServoAngles(180, 90, 90, 90, 90);
  delay(1000); // Adjust delay as needed
  // Release object
  setServoAngles(90, 90, 90, 90, 90);
  delay(1000); // Adjust delay as needed
}

void setServoAngles(int servo1, int servo2, int servo3, int servo4, int servo5) {
  pwm.setPWM(servoPins[0], 0, map(servo1, 0, 180, SERVOMIN, SERVOMAX));
  pwm.setPWM(servoPins[1], 0, map(servo2, 0, 180, SERVOMIN, SERVOMAX));
  pwm.setPWM(servoPins[2], 0, map(servo3, 0, 180, SERVOMIN, SERVOMAX));
  pwm.setPWM(servoPins[3], 0, map(servo4, 0, 180, SERVOMIN, SERVOMAX));
  pwm.setPWM(servoPins[4], 0, map(servo5, 0, 180, SERVOMIN, SERVOMAX));
}
