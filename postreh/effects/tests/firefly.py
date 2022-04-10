import utime

from postreh.effects.firefly import Firefly
from postreh.hw import LED_NUMBERS
from postreh.colors import BLACK, WHITE, BLUE


while True:
    # zacneme s vypnutyma diodama
    LED_NUMBERS.fill(BLACK)
    LED_NUMBERS.show()
    utime.sleep_ms(1000)

    # nastaveni efektu
    firefly = Firefly(200, 2, LED_NUMBERS.set)
    i = 0

    print("poblikavani")
    while True:
        i += 1
        if i == 2000:
            # po 2000 cyklu prenastavime svetlusky at se rozsviti
            print("rozsviceni")
            firefly.reconfigure(period=50, flies_per_period=4, dimming=False)
        if firefly.cycle():
            break
        LED_NUMBERS.show()
        utime.sleep_ms(3)

    del firefly

    LED_NUMBERS.fill(WHITE)
    LED_NUMBERS.show()
    utime.sleep_ms(2000)
