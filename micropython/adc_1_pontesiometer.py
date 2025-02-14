from  machine import ADC, Pin
from time import sleep

PIN = 34

pin = ADC(Pin(PIN))
pin.atten(ADC.ATTN_2_5DB)

led = Pin(2,Pin.OUT)

while True:
  pot_value = pin.read_u16() #pin.read()
  print(pot_value)
  if pot_value > 500:
      led.value(1)
  else:
      led.value(0)
  sleep(0.1)