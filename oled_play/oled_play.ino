#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "I2C_Scanner.h"
#include "OLED_Helper.h"


#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

OledHelper oledHelper(display,SCREEN_WIDTH,SCREEN_HEIGHT);


void setup() {
  Serial.begin(115200);
  oledHelper.begin();

}


void loop() {
  Serial.println("in loop");
  oledHelper.displayStatus("1234567890123456789012");
  delay(5000);

}

/*

void setup() {
  //Wire.begin();
  Serial.begin(115200);


  // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if(!display1.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }

  // Clear the buffer
  display1.clearDisplay();


}

void loop() {

  display1.clearDisplay();

  display1.setTextSize(1);      // Normal 1:1 pixel scale
  display1.setTextColor(SSD1306_WHITE); // Draw white text
  display1.cp437(true);         // Use full 256 char 'Code Page 437' font

  display1.setCursor(0, 0);     // Start at top-left corner
  display1.write("Galatsion");
  display1.setCursor(0, 10);     // Start at top-left corner
  display1.write("Temp: 5.1 C Feels: 7.3 C");

  display1.setCursor(0,20);
  display1.println("Hello");
  display1.println("I am George");

  display1.drawFastHLine(0,54,128,WHITE);

  display1.setCursor(0, 55);     // Start at top-left corner
  display1.write("Connected (Vodafon)");

  display1.display();

  //scan();
  delay(5000); 
}
*/
