from machine import ADC, Pin
import time

# Configure ADC (GPIO34)
adc = ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)  # Allows reading from 0V to ~3.6V

# Define LED pins
led_pins = [12, 13, 14, 15, 16, 17, 18, 19]
leds = [Pin(pin, Pin.OUT) for pin in led_pins]

# Define ADC thresholds (adjust as needed)
thresholds = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000]

# Moving average filter settings
SAMPLE_SIZE = 5  # Number of samples for smoothing
samples = [0] * SAMPLE_SIZE  # Circular buffer for smoothing

def read_smoothed_audio():
    """Reads the analog signal and applies a moving average filter."""
    global samples
    new_value = adc.read()  # Read ADC (0-4095)
    
    # Update the circular buffer
    samples.pop(0)
    samples.append(new_value)

    # Return the moving average
    return sum(samples) // SAMPLE_SIZE

def update_vu_meter(level):
    """Update LEDs based on the smoothed signal level."""
    for i in range(8):
        if level >= thresholds[i]:
            leds[i].on()  # Light up LED
        else:
            leds[i].off()  # Turn off LED

# Fill buffer initially with the first ADC reading
initial_value = adc.read()
samples = [initial_value] * SAMPLE_SIZE

while True:
    audio_level = read_smoothed_audio()
    update_vu_meter(audio_level)
    time.sleep(0.05)  # Small delay for smooth animation
