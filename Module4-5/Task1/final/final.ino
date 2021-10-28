#include <Stepper.h>

#define STEPSPERREVOLUTION 2048

// ULN2003 Motor Driver Pins
#define IN1 19
#define IN2 18
#define IN3 5
#define IN4 17

#define SPEED 10

Stepper my_stepper(STEPSPERREVOLUTION, IN1, IN3, IN2, IN4);


#include <Servo.h>

#define SERVO 4

Servo servo;
int servo_pos = 0;


void setup() {
  // set the speed at SPEED rpm
  my_stepper.setSpeed(SPEED);
  // attach the servo pin
  servo.attach(SERVO);
  servo.write(servo_pos);
  // initialize the serial port
  Serial.begin(115200);
}

void loop() {
  // step one revolution in one direction:
  my_stepper.step(STEPSPERREVOLUTION);
  servo_pos += 10;
  if (servo_pos > 180) {
    servo_pos = 0;
  }
  servo.write(servo_pos);
}
