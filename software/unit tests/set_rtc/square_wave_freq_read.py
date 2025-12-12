import machine
import time

pin = machine.Pin(12, machine.Pin.IN)

# -------- CONFIG ----------
AVG_SAMPLES = 32      # Good for 1 Hz → 10 kHz
# --------------------------

last_time = 0
period_buf = [0] * AVG_SAMPLES
buf_i = 0
buf_filled = False

def edge(pin):
    global last_time, buf_i, buf_filled
    now = time.ticks_us()

    if last_time != 0:
        period_us = time.ticks_diff(now, last_time)

        # Reject extremely small or crazy values (< 1 µs or > 2 sec)
        if 1 < period_us < 2_000_000:
            period_buf[buf_i] = period_us
            buf_i = (buf_i + 1) % AVG_SAMPLES
            if buf_i == 0:
                buf_filled = True

    last_time = now

# Interrupt on rising edge
pin.irq(trigger=machine.Pin.IRQ_RISING, handler=edge)

def get_freq():
    if not buf_filled and buf_i < 2:
        return 0.0

    # How many samples exist
    count = AVG_SAMPLES if buf_filled else buf_i

    # Average the periods
    total = sum(period_buf[:count])
    avg_period = total / count

    return 1_000_000 / avg_period


while True:
    f = get_freq()
    print("Frequency:", round(f, 3), "Hz")
    time.sleep(1)

