import machine

i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))
DS1307_ADDR = 0x68
CTRL_REG = 0x07

# ---------------------------
# Square-wave frequency options
# Uncomment the one you want:
# ---------------------------

# 1 Hz  (default)
control_value = 0b00010000     # SQWE=1, RS1=0, RS0=0

# 4.096 kHz
# control_value = 0b00010001   # SQWE=1, RS1=0, RS0=1

# 8.192 kHz
# control_value = 0b00010010   # SQWE=1, RS1=1, RS0=0

# 32.768 kHz
# control_value = 0b00010011   # SQWE=1, RS1=1, RS0=1
# ---------------------------

# Write the control register
i2c.writeto_mem(DS1307_ADDR, CTRL_REG, bytes([control_value]))

print("DS1307 SQW set. Control register =", bin(control_value))

