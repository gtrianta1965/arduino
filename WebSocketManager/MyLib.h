#ifndef MYLIB_H
#define MYLIB_H

#define LOG(f_, ...) \
  { Serial.printf((f_), ##__VA_ARGS__); }


#endif


