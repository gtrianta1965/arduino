#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define BUTTON_PIN 2

// set the LCD number of columns and rows
int lcdColumns = 16;
int lcdRows = 2;


// Variables will change:
int lastState = HIGH; // the previous state from the input pin
int currentState;     // the current reading from the input pin

LiquidCrystal_I2C lcd(0x27,16,2);
 
void setup() {

  Wire.begin();
  Serial.begin(115200);
  Serial.println("\nI2C Scanner");
  lcd.init();
  lcd.clear();         
  lcd.backlight();      // Make sure backlight is on
  pinMode(BUTTON_PIN,INPUT_PULLUP);
  
  // Print a message on both lines of the LCD.
  lcd.setCursor(1,0);   //Set cursor to character 2 on line 0
  lcd.print("Hello world!");
  
  lcd.setCursor(1,1);   //Move cursor to character 2 on line 1
  lcd.print("LCD Tutorial");
}
 
void loop() {
   // read the state of the switch/button:
  currentState = digitalRead(BUTTON_PIN);

  if(lastState == LOW && currentState == HIGH)
    Serial.println("The state changed from LOW to HIGH");

  // save the last state
  lastState = currentState;

  /*
  byte error, address;
  int nDevices;
  Serial.println("Scanning...");
  nDevices = 0;
  for(address = 1; address < 127; address++ ) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();
    if (error == 0) {
      Serial.print("I2C device found at address 0x");
      if (address<16) {
        Serial.print("0");
      }
      Serial.println(address,HEX);
      nDevices++;
    }
    else if (error==4) {
      Serial.print("Unknow error at address 0x");
      if (address<16) {
        Serial.print("0");
      }
      Serial.println(address,HEX);
    }    
  }
  if (nDevices == 0) {
    Serial.println("No I2C devices found\n");
  }
  else {
    Serial.println("done\n");
  }
  delay(5000); 
  */         
}
