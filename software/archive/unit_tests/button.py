import machine
import utime

button0 = machine.Pin(0, machine.Pin.IN) #gpio 0 or 1
button1 = machine.Pin(1, machine.Pin.IN) 

while True:
    if button0.value() == 0:
        print("You pressed button 0")
    if button1.value() == 0:
        print("You pressed button 1")
    utime.sleep(0.1)
    
    