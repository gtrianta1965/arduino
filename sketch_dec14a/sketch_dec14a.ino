/*
  Example from WiFi > WiFiScan
  Complete details at https://RandomNerdTutorials.com/esp32-useful-wi-fi-functions-arduino/
*/

//#include "WiFi.h"
#include <WiFiMulti.h>

const uint32_t connectTimeoutMs = 20000;

WiFiMulti wifiMulti;

void setup() {
  Serial.begin(115200);

  // Set WiFi to station mode and disconnect from an AP if it was previously connected
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);

}

void loop() {
   printStatus();
   //scanWifi();

   // Connect to WiFi if are not connected
   if (WiFi.status() != WL_CONNECTED) {
     connectWifiMulti();
   }
   delay(5000);

}


void connectWifiMulti() {

    Serial.println("connectWifiMulti()");
    WiFi.mode(WIFI_STA);
    WiFi.disconnect(true,true);delay(200);
    wifiMulti.addAP("G30iphone12", "manager2");
    wifiMulti.addAP("TP-Link_1196", "50874811");
    wifiMulti.addAP("Vodafone-E77640838", "4JAbcK3GGxKN3sr6");
    //scanWifi();

  if(wifiMulti.run(connectTimeoutMs) == WL_CONNECTED) {
    Serial.println("");
    Serial.print("WiFi connected to ");
    Serial.println(WiFi.SSID());
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  }
    else {
      Serial.print("Error connecting to WiFi:");
      Serial.println(WiFi.status());
    }
    
}

void printStatus() {
  Serial.print("Wifi status:");
  if (WiFi.status() == WL_CONNECTED) {
    Serial.print("Connected");
  }
  else {
    Serial.print("Not connected:");Serial.print(WiFi.status());
  }
  Serial.println();
}