"""
Globalni konfigurace hry.
"""

from postreh.colors import BLACK, WHITE, RED, GREEN, ORANGE

# obecne ----------------------------------------------------------------------

PLAYERS = 4
SCORES_PER_PLAYER = 9
MAIN_SLEEP = 1  # us


# konfigurace HW --------------------------------------------------------------

# tlacitka
PLAYER1_GPIO = 6
PLAYER2_GPIO = 7
PLAYER3_GPIO = 8
PLAYER4_GPIO = 9

# konfigurace NeoPixel prouzku v hlavnim svetle uprostred stolu
LED_MAIN_GPIO = 4
# majak je slozeny z LED_MAIN_COLUMNS prouzku, kde kazdy ma
# LED_MAIN_HEIGHT diod; jsou zapojene za sebe, takze se ovladaji
# pres jeden pin jako jeden souvisly pruh
LED_MAIN_COLUMNS = 8
LED_MAIN_HEIGHT = 7
LED_MAIN_COUNT = LED_MAIN_HEIGHT * LED_MAIN_COLUMNS
LED_MAIN_BRIGHTNESS = 1

# konfigurace NeoPixel prouzku zobrazujici skore hracu
LED_NUMBERS_GPIO = 5
LED_NUMBERS_COUNT = SCORES_PER_PLAYER * PLAYERS
LED_NUMBERS_BRIGHTNESS = 1

# konfigurace tlacitek hracu (podrobnosti viz postreh.hw.get_player_button)
BUTTON_CONFIG = {
    0: 1,
    1: 1,
    2: 0,
    3: 0,
}

# probe vystup (signal generovany na vystupnim pinu, v hlavni smycce)
# slouzi pro mereni realne doby jednoho ticku v ruznych stavech krz osciloskop
PROBE_ENABLED = False
PROBE_GPIO = 3


# stavy -----------------------------------------------------------------------

# NEW_ROUND
# jeden cyklus ve stavu KEYS trva 10.24ms
NEW_ROUND_RANDOM_MIN = 1  # ~1 vterina
NEW_ROUND_RANDOM_MAX = 30  # ~30 vterin
NEW_ROUND_RANDOM_BASE = 100

# WIN
# parametry efektu zmeny barvy hlavniho svetla na zelene
WIN_MAIN_PERIOD = 26
WIN_MAIN_COLOR1 = ORANGE
WIN_MAIN_COLOR2 = GREEN
WIN_MAIN_CYCLES = 1

# parametry efektu pri zablikani noveho skore u nejrychlejsiho hrace
WIN_NUMBER_PERIOD = 10
WIN_NUMBER_COLOR1 = BLACK
WIN_NUMBER_COLOR2 = WHITE
WIN_NUMBER_CYCLES = 15

# cekacka po zezelenani hlavniho svetla
WIN_WAIT_SLEEP = 10
WIN_WAIT_SLEEP_LIMIT = 60

# FAIL
# parametry efektu zmeny barvy hlavniho svetla na cervene
FAIL_MAIN_PERIOD = 26
FAIL_MAIN_COLOR1 = RED
FAIL_MAIN_CYCLES = 1

# parametry efektu pri zablikani ztraceneho skore u loosera
FAIL_NUMBER_PERIOD = 10
FAIL_NUMBER_COLOR1 = WHITE
FAIL_NUMBER_COLOR2 = BLACK
FAIL_NUMBER_CYCLES = 15

# cekacka po zcervenani hlavniho svetla
FAIL_WAIT_SLEEP = 10
FAIL_WAIT_SLEEP_LIMIT = 60

# SUNSET
# parametry efektu pri zhasinani hlavniho svetla
SUNSET_MAIN_PERIOD = 1000
SUNSET_MAIN_COLOR1 = ORANGE
SUNSET_MAIN_CYCLES = 1

# parametry efektu pri zhasinani cisel skore
SUNSET_NUMBERS_PERIOD = 2
SUNSET_NUMBERS_CYCLES = 500

# cekacka po zhasnuti
SUNSET_WAIT_SLEEP = 10
SUNSET_WAIT_SLEEP_LIMIT = 60

# KEYS
KEYS_SUNSET_TIMEOUT = 1200
KEYS_SLEEP = 10


# INTRO
# parametry efektu kdyz je hra v idle modu; poblikavani svetlusek
INTRO_CALM_FIREFLY_PERIOD = 100
INTRO_CALM_FIREFLY_PER_PERIOD = 2

# parametry efektu nekdo zmackne tlacitko; probuzeni vsech svetlusek
INTRO_ANGRY_FIREFLY_PERIOD = 4
INTRO_ANGRY_FIREFLY_PER_PERIOD = 1

# cekacka po probuzeni svetlusek
INTRO_WAIT_SLEEP = 10
INTRO_WAIT_SLEEP_LIMIT = 60

# parametry efektu odpoctu cisel skore
INTRO_COUNTDOWN_PERIOD = 20
INTRO_COUNTDOWN_COLOR = WHITE
INTRO_COUNTDOWN_WAIT = 40

# parametry efektu majaku
INTRO_BEACON_PERIOD = 4
INTRO_BEACON_COLOR = ORANGE
INTRO_BEACON_CYCLES = 17
INTRO_BEACON_SECTORS = 1


# GAME_OVER
# parametry efektu plazma koule
GAME_OVER_PLASMA_PERIOD = 1
GAME_OVER_PLASMA_CYCLES = 10
GAME_OVER_PLASMA_FADEOUT = 10

# parametry efektu tmavnuti skore spoluhracu
GAME_OVER_FADEOUT_PERIOD = 2
GAME_OVER_FADEOUT_CYCLES = 160
