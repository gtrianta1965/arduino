#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Arduino.h>
#include "Oled_Helper.h"

#define STATUS_LINE_Y 54

OledHelper::OledHelper(Adafruit_SSD1306& display,int width, int height, byte screen_address)
  : oledDisplay(display),_w(width), _h(height), _screen_address(screen_address) {}
void OledHelper::begin() {
  if (!oledDisplay.begin(SSD1306_SWITCHCAPVCC, _screen_address)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;)
      ;
  }
  oledDisplay.clearDisplay();
  oledDisplay.display();
}

void  OledHelper::display(int x, int y, char *text) {
      setText1();
      oledDisplay.fillRect(x, y,  _w, 8, BLACK);
      oledDisplay.setCursor(x,y); 
      oledDisplay.write(text);
      oledDisplay.display();
}

void OledHelper::displayStatus(char* text) {
  setText1();
  oledDisplay.drawFastHLine(0, STATUS_LINE_Y, _w, WHITE);

  //Clear the line


  Serial.println(text);
  oledDisplay.fillRect(0, STATUS_LINE_Y + 2, _w, 8, BLACK);
  oledDisplay.setCursor(0, STATUS_LINE_Y + 2);  // Start at top-left corner
  oledDisplay.write(text);

  oledDisplay.display();
}

void OledHelper::clearStatus() {
   oledDisplay.fillRect(0, STATUS_LINE_Y + 2, _w, 8, BLACK);
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
        n = _w;
    }

    // Fill the buffer with spaces
    memset(buffer, ' ', n);

    // Null-terminate the string
    buffer[n] = '\0';

    return buffer;
}

