"""
GAME_OVER

Hra skoncila, skore spoluhracu pomalu pohasnou, hlavni svetlo
se promeni v plazmu. Po chvili se plazma zacne ztmavovat
a po uplnem zcernani se hra vraci na zacatek.
"""

from postreh.config import (
    GAME_OVER_FADEOUT_CYCLES,
    GAME_OVER_FADEOUT_PERIOD,
    GAME_OVER_PLASMA_PERIOD,
    GAME_OVER_PLASMA_FADEOUT,
    GAME_OVER_PLASMA_CYCLES,
)

from postreh import states
from postreh.hw import LED_MAIN, LED_NUMBERS
from postreh.effects import Plasma, Fadeout
from postreh.colors import BLACK

main = None
numbers = None
internal_state = None
next_state = None
original_brightness = None


def process(tick, context):
    global main
    global numbers
    global internal_state
    global next_state
    global original_brightness

    if tick == 0:
        print("GAME_OVER: inicializace")
        # hlavni svetlo bude MAGIC
        main = Plasma(
            period=GAME_OVER_PLASMA_PERIOD,
            cycles=GAME_OVER_PLASMA_CYCLES,
            strip=LED_MAIN,
        )
        # skore looseru zacnou hasnout
        numbers = Fadeout(
            period=GAME_OVER_FADEOUT_PERIOD,
            cycles=GAME_OVER_FADEOUT_CYCLES,
            strip=LED_NUMBERS,
            winner=context["winner"],
        )
        internal_state = None
        next_state = "done"
        # musime si zapamatovat vychozi hodnotu jasu, protoze ji mozna budem pozdeji ovlivnovat
        original_brightness = LED_MAIN.get_brightness()
        return

    if main or numbers:
        if main and main.cycle():
            if main.fadeout is None:
                print("GAME_OVER: ztmavovani magic")
                main.prepare_fadeout(GAME_OVER_PLASMA_FADEOUT)
            else:
                print("GAME_OVER: magic je u konce")
                LED_MAIN.fill(BLACK)
                LED_MAIN.set_brightness(original_brightness)
                main = None
        if numbers and numbers.cycle():
            print("GAME_OVER: fadeout hracu je u konce")
            numbers = None

        if not numbers and not main:
            # efekty dobehly presun na dalsi interni stav
            internal_state = next_state

    elif internal_state and internal_state == "done":
        # stacilo, pojdme na novou hru
        print("GAME_OVER: konec")
        LED_NUMBERS.fill(BLACK)
        LED_NUMBERS.show()
        return states.INTRO

    LED_MAIN.show()
    LED_NUMBERS.show()
