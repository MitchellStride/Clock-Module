from machine import ADC, Pin
import time

# Initialize ADC on GPIO26 (ADC0)
ldr = ADC(Pin(26))

# ADC reference voltage
VREF = 3.3

while True:
    raw = ldr.read_u16()                     # 0–65535
    voltage = (raw / 65535) * VREF           # convert to voltage

    # Determine light class
    if voltage >= 2.8:
        light_class = "Flash"
    elif 2.5 <= voltage < 2.8:
        light_class = "Hi"
    elif 2.0 <= voltage < 2.5:
        light_class = "Light"
    elif 1.4 <= voltage < 2.0:
        light_class = "Dim"
    elif 0.1 <= voltage < 1.4:
        light_class = "Dark"
    else:
        light_class = "NoLDR"

    # Print output
    print("Raw:", raw, "Voltage: {:.2f} V".format(voltage), "Light class:", light_class)

    time.sleep(0.1)  # 100 ms delay

