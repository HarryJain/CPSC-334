// Include esp_now and WiFi libraries for mesh networking
#include <esp_now.h>
#include <WiFi.h>

// Set the channel for ESP Now
#define CHANNEL 1

// Control pin for the buzzer motor
#define BUZZER_PIN 13

// Control pin for the indicator LED
#define LED_PIN 9

// Set PWM properties
#define FREQ 5000
#define BUZZER_CHANNEL 0
#define RESOLUTION 8

// Initialize ESP Now with fallback
void InitESPNow() {
  WiFi.disconnect();
  if (esp_now_init() == ESP_OK) {
    Serial.println("ESPNow Init Success");
  }
  else {
    Serial.println("ESPNow Init Failed");
    ESP.restart();
  }
}

// Configure AP SSID
void configDeviceAP() {
  const char *SSID = "Ghost_1";
  bool result = WiFi.softAP(SSID, "Ghost_1_Password", CHANNEL, 0);
  if (!result) {
    Serial.println("AP Config failed.");
  } else {
    Serial.println("AP Config Success. Broadcasting with AP: " + String(SSID));
  }
}

void setup() {
  // Set upload speed
  Serial.begin(115200);
  
  //Set device in AP mode to begin with
  WiFi.mode(WIFI_AP);
  // configure device AP mode
  configDeviceAP();
  // This is the mac address of the Slave in AP Mode
  Serial.print("AP MAC: "); Serial.println(WiFi.softAPmacAddress());
  
  // Initialize ESPNow with a fallback logic
  InitESPNow();
  
  // Once ESPNow is successfully initialized, we will register for recv CB to
  // get recv packer info.
  esp_now_register_recv_cb(OnDataRecv);

  // Configure buzzer motor PWM functionalities
  ledcSetup(BUZZER_CHANNEL, FREQ, RESOLUTION);

  // Attach the channel to the GPIO to be controlled
  ledcAttachPin(BUZZER_PIN, BUZZER_CHANNEL);

  // Set the LED control pin to be a digital output
  pinMode(LED_PIN, OUTPUT);
}

// Callback when data is received from Master
void OnDataRecv(const uint8_t *mac_addr, const uint8_t *data, int data_len) {
  char macStr[18];
  snprintf(macStr, sizeof(macStr), "%02x:%02x:%02x:%02x:%02x:%02x",
           mac_addr[0], mac_addr[1], mac_addr[2], mac_addr[3], mac_addr[4], mac_addr[5]);
  Serial.print("Last Packet Recv from: "); Serial.println(macStr);
  Serial.print("Last Packet Recv Data: "); Serial.println(*data);
  Serial.println(WiFi.RSSI());
  Serial.println("");
  
  // If the remote is close to one of the ghosts, activate the buzzer motor
  if (*data < 50 && *data > 0) {
    int buzz_val = sqrt(abs(*data - 50) * 1000);
    ledcWrite(BUZZER_CHANNEL, buzz_val);
    digitalWrite(LED_PIN, HIGH);
  } else {
    ledcWrite(BUZZER_CHANNEL, 0);
    digitalWrite(LED_PIN, LOW);
  }
}

void loop() {
  // Chill
}

// References and Copyrights
/** Inspired by (apologies for the insensitive terminology):
   ESPNOW - Basic communication - Slave
   Date: 26th September 2017
   Author: Arvind Ravulavaru <https://github.com/arvindr21>
   Purpose: ESPNow Communication between a Master ESP32 and a Slave ESP32
   Description: This sketch consists of the code for the Slave module.
   Resources: (A bit outdated)
   a. https://espressif.com/sites/default/files/documentation/esp-now_user_guide_en.pdf
   b. http://www.esploradores.com/practica-6-conexion-esp-now/
   << This Device Slave >>
   Flow: Master
   Step 1 : ESPNow Init on Master and set it in STA mode
   Step 2 : Start scanning for Slave ESP32 (we have added a prefix of `slave` to the SSID of slave for an easy setup)
   Step 3 : Once found, add Slave as peer
   Step 4 : Register for send callback
   Step 5 : Start Transmitting data from Master to Slave
   Flow: Slave
   Step 1 : ESPNow Init on Slave
   Step 2 : Update the SSID of Slave with a prefix of `slave`
   Step 3 : Set Slave in AP mode
   Step 4 : Register for receive callback and wait for data
   Step 5 : Once data arrives, print it in the serial monitor
   Note: Master and Slave have been defined to easily understand the setup.
         Based on the ESPNOW API, there is no concept of Master and Slave.
         Any devices can act as master or salve.
*/
