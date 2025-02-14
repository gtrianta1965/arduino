from machine import ADC, Pin
import time

Vin = 3.3
# ADC setup
adc = ADC(Pin(0))  # Use any ADC pin
adc.atten(ADC.ATTN_11DB)  # Set full range (0-3.3V)

# Calibration
V1_real = 2.88  # Measured voltage with a multimeter
ADC1_raw = 4095  # ADC reading at V1_real
V2_real = 1.58  # Measured voltage with a multimeter
ADC2_raw = 2224  # ADC reading at V2_real
# Compute calibration coefficients
m = (V2_real - V1_real) / (ADC2_raw - ADC1_raw)
b = V1_real - m * ADC1_raw

def get_calibrated_voltage():
    adc_raw = adc.read()  # Read ADC value (0-4095)
    voltage = m * adc_raw + b  # Apply calibration formula
    return voltage


# Known resistor value (Ohms)
R1 = 10000  # 10kΩ

while True:
    adc_value = adc.read()  # Get raw ADC value (0-4095)
    print("adc_value=",adc_value)
    voltage = get_calibrated_voltage()
    #voltage = adc_value * (Vin / 4095)  # Convert ADC value to voltage
    
    # Calculate unknown resistance using voltage divider formula
    if voltage > 0:
        print("Voltage",voltage)
        try:
            Rx =  0
            #Rx = R1 * ((Vin / voltage) - 1)  # Ohm's Law
            Rx = (R1 * voltage) / (Vin - voltage)
        except ZeroDivisionError:
            print("Zero division")
    else:
        Rx = float("inf")  # If voltage is 0, resistance is infinite (open circuit)

    print(f"ADC: {adc_value}, Voltage: {voltage:.2f}V, Resistance: {Rx:.2f}Ω")
    time.sleep(1)