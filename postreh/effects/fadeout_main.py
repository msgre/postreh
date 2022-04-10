import utime
import random

from postreh.effects import Fadeout
from postreh.neopixels import NeopixelStrip
from postreh.hw import LED_NUMBERS
from postreh.colors import WHITE, BLACK, RED, GREEN


    

while True:
    LED_NUMBERS.fill(WHITE)
#     for i in range(10):
#         idx = random.randint(0, 4*9 - 1)
#         LED_NUMBERS.set(idx, BLACK)
    LED_NUMBERS.show()
    utime.sleep_ms(1000)

    winner = random.randint(0, 3)
    print(winner)
    f = Fadeout(2, 120, LED_NUMBERS, winner=winner)
    while True:
        if f.cycle():
            break
        #f.debug()
        LED_NUMBERS.show()
        # utime.sleep_ms(5)

    del f
    
    utime.sleep_ms(2000)


    LED_NUMBERS.fill(BLACK)
    LED_NUMBERS.show()
    utime.sleep_ms(2000)

