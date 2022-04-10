import utime
from machine import Pin

from postreh.effects.firefly import Firefly
from postreh.hw import LED_NUMBERS
from postreh.colors import BLACK


button1 = Pin(6, Pin.IN, Pin.PULL_DOWN)

        
PERIOD = 300
FPP = 2
f = Firefly(9, PERIOD, FPP, dimming=True, led_fn=LED_NUMBERS.set)
LED_NUMBERS.fill(BLACK)
LED_NUMBERS.show()
once = True

while True:
    if f.cycle() and not once:
        break
    LED_NUMBERS.show()
    if button1.value() and once:
        f.reconfigure(period=int(round(PERIOD/2)), flies_per_period=FPP*2, dimming=False)
        once = False
    utime.sleep_ms(3)
    
LED_NUMBERS.show()
while True:
    utime.sleep_ms(100)
