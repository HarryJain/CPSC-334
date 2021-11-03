// Stepper imports and constants
#include <Stepper.h>

// Number of steps per 360 degree revolution
#define STEPSPERREVOLUTION 2048

// ULN2003 Motor Driver Pins
#define DRIVER_IN1 19
#define DRIVER_IN2 18
#define DRIVER_IN3 5
#define DRIVER_IN4 17

// Speed constant for rpm
#define SPEED 15

// Stepper object for 28BYJ-48 stepper motor
Stepper stepper(STEPSPERREVOLUTION, DRIVER_IN1, DRIVER_IN3, DRIVER_IN2, DRIVER_IN4);


// Server imports and constants
#include <Servo.h>

// Pin for server input
#define SERVO_PIN 4

// Servo object for MG90S servo motor
Servo servo;

// Set initial server position to 0
int servo_pos = 100;


// Set up the stepper and server motors
void setup() {
  // Set the stepper speed at SPEED rpm
  stepper.setSpeed(SPEED);
  // Attach the servo pin
  servo.attach(SERVO_PIN);
  // Reset the stepper position
  servo.write(servo_pos);
  // Initialize the serial port
  Serial.begin(115200);
}


// Move the stepper and servo such that each time the stepper motor rotates
//  360 degrees, the servo motor rotates 10 degrees until it reaches 180, when
//  it returns to 0 degrees
void loop() {
  // Move the stepper one revolution (360 degrees)
  stepper.step(STEPSPERREVOLUTION);
  // Rotate the servo 10 degrees
  servo_pos += 10;
  // At 180 degrees, return the servo to 0 degrees
  if (servo_pos > 180) {
    servo_pos = 0;
  }
  // Rotate the servo to the calculated position
  servo.write(servo_pos);
}
