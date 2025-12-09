import machine
import time

# I2C0 on GP0=SDA, GP1=SCL
i2c0 = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))

DS1307_ADDR = 0x68

def bcd2dec(val):
    return (val // 16) * 10 + (val % 16)

def read_time():
    data = i2c0.readfrom_mem(DS1307_ADDR, 0x00, 7)
    second = bcd2dec(data[0] & 0x7F)
    minute = bcd2dec(data[1])
    hour   = bcd2dec(data[2])
    day    = bcd2dec(data[4])
    month  = bcd2dec(data[5])
    year   = bcd2dec(data[6]) + 2000
    return (year, month, day, hour, minute, second)

while True:
    print(read_time())
    time.sleep(1)
