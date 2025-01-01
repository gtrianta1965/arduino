#include <Arduino.h>
#include "OledLib.h"

OledLib::OledLib() {
  Serial.println("Constructor called");
}

void OledLib::say() {
  Serial.println("I supposed to say something");
};