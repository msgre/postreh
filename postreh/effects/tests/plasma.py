import utime

from postreh.effects import Plasma
from postreh.neopixels import NeopixelStrip
from postreh.hw import LED_MAIN
from postreh.colors import WHITE, BLACK, RED, GREEN, ORANGE


LED_MAIN.fill(BLACK)
LED_MAIN.show()

while True:
    # nejprve klasicka plazma, 10 cyklu
    plasma = Plasma(1, 10, LED_MAIN)
    while True:
        if plasma.cycle():
            print("preruseni")
            break
        LED_MAIN.show()
        utime.sleep_ms(1)

    # ted ji prepnem do rezimu fadeout
    print("fadeout")
    plasma.prepare_fadeout(10)

    # tmavnuti
    while True:
        if plasma.cycle():
            print("preruseni")
            break
        LED_MAIN.show()
        utime.sleep_ms(1)

    print("kanec")
    LED_MAIN.set_brightness(0.8)
    LED_MAIN.fill(BLACK)
    LED_MAIN.show()
    utime.sleep_ms(2000)
