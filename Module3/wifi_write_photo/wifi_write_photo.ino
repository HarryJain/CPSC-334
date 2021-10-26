#include "Arduino.h"
#include <analogWrite.h>
#include <WiFi.h>

#define PHOTO_PIN 36
#define RED_PIN 33
#define BLUE_PIN 25
#define GREEN_PIN 26

const char* ssid     = "yale wireless";
const char* password = "";

const uint16_t port = 8090;
const char* host = "172.27.118.116";

WiFiClient client;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  if (!client.connect(host, port)) {
      Serial.println("Connection to host failed");

      delay(1000);
      return;
  }

  Serial.println("Connected to server successful!");

  pinMode(PHOTO_PIN, INPUT);
  pinMode(RED_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
}

void loop() {
  int analogValue = analogRead(PHOTO_PIN);
 
  client.print(analogValue);

  if (analogValue > 2000) {
    //Serial.print(analogValue);
    
    analogWrite(RED_PIN, 255);
    analogWrite(GREEN_PIN, 255);
    analogWrite(BLUE_PIN, 255);

    /*digitalWrite(RED_PIN, HIGH);
    digitalWrite(GREEN_PIN, HIGH);
    digitalWrite(BLUE_PIN, HIGH);*/
  } else {
    analogWrite(RED_PIN, 255);
    analogWrite(GREEN_PIN, 165);
    analogWrite(BLUE_PIN, 0);
    
    /*digitalWrite(RED_PIN, LOW);
    digitalWrite(GREEN_PIN, LOW);
    digitalWrite(BLUE_PIN, LOW);*/
  }

  //Serial.println("Disconnecting...");
  //client.stop();
  
  // put your main code here, to run repeatedly:


  delay(1000);
}
