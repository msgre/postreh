from firefly import Firefly
from machine import Pin
import utime
import array


button1 = Pin(6, Pin.IN, Pin.PULL_DOWN)


BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

NEOPIXEL_COUNT = 9
NEOPIXEL_PIN = 5

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()

# state machines
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(NEOPIXEL_PIN))
sm.active(1)

ar = array.array("I", [0 for _ in range(NEOPIXEL_COUNT)])

def pixels_show(brightness=0.2):
    count = NEOPIXEL_COUNT
    dimmer_ar = array.array("I", [0 for _ in range(count)])
        
    for i,c in enumerate(ar):
        r = int(((c >> 8) & 0xFF) * brightness)
        g = int(((c >> 16) & 0xFF) * brightness)
        b = int((c & 0xFF) * brightness)
        dimmer_ar[i] = (g<<16) + (r<<8) + b
    
    sm.put(dimmer_ar, 8)
    
def pixels_set(i, color):
    value = (color[1]<<16) + (color[0]<<8) + color[2]
    ar[i] = value
    
def pixels_fill(color):
    count = len(ar)
    for i in range(count):
        pixels_set(i, color)
        
        
PERIOD = 300
FPP = 2
f = Firefly(9, PERIOD, FPP, dimming=True, led_fn=pixels_set)
pixels_fill(BLACK)
pixels_show()
once = True

while True:
    if f.cycle() and not once:
        break
    pixels_show()
    if button1.value() and once:
        f.reconfigure(period=int(round(PERIOD/2)), flies_per_period=FPP*2, dimming=False)
        once = False
    utime.sleep_ms(3)
    
pixels_show()
while True:
    utime.sleep_ms(100)
