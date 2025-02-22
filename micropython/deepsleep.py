import machine
from machine import Pin
from time import sleep

led = Pin(8, Pin.OUT)

  
#blink LED
led.value(1)
sleep(1)
led.value(0)
sleep(1)

# wait 5 seconds so that you can catch the ESP awake to establish a serial communication later
# you should remove this sleep line in your final script
sleep(5)


print("Going to deep sleep for 5 seconds...")
machine.deepsleep(5000)

print("You won’t see this message until the next reboot!")