import machine

# Set GPIO 0 as wake-up source
wake_pin = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)

# Enable wake-up on falling edge (LOW signal when button is pressed)
machine.Pin.wake_on_ext0(wake_pin, machine.Pin.WAKE_LOW)

print("Going to deep sleep. Press the button to wake up...")
machine.deepsleep()

# This runs ONLY after wake-up
print("Woke up! Button was pressed.")
