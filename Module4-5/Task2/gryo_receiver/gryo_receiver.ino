// Library imports for ESP-NOW communication
#include <esp_now.h>
#include <WiFi.h>

// Structure to receive gyro data (acceleration and rotation for x, y, and z)
typedef struct gyro_data {
  float accel_x;
  float accel_y;
  float accel_z;
  float rot_x;
  float rot_y;
  float rot_z;
} gyro_data;

// Create a gyro_data struct to receive and store the current values
gyro_data myData;

// Callback function to print MPU-6050 readings when data is sent
void OnDataRecv(const uint8_t *mac, const uint8_t *incomingData, int len) {
  memcpy(&myData, incomingData, sizeof(myData));
  Serial.print("Bytes received: ");
  Serial.println(len);
  Serial.print("Acceleration X: ");
  Serial.print(myData.accel_x);
  Serial.print(", Y: ");
  Serial.print(myData.accel_y);
  Serial.print(", Z: ");
  Serial.print(myData.accel_z);
  Serial.println(" m/s^2");

  Serial.print("Rotatation X: ");
  Serial.print(myData.rot_x);
  Serial.print(", Y: ");
  Serial.print(myData.rot_y);
  Serial.print(", Z: ");
  Serial.print(myData.rot_z);
  Serial.println(" m/s^2");
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
