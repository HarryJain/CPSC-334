#include "WiFi.h"

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  WiFi.mode(WIFI_MODE_STA);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(WiFi.macAddress());

  delay(500);
}
