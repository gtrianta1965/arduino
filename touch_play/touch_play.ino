#include "TouchHelper.h"
// ESP32 Touch Test
// Just test touch pin - Touch0 is T0 which is on GPIO 4.
#define TOUCH_PIN 32
#define TOUCH_THRESHOLD 25

void setup() {
  Serial.begin(115200);
  delay(1000); // give me time to bring up serial monitor
  Serial.println("ESP32 Touch Test");
}

int touchValue;
bool touchActivated = false;

TouchHelper touchHelper(TOUCH_PIN,TOUCH_THRESHOLD);
void loop() {

  touchHelper.loop();
  if (touchHelper.isTouched()) {
    Serial.println("Touched");
  } else {
    Serial.println("Released");
  }

  /*
  //Serial.println(touchRead(TOUCH_PIN));  // get value of Touch 0 pin = GPIO 4
  touchValue = touchRead(TOUCH_PIN);
  if (touchValue < TOUCH_THRESHOLD) {
    if (!touchActivated) {
      Serial.println("Touch activated");
      touchActivated = true;
    }
  } else {
    if (touchActivated == true) {
      Serial.println("Touch de-activated");
      touchActivated = false;
    }
  }
  */

  delay(1000);
}