"""
INTRO

Ceka se na stisk nektereho z tlacitek, behem toho nahodne poblikavaji
cisla (svetlusky). Jakmile se nektere tlacitko zmackne, vsechny
svetlusky se probudi, rozsviti, zapulzuji a zacne jejich odpocet.
Zaroven se hlavni svetlo zmeni na majak a po dobu odpoctu zacne blikat.

Jakmile odpocet dobehne, vse zhasne a prechazi se do dalsi faze.
"""

import utime

from postreh.hw import LED_MAIN, LED_NUMBERS, get_player_button
from postreh import states
from postreh.effects import Firefly, Countdown, Beacon
from postreh.colors import BLACK, WHITE, RED
from postreh.config import INTRO_ANGRY_FIREFLY_PER_PERIOD, INTRO_ANGRY_FIREFLY_PERIOD, INTRO_BEACON_COLOR, INTRO_BEACON_CYCLES, INTRO_CALM_FIREFLY_PERIOD, INTRO_CALM_FIREFLY_PER_PERIOD, INTRO_ANGRY_FIREFLY_PERIOD, INTRO_ANGRY_FIREFLY_PER_PERIOD, INTRO_COUNTDOWN_COLOR, INTRO_COUNTDOWN_PERIOD, INTRO_COUNTDOWN_WAIT, LED_NUMBERS_COUNT, PLAYERS, INTRO_WAIT_SLEEP, INTRO_WAIT_SLEEP_LIMIT, SCORES_PER_PLAYER, INTRO_BEACON_PERIOD, INTRO_BEACON_SECTORS


# globalni promenne; jejich hodnota musi prezit do dalsiho cyklu process
main = None
numbers = None
next_state = None
internal_state = None
internal_tick = 0
touched = None


def process(tick, context):
    global main
    global numbers
    global next_state
    global internal_state
    global internal_tick
    global touched
    
    if tick == 0:
        print('INTRO: inicializace')
        # vypnout hlavni svetlo
        LED_MAIN.fill(BLACK)
        LED_MAIN.show()
        # vypnout LEDky s cislama
        LED_NUMBERS.fill(BLACK)
        LED_NUMBERS.show()
        # inicilizace effektu svetluska
        main = None
        numbers = Firefly(LED_NUMBERS_COUNT, INTRO_CALM_FIREFLY_PERIOD, INTRO_CALM_FIREFLY_PER_PERIOD, dimming=True, led_fn=LED_NUMBERS.set)
        touched = False
        internal_state = None
        internal_tick = 0
        next_state = 'wait'
        return
        
    elif not touched and (context['quick_wakeup'] or get_player_button() != -1):
        print('INTRO: stisknuto tlacitko, svetlusky rozsvitte se')
        touched = True
        numbers.reconfigure(period=INTRO_ANGRY_FIREFLY_PERIOD, flies_per_period=INTRO_ANGRY_FIREFLY_PER_PERIOD, dimming=False)
    
    elif main or numbers:
        # obsluha probihajicich efektu
        if main and main.cycle():
            print('INTRO: majak na hlavnim svetle doblikal')
            main = None
        if numbers and numbers.cycle():
            print('INTRO: efekt na cislech dokoncen')
            numbers = None
            
        if not numbers and not main:
            # efekty dobehly presun na dalsi interni stav
            internal_state = next_state
            internal_tick = 0

    elif internal_state and internal_state == 'wait':
        # cekacka po probuzeni svetlusek
        internal_tick += 1            
        utime.sleep_ms(INTRO_WAIT_SLEEP)

        if internal_tick >= INTRO_WAIT_SLEEP_LIMIT:
            print('INTRO: svetlusky sviti uz dost dlouho, pojdme na countdown a majak')
            numbers = Countdown(INTRO_COUNTDOWN_PERIOD, PLAYERS, SCORES_PER_PLAYER, INTRO_COUNTDOWN_COLOR, INTRO_COUNTDOWN_WAIT, led_fn=LED_NUMBERS.set)
            main = Beacon(INTRO_BEACON_PERIOD, INTRO_BEACON_COLOR, BLACK, INTRO_BEACON_CYCLES, sectors=INTRO_BEACON_SECTORS, strip=LED_MAIN)
            internal_state = None
            next_state = 'beacon_full'
    
    elif internal_state and internal_state == 'beacon_full':
        print('INTRO: rozsviceni majaku')
        main = Beacon(INTRO_BEACON_PERIOD, INTRO_BEACON_COLOR, INTRO_BEACON_COLOR, 2, sectors=INTRO_BEACON_SECTORS, strip=LED_MAIN)
        LED_NUMBERS.fill(BLACK)
        internal_state = None
        next_state = 'beacon_clear'

    elif internal_state and internal_state == 'beacon_clear':
        print('INTRO: zhasnuti majaku')
        main = Beacon(INTRO_BEACON_PERIOD, BLACK, BLACK, 1, sectors=INTRO_BEACON_SECTORS, strip=LED_MAIN)
        internal_state = None
        next_state = 'done'

    elif internal_state and internal_state == 'done':
        print('INTRO: konec')
        LED_NUMBERS.fill(BLACK)
        LED_NUMBERS.show()
        LED_MAIN.fill(BLACK)
        LED_MAIN.show()
        # vychozi nastaveni skore hracu (vsichni 0)
        context['score'] = {i: 0 for i in range(PLAYERS)}
        return states.NEW_ROUND
    
    LED_NUMBERS.show()
    LED_MAIN.show()