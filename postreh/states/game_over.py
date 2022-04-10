"""
TODO:
- tohle neni dokoncene
"""

from postreh.config import GAME_OVER_FADEOUT_CYCLES, GAME_OVER_FADEOUT_PERIOD, GAME_OVER_PLASMA_PERIOD
import utime

from postreh.hw import LED_MAIN, LED_NUMBERS
from postreh.states import states
from postreh.effects import Plasma, Fadeout

main = None
numbers = None
internal_state = None
next_state = None

def process(tick, context):
    global main
    global numbers
    global internal_state
    global next_state

    if tick == 0:
        print('GAME_OVER: inicializace')
        # hlavni svetlo bude MAGIC
        main = Plasma(GAME_OVER_PLASMA_PERIOD, LED_MAIN.set)
        # skore looseru zacnou hasnout
        numbers = Fadeout(GAME_OVER_FADEOUT_PERIOD, GAME_OVER_FADEOUT_CYCLES, LED_NUMBERS, winner=context['winner'])
        internal_state = None
        next_state = None
        return
    
    elif main or numbers:
        if main and main.cycle():
            print('GAME_OVER: magic je u konce')
            main = None
        if numbers and numbers.cycle():
            print('GAME_OVER: fadeout hracu je u konce')
            numbers = None

        if not numbers and not main:
            # efekty dobehly presun na dalsi interni stav
            internal_state = next_state

    elif internal_state and internal_state == 'done':
        # stacilo, pojdme na novou hru
        print('GAME_OVER: konec')
        LED_MAIN.fill(BLACK)
        LED_MAIN.show()
        LED_NUMBERS.fill(BLACK)
        LED_NUMBERS.show()
        return states.NEW_ROUND

    LED_MAIN.show()
    LED_NUMBERS.show()