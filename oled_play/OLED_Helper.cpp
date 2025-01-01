#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Arduino.h>
#include "Oled_Helper.h"

#define SCREEN_WIDTH 128     // OLED display width, in pixels
#define SCREEN_HEIGHT 64     // OLED display height, in pixels
#define OLED_RESET -1        // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C  ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
#define STATUS_LINE_Y 54

OledHelper::OledHelper(Adafruit_SSD1306& display,int width, int height)
  : oledDisplay(display),_w(width), _h(height) {}
void OledHelper::begin() {
  if (!oledDisplay.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;)
      ;
  }
  oledDisplay.clearDisplay();
  oledDisplay.display();
}

void OledHelper::displayStatus(char* text) {
  setText1();
  oledDisplay.drawFastHLine(0, STATUS_LINE_Y, SCREEN_WIDTH, WHITE);

  oledDisplay.setCursor(0, STATUS_LINE_Y + 2);  // Start at top-left corner
  Serial.println(text);
  oledDisplay.write(text);

  oledDisplay.display();
}

void OledHelper::setText1() {
  oledDisplay.setTextSize(1);               // Normal 1:1 pixel scale
  oledDisplay.setTextColor(SSD1306_WHITE);  // Draw white text
  oledDisplay.cp437(true);                  // Use full 256 char 'Code Page 437' font
}

Adafruit_SSD1306& OledHelper::getDisplay() {
  return oledDisplay;
}

const char* OledHelper::createStringWithSpaces(int n) {
    static char buffer[65]; // Fixed-size buffer
    if (n < 0 || n >= sizeof(buffer)) {
        n = SCREEN_WIDTH;
    }

    // Fill the buffer with spaces
    memset(buffer, ' ', n);

    // Null-terminate the string
    buffer[n] = '\0';

    return buffer;
}

/*

class OledHelper {
public:
  OledHelper(int a) {
    //_address = address;
    Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
    _display = display;
    if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
      Serial.println(F("SSD1306 allocation failed"));
    }
  }
  
  void displayStatus(char *text) {
    _display.drawFastHLine(0, STATUS_LINE_X, SCREEN_WIDTH, WHITE);
    _display.setCursor(0, STATUS_LINE_X + 1);  // Start at top-left corner
    _display.write(text);
  }
  void lala() {

  }
  
private:
  byte _address;
  Adafruit_SSD1306 _display;
};
*/