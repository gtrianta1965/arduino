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


thresholds = [30, 60, 80, 100, 120, 160, 190, 240]

##############################################
#
# Filter / Smoothing classes
#
##############################################
class MovingAverage:
    def __init__(self, size=5):
        self.size = size
        self.values = []

    def filter(self, new_value):
        self.values.append(new_value)
        if len(self.values) > self.size:
            self.values.pop(0)  # Keep only last `size` values
        return sum(self.values) / len(self.values)  # Average

class PeakHold:
    def __init__(self, decay=0.05):
        self.peak = 0
        self.decay = decay

    def filter(self, new_value):
        if new_value > self.peak:
            self.peak = new_value  # Update peak
        else:
            self.peak -= self.decay  # Gradual decay
            if self.peak < 0:
                self.peak = 0  # Prevent negative values
        return self.peak
    
class DropFilter:
    def __init__(self, hold_time=3, low_threshold=30):
        self.hold_counter = 5
        self.last_value = 0
        self.low_threshold = low_threshold
        self.hold_time = hold_time  # How long to ignore sudden drops

    def filter(self, new_value):
        if new_value <= self.low_threshold and self.last_value > 0:
            self.hold_counter += 1
            if self.hold_counter < self.hold_time:
                return self.last_value  # Ignore sudden drop
        else:
            self.hold_counter = 0  # Reset if signal is valid

        self.last_value = new_value
        return new_value
    
mal = MovingAverage(10)  # Smooth over 5 samples
mar = MovingAverage(10)  # Smooth over 5 samples
phl = PeakHold(15)
phr = PeakHold(15)
dfl = DropFilter(1000,50)
dfr = DropFilter(1000,50)


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

previous_level = 0 

def update_vu_meter(level, np):
    global previous_level
    if previous_level == level:
       return
    else:
       previous_level = level
    
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
        #if i == 0 and np[i][0] == 0:
            #print("Zero first")
    np.write()

#Adjust the thresholds
thresholds = get_thresholds(8,40,170)
print(f"Thresholds {thresholds}")


while True:
    
    value = mal.filter(audio_pin_l.read())
    #value = phl.filter(audio_pin_l.read())
    #value = dfl.filter(audio_pin_l.read())
    update_vu_meter(value,np_l)
    
    value = mar.filter(audio_pin_r.read())
    #value = phr.filter(audio_pin_r.read())
    #value = dfr.filter(audio_pin_r.read())
    update_vu_meter(value,np_r)
    
    #sleep(0.001)
    
    #this is for internal led pick
    led.value(0 if value > 100 else 1)
    
    
    
    
