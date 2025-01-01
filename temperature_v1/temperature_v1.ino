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
#include <Wire.h>
#include "OLED_Helper.h"

#define LED_RED 2
#define LED_YELLOW 4
#define LED_GREEN 5
#define TOUCH_PIN 32
#define API_REFRESH 5 * 60 * 1000L  //call API ms
#define LCD_BACKLIGHT_DURATION 10 * 1000L
#define TOUCH_THRESHOLD 25

// OLED Constants
#define SCREEN_WIDTH 128     // OLED display width, in pixels
#define SCREEN_HEIGHT 64     // OLED display height, in pixels
#define OLED_RESET -1        // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C  ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

OledHelper oledHelper(display, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_ADDRESS);


/* OLED pins **
SCL => GPIO 22
SDA => GPIO 21
GND => GND
VCC => 3V3
****************************/

const uint32_t connectTimeoutMs = 20000;

//Generic buffer for string formatting
char buffer[80];

//URL Endpoint for the API
String URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/";
String URL_Parameters = "?unitGroup=metric&include=current&key=U9ELWL9D9E9CJR9ND72FY6LKP&contentType=json";
String ApiKey = "U9ELWL9D9E9CJR9ND72FY6LKP";

unsigned long lastTimeCalledAPI = 0;
unsigned long lastTimeBackLightOn = 0;
bool touchActivated = false;
unsigned long now;
int touchValue;

WiFiMulti wifiMulti;


void setup() {
  Serial.begin(115200);

  lastTimeBackLightOn = millis();  //set it on in the beginning

  //Initialize OLED
  oledHelper.begin();

  //Initialize LED pins
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_YELLOW, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);

  // Set WiFi to station mode and disconnect from an AP if it was previously connected
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  turnLED(LED_RED, HIGH);
  delay(100);
}

void loop() {

  now = millis();
  //printStatus();
  //scanWifi();

  //Check if we need to turn off backlight
  touchValue = touchRead(TOUCH_PIN);
  if (touchValue < TOUCH_THRESHOLD) {
    if (!touchActivated) {
      Serial.println("Touch activated");
      //Do something when touch is on lcd.backlight();
      touchActivated = true;
      lastTimeBackLightOn = now;
    }
  }

  // Connect to WiFi if are not connected
  if (WiFi.status() != WL_CONNECTED) {
    oledHelper.displayStatus("Connecting....");
    turnLED(LED_YELLOW, HIGH);
    connectWifiMulti();
  } else {
    // we are connected
    turnLED(LED_GREEN, HIGH);
    if ((now - lastTimeCalledAPI >= API_REFRESH) || (lastTimeCalledAPI == 0)) {
      turnLED(LED_YELLOW, HIGH);
      callAPI("galatsi%20attiki%20greece");
      turnLED(LED_GREEN, HIGH);
      lastTimeCalledAPI = now;
    }
    //callAPI("xanthi%20greece");
    //callAPI("vilnius%20lithuania");
    //delay(API_REFRESH);
  }
}

void connectWifiMulti() {

  Serial.println("connectWifiMulti()");
  WiFi.mode(WIFI_STA);
  WiFi.disconnect(true, true);
  delay(200);
  wifiMulti.addAP("G30iphone12", "manager2");
  wifiMulti.addAP("TP-Link_1196", "50874811");
  wifiMulti.addAP("Vodafone-E77640838", "4JAbcK3GGxKN3sr6");
  //scanWifi();

  if (wifiMulti.run(connectTimeoutMs) == WL_CONNECTED) {
    sprintf(buffer, "Connected:%s", WiFi.SSID().c_str());
    oledHelper.displayStatus(buffer);
    Serial.print("IP Address:");
    Serial.println(WiFi.localIP());
  } else {
    oledHelper.displayStatus("Error connecting to WiFi:");
    Serial.print("Error connecting to WiFi:");
    Serial.println(WiFi.status());
    turnLED(LED_RED, HIGH);
  }
}

void printStatus() {
  Serial.print("Wifi status:");
  if (WiFi.status() == WL_CONNECTED) {
    sprintf(buffer, "Connected:%s", WiFi.SSID().c_str());
    oledHelper.displayStatus(buffer);
    Serial.print(buffer);
  } else {
    Serial.print("Not connected:");
    Serial.print(WiFi.status());
    sprintf(buffer, "Not connected :%s", WiFi.status());
    oledHelper.displayStatus(buffer);
  }
  Serial.println();
}

/*
  Turn off all the LEDs and then turn off/on the LED that is passed as parameter
*/
void turnLED(int led, int high_low) {
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_YELLOW, LOW);
  digitalWrite(LED_RED, LOW);
  digitalWrite(led, high_low);
}

void callAPI(String place) {
  HTTPClient http;

  String finalURL = URL + place + URL_Parameters;
  Serial.print("Final URL:");
  Serial.print(finalURL);

  sprintf(buffer, "%16.16s", "Refresh Data...");
  oledHelper.displayStatus(buffer);

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
    const char* conditions = obj["currentConditions"]["conditions"].as<const char*>();
    const float currentTemp = obj["currentConditions"]["temp"].as<float>();
    const float currentfeelslike = obj["currentConditions"]["feelslike"].as<float>();
    const float windspeed = obj["currentConditions"]["windspeed"].as<float>();
    const float snow = obj["currentConditions"]["snow"].as<float>();

    sprintf(buffer, "Galatsi (%5.5s)", currentTime);
    oledHelper.display(0, oledHelper.LINE1, buffer);
    sprintf(buffer, "Temp:%3.1f Feels:%3.1f", currentTemp, currentfeelslike);
    oledHelper.display(0, oledHelper.LINE2, buffer);
    sprintf(buffer, "%s", conditions);
    oledHelper.display(0, oledHelper.LINE3, buffer);
    sprintf(buffer, "Wind:%2.1f, Snow:%1.1f", windspeed, snow);
    oledHelper.display(0, oledHelper.LINE4, buffer);

    sprintf(buffer, "%s %s -> %f (%f) %s", "Galatsi", currentTime, currentTemp, currentfeelslike, conditions);
    Serial.print(buffer);
    printStatus();

  } else {
    Serial.println("Error!");
    sprintf(buffer, "%s (%d)", "HTTP Error", httpCode);
    oledHelper.displayStatus(buffer);
  }

  http.end();

}  //callApi

void print(char* format, ...) {
  char buffer[200];
  int result;
  va_list argptr;
  va_start(argptr, format);
  result = vsprintf(buffer, format, argptr);
  va_end(argptr);
  Serial.println(buffer);
}

String millisToUserFriendly(unsigned long ms) {
  // Calculate time components
  unsigned long seconds = ms / 1000;
  unsigned long days = seconds / 86400;            // 86400 seconds in a day
  unsigned long hours = (seconds % 86400) / 3600;  // 3600 seconds in an hour
  unsigned long minutes = (seconds % 3600) / 60;   // 60 seconds in a minute
  unsigned long remainingSeconds = seconds % 60;   // Remaining seconds

  // Construct the formatted string
  String result = "";
  if (days > 0) {
    result += String(days) + "d ";
  }
  if (hours > 0 || days > 0) {
    result += String(hours) + "h ";
  }
  if (minutes > 0 || hours > 0 || days > 0) {
    result += String(minutes) + "min ";
  }
  result += String(remainingSeconds) + "s";

  return result;
}