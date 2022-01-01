// Library imports for ESP-NOW communication
#include <esp_now.h>
#include <WiFi.h>

// MAC address of receiver (E8-68-E7-30-2B-DC or 94-B9-7E-DA-B4-B0)
uint8_t broadcastAddress[] = {0xE8, 0x68, 0xE7, 0x30, 0x2B, 0xDC};
//uint8_t broadcastAddress[] = {0x94, 0xB9, 0x7E, 0xDA, 0xB4, 0xB0};


// Library imports for MPU-6050 readings
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

// Create an MPU-6050 object to read data from
Adafruit_MPU6050 mpu;

// Structure to receive gyro data
//  (one-hot encoding of movement directions)
typedef struct gyro_data {
  bool forwards;
  bool backwards;
  bool clockwise;
  bool counterclockwise;
} gyro_data;

// Create a gyro_data struct to store and send the current values
gyro_data myData;


// Limits for triggering motion in each direction
#define FORWARDS_LIM 6
#define BACKWARDS_LIM 3
#define CLOCKWISE_LIM 4
#define COUNTERCLOCKWISE_LIM 4


// Callback function to print status when data is sent
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("\r\nLast Packet Send Status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Deliver Success": "Delivery Fail");
}


// Vibration motor pin and PWM properties
#define VIBRATION_PIN 13
#define FREQUENCY 5000
#define CHANNEL 0
#define RESOLUTION 8
#define VIBRATION_STRENGTH 100


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

  // When ESP-NOW is fulled intialized, register our callback function on send
  esp_now_register_send_cb(OnDataSent);

  // Register peer device with above MAC address
  esp_now_peer_info_t peerInfo;
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;

  // Add peer device and check for errors
  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("Failed to add peer");
    return;
  }


  // Try to initialize the MPU-6050 and wait while there are errors
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU-6050 chip...");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU-6050 found!");

  // Set accelerometer range and print its value
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  Serial.print("Accelerometer range set to: ");
  switch (mpu.getAccelerometerRange()) {
  case MPU6050_RANGE_2_G:
    Serial.println("+-2G");
    break;
  case MPU6050_RANGE_4_G:
    Serial.println("+-4G");
    break;
  case MPU6050_RANGE_8_G:
    Serial.println("+-8G");
    break;
  case MPU6050_RANGE_16_G:
    Serial.println("+-16G");
    break;
  }

  // Set gyroscope range and print its value
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  Serial.print("Gyro range set to: ");
  switch (mpu.getGyroRange()) {
  case MPU6050_RANGE_250_DEG:
    Serial.println("+- 250 deg/s");
    break;
  case MPU6050_RANGE_500_DEG:
    Serial.println("+- 500 deg/s");
    break;
  case MPU6050_RANGE_1000_DEG:
    Serial.println("+- 1000 deg/s");
    break;
  case MPU6050_RANGE_2000_DEG:
    Serial.println("+- 2000 deg/s");
    break;
  }

  // Set bandwith and print its value
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  Serial.print("Filter bandwidth set to: ");
  switch (mpu.getFilterBandwidth()) {
  case MPU6050_BAND_260_HZ:
    Serial.println("260 Hz");
    break;
  case MPU6050_BAND_184_HZ:
    Serial.println("184 Hz");
    break;
  case MPU6050_BAND_94_HZ:
    Serial.println("94 Hz");
    break;
  case MPU6050_BAND_44_HZ:
    Serial.println("44 Hz");
    break;
  case MPU6050_BAND_21_HZ:
    Serial.println("21 Hz");
    break;
  case MPU6050_BAND_10_HZ:
    Serial.println("10 Hz");
    break;
  case MPU6050_BAND_5_HZ:
    Serial.println("5 Hz");
    break;
  }


  // Configure buzzer motor PWM functionalitites
  ledcSetup(CHANNEL, FREQUENCY, RESOLUTION);
  // Attach the channel to the GPIO to be controlled
  ledcAttachPin(VIBRATION_PIN, CHANNEL);


  // Put a linebreak and short delay after setup
  Serial.println("");
  delay(100);
}


void loop() {
  // Get new sensor event with the readings
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Set myData movement struct values to false by default
  myData.forwards = false;
  myData.backwards = false;
  myData.clockwise = false;
  myData.counterclockwise = false;

  // Print the acceleration values
  Serial.print("x: ");
  Serial.println(a.acceleration.x);
  Serial.print("y: ");
  Serial.println(a.acceleration.y);
  Serial.print("z: ");
  Serial.println(a.acceleration.z);

  // Vibrate gently if GBBO is moving and print the direction
  if (a.acceleration.z > FORWARDS_LIM) {
    // Turn on the vibration motor
    ledcWrite(CHANNEL, VIBRATION_STRENGTH);
    
    // Move Rollie forwards
    myData.forwards = true;
    Serial.println("Moving forwards");
  } else if (a.acceleration.z < -BACKWARDS_LIM) {
    // Turn on the vibration motor
    ledcWrite(CHANNEL, VIBRATION_STRENGTH);
    
    // Move Rollie backwards
    myData.backwards = true;
    Serial.println("Moving backwards");
  } else if (a.acceleration.x > CLOCKWISE_LIM) {
    // Turn on the vibration motor
    ledcWrite(CHANNEL, VIBRATION_STRENGTH);
    
    // Turn Rollie clockwise
    myData.clockwise = true;
    Serial.println("Moving right");
  } else if (a.acceleration.x < -COUNTERCLOCKWISE_LIM) {
    // Turn on the vibration motor
    ledcWrite(CHANNEL, VIBRATION_STRENGTH);
    
    // Turn Rollie counterclockwise
    myData.counterclockwise = true;
    Serial.println("Moving left");
  } else {
    // Turn off the vibration motor
    ledcWrite(CHANNEL, 0);
    
    // Stop Rollie
    Serial.println("Stopped");
  }

  
  // Send message via ESP-NOW and check for errors
  esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &myData, sizeof(myData));
  if (result == ESP_OK) {
    Serial.println("Send with success");
  } else {
    Serial.println("Error sending the data");
  }
  
  // Put a linebreak and short delay after values sent
  Serial.println("");
  delay(50);
}

R
// References and Copyrights
/*
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/esp-now-esp32-arduino-ide/
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files.
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
*/
