/*
  Example from WiFi > WiFiScan
  Complete details at https://RandomNerdTutorials.com/esp32-useful-wi-fi-functions-arduino/
*/

#include "WiFi.h"

const char* ssid = "TP-Link_1196";
const char* password = "50874811";

const String ssd[2] = {"Link_1196","Vodafone-E77640838"};
const String pswd[2] = {"50874811","4JAbcK3GGxKN3sr6"};


const int CONNECT_RETRIES = 20;

void setup() {
  Serial.begin(115200);

  // Set WiFi to station mode and disconnect from an AP if it was previously connected
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);

  Serial.println("Setup done");
  scanWifi();
}

void loop() {
   Serial.print("Wifi Status:");
   printStatus();
   Serial.println();

   // Connect to WiFi if are not connected
   if (WiFi.status() != WL_CONNECTED) {
     connectWifi();
   }
   delay(5000);

}

int scanWifi() {
  Serial.println("scan start");

  // WiFi.scanNetworks will return the number of networks found
  int n = WiFi.scanNetworks();
  Serial.println("scan done");
  if (n == 0) {
      Serial.println("no networks found");
  } else {
    Serial.print(n);
    Serial.println(" networks found");
    for (int i = 0; i < n; ++i) {
      // Print SSID and RSSI for each network found
      Serial.print(i + 1);
      Serial.print(": ");
      Serial.print(WiFi.SSID(i));
      Serial.print(" (");
      Serial.print(WiFi.RSSI(i));
      Serial.print(")");
      Serial.println((WiFi.encryptionType(i) == WIFI_AUTH_OPEN)?" ":"*");
      delay(10);
    }
  }
  Serial.print("WIFIs found:");
  Serial.println(n);

  return n;
  // Wait a bit before scanning again
}

void connectWifi() {
    int retries = CONNECT_RETRIES;
    Serial.println("Trying to connect to wifi");
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi ");Serial.println(ssid);
    while ((WiFi.status() != WL_CONNECTED) && retries > 0) {
      Serial.print('.');
      delay(1000);
      retries = retries - 1;
    }

    if (WiFi.status() == WL_CONNECTED) {
      Serial.print("Connected, IP=");
      Serial.println(WiFi.localIP());
    }
    else {
      Serial.print("Error connecting to WiFi:");
      Serial.println(WiFi.status());
    }
    
}

void printStatus() {
  if (WiFi.status() == WL_CONNECTED) {
    Serial.print("Connected");
  }
  else {
    Serial.print("Not connected:");Serial.print(WiFi.status());
  }
}