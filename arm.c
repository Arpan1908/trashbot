#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
#define SERVOMIN  150
#define SERVOMAX  600

#define CRAW_SERVO 5
#define WRIST_SERVO 4
#define ELBOW_SERVO 3
#define SHOULDER_SERVO 2
#define WAIST_SERVO 1
#define HIP_SERVO 0

const int trigPin = 2;  // Trig Pin of Ultrasonic Sensor
const int echoPin = 3; // Echo Pin of Ultrasonic Sensor

void setup() {
  Serial.begin(9600);
  
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  pwm.begin();
  pwm.setPWMFreq(60);
  delay(10);

  OpenCraw();
}

void loop() {
  // Measure distance using ultrasonic sensor
  long duration, distance;
  digitalWrite(trigPin, LOW);  
  delayMicroseconds(2); 
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10); 
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2; // Calculate distance in cm

  Serial.print("Distance: ");
  Serial.println(distance);

  // Check if the distance is less than 10cm
  if (distance < 10) {
    CloseCraw(); // If object detected close claw
    delay(1000); // Wait for 1 second
  } else {
    OpenCraw(); // If no object detected open claw
    delay(1000); // Wait for 1 second
  }
}

void OpenCraw() {
  Serial.println("open craw");
  pwm.setPWM(CRAW_SERVO, 0, SERVOMIN);
}

void CloseCraw() {
  Serial.println("close craw");
  pwm.setPWM(CRAW_SERVO, 0, SERVOMAX);
}
