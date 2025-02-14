from  machine import ADC, Pin
from time import sleep
import math


PIN = 34
leds = [
    Pin( 17, Pin.OUT, value=1),
    Pin( 16, Pin.OUT, value=1),
    Pin( 32, Pin.OUT, value=1),
    Pin( 33, Pin.OUT, value=1),
    Pin( 25, Pin.OUT, value=1),
    Pin( 26, Pin.OUT, value=1),
    Pin( 27, Pin.OUT, value=1),
    Pin( 14, Pin.OUT, value=1),
    Pin( 12, Pin.OUT, value=1),
    Pin( 13, Pin.OUT, value=1)
    ]

# Define ADC thresholds (adjust based on signal level)
thresholds = [10,25,40, 60, 80, 90, 120, 150, 200, 300]

#The total leds of VU Meter
TOTAL_LEDS = 10 

# Moving average filter settings
SAMPLE_SIZE = 5  # Number of samples for smoothing
samples = [0] * SAMPLE_SIZE  # Circular buffer for smoothing

pin = ADC(Pin(PIN))
max = 0
count = 0

# Peak hold variables
peak_led = -1  # Stores the highest lit LED index
peak_hold_time = 400  # Number of cycles to hold the peak
peak_timer = 0  # Counter for peak hold

# ADC.ATTN_0DB — the full range voltage: 1.2V
# ADC.ATTN_2_5DB — the full range voltage: 1.5V
# ADC.ATTN_6DB — the full range voltage: 2.0V
# ADC.ATTN_11DB — the full range voltage: 3.3V
pin.atten(ADC.ATTN_0DB)
#pin.atten(ADC.ATTN_11DB)

######################################
# Return a logarithmic threasold array
######################################
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

def read_smoothed_audio():
    """Reads the analog signal and applies a moving average filter."""
    global samples
    new_value = pin.read()  # Read ADC (0-4095)
    
    # Update the circular buffer
    samples.pop(0)
    samples.append(new_value)

    # Return the moving average
    return sum(samples) // SAMPLE_SIZE

def update_vu_meter(level):
    """Update LEDs based on the signal level."""
    global peak_led, peak_timer
    
    active_led = -1  # Track the highest LED turned on in this update
    
    for i in range(TOTAL_LEDS):
        if level >= thresholds[i]:
            leds[i].on()  # Light up LED
            active_led = i
        else:
            leds[i].off()  # Turn off LED
            
    # Peak hold logic
    if active_led > peak_led:  # If a new peak is reached, update it
        peak_led = active_led
        peak_timer = peak_hold_time  # Reset peak hold timer

    # Keep peak LED on while timer lasts
    if peak_led >= 0:
        leds[peak_led].on()
        if peak_timer > 0:
            peak_timer -= 1  # Decrease hold timer
        else:
            peak_led = -1  # Reset peak when timer expires           

initial_value = pin.read()
samples = [initial_value] * SAMPLE_SIZE
thresholds = get_thresholds(10,10,200)
print(f"Program started with threshold",thresholds)

while True:

  #pot_value = pin.read()
  pot_value = read_smoothed_audio()
  max = pot_value if pot_value > max else max
  #print("signal",pot_value,"max",max)
  update_vu_meter(pot_value)
  sleep(0.005)