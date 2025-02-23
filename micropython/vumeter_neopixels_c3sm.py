from machine import  ADC, Pin
from time import sleep
import neopixel
import math

BRIGHTNESS = 0.3
AUDIO_PIN_L = 0
AUDIO_PIN_R = 1
NUMBER_OF_LEDS = 8
LEDS_PIN_L = 4
LEDS_PIN_R = 3

np_l = neopixel.NeoPixel(Pin(LEDS_PIN_L), NUMBER_OF_LEDS)
np_r = neopixel.NeoPixel(Pin(LEDS_PIN_R), NUMBER_OF_LEDS)

led = Pin(8, Pin.OUT)  # internal Led (blue)
led.value(1)

audio_pin_l = ADC(Pin(AUDIO_PIN_L))
audio_pin_l.atten(ADC.ATTN_11DB)

audio_pin_r = ADC(Pin(AUDIO_PIN_R))
audio_pin_r.atten(ADC.ATTN_11DB)

# ADC.ATTN_0DB — the full range voltage: 1.2V
# ADC.ATTN_2_5DB — the full range voltage: 1.5V
# ADC.ATTN_6DB — the full range voltage: 2.0V
# ADC.ATTN_11DB — the full range voltage: 3.3V
#audio_pin.atten(ADC.ATTN_0DB)


thresholds = [100, 116, 136, 160, 187, 219, 256, 300]

def get_thresholds(count,min, max):

    _size = count
    min_value = min
    max_value = max

    # Generate logarithmically spaced values
    log_values = []
    log_min = math.log(min_value)
    log_max = math.log(max_value)

    for i in range(_size):
        fraction = i / (_size - 1)  # Normalize to range 0-1
        log_value = math.exp(log_min + fraction * (log_max - log_min))  # Exponential mapping
        log_values.append(int(log_value))  # Convert to integer
        
    return log_values

def update_vu_meter(level, np):
    
    """Update LEDs based on the smoothed signal level."""
    red = 0
    for i in range(8):
        if i > 4:
            red = 50
        if i> 6:
            red = 100
        if level >= thresholds[i]:
            np[i] = (int(red * BRIGHTNESS),int((100-red) * BRIGHTNESS),0)
        else:
            np[i] = (0,0,0)
    np.write()

#Adjust the thresholds
thresholds = get_thresholds(8,100,300)
print(f"Thresholds {thresholds}")


while True:
    value = audio_pin_l.read()
    update_vu_meter(value,np_l)
    
    value = audio_pin_r.read()
    update_vu_meter(value,np_r)
    
    #sleep(0.001)
    
    #this is for internal led pick
    led.value(0 if value > 100 else 1)
    
    
    
    