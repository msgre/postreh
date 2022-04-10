import utime
import random

from postreh.effects import Fadeout
from postreh.hw import LED_NUMBERS
from postreh.colors import WHITE, BLACK


while True:
    # demo 1 ----------------------------------------------------
    # ztmaveni VSECH diod
    LED_NUMBERS.fill(WHITE)
    LED_NUMBERS.show()
    utime.sleep_ms(1000)

    fadeout = Fadeout(2, 120, LED_NUMBERS)
    while True:
        if fadeout.cycle():
            break
        LED_NUMBERS.show()
    del fadeout

    LED_NUMBERS.fill(BLACK)
    LED_NUMBERS.show()
    utime.sleep_ms(2000)

    # demo 2 ----------------------------------------------------
    # ztmaveni diod hracu kteri prohrali
    LED_NUMBERS.fill(WHITE)
    LED_NUMBERS.show()
    utime.sleep_ms(1000)

    winner = random.randint(0, 3)
    fadeout = Fadeout(2, 120, LED_NUMBERS, winner=winner)
    while True:
        if fadeout.cycle():
            break
        LED_NUMBERS.show()
    del fadeout
    utime.sleep_ms(2000)

    LED_NUMBERS.fill(BLACK)
    LED_NUMBERS.show()
    utime.sleep_ms(2000)
