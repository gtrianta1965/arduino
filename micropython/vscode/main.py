from machine import Pin,Signal
from time import sleep


button = Pin(13,Pin.IN, Pin.PULL_DOWN) 
led = Pin(2,Pin.OUT)
#led = Signal(2,Pin.OUT,invert = True)  #LOW means the led is ON
coolDown = 0
button_value = 0;
while True:
    button_value = button.value()
    print("Button",button_value)
    led.value(button_value)


    sleep(0.01)
