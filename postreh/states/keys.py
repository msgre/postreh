"""
KEYS

Dle hodnoty `context['round_timeout']` (vypocitane v predchozi fazi NEW_ROUND)
se ceka na spravny okamzik. Jakmile nastane, rozne se hlavni svetlo a ceka se
na reakci hracu.

Ta muze byt troji:

1) nekdo to nevydrzi s nervama a zmackne tlacitko driv; v tom pripade se presune
   do stavu FAIL
2) hrac s pevnyma nervama a rychlou reakci zmackne tlacitko hned po rozsviceni;
   pak prechazime do stavu WIN
3) nikdo nic nezmackne, pravdepodobne je hra prestala bavit a odesli; pak prejdeme
   do stavu SUNSET

Specialnim pripadem (2) je, ze hrac ziska posledni devaty bod. V tomto pripade
prechazi do stavu GAME_OVER. 

Resi se zde i situace, kdy hrac bez skore zamerne macka tlacitko jeste pred tim
nez se rozsviti svetlo. V tomto pripade je hrac docasne vyrazen a jeho dalsi
stisky tlacitka se neeviduji.
Hry se ovsem muze zucastnit parta makaku, kdy vsichni tlacitka pomackaji jeste
pred roznutim. V tom pripade se seznam diskvalifikovanych hracu resetuje a zas
evidujem vsecky (protoze jinak bychom se dostali do death-locku).
"""

import utime

from postreh import states
from postreh.colors import ORANGE, WHITE
from postreh.hw import LED_MAIN, LED_NUMBERS, get_player_button
from postreh.config import SCORES_PER_PLAYER, KEYS_SUNSET_TIMEOUT, KEYS_SLEEP, PLAYERS


# globalni promenne; jejich hodnota musi prezit do dalsiho cyklu process
timeout_tick = None
disqualified = []


def process(tick, context):
    global timeout_tick
    global disqualified
    
    utime.sleep_ms(KEYS_SLEEP)
        
    if tick == 0:
        # inicializace stavu
        print('KEYS: Cekani na stisk tlacitka')
        # reset hodnot
        timeout_tick = None
        disqualified = []
        return

    elif tick == context['round_timeout']:
        # dopocitali jsme se k roznuti hlavniho svetla
        print('KEYS: Rozinam hlavni svetlo')
        LED_MAIN.fill(ORANGE)
        LED_MAIN.show()
        # limit pro ukonceni hry, pokud nikdo nezareaguje
        timeout_tick = tick + KEYS_SUNSET_TIMEOUT
        return
    
    # zmackl nekdo tlacitko?
    keys_player = get_player_button()
    
    if keys_player >= 0 and keys_player not in disqualified:
        # ano, zmackl...
        context['last_player'] = keys_player
        if tick < context['round_timeout']:
            # ...ale prilis brzy
            print('KEYS: Hrac {} stiskl tlacitko prilis brzy'.format(keys_player))
            if context['score'][keys_player] > 0:
                context['score'][keys_player] -= 1
                return states.FAIL
            
            # mohlo by se stat, ze ti co nemaji ani jeden bod budou hru sabotovat;
            # abychom tomu zamezeli, budem si je pamatovat a jejich pripadne dalsi
            # stisky tlacitka nebudem brat v potaz
            disqualified.append(keys_player)
            if len(disqualified) == PLAYERS:
                disqualified = []
                print('KEYS: Vsichni diskvalifikovani, co je toto za partu? Reset disqualified')
            else:
                print('KEYS: Hrac {} docasne vyrazen ze hry'.format(keys_player))
            return
        else:
            # ...a ve spravnou dobu!
            context['score'][keys_player] += 1
            if context['score'][keys_player] >= SCORES_PER_PLAYER:
                # vida, tohle byl posledni bod, konec hry a vitezstvi
                print('KEYS: Hrac {} vitezi!'.format(keys_player))
                context['winner'] = keys_player
                LED_NUMBERS.set(keys_player * SCORES_PER_PLAYER + SCORES_PER_PLAYER - 1, WHITE)
                LED_NUMBERS.show()
                return states.GAME_OVER
            else:
                # pridani dalsiho bodu ke skore
                print('KEYS: Hrac {} ziskava dalsi bod, celkem ma uz {}'.format(keys_player, context['score'][keys_player]))
                return states.WIN
    
    elif timeout_tick and tick > timeout_tick:
        # nikdo nereaguje
        print('KEYS: Nikdo nereaguje, hraci asi odesli')
        return states.SUNSET