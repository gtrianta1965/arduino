#
# L9110S Motor Driver

from machine import Pin, PWM
import time

# Define motor control pins
IN1 = Pin(6, Pin.OUT)  # Direction 1
IN2 = Pin(7, Pin.OUT)  # Direction 2

# Use PWM for speed control
speed_pwm = PWM(IN1, freq=1000)

# Define Encoder Pins
ENC_A = Pin(4, Pin.IN, Pin.PULL_UP)  
ENC_B = Pin(5, Pin.IN, Pin.PULL_UP)

encoder_active = True
encoder_count = 0  # Stores the number of pulses
previous_A = 0
previous_B = 0
direction = 0

entry_count = 0

# Define encoder callback
def encoder_callback(pin):
    global encoder_count, entry_count
    global previous_A,previous_B,direction
    if encoder_active:
        entry_count += 1
        value_A = ENC_A.value()
        value_B = ENC_B.value()
        if value_A == 1 and value_B == 1:
            #print("Forward direction")
            direction = 1
            pass
        if value_A == 1 and value_B == 0:
            #print("Backward direction")
            direction = -1
            pass

        # Calculate rotations
        
        if (value_B == 1 and previous_B == 0) or (value_B == 0 and previous_B == 1):  # Check direction
            encoder_count += 1
            previous_B = value_B
        #else:
        #    encoder_count -= 1  # Reverse count if rotating opposite way
        #print("encoder_count",encoder_count,direction)
        print("Entry count=",entry_count)
        
    
# Setup encoder IRS routine
ENC_A.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=encoder_callback)

def motor_forward(speed):
    speed_pwm.duty(speed)  # Set speed (0-1023)
    IN1.value(1)
    IN2.value(0)

def motor_backward(speed):
    #speed_pwm.duty(speed)  # Set speed (0-1023)
    IN1.value(0)
    IN2.value(1)

def motor_stop():
    #speed_pwm.duty(0)  # Set speed (0-1023)
    
    IN1.value(1)
    IN2.value(1)
    time.sleep(0.1)
# Test motor
motor_forward(500)  # 50% speed forward
print("encoder_count1",encoder_count,entry_count)
encoder_count = 0
time.sleep(1)
#motor_backward(500)  # 50% speed backward
print("encoder_count2",encoder_count,entry_count)
time.sleep(1)
motor_stop()  # Stop motor
encoder_active = False
time.sleep(1)



print("Thats it")

