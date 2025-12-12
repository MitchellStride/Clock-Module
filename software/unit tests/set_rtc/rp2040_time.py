import machine
import time
import sys

i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))
ADDR = 0x68

def dec2bcd(val):
    return (val // 10) << 4 | (val % 10)

def set_ds1307(y, m, d, hh, mm, ss):
    data = bytes([
        dec2bcd(ss),
        dec2bcd(mm),
        dec2bcd(hh),
        1,                  # day of week (ignored)
        dec2bcd(d),
        dec2bcd(m),
        dec2bcd(y - 2000)
    ])
    i2c.writeto_mem(ADDR, 0x00, data)

while True:
    line = sys.stdin.readline().strip()
    if not line:
        continue

    try:
        y, m, d, hh, mm, ss = map(int, line.split())
        print("Setting:", y, m, d, hh, mm, ss)
        set_ds1307(y, m, d, hh, mm, ss)
    except:
        print("Bad data:", line)
