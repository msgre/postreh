"""
WIN

Reakce na spravnou reakci, hrac jako prvni zmackl tlacitko po rozsviceni hlavniho svetla.

Hlavni svetlo zmeni barvu na zelenou, viteznemu hraci zablika ziskane skore.
Hlavni svetlo zustane chvili zelene a pak se vypne. V tu chvili se prechazi
zpet do stavu NEW_ROUND.
"""

import utime

from postreh.hw import LED_MAIN, LED_NUMBERS
from postreh import states
from postreh.colors import BLACK
from postreh.effects import Pulse
from postreh.config import (
    WIN_MAIN_PERIOD,
    WIN_MAIN_COLOR1,
    WIN_MAIN_COLOR2,
    WIN_MAIN_CYCLES,
    WIN_NUMBER_PERIOD,
    WIN_NUMBER_COLOR1,
    WIN_NUMBER_COLOR2,
    WIN_NUMBER_CYCLES,
    WIN_WAIT_SLEEP,
    WIN_WAIT_SLEEP_LIMIT,
)


# globalni promenne; jejich hodnota musi prezit do dalsiho cyklu process
main = None
number = None
next_state = None
internal_state = None
internal_tick = 0


def process(tick, context):
    global main
    global number
    global next_state
    global internal_state
    global internal_tick

    if tick == 0:
        print("WIN: inicializace")
        # hlavni svetlo zmeni barvu na zelenou
        main = Pulse(
            period=WIN_MAIN_PERIOD,
            color1=WIN_MAIN_COLOR1,
            color2=WIN_MAIN_COLOR2,
            cycles=WIN_MAIN_CYCLES,
            led_fill=LED_MAIN.fill,
        )
        # hraci zablika nove ziskane skore
        number = Pulse(
            period=WIN_NUMBER_PERIOD,
            color1=WIN_NUMBER_COLOR1,
            color2=WIN_NUMBER_COLOR2,
            cycles=WIN_NUMBER_CYCLES,
            led_fill=lambda c: LED_NUMBERS.set(
                context["winner"] * 9
                + context["score"][context["winner"]]
                - 1,
                c,
            ),
        )
        # reset hodnot
        internal_state = None
        internal_tick = 0
        next_state = "wait"
        return

    if main or number:
        # obsluha probihajicich efektu
        if main and main.cycle():
            print("WIN: hlavni svetlo zezelenalo")
            main = None
        if number and number.cycle():
            print("WIN: cislo s novym skore zablikalo")
            number = None

        if not number and not main:
            # efekty dobehly presun na dalsi interni stav
            internal_state = next_state
            internal_tick = 0

    elif internal_state and internal_state == "wait":
        # chvilka na vydechnuti po dokonceni efektu
        # hlavni svetlo zezelenalo a je treba ho nechat chvili svitit,
        # at si vsichni uvedomi co se stalo
        internal_tick += 1
        utime.sleep_ms(WIN_WAIT_SLEEP)

        if internal_tick >= WIN_WAIT_SLEEP_LIMIT:
            print("WIN: zelena sviti uz dost dlouho, priprava ztmaveni")
            main = Pulse(
                period=WIN_MAIN_PERIOD,
                color1=WIN_MAIN_COLOR2,
                color2=BLACK,
                cycles=WIN_MAIN_CYCLES,
                fadeout=True,
                led_fill=LED_MAIN.fill,
            )
            internal_state = None
            next_state = "done"

    elif internal_state and internal_state == "done":
        # zelene svetlo zhaslo, uklidime a muzem se presunout na dalsi stav
        print("WIN: konec")
        main = None
        LED_MAIN.fill(BLACK)
        LED_MAIN.show()
        return states.NEW_ROUND

    LED_MAIN.show()
    LED_NUMBERS.show()
