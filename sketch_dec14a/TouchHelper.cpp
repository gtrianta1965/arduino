#include "TouchHelper.h"
#include <Arduino.h>

TouchHelper::TouchHelper(int pin) {
  TouchHelper(pin,22);
}

TouchHelper::TouchHelper(int pin, int threshold) {
  _threshold = threshold;
  _touchPin = pin;
  _touchActivated = false;
}

void TouchHelper::loop() {
  int touchValue;

  touchValue = touchRead(_touchPin);
  if (touchValue < _threshold) {
    if (!_touchActivated) {
      Serial.println("Touch activated");
      _touchActivated = true;
    }
  } else {
    if (_touchActivated) {
      Serial.println("Touch de-activated");
      _touchActivated = false;
    }
  }
}

bool TouchHelper::isTouched() {
  return _touchActivated;
}
