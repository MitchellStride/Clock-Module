"""***********************************************************
PROGRAM NAME:   main.py
PROGRAMMER:     M. STRIDE, 2025 11 28
DESCRIPTION:    Firmware for clock PCB.
TODO:           
BUGS:           
***********************************************************"""
#---------------------------LIBS-----------------------------------
import machine
import utime
import time
import ssd1306 #save ssd1306 lib to pico first

from machine import ADC, Pin, Timer, PWM
from utime import sleep

#---------------------------SETUP-----------------------------------
#PINS
sensor_RP2040_die_temp = machine.ADC(4)
led = Pin(25, Pin.OUT)
ldr = ADC(Pin(26))
oled_rst = machine.Pin(15, machine.Pin.OUT)
button_SW4 = machine.Pin(1, machine.Pin.IN)
button_SW5 = machine.Pin(0, machine.Pin.IN) 
piezo = PWM(Pin(11))
piezo.duty_u16(0) 

#I2C
i2c0 = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17), freq=400000)
oled = ssd1306.SSD1306_I2C(width=128, height=64, i2c=i2c0, addr=0x3C)

#GLOBAL VARS
adc_conversion_factor = 3.3 / (65535)
# debounce timers
last_sw4 = 0
last_sw5 = 0
DEBOUNCE_MS = 200   # ignore presses within 200 ms

#---------------------------FUNCTIONS-----------------------------------
def read_temp():
    data = sensor_RP2040_die_temp.read_u16() * adc_conversion_factor
    # Typically, Vbe = 0.706V @ 27°C, with a slope of -1.721mV (0.001721) per degree. 
    RP2040_die_temp = 27 - (data - 0.706)/0.001721
    return RP2040_die_temp

# --- Function: short beep ---
def beep(duration_ms=250, freq=2000, duty=500):    
    piezo.freq(freq)
    piezo.duty_u16(duty)
    utime.sleep_ms(duration_ms)
    piezo.duty_u16(0)
    
def oled_setup():
    oled_rst.low()
    utime.sleep(0.1)
    oled_rst.high()
    utime.sleep(0.1)

def refresh_oled(t):
    #oled_pixel_check()
    oled.fill(0)   #clears screen
    oled.text("---Clock PCB---", 2, 0)
    oled.text(f"RP2040 Die:{read_temp():.1f}C", 0, 10)
    volt, light_class = read_LDR()
    oled.text(f"LDR:{volt:.2f}V, {light_class}", 0, 20)
    oled.show()

# Timer callback toggles LED
def toggle_led(t):
    led.value(not led.value())

def oled_off():
    oled.fill(0)
    oled.show()
    oled_rst.low()

def read_LDR():
    raw = ldr.read_u16()                     # 0–65535
    voltage = (raw / 65535) * 3.3           # convert to voltage
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
    return voltage, light_class

def button_SW4_pressed(pin):   #ISR
    global last_sw4
    now = utime.ticks_ms()
    if utime.ticks_diff(now, last_sw4) > DEBOUNCE_MS:
        print("SW4 Pressed!")
        beep()  # quarter second beep, care function has wait and blocks, better to set a flah=g
        #one shot timer would also be better
        last_sw4 = now

def button_SW5_pressed(pin):   #ISR, no SW deboucing
    print("SW5 Pressed!")



#---------------------------MAIN-----------------------------------
def main():
    utime.sleep(0.5)   #wait for serial terminal
    print("Clock PCB SW")

    # Create timer, period = 1000 ms (1 second)
    timer = Timer()
    timer.init(period=1000, mode=Timer.PERIODIC, callback=toggle_led)
    timer1 = Timer()
    timer1.init(period=500, mode=Timer.PERIODIC, callback=refresh_oled)
    # Setup IRQ buttons
    button_SW4.irq(trigger=machine.Pin.IRQ_FALLING,  handler=button_SW4_pressed)
    button_SW5.irq(trigger=machine.Pin.IRQ_FALLING,  handler=button_SW5_pressed)
    #ADD RGB,
    #Add up button plays buzzer and says on screen
    #down increments counter on screen

    
    utime.sleep(3) #run for X seconds
    beep()
    utime.sleep(0.250) 
    beep()
    piezo.duty_u16(0) 

    while True():
        utime.sleep(60) 
    #Turn OFF everything but LED toggle
    #timer1.deinit()
    #oled_off()
    print("END")

if __name__ == "__main__":
    main()
#------------------------------------------------------------------
