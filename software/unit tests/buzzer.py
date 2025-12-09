from machine import Pin, PWM
import time

# PWM on GPIO11
piezo = PWM(Pin(11))


# Set duty cycle (0–65535)
#piezo.duty_u16(65535)   # Maximum duty (100%) will be distorted
piezo.duty_u16(45875)	#70% likely max
#piezo.duty_u16(32768)  # 50% duty for piezo
#piezo.duty_u16(8000)    # ~12% duty (quiet)
#piezo.duty_u16(4000)    # 
#piezo.duty_u16(1000)    # 

start_freq = 1000      # 1 kHz
end_freq   = 5000      # example: sweep to 5 kHz
duration   = 1.0       # seconds total sweep

steps = 200             # number of increments
step_time = duration / steps
freq_step = (end_freq - start_freq) / steps

freq = start_freq

for i in range(steps):
    piezo.freq(int(freq))
    freq += freq_step
    time.sleep(step_time)

# Optional: turn off piezo after sweep
piezo.duty_u16(0)
piezo.deinit()
