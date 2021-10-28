#include <WiFi.h>
#include <HTTPClient.h>
#define DEVICE_COUNT 1

// Wifi connection constants
const char* ssid = "yale wireless";
const char* password = "";

// Define http server and port
WiFiServer server(80);

// Header to store the HTTP request
String header;

// MAC address to name map
String devices[DEVICE_COUNT] = {"E8:68:E7:30:2B:DC"};
String names[DEVICE_COUNT] = {"Red"};
String name;
const char* domains[DEVICE_COUNT] = {"https://red.cody.ws/"};

int nearbyFlags[DEVICE_COUNT] = {0};

// Current time (ms)
unsigned long currentTime = millis();
// Previous time (ms)
unsigned long previousTime = 0;
// Timeout (ms)
const long timeoutTime = 2000;

void setup()
{
  // Open serial stream
  Serial.begin(115200);

  // Newline after startup debug lines
  Serial.println("");

  // Resolve mac address to name map
  for (size_t i = 0; i < DEVICE_COUNT; i++) {
    Serial.println(WiFi.macAddress());
    if (devices[i] == WiFi.macAddress()) {
      name = names[i];
    }
  }

  // Allow time for serial client to connect
  delay(100);
}

void loop()
{
  // Refresh wifi connection
  Serial.print("Refreshing connection to: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  // Wait until fully connected
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  // Print ip to serial for debug
  Serial.println(WiFi.localIP());
  // Start server on defined ip and port
  server.begin();

  for (size_t i = 0; i < DEVICE_COUNT; i++){
    HTTPClient scanner;
    if (name != names[i]) {
      Serial.println("CONNECTED:");
      scanner.begin(domains[i]);

      // Send HTTP GET request
      int httpResponseCode = scanner.GET();

      if (httpResponseCode > 0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        String payload = scanner.getString();
        Serial.println(payload);
        Serial.println("---");
        Serial.println(WiFi.BSSIDstr());
        Serial.println(payload.indexOf(WiFi.BSSIDstr()));
        if (payload.indexOf(WiFi.BSSIDstr()) > 0) {
          nearbyFlags[i] = 1;
        } else {
          nearbyFlags[i] = 0;
        }
      } else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
      }
      scanner.end();

    } else {
      Serial.print("did not connect: ");
      Serial.print(name);
      Serial.print(" == ");
      Serial.println(names[i]);
    }
  }

  // Count refreshed user sessions
  int lcount = 0;
  while (lcount < 10000 && WiFi.status() == WL_CONNECTED) {
    // Listen for incoming clients
    WiFiClient client = server.available();
    lcount += 1;
    delay(1);
    // Loop unless client connected
    if (client && WiFi.status() == WL_CONNECTED) {

      // Define new connection
      currentTime = millis();
      previousTime = currentTime;
      Serial.println("New Client.");

      // String to hold incoming data from client
      String currentLine = "";

      // Loop while client connected
      while (client.connected() && currentTime - previousTime <= timeoutTime) {
        currentTime = millis();

        // If there're bytes to read from the client
        if (client.available()) {
          // Read a byte and print to serial
          char c = client.read();
          Serial.write(c);
          header += c;

          // If newline
          if (c == '\n') {

            // If the current line is blank, two newline characters in a row
            // The end of the client HTTP request, so send response
            if (currentLine.length() == 0) {

              // HTTP header starts with a response code, content-type, then a blank line
              client.println("HTTP/1.1 200 OK");
              client.println("Content-type:text/html");
              client.println("Connection: close");
              client.println();

              // Begin html to http serve
              client.println("<!DOCTYPE html><html>");
              client.println("<head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">");
              client.println("<link rel=\"icon\" href=\"data:,\">");

              // Print CSS styles to http serve
              client.println("<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;} input[type='checkbox'] { display: none; } .wrap-collapsible { margin: 1.2rem 0; } .lbl-toggle { display: block; font-weight: bold; font-family: monospace; font-size: 1.2rem; text-transform: uppercase; text-align: center; padding: 1rem; color: #DDD; background: #0069ff; cursor: pointer; border-radius: 7px; transition: all 0.25s ease-out; } .lbl-toggle:hover { color: #FFF; } .lbl-toggle::before { content: ' '; display: inline-block; border-top: 5px solid transparent; border-bottom: 5px solid transparent; border-left: 5px solid currentColor; vertical-align: middle; margin-right: .7rem; transform: translateY(-2px); transition: transform .2s ease-out; } .toggle:checked+.lbl-toggle::before { transform: rotate(90deg) translateX(-3px); } .collapsible-content { max-height: 0px; overflow: hidden; transition: max-height .25s ease-in-out; } .toggle:checked + .lbl-toggle + .collapsible-content { max-height: 350px; } .toggle:checked+.lbl-toggle { border-bottom-right-radius: 0; border-bottom-left-radius: 0; } .collapsible-content .content-inner { background: rgba(0, 105, 255, .2); border-bottom: 1px solid rgba(0, 105, 255, .45); border-bottom-left-radius: 7px; border-bottom-right-radius: 7px; padding: .5rem 1rem; } .collapsible-content p { margin-bottom: 0; }</style></head>");

              // Open body on http serve
              client.println("<body>");

              // Open about pet collapsible
              client.println("<div class=\"wrap-collapsible\"><input id=\"collapsible1\" class=\"toggle\" type=\"checkbox\" checked><label for=\"collapsible1\" class=\"lbl-toggle\">About My Pet</label><div class=\"collapsible-content\"><div class=\"content-inner\"><p>");

              // Print name to http serve
              client.println("Name: ");
              client.println(name);
              client.println("<br />");

              // Print age to http serve
              client.println("Age: ");
              if (currentTime > 60000) {
                client.println(currentTime / 60000);
                client.println(" minutes, ");
              }
              client.println((currentTime % 60000) / 1000);
              client.println(" seconds");

              // Close about pet collapsible
              client.println("</p></div></div></div>");

              // Open more info collapsible
              client.println("<div class=\"wrap-collapsible\"><input id=\"collapsible2\" class=\"toggle\" type=\"checkbox\"><label for=\"collapsible2\" class=\"lbl-toggle\">More Info</label><div class=\"collapsible-content\"><div class=\"content-inner\"><p>");

              // Print SSID to http serve
              client.println("SSID: ");
              client.println(ssid);
              client.println("<br />");

              // Print BSSID to http serve
              client.println("BSSID: ");
              client.println(WiFi.BSSIDstr());
              client.println("<br />");

              // Print IP to http serve
              client.println("IP: ");
              client.println(WiFi.localIP());
              client.println("<br />");

              // Print MAC to http serve
              client.println("MAC: ");
              client.println(WiFi.macAddress());
              client.println("<br />");

              for (int i = 0; i < DEVICE_COUNT; i++) {
                client.println(nearbyFlags[i]);
              }

              // Close more info collapsible
              client.println("</p></div></div></div>");

              // Close html on http serve
              client.println("</body></html>");

              // HTTP response ends with blank line
              client.println();
              // Break out of the while loop
              break;
            } else {
              // If there is a newline, clear currentLine
              currentLine = "";
            }
          } else if (c != '\r') {
            // If but a carriage return character, add it to the end of the currentLine
            currentLine += c;
          }
        }
      }
      // Clear the header variable
      header = "";
      // Close the connection
      client.stop();

      // Print disconnect to serial debug
      Serial.println("Client disconnected.");
      Serial.println("");
    }
  }
}
