from  machine import ADC, Pin
from time import sleep


PIN = 34

pin = ADC(Pin(PIN))
max = 0
count = 0

# ADC.ATTN_0DB — the full range voltage: 1.2V
# ADC.ATTN_2_5DB — the full range voltage: 1.5V
# ADC.ATTN_6DB — the full range voltage: 2.0V
# ADC.ATTN_11DB — the full range voltage: 3.3V
pin.atten(ADC.ATTN_0DB)

led = Pin(2,Pin.OUT)

while True:

  pot_value = pin.read()
  max = pot_value if pot_value > max else max
  print("signal",pot_value,"max",max)
  if pot_value > 100:
      led.value(1)
  else:
      led.value(0)
  sleep(0.01)