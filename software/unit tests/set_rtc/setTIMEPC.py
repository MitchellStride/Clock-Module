import serial
import time
from datetime import datetime

# Change COM3 to whatever your Pico shows up as
ser = serial.Serial("COM3", 115200)

while True:
    now = datetime.now()
    # Format: YYYY MM DD HH mm SS
    msg = now.strftime("%Y %m %d %H %M %S")
    ser.write((msg + "\n").encode())
    print("Sent:", msg)
    time.sleep(1)
