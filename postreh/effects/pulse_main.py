import utime

from postreh.effects.pulse import Pulse
from postreh.neopixels import NeopixelStrip
from postreh.hw import LED_NUMBERS
from postreh.colors import WHITE, BLACK


LED_NUMBERS.fill(BLACK)
LED_NUMBERS.show()


while True:
    f = Pulse(50, WHITE, (120, 120, 120), 10, led_fn=LED_NUMBERS.fill)
    while True:
        if f.cycle():
            break
        LED_NUMBERS.show()
        utime.sleep_ms(3)

    del f

    LED_NUMBERS.fill(WHITE)
    LED_NUMBERS.show()
    utime.sleep_ms(2000)

    LED_NUMBERS.fill(BLACK)
    LED_NUMBERS.show()
    utime.sleep_ms(2000)