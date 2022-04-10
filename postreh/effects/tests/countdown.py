import utime

from postreh.effects.countdown import Countdown
from postreh.hw import LED_NUMBERS
from postreh.colors import WHITE, BLACK


while True:
    # roznuti vsech diod do bile
    LED_NUMBERS.fill(WHITE)
    LED_NUMBERS.show()

    # efekt
    countdown = Countdown(50, WHITE, 100, LED_NUMBERS.set)
    while True:
        if countdown.cycle():
            break
        LED_NUMBERS.show()
        utime.sleep_ms(3)
    del countdown

    # vydechnuti
    LED_NUMBERS.fill(BLACK)
    LED_NUMBERS.show()
    utime.sleep_ms(2000)
