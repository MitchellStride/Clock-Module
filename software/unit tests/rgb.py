import array, time
from machine import Pin
import rp2

# --------------------------
# Config
# --------------------------
NUM_LEDS = 1
PIN_NUM = 6
brightness = 0.2  # 0.0 to 1.0

# --------------------------
# WS2812 PIO program (timing adjusted for 4 MHz)
# --------------------------
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT,
             autopull=True, pull_thresh=24)
def ws2812():
    T1 = 1  # high time for '1'
    T2 = 3  # total cycle time
    T3 = 2  # low time for '0'
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0) [T3 - 1]
    jmp(not_x, "do_zero")   .side(1) [T1 - 1]
    jmp("bitloop")          .side(1) [T2 - 1]
    label("do_zero")
    nop()                   .side(0) [T2 - 1]
    wrap()

# --------------------------
# StateMachine
# --------------------------
sm = rp2.StateMachine(0, ws2812, freq=4_000_000, sideset_base=Pin(PIN_NUM))
sm.active(1)

# --------------------------
# LED array
# --------------------------
ar = array.array("I", [0 for _ in range(NUM_LEDS)])

def pixels_set(i, color):
    # color = (R,G,B)
    r = int(color[0] * brightness)
    g = int(color[1] * brightness)
    b = int(color[2] * brightness)
    ar[i] = (g << 16) + (r << 8) + b

def pixels_show():
    for c in ar:
        sm.put(c)
    time.sleep_ms(10)

# --------------------------
# Test: cycle colors
# --------------------------
colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,255)]
while True:
    for color in colors:
        pixels_set(0, color)
        pixels_show()
        time.sleep(0.5)
