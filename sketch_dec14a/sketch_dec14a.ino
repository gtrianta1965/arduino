/*
  Example from WiFi > WiFiScan
  Complete details at https://RandomNerdTutorials.com/esp32-useful-wi-fi-functions-arduino/

  API site used:https://weather.visualcrossing.com 

  Example :
    https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/galatsi%20attiki%20greece?unitGroup=metric&include=current&key=U9ELWL9D9E9CJR9ND72FY6LKP&contentType=json

*/

//#include "WiFi.h"
#include <WiFiMulti.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

#define LED_RED  2
#define LED_YELLOW  4
#define LED_GREEN  5

const uint32_t connectTimeoutMs = 20000;

//URL Endpoint for the API
String URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/";
String URL_Parameters = "?unitGroup=metric&include=current&key=U9ELWL9D9E9CJR9ND72FY6LKP&contentType=json";
String ApiKey = "U9ELWL9D9E9CJR9ND72FY6LKP";


WiFiMulti wifiMulti;

void setup() {
  Serial.begin(115200);

  pinMode(LED_RED,OUTPUT);
  pinMode(LED_YELLOW,OUTPUT);
  pinMode(LED_GREEN,OUTPUT);

  // Set WiFi to station mode and disconnect from an AP if it was previously connected
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  turnLED(LED_RED,HIGH);
  delay(100);

}

void loop() {
   printStatus();
   //scanWifi();

   // Connect to WiFi if are not connected
   if (WiFi.status() != WL_CONNECTED) {
     turnLED(LED_YELLOW,HIGH);
     connectWifiMulti();
   } else {
     turnLED(LED_YELLOW,HIGH);
     callAPI("galatsi%20attiki%20greece");
     callAPI("xanthi%20greece");
     callAPI("vilnius%20lithuania");
     turnLED(LED_GREEN,HIGH);
   }
   delay(15000);

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
      turnLED(LED_RED,HIGH);
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

/*
  Turn off all the LEDs and then turn off/on the LED that is passed as parameter
*/ 
void turnLED(int led, int high_low) {
   digitalWrite(LED_GREEN,LOW);
   digitalWrite(LED_YELLOW,LOW);
   digitalWrite(LED_RED,LOW);
   digitalWrite(led,high_low);
}

void callAPI(String place) {
  HTTPClient http;

  String finalURL = URL + place + URL_Parameters;
  Serial.print("Final URL:");
  Serial.print(finalURL);

  //Set HTTP Request Final URL with Location and API key information
  http.begin(finalURL);

  // star connection and send HTTP Request
  int httpCode = http.GET();

  // httpCode will be negative on error
  if (httpCode > 0) {

    //Read Data as a JSON string
    String JSON_Data = http.getString();
    Serial.println(JSON_Data);


    //Retrieve some information about the weather from the JSON format
    DynamicJsonDocument doc(4096);
    deserializeJson(doc, JSON_Data);
    JsonObject obj = doc.as<JsonObject>();

    //Display the Current Weather Info
    const char* resolvedAddress = obj["resolvedAddress"].as<const char*>();
    const char* currentTime = obj["currentConditions"]["datetime"].as<const char*>();
    const float currentTemp = obj["currentConditions"]["temp"].as<float>();
    const float currentfeelslike = obj["currentConditions"]["feelslike"].as<float>(); 
    Serial.print("resolvedAddress=");Serial.println(resolvedAddress);
    Serial.print("currentTime=");Serial.println(currentTime);
    Serial.print("currentTemp=");Serial.println(currentTemp);
    Serial.print("currentfeelslike=");Serial.println(currentfeelslike);
    
  
  /*
    const char* description = obj["weather"][0]["description"].as<const char*>();
    const float temp = obj["main"]["temp"].as<float>();
    const float humidity = obj["main"]["humidity"].as<float>();

/*
    lcd.clear();
    lcd.print(description);
    lcd.setCursor(0, 1);
    lcd.print(temp);
    lcd.print(" C, ");
    lcd.print(humidity);
    lcd.print(" %");
*/
  } else {
    Serial.println("Error!");
    //lcd.clear();
    //lcd.print("Can't Get DATA!");
  }

  http.end();


}