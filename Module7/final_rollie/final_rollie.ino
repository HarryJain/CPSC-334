// Library imports for ESP-NOW communication
#include <esp_now.h>
#include <WiFi.h>


// L298N motor controller Pins
#define CONTROLLER_IN1 27
#define CONTROLLER_IN2 26
#define CONTROLLER_IN3 25
#define CONTROLLER_IN4 33


// Structure to receive gyro data
//  (one-hot encoding of movement directions)
typedef struct gyro_data {
  bool forwards;
  bool backwards;
  bool clockwise;
  bool counterclockwise;
} gyro_data;

// Create a gyro_data struct to receive and store the current values
gyro_data myData;


// Callback function to print MPU-6050 readings when data is sent
void OnDataRecv(const uint8_t *mac, const uint8_t *incomingData, int len) {
  // Copy the incoming data to the myData variable
  memcpy(&myData, incomingData, sizeof(myData));

  // Move GBBO according to the tilt of the glove
  if (myData.forwards) {    
    // Move Rollie forwards
    digitalWrite(CONTROLLER_IN1, LOW);
    digitalWrite(CONTROLLER_IN2, HIGH);
    digitalWrite(CONTROLLER_IN3, LOW);
    digitalWrite(CONTROLLER_IN4, HIGH);
    Serial.println("Moving forwards");
  } else if (myData.backwards) {
    // Move Rollie backwards
    digitalWrite(CONTROLLER_IN1, HIGH);
    digitalWrite(CONTROLLER_IN2, LOW);
    digitalWrite(CONTROLLER_IN3, HIGH);
    digitalWrite(CONTROLLER_IN4, LOW);
    Serial.println("Moving backwards");
  } else if (myData.clockwise) {
    // Turn GBBO clockwise
    digitalWrite(CONTROLLER_IN1, LOW);
    digitalWrite(CONTROLLER_IN2, HIGH);
    digitalWrite(CONTROLLER_IN3, LOW);
    digitalWrite(CONTROLLER_IN4, LOW);
    Serial.println("Moving clockwise");
  } else if (myData.counterclockwise) {
    // Turn GBBO counterclockwise
    digitalWrite(CONTROLLER_IN1, LOW);
    digitalWrite(CONTROLLER_IN2, LOW);
    digitalWrite(CONTROLLER_IN3, LOW);
    digitalWrite(CONTROLLER_IN4, HIGH);
    Serial.println("Moving counterclockwise");
  } else {
    // Stop GBBO
    digitalWrite(CONTROLLER_IN1, LOW);
    digitalWrite(CONTROLLER_IN2, LOW);
    digitalWrite(CONTROLLER_IN3, LOW);
    digitalWrite(CONTROLLER_IN4, LOW);
    Serial.println("Stopped");
  }
  

  // Add delay in between data reads in order to avoid task
  //  watchdog error
  //  (https://github.com/espressif/arduino-esp32/issues/3871)
  delay(1);
}


void setup() {
  // Set upload speed
  Serial.begin(115200);

  // Set device as a Wi-Fi station
  WiFi.mode(WIFI_STA);

  // Initialize ESP-NOW and check for errors
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // When ESP-NOW is fulled intialized, register our callback function on receive
  esp_now_register_recv_cb(OnDataRecv);


  // Set the motor pins as outputs
  pinMode(CONTROLLER_IN1, OUTPUT);
  pinMode(CONTROLLER_IN2, OUTPUT);
  pinMode(CONTROLLER_IN3, OUTPUT);
  pinMode(CONTROLLER_IN4, OUTPUT);
}


void loop() {
  
}


// References and Copyrights
/*
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/esp-now-esp32-arduino-ide/
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files.
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
*/
