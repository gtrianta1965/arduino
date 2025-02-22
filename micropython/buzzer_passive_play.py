from machine import Pin, PWM
import time

buzzer = PWM(Pin(6))  # Connect buzzer to GPIO 15
buzzer.duty(0)

def play_tone(frequency, duration):
    buzzer.freq(frequency)  # Set frequency (e.g., 1000Hz)
    buzzer.duty(500)  # 50% duty cycle
    time.sleep(duration)
    buzzer.duty(0)  # Turn off sound

# Test buzzer with a 1 kHz tone for 1 second
#play_tone(500, 3)