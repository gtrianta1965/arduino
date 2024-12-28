#ifndef TOUCH_HELPER_H
#define TOUCH_HELPER_H

class TouchHelper {

public:
  // Constructors
  TouchHelper(int pin);
  TouchHelper(int pin, int threshold);

  void loop();
  bool isTouched();
private:
  int _touchPin;
  int _threshold;
  bool _touched;
  bool _touchActivated;
};
#endif