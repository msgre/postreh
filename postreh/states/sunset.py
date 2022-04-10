"""
SUNSET

Hraci asi odesli, hlavni svetlo sviti a nikdo nic nemacka.
V tom pripadku ukoncime hru. Pomalu zhasnem hlavni svetlo i skore
hracu a prejde do dalsi faze.
"""

import utime

from postreh.hw import LED_MAIN, LED_NUMBERS, get_player_button
from postreh import states
from postreh.colors import BLACK
from postreh.effects import Pulse, Fadeout
from postreh.config import (
    SUNSET_MAIN_PERIOD,
    SUNSET_MAIN_COLOR1,
    SUNSET_MAIN_CYCLES,
    SUNSET_NUMBERS_PERIOD,
    SUNSET_NUMBERS_CYCLES,
    SUNSET_WAIT_SLEEP,
    SUNSET_WAIT_SLEEP_LIMIT,
)


# globalni promenne; jejich hodnota musi prezit do dalsiho cyklu process
main = None
numbers = None
next_state = None
internal_state = None
internal_tick = 0
pressed = False


def process(tick, context):
    global main
    global numbers
    global next_state
    global internal_state
    global internal_tick
    global pressed

    if tick == 0:
        print("SUNSET: inicializace")
        # hlavni svetlo pomalu zhasne
        main = Pulse(
            period=SUNSET_MAIN_PERIOD,
            color1=SUNSET_MAIN_COLOR1,
            color2=BLACK,
            cycles=SUNSET_MAIN_CYCLES,
            fadeout=True,
            led_fill=LED_MAIN.fill,
        )
        # cisla se skore pomalu zhasnou
        numbers = Fadeout(
            period=SUNSET_NUMBERS_PERIOD,
            cycles=SUNSET_NUMBERS_CYCLES,
            strip=LED_NUMBERS,
        )
        # reset hodnot
        internal_state = None
        next_state = "wait"
        internal_tick = 0
        context["quick_wakeup"] = False
        pressed = False
        return

    # zmackl nekdo tlacitko?
    keys_player = get_player_button()

    if not pressed and keys_player >= 0:
        print("SUNSET: nekdo chce hrat! urychlime sunset...")
        context["quick_wakeup"] = True
        pressed = True
        main = None
        numbers = None
        internal_state = "done"

    elif main or numbers:
        # obsluha probihajicich efektu
        if main and main.cycle():
            print("SUNSET: hlavni svetlo zhaslo")
            main = None
        if numbers and numbers.cycle():
            print("SUNSET: cisla se skore zhasla")
            numbers = None

        if not numbers and not main:
            # efekty dobehly presun na dalsi interni stav
            internal_state = next_state
            internal_tick = 0

    elif internal_state and internal_state == "wait":
        # chvilka na vydechnuti po dokonceni efektu
        # vsecko zhaslo, zustanme chvili ve tme
        internal_tick += 1
        utime.sleep_ms(SUNSET_WAIT_SLEEP)

        if internal_tick >= SUNSET_WAIT_SLEEP_LIMIT:
            print("SUNSET: temnota je u konce")
            internal_state = "done"

    elif internal_state and internal_state == "done":
        # pauza skoncila, uklidime a muzem se presunout na dalsi stav
        print("SUNSET: konec")
        return states.INTRO

    LED_MAIN.show()
    LED_NUMBERS.show()
