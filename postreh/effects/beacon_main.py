import utime

from postreh.effects.beacon import Beacon
from postreh.neopixels import NeopixelStrip
from postreh.hw import LED_MAIN
from postreh.colors import RED, BLACK, ORANGE, BLUE


LED_MAIN.fill(BLACK)
LED_MAIN.show()


while True:
    # 6 / 2
    # 4 / 1
    b = Beacon(200, RED, BLACK, 8, sectors=1, led_fn=LED_MAIN.set, fill=LED_MAIN.fill)
    while True:
        if b.cycle():
            break
        # b.debug()
        LED_MAIN.show()
        utime.sleep_ms(3)

    del b

    LED_MAIN.fill(BLACK)
    LED_MAIN.show()
    utime.sleep_ms(2000)
