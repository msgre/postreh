import utime

from postreh.effects import Plasma
from postreh.neopixels import NeopixelStrip
from postreh.hw import LED_MAIN
from postreh.colors import WHITE, BLACK, RED, GREEN, ORANGE

    
LED_MAIN.fill(BLACK)
LED_MAIN.show()

f = Plasma(1, LED_MAIN.set)
while True:
    if f.cycle():
        break
    #f.debug()
    LED_MAIN.show()
    utime.sleep_ms(1)