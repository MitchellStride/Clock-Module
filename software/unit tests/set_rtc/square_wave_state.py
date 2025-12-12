import machine
import time

pin = machine.Pin(12, machine.Pin.IN)
last = pin.value()

while True:
    cur = pin.value()
    if cur != last:
        print("Edge detected:", "Rising" if cur else "Falling")
        last = cur
    time.sleep(0.001)

