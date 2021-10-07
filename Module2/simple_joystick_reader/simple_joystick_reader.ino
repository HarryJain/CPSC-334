// Include Libraries
#include "Arduino.h"


// Pin constants for x, y, and button
#define JOYSTICK_PIN_X 36
#define JOYSTICK_PIN_Y 39
#define JOYSTICK_PIN_BUTTON 34
#define PIN_BUTTON 35
#define PIN_SWITCH 32


// Set the serial baud and the pinmodes
void setup() {
  Serial.begin(115200);

  pinMode(JOYSTICK_PIN_X, INPUT);
  pinMode(JOYSTICK_PIN_Y, INPUT);
  pinMode(JOYSTICK_PIN_BUTTON, INPUT);
  pinMode(PIN_BUTTON, INPUT);
  pinMode(PIN_SWITCH, INPUT);
}


// Get the analog values for the joystick axes and button and print them to the serial port
void loop() {
  int joystick_x = analogRead(JOYSTICK_PIN_X);
  int joystick_y = analogRead(JOYSTICK_PIN_Y);
  int joystick_button = analogRead(JOYSTICK_PIN_BUTTON);
  int button = analogRead(PIN_BUTTON);
  int switch_val = analogRead(PIN_SWITCH);

  Serial.print(joystick_x);
  Serial.print(", ");
  Serial.print(joystick_y);
  Serial.print(", ");
  Serial.print(joystick_button);
  Serial.print(", ");
  Serial.print(button);
  Serial.print(", ");
  Serial.print(switch_val);
  Serial.print("\n");
}
