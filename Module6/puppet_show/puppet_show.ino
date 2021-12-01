// Include esp_now and WiFi libraries for mesh networking
#include <esp_now.h>
#include <WiFi.h>

// Global copy of remote
esp_now_peer_info_t remote;
#define CHANNEL 1
#define PRINTSCANRESULTS 0
#define DELETEBEFOREPAIR 0

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

uint8_t rssi = 0;
// Scan for remotes in AP mode
void ScanForRemote() {
  int8_t scanResults = WiFi.scanNetworks();
  
  // Reset on each scan
  bool remoteFound = 0;
  memset(&remote, 0, sizeof(remote));

  Serial.println("");
  if (scanResults == 0) {
    Serial.println("No WiFi devices in AP Mode found");
  } else {
    Serial.print("Found "); Serial.print(scanResults); Serial.println(" devices ");
    for (int i = 0; i < scanResults; ++i) {
      // Print SSID and RSSI for each device found
      String SSID = WiFi.SSID(i);
      int32_t RSSI = WiFi.RSSI(i);
      String BSSIDstr = WiFi.BSSIDstr(i);

      if (PRINTSCANRESULTS) {
        Serial.print(i + 1);
        Serial.print(": ");
        Serial.print(SSID);
        Serial.print(" (");
        Serial.print(RSSI);
        Serial.print(")");
        Serial.println("");
      }
      delay(10);
      
      // Check if the current device starts with `Ghost`
      if (SSID.indexOf("Ghost") == 0) {
        // SSID of interest
        Serial.println("Found a Remote.");
        Serial.print(i + 1); Serial.print(": "); Serial.print(SSID); Serial.print(" ["); Serial.print(BSSIDstr); Serial.print("]"); Serial.print(" ("); Serial.print(rssi); Serial.print(")"); Serial.println("");
        // Get BSSID => Mac Address of the Remote
        int mac[6];
        if ( 6 == sscanf(BSSIDstr.c_str(), "%x:%x:%x:%x:%x:%x",  &mac[0], &mac[1], &mac[2], &mac[3], &mac[4], &mac[5] ) ) {
          for (int ii = 0; ii < 6; ++ii ) {
            remote.peer_addr[ii] = (uint8_t) mac[ii];
          }
        }

        rssi = abs(WiFi.RSSI(i));

        // Pick a channel for connecting to the remote
        remote.channel = CHANNEL;

        // Do not encrypt the ESP Now connection
        remote.encrypt = 0;

        remoteFound = 1;
      }
    }
  }

  if (remoteFound) {
    Serial.println("Remote Found, processing..");
  } else {
    Serial.println("Remote Not Found, trying again.");
  }

  // Clean up WiFi scan RAM
  WiFi.scanDelete();
}

// Check if the remote is already paired with the puppet show
//  If not, pair them
bool manageRemote() {
  if (remote.channel == CHANNEL) {
    if (DELETEBEFOREPAIR) {
      deletePeer();
    }

    Serial.print("Remote Status: ");
    // Check if the peer exists
    bool exists = esp_now_is_peer_exist(remote.peer_addr);
    if (exists) {
      // Remote already paired.
      Serial.println("Already Paired");
      return true;
    } else {
      // Remote not paired, attempt pair
      esp_err_t addStatus = esp_now_add_peer(&remote);
      if (addStatus == ESP_OK) {
        // Pair success
        Serial.println("Pair success");
        return true;
      } else if (addStatus == ESP_ERR_ESPNOW_NOT_INIT) {
        // How did we get so far!!
        Serial.println("ESPNOW Not Init");
        return false;
      } else if (addStatus == ESP_ERR_ESPNOW_ARG) {
        Serial.println("Invalid Argument");
        return false;
      } else if (addStatus == ESP_ERR_ESPNOW_FULL) {
        Serial.println("Peer list full");
        return false;
      } else if (addStatus == ESP_ERR_ESPNOW_NO_MEM) {
        Serial.println("Out of memory");
        return false;
      } else if (addStatus == ESP_ERR_ESPNOW_EXIST) {
        Serial.println("Peer Exists");
        return true;
      } else {
        Serial.println("Not sure what happened");
        return false;
      }
    }
  } else {
    // No remote found to process
    Serial.println("No Remote found to process");
    return false;
  }
}

void deletePeer() {
  esp_err_t delStatus = esp_now_del_peer(remote.peer_addr);
  Serial.print("Remote Delete Status: ");
  if (delStatus == ESP_OK) {
    // Delete success
    Serial.println("Success");
  } else if (delStatus == ESP_ERR_ESPNOW_NOT_INIT) {
    // How did we get so far!!
    Serial.println("ESPNOW Not Init");
  } else if (delStatus == ESP_ERR_ESPNOW_ARG) {
    Serial.println("Invalid Argument");
  } else if (delStatus == ESP_ERR_ESPNOW_NOT_FOUND) {
    Serial.println("Peer not found.");
  } else {
    Serial.println("Not sure what happened");
  }
}

// Send RSSI data to remote
void sendData() {
  const uint8_t *peer_addr = remote.peer_addr;
  Serial.print("Sending: "); Serial.println(rssi);
  esp_err_t result = esp_now_send(peer_addr, &rssi, sizeof(rssi));
  Serial.print("Send Status: ");
  if (result == ESP_OK) {
    Serial.println("Success");
  } else if (result == ESP_ERR_ESPNOW_NOT_INIT) {
    // How did we get so far!!
    Serial.println("ESPNOW not Init.");
  } else if (result == ESP_ERR_ESPNOW_ARG) {
    Serial.println("Invalid Argument");
  } else if (result == ESP_ERR_ESPNOW_INTERNAL) {
    Serial.println("Internal Error");
  } else if (result == ESP_ERR_ESPNOW_NO_MEM) {
    Serial.println("ESP_ERR_ESPNOW_NO_MEM");
  } else if (result == ESP_ERR_ESPNOW_NOT_FOUND) {
    Serial.println("Peer not found.");
  } else {
    Serial.println("Not sure what happened");
  }
}

// Callback when data is sent from puppet show to remote
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  char macStr[18];
  snprintf(macStr, sizeof(macStr), "%02x:%02x:%02x:%02x:%02x:%02x",
           mac_addr[0], mac_addr[1], mac_addr[2], mac_addr[3], mac_addr[4], mac_addr[5]);
  Serial.print("Last Packet Sent to: "); Serial.println(macStr);
  Serial.print("Last Packet Send Status: "); Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
  Serial.println(WiFi.RSSI());
}

void setup() {
  Serial.begin(115200);
  //Set device in STA mode to begin with
  WiFi.mode(WIFI_STA);
  
  // This is the mac address of the pupper show in Station Mode
  Serial.print("STA MAC: "); Serial.println(WiFi.macAddress());
  
  // Initialize ESPNow with a fallback logic
  InitESPNow();
  
  // Once ESPNow is successfully initialized, we will register for Send CB to
  //  get the status of Trasnmitted packet
  esp_now_register_send_cb(OnDataSent);
}

void loop() {
  // In the loop we scan for remote
  ScanForRemote();
  // If remote is found, it would be populate in `remote` variable
  // We will check if `remote` is defined and then we proceed further
  if (remote.channel == CHANNEL) { // check if remote channel is defined
    // `remote` is defined
    // Add remote as peer if it has not been added already
    bool isPaired = manageRemote();
    if (isPaired) {
      // Pair success or already paired
      // Send data to device
      sendData();
    } else {
      // Remote pair failed
      Serial.println("Remote pair failed!");
    }
  }
  else {
    // No remote found to process
  }

  // wait for 1ms to run the logic again
  delay(1);
}

// References and Copyrights
/** Inspired by (apologies for the insensitive terminology):
   ESPNOW - Basic communication - Master
   Date: 26th September 2017
   Author: Arvind Ravulavaru <https://github.com/arvindr21>
   Purpose: ESPNow Communication between a Master ESP32 and a Slave ESP32
   Description: This sketch consists of the code for the Master module.
   Resources: (A bit outdated)
   a. https://espressif.com/sites/default/files/documentation/esp-now_user_guide_en.pdf
   b. http://www.esploradores.com/practica-6-conexion-esp-now/
   << This Device Master >>
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
