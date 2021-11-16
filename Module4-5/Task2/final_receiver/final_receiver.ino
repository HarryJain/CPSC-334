// Library imports for ESP-NOW communication
#include <esp_now.h>
#include <WiFi.h>


// Library import for stepper
#include <Stepper.h>

// Number of steps per 360 degree revolution
#define STEPSPERREVOLUTION 2048

// ULN2003 Motor Driver Pins
#define DRIVER_IN1 19
#define DRIVER_IN2 18
#define DRIVER_IN3 5
#define DRIVER_IN4 17

// Speed constant for rpm
#define SPEED 10

// Stepper object for 28BYJ-48 stepper motor
Stepper stepper(STEPSPERREVOLUTION, DRIVER_IN1, DRIVER_IN3, DRIVER_IN2, DRIVER_IN4);


// The pin connections for the LEDs
#define RED 26
#define YELLOW 25
#define GREEN 33
#define BLUE 32

// The PWM channel (0 to 15)
#define CHANNEL 0

// The PWM signal frequency for LED
#define FREQ 5000

// The signal's duty cycle resolution (1 to 16-bit)
//  8-bit for 0 to 255 LED brightness values
#define RESOLUTION 8
#define MIN 0
#define MAX 255


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
  // Copy the incoming data to the myData variable
  memcpy(&myData, incomingData, sizeof(myData));
  
  // Print the values received
  Serial.print("Bytes received: ");
  Serial.println(len);
  Serial.print("Acceleration X: ");
  Serial.print(myData.accel_x);
  Serial.print(", Y: ");
  Serial.print(myData.accel_y);
  Serial.print(", Z: ");
  Serial.print(myData.accel_z);
  Serial.println(" m/s^2");

  // Move the stepper motor in accordance with the
  //  x-acceleration values
  if (myData.accel_x < -4) {
    // Move the stepper one step clockwise
    Serial.println("Stepping");
    stepper.step(-20);
  } else if (myData.accel_x > 4) {
    // Move the stepper one step counterclockwise
    stepper.step(20);
  }
  int brightness = int(max(min((myData.accel_z) / 12, float(1.0)), float(0.0)) * MAX);
  ledcWrite(CHANNEL, brightness);

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

  // Configure LED PWM functionalities
  ledcSetup(CHANNEL, FREQ, RESOLUTION);

  // Attach the channel to the GPIO pins to be controlled
  ledcAttachPin(RED, CHANNEL);
  ledcAttachPin(YELLOW, CHANNEL);
  ledcAttachPin(GREEN, CHANNEL);
  ledcAttachPin(BLUE, CHANNEL);

  // Set the stepper speed at SPEED rpm
  stepper.setSpeed(SPEED);
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
