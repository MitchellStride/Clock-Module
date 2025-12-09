#LED blink
from machine import Pin
from utime import sleep

led = Pin(25, Pin.OUT)

print("LED starts flashing...")
while True:
    try:
        led.toggle()
        sleep(1) # sleep 1sec
    except KeyboardInterrupt:
        break
led.off()
print("Finished.")
