from machine import Pin, PWM
import time

piezo = PWM(Pin(11))
piezo.duty_u16(30000)   # volume (~45%) adjust as needed

# Note frequencies (Hz)
C4 = 262
D4 = 294
E4 = 330
F4 = 349
G4 = 392
A4 = 440
B4 = 494
C5 = 523

def play(freq, duration):
    if freq == 0:
        piezo.duty_u16(0)      # rest
    else:
        piezo.freq(freq)
        piezo.duty_u16(30000)  # volume
    time.sleep(duration)
    piezo.duty_u16(0)          # silence between notes
    time.sleep(0.05)

melody = [
    (C4, 0.4), (C4, 0.4), (G4, 0.4), (G4, 0.4),
    (A4, 0.4), (A4, 0.4), (G4, 0.6),

    (F4, 0.4), (F4, 0.4), (E4, 0.4), (E4, 0.4),
    (D4, 0.4), (D4, 0.4), (C4, 0.6),

    (G4, 0.4), (G4, 0.4), (F4, 0.4), (F4, 0.4),
    (E4, 0.4), (E4, 0.4), (D4, 0.6),

    (G4, 0.4), (G4, 0.4), (F4, 0.4), (F4, 0.4),
    (E4, 0.4), (E4, 0.4), (D4, 0.6),

    (C4, 0.4), (C4, 0.4), (G4, 0.4), (G4, 0.4),
    (A4, 0.4), (A4, 0.4), (G4, 0.6),

    (F4, 0.4), (F4, 0.4), (E4, 0.4), (E4, 0.4),
    (D4, 0.4), (D4, 0.4), (C4, 0.8)
]

for freq, dur in melody:
    play(freq, dur)

piezo.deinit()
