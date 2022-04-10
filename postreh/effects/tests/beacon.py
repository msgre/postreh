import utime

from postreh.effects.beacon import Beacon
from postreh.hw import LED_MAIN
from postreh.colors import RED, BLACK


LED_MAIN.fill(BLACK)
LED_MAIN.show()


while True:
    # klasicky majak
    beacon = Beacon(5, RED, BLACK, 5, sectors=1, strip=LED_MAIN)
    while True:
        if beacon.cycle():
            break
        LED_MAIN.show()
        utime.sleep_ms(3)
    del beacon

    # rozsviceni (prestanem premazavat pozice prouzku)
    beacon = Beacon(5, RED, RED, 2, sectors=1, strip=LED_MAIN)
    while True:
        if beacon.cycle():
            break
        # beacon.debug()
        LED_MAIN.show()
        utime.sleep_ms(3)
    del beacon

    # zhasnuti (cerny prouzek majak vypne)
    beacon = Beacon(5, BLACK, BLACK, 1, sectors=1, strip=LED_MAIN)
    while True:
        if beacon.cycle():
            break
        # beacon.debug()
        LED_MAIN.show()
        utime.sleep_ms(3)
    del beacon

    # vydech
    LED_MAIN.fill(BLACK)
    LED_MAIN.show()
    utime.sleep_ms(2000)
