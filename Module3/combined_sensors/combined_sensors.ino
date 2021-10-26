#include "Arduino.h"
#include <WiFi.h>

#define COLOR_S0 34
#define COLOR_S1 35
#define COLOR_S2 32
#define COLOR_S3 33
#define COLOR_OUT 25
#define DIY_IN 26
#define PIEZO_IN 27
#define SOUND_IN 14
#define PHOTO_IN 13

int frequency = 0;
int frequency_r = 0;
int frequency_g = 0;
int frequency_b = 0;

const char* ssid = "yale wireless";
const char* password = "";

const uint16_t port = 8090;
const char* host = "172.27.120.240";

WiFiClient client;

void setup() {
  // put your setup code here, to run once:
  pinMode(COLOR_S0, OUTPUT);
  pinMode(COLOR_S1, OUTPUT);
  pinMode(COLOR_S2, OUTPUT);
  pinMode(COLOR_S3, OUTPUT);
  pinMode(COLOR_OUT, INPUT);
  // Setting frequency-scaling to 20%
  digitalWrite(COLOR_S0, HIGH);
  digitalWrite(COLOR_S1, LOW);
  
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
  pinMode(DIY_IN, INPUT);
  pinMode(PIEZO_IN, INPUT);
  pinMode(SOUND_IN, INPUT);
  pinMode(PHOTO_IN, INPUT);
}

void loop() {
  // Setting red filtered photodiodes to be read
  digitalWrite(COLOR_S2, LOW);
  digitalWrite(COLOR_S3, LOW);
  // Reading the output frequency
  frequency = pulseIn(COLOR_OUT, LOW);
  frequency_r = frequency;
  //client.print(frequency_r);
  //client.print(",");
  Serial.print(frequency_r);
  Serial.print(",");

  // Setting Green filtered photodiodes to be read
  digitalWrite(COLOR_S2, HIGH);
  digitalWrite(COLOR_S3, HIGH);
  // Reading the output frequency
  frequency = pulseIn(COLOR_OUT, LOW);
  frequency_g = frequency;
  //client.print(frequency_g);
  //client.print(",");
  Serial.print(frequency_g);
  Serial.print(",");

  // Setting Blue filtered photodiodes to be read
  digitalWrite(COLOR_S2, LOW);
  digitalWrite(COLOR_S3, HIGH);
  // Reading the output frequency
  frequency = pulseIn(COLOR_OUT, LOW);
  frequency_b = frequency;
  //client.print(frequency_b);
  //client.print(",");
  Serial.print(frequency_b);
  Serial.print(",");

  int diy_val = analogRead(DIY_IN);
  //client.print(diy_val);
  //client.print(",");
  Serial.print(diy_val);
  Serial.print(",");

  int piezo_val = analogRead(PIEZO_IN);
  //client.print(piezo_val);
  //client.print(",");
  Serial.print(piezo_val);
  Serial.print(",");

  int sound_val = analogRead(SOUND_IN);
  //client.print(sound_val);
  //client.print(",");
  Serial.print(sound_val);
  Serial.print(",");

  int photo_val = analogRead(PHOTO_IN);
  //client.print(photo_val);
  //client.print("\n");
  Serial.print(photo_val);
  Serial.print("\n");

  delay(10);
}
