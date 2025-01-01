#ifndef OLED_HELPER_H
#define OLED_HELPER_H
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Arduino.h>

class OledHelper {
public:
  static int const LINE1 = 0;
  static int const LINE2 = 14;
  static int const LINE3 = 28;
  static int const LINE4 = 40;

  OledHelper(Adafruit_SSD1306& display,int width, int height,byte screen_address);
  void begin();
  void display(int x, int y, char *text);
  void displayStatus(char *text);
  void clearStatus();
  Adafruit_SSD1306& getDisplay();
private:
  void setText1();
  const char* createStringWithSpaces(int n);
  Adafruit_SSD1306 oledDisplay;
  int _w;
  int _h;
  byte _screen_address;
};


#endif