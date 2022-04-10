from . import fail
from . import game_over
from . import intro
from . import keys
from . import new_round
from . import sunset
from . import win

# stavy hry
INTRO = 1
NEW_ROUND = 2
KEYS = 3
WIN = 4
SUNSET = 5
GAME_OVER = 6
FAIL = 7

# mapovani stavu hry na konkretni modul, ktery se o jeho obsluhu stara
STATES = {
    INTRO: intro,
    NEW_ROUND: new_round,
    KEYS: keys,
    WIN: win,
    SUNSET: sunset,
    GAME_OVER: game_over,
    FAIL: fail,
}
