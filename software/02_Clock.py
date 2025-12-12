"""***********************************************************
PROGRAM NAME:   main.py
PROGRAMMER:     M. STRIDE, 2025 11 28
DESCRIPTION:    Firmware for clock PCB.
TODO:           Note clock is free run updates not based on RTC SQWV
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
# GPIO12 input for 1Hz pulse
pulse = machine.Pin(12, machine.Pin.IN)

#I2C
i2c0 = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17), freq=400000)
oled = ssd1306.SSD1306_I2C(width=128, height=64, i2c=i2c0, addr=0x3C)
DS1307_ADDR = 0x68

#GLOBAL VARS
adc_conversion_factor = 3.3 / (65535)
BIRTH_YEAR, BIRTH_MONTH, BIRTH_DAY = 1997, 3, 1  # Replace with your birthday
LIFE_EXPECTANCY=80  #Look up 

# debounce timers
last_sw4 = 0
last_sw5 = 0
DEBOUNCE_MS = 200   # ignore presses within 200 ms
RTC=False
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")



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

def oled_text_center(text, y):
    # Calculate start x to center text
    x = (128 - len(text) * 8) // 2
    oled.text(text, x, y)

def refresh_oled():
    #oled_pixel_check()
    oled.fill(0)   #clears screen
    #oled_text_center("---Clock PCB---", 0)
    #oled.text(f"RP2040 Die:{read_temp():.1f}C", 0, 9*1)
    #volt, light_class = read_LDR()
    #oled.text(f"LDR:{volt:.2f}V, {light_class}", 0, 9*2)
    if RTC:
        year, month, day, hour, minute, second, hour_12, ampm = read_time()
        month_str = MONTHS[month-1]           # Convert month number to 3-letter abbreviation
        oled_text_center(f"{year} {month_str} {day:02}", 0)
        oled_text_center(f"{hour_12:02}:{minute:02}:{second:02} {ampm}", 9*1)    #:02 pads leading zeros to ensure 2 dig

        spacing = 6
        # ---- Age display middle two lines ----
        d1, d2 = age_countup(BIRTH_YEAR, BIRTH_MONTH, BIRTH_DAY)
        oled_text_center(f"AGE: {d1}", spacing+(9*2))   # Age in years, months, days
        oled_text_center(d2, spacing+(9*3))   # Age in hours, minutes, seconds
        
        # ---- Death clock bottom two lines ----
        d1, d2 = death_countdown(year, month, day, hour, minute, second)
        oled_text_center(f"TTD:{d1}", 2*spacing+(9*4))   # Years and days
        oled_text_center(d2, 2*spacing+(9*5))   # Hours, minutes, seconds
    else:
        oled.text(f"No RTC", 0, 30)
    oled.show()

# Timer callback toggles LED
def toggle_led():
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

#RTC Code
def bcd2dec(val):
    return (val // 16) * 10 + (val % 16)

def to_12h(hour):
    if hour == 0: return 12, "AM"
    if hour < 12: return hour, "AM"
    if hour == 12: return 12, "PM"
    return hour - 12, "PM"

def read_time():
    data = i2c0.readfrom_mem(DS1307_ADDR, 0x00, 7)
    second = bcd2dec(data[0] & 0x7F)
    minute = bcd2dec(data[1])
    hour   = bcd2dec(data[2])
    day    = bcd2dec(data[4])
    month  = bcd2dec(data[5])
    year   = bcd2dec(data[6]) + 2000

    hour_12, ampm = to_12h(hour)
    
    return (year, month, day, hour, minute, second, hour_12, ampm)

def RTC_FUNCTIONAL():
    global RTC
    if DS1307_ADDR in i2c0.scan():
        print("DS1307 RTC detected!")
        RTC=True
    else:
        print("DS1307 RTC not found!")
        RTC=False

def age_countup(birth_year, birth_month, birth_day, birth_hour=0, birth_minute=0, birth_second=0):
    # Get current time from RTC
    year, month, day, hour, minute, second, _, _ = read_time()
    
    # Convert birth and now into seconds since epoch
    now_secs = utime.mktime((year, month, day, hour, minute, second, 0, 0))
    birth_secs = utime.mktime((birth_year, birth_month, birth_day, birth_hour, birth_minute, birth_second, 0, 0))
    
    diff = now_secs - birth_secs
    if diff < 0:
        return ("NOT BORN", "")
    
    total_days = diff // 86400
    years = total_days // 365
    days_remaining = total_days % 365
    months = days_remaining // 30          # Approximate month length
    days = days_remaining % 30
    hours = (diff % 86400) // 3600
    minutes = (diff % 3600) // 60
    seconds = diff % 60
    
    line1 = f"{years:02}y {months:02}m {days:02}d"
    line2 = f"{hours:02}h {minutes:02}m {seconds:02}s"
    return line1, line2

def death_countdown(year, month, day, hour, minute, second):
    death_year, death_month, death_day = BIRTH_YEAR+LIFE_EXPECTANCY, BIRTH_MONTH, BIRTH_DAY

    now = utime.mktime((year, month, day, hour, minute, second, 0, 0))
    target = utime.mktime((death_year, death_month, death_day, 0, 0, 0, 0, 0))
    diff = target - now  # seconds until death (can be negative)

    total_seconds = abs(diff)

    years = total_seconds // (365 * 86400)
    remaining_seconds = total_seconds % (365 * 86400)

    months = remaining_seconds // (30 * 86400)
    remaining_seconds %= (30 * 86400)

    days = remaining_seconds // 86400
    remaining_seconds %= 86400

    hours = remaining_seconds // 3600
    remaining_seconds %= 3600

    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60

    # Only prefix years with negative if diff < 0
    if diff < 0:
        years = -years
        line1 = f"-{years:02}y {months:02}m {days:02}d"
    else:
        line1 = f" {years:02}y {months:02}m {days:02}d"
    line2 = f"{hours:02}h {minutes:02}m {seconds:02}s"
    return line1, line2


#---------------------------MAIN-----------------------------------
def main():
    #utime.sleep(0.5)   #wait for serial terminal
    #print("Clock PCB SW")
    RTC_FUNCTIONAL()

    # Create timer, period = 1000 ms (1 second)
    #timer = Timer()
    #timer.init(period=1000, mode=Timer.PERIODIC, callback=toggle_led)
    #timer1 = Timer()
    #timer1.init(period=500, mode=Timer.PERIODIC, callback=refresh_oled)
    # Setup IRQ buttons
    #button_SW4.irq(trigger=machine.Pin.IRQ_FALLING,  handler=button_SW4_pressed)
    #button_SW5.irq(trigger=machine.Pin.IRQ_FALLING,  handler=button_SW5_pressed)
    #ADD RGB,
    #Add up button plays buzzer and says on screen
    #down increments counter on screen

    
    utime.sleep(0.1) #run for X seconds
    beep()
    piezo.duty_u16(0) 

    last_state=0
    while True:
        state = pulse.value()
        if state == 1 and last_state == 0:  # rising edge
            refresh_oled()
            toggle_led()
        last_state = state
        utime.sleep_ms(10)

if __name__ == "__main__":
    main()
#------------------------------------------------------------------
