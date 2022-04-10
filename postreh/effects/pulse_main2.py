import utime

from postreh.effects.pulse2 import Pulse2
from postreh.neopixels import NeopixelStrip
from postreh.hw import LED_MAIN
from postreh.colors import WHITE, BLACK, RED, GREEN, ORANGE

    
# cerna -> cervena
while True:
    LED_MAIN.fill(BLACK)
    LED_MAIN.show()
    utime.sleep_ms(1000)

    f = Pulse2(26, BLACK, RED, 1, fadein=True, led_fn=LED_MAIN.fill)
    while True:
        if f.cycle():
            break
        f.debug()
        LED_MAIN.show()
        utime.sleep_ms(10)

    del f

    LED_MAIN.fill(RED)
    LED_MAIN.show()
    utime.sleep_ms(2000)

