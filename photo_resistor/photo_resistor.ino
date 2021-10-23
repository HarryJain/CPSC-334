#include "Arduino.h"

#define PHOTO_PIN 36

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  pinMode(PHOTO_PIN, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  int analogValue = analogRead(PHOTO_PIN);

  Serial.print("Analog reading: ");
  Serial.println(analogValue);

  delay(500);
}
