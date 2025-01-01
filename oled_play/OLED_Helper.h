#ifndef OLED_HELPER_H
#define OLED_HELPER_H
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Arduino.h>

class OledHelper {
public:
  OledHelper(Adafruit_SSD1306& display,int width, int height);
  void begin();
  void displayStatus(char *text);
  Adafruit_SSD1306& getDisplay();
private:
  void setText1();
  const char* createStringWithSpaces(int n);
  Adafruit_SSD1306 oledDisplay;
  int _w;
  int _h;
};


#endif