from machine import Pin, PWM
import time

# PWM on GPIO 1 and 2
pwm1 = PWM(Pin(1))
pwm2 = PWM(Pin(2))

# PWM on onboard LED (portable)
try:
    pwm_led = PWM(Pin("LED"))
except:
    pwm_led = PWM(Pin(25))

# Set PWM frequency (1 kHz is fine for LEDs)
pwm1.freq(1000)
pwm2.freq(1000)
pwm_led.freq(1000)

# 16-bit PWM range in MicroPython: 0–65535
MAX_DUTY = 65535

while True:
    for percent in range(0, 101, 10):
        duty = int((percent / 100) * MAX_DUTY)

        pwm1.duty_u16(duty)
        pwm2.duty_u16(duty)
        pwm_led.duty_u16(duty)

        print(f"Brightness: {percent}%  (duty={duty})")

        time.sleep(3)
