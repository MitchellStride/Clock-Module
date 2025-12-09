import machine
import utime
import ssd1306

#Reset any devices
oled_rst = machine.Pin(15, machine.Pin.OUT)
oled_rst.low()
utime.sleep(0.1)
oled_rst.high()

i2c0 = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))

print(i2c0.scan())
