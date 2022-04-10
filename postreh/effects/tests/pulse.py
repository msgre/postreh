import utime

from postreh.effects.pulse import Pulse
from postreh.hw import LED_MAIN
from postreh.colors import BLACK, RED, GREEN, WHITE


while True:
    LED_MAIN.fill(BLACK)
    LED_MAIN.show()
    utime.sleep_ms(1000)

    # plynule rozsviceni zarovky z cerne do cervene
    pulse = Pulse(26, BLACK, RED, 1, fadein=True, led_fn=LED_MAIN.fill)
    while True:
        if pulse.cycle():
            break
        LED_MAIN.show()
        utime.sleep_ms(10)
    del pulse

    utime.sleep_ms(1000)

    # plynula zmena svetla z cervene do zelene
    pulse = Pulse(26 * 3, RED, GREEN, 1, led_fn=LED_MAIN.fill)
    while True:
        if pulse.cycle():
            break
        LED_MAIN.show()
        utime.sleep_ms(10)
    del pulse

    utime.sleep_ms(1000)

    # plynule zhasnuti zarovky ze zelene do cerne
    pulse = Pulse(26, GREEN, BLACK, 1, fadeout=True, led_fn=LED_MAIN.fill)
    while True:
        if pulse.cycle():
            break
        LED_MAIN.show()
        utime.sleep_ms(10)
    del pulse

    LED_MAIN.fill(BLACK)
    LED_MAIN.show()

    utime.sleep_ms(1000)

    # zablikani

    pulse = Pulse(26, BLACK, WHITE, 1, fadein=True, led_fn=LED_MAIN.fill)
    while True:
        if pulse.cycle():
            break
        LED_MAIN.show()
        utime.sleep_ms(10)
    del pulse
    LED_MAIN.fill(WHITE)
    LED_MAIN.show()

    pulse = Pulse(26, WHITE, (120, 120, 120), 6, led_fn=LED_MAIN.fill)
    while True:
        if pulse.cycle():
            break
        LED_MAIN.show()
        utime.sleep_ms(10)
    del pulse
    LED_MAIN.fill(WHITE)
    LED_MAIN.show()

    pulse = Pulse(26, WHITE, BLACK, 1, fadeout=True, led_fn=LED_MAIN.fill)
    while True:
        if pulse.cycle():
            break
        LED_MAIN.show()
        utime.sleep_ms(10)
    del pulse
    LED_MAIN.fill(BLACK)
    LED_MAIN.show()

    utime.sleep_ms(2000)
