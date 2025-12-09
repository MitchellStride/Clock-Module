import machine
import utime

button_SW4_UP = machine.Pin(0, machine.Pin.IN)
button_SW5_DOWN = machine.Pin(1, machine.Pin.IN) 

button_SW4_UP.irq(lambda pin: print("IRQ with flags:", pin.irq().flags()), machine.Pin.IRQ_FALLING)