"""
 URL
  https://microcontrollerslab.com/i2c-lcd-esp32-esp8266-micropython-tutorial/
  https://randomnerdtutorials.com/micropython-i2c-lcd-esp32-esp8266/
 
"""

import machine
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep

I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

#i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)     #initializing the I2C method for ESP32
i2c = SoftI2C(scl=Pin(9), sda=Pin(8), freq=10000)     #initializing the I2C method for ESP32 C3 Super Mini

#i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000)       #initializing the I2C method for ESP8266

lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

while True:
    lcd.putstr("I2C LCD Tutorial")
    
    sleep(2)
    lcd.clear()
    lcd.move_to(0,1)
    lcd.putstr("Lets Count 0-10!")
    sleep(2)
    lcd.clear()
    for i in range(11):
        lcd.putstr(str(i))
        sleep(1)
        lcd.clear()