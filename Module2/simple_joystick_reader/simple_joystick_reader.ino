// Include Libraries
#include "Arduino.h"


// Pin constants for x, y, and button
#define JOYSTICK_PIN_X 36
#define JOYSTICK_PIN_Y 39
#define JOYSTICK_PIN_BUTTON 34


// Set the serial baud and the pinmodes
void setup() {
  Serial.begin(115200);

  pinmode(JOYSTICK_PIN_X, INPUT);
  pinmode(JOYSTICK_PIN_Y, INPUT);
  pinmode(JOYSTICK_PIN_X, INPUT_PULLUP);
}


// Get the analog values for the joystick axes and button and print them to the serial port
void loop() {
  int joystick_x = analogRead(JOYSTICK_PIN_X);
  int joystick_y = analogRead(JOYSTICK_PIN_Y);
  int joystick_button = analogRead(JOYSTICK__PIN_BUTTON);

  Serial.print(joystick_x, joystick_y, joystick_button);
}
