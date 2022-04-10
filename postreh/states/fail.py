"""
FAIL

Reakce na spatenou reakci, hrac zmackl tlacitko jeste pred rozsvicenim hlavniho svetla.

Hlavni svetlo zmeni barvu na cervenou, looserovi zablika ztracene skore.
Hlavni svetlo zustane chvili cervene a pak se vypne. V tu chvili se prechazi
zpet do stavu NEW_ROUND.
"""

import utime

from postreh.hw import LED_MAIN, LED_NUMBERS
from postreh import states
from postreh.colors import BLACK, RED, WHITE
from postreh.effects import Pulse2
from postreh.config import FAIL_MAIN_PERIOD, FAIL_MAIN_COLOR1, FAIL_MAIN_CYCLES, FAIL_NUMBER_PERIOD, FAIL_NUMBER_COLOR1, FAIL_NUMBER_COLOR2, FAIL_NUMBER_CYCLES, FAIL_WAIT_SLEEP, FAIL_WAIT_SLEEP_LIMIT

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
        print('FAIL: inicializace')
        # hlavni svetlo zmeni barvu na cervenou
        main = Pulse2(FAIL_MAIN_PERIOD, BLACK, FAIL_MAIN_COLOR1, FAIL_MAIN_CYCLES, fadein=True, led_fn=LED_MAIN.fill)
        # hraci zablika mizejici skore
        number = Pulse2(FAIL_NUMBER_PERIOD, FAIL_NUMBER_COLOR1, FAIL_NUMBER_COLOR2, FAIL_NUMBER_CYCLES, led_fn=lambda c: LED_NUMBERS.set(context['last_player'] * 9 + context['score'][context['last_player']], c))
        # reset hodnot
        internal_state = None
        internal_tick = 0
        next_state = 'wait'
        return

    elif main or number:
        # obsluha probihajicich efektu
        if main and main.cycle():
            print('FAIL: hlavni svetlo zcervenalo')
            main = None
        if number and number.cycle():
            print('FAIL: cislo se ztracenym skore zablikalo')
            number = None
            
        if not number and not main:
            # efekty dobehly presun na dalsi interni stav
            internal_state = next_state
            internal_tick = 0

    elif internal_state and internal_state == 'wait':
        # chvilka na vydechnuti
        # hlavni svetlo zcervenalo a je treba ho nechat chvili svitit,
        # at si vsichni uvedomi co se stalo
        internal_tick += 1            
        utime.sleep_ms(FAIL_WAIT_SLEEP)

        if internal_tick >= FAIL_WAIT_SLEEP_LIMIT:  # TODO:
            print('FAIL: cervena sviti uz dost dlouho, priprava ztmaveni')
            main = Pulse2(FAIL_MAIN_PERIOD, FAIL_MAIN_COLOR1, BLACK, FAIL_MAIN_CYCLES, fadeout=True, led_fn=LED_MAIN.fill)
            internal_state = None
            next_state = 'done'

    elif internal_state and internal_state == 'done':
        # cervene svetlo zhaslo, uklidime a muzem se presunout na dalsi stav
        print('FAIL: konec')
        main = None
        LED_MAIN.fill(BLACK)
        LED_MAIN.show()
        return states.NEW_ROUND

    LED_MAIN.show()
    LED_NUMBERS.show()