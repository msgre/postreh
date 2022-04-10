import utime

from postreh.effects.pulse import Pulse
from postreh.neopixels import NeopixelStrip
from postreh.hw import LED_NUMBERS
from postreh.colors import WHITE, BLACK, RED, GREEN


LED_NUMBERS.fill(BLACK)
LED_NUMBERS.show()

IDX = 3


def single_fill(color):
    LED_NUMBERS.set(IDX, color)
    

while True:
    f = Pulse(30, WHITE, (120, 120, 120), 10, led_fn=single_fill)
    while True:
        if f.cycle():
            break
        #f.debug()
        LED_NUMBERS.show()
        utime.sleep_ms(10)

    del f

    LED_NUMBERS.set(IDX, WHITE)
    LED_NUMBERS.show()
    utime.sleep_ms(2000)

    LED_NUMBERS.set(IDX, BLACK)
    LED_NUMBERS.show()
    utime.sleep_ms(2000)

