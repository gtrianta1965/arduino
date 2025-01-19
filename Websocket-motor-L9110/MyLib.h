#ifndef MYLIB_H
#define MYLIB_H

#define DEBUG true

#define LOG(f_, ...) \
  { if (DEBUG) {Serial.printf((f_), ##__VA_ARGS__);} }


#endif


