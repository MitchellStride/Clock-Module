import machine
import utime
import ssd1306

oled_rst = machine.Pin(15, machine.Pin.OUT)
oled_rst.low()
utime.sleep(0.1)
oled_rst.high()
utime.sleep(0.1)

i2c0 = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17), freq=400000)
oled = ssd1306.SSD1306_I2C(width=128, height=64, i2c=i2c0, addr=0x3C)

oled.fill(0)
oled.text("#badgelife", 25, 25)
oled.text("5", 5, 5)
oled.show()
print('updated')

