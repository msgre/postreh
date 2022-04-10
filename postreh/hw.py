"""
Inicializace hardware.
"""

from machine import Pin

from postreh.config import LED_MAIN_PIN, LED_MAIN_COUNT, LED_NUMBERS_PIN, LED_NUMBERS_COUNT, LED_MAIN_BRIGHTNESS, LED_NUMBERS_BRIGHTNESS, BUTTON_CONFIG, PLAYER1_PIN, PLAYER2_PIN, PLAYER3_PIN, PLAYER4_PIN, PROBE_ENABLED, PROBE_PIN
from postreh.neopixels import NeopixelStrip


# tlacitka hracu
BUTTON1 = Pin(PLAYER1_PIN, Pin.IN, Pin.PULL_DOWN)
BUTTON2 = Pin(PLAYER2_PIN, Pin.IN, Pin.PULL_DOWN)
BUTTON3 = Pin(PLAYER3_PIN, Pin.IN, Pin.PULL_DOWN)
BUTTON4 = Pin(PLAYER4_PIN, Pin.IN, Pin.PULL_DOWN)

# Neopixel prouzky

# hlavni svetlo uprostred stolu
LED_MAIN = NeopixelStrip(LED_MAIN_PIN, LED_MAIN_COUNT, 0, brightness=LED_MAIN_BRIGHTNESS)
# cisla se skorem u hracu
LED_NUMBERS = NeopixelStrip(LED_NUMBERS_PIN, LED_NUMBERS_COUNT, 1, brightness=LED_NUMBERS_BRIGHTNESS)

# probe
# vystupni pin, na kterem se generuje signal z hlavni smycky hry
# pri kazde zmene ticku se invertuje
# slouzi pro zmereni realne doby ticku na osciloskopu
if PROBE_ENABLED:
    PROBE = Pin(PROBE_PIN, Pin.OUT)
else:
    PROBE = None


def get_player_button():
    """
    Vrati ID hrace (0-3), ktery zmackl tlacitko a -1 v pripade ze neni zmackleho nic.

    S pomoci konfiguracniho slovniku BUTTON_CONFIG je mozne ovlivnit,
    co se povazuje za stisknuti tlacitka:
    
    * hodnota 1 je pro klasicke tlacitka, kdy je po stisku tlacitka na pin
      pripojena logicka 1
    * hodnota 0 je pro pripady, kdy je pouzito rozpojovaci tlacitko; tj. na pinu
      je trvale logicka 1 a pri stisku se tam objevi logicka 0

    Timto zpusobem muzeme vyuzit i rozpojovaci tlacitka uvnitr krabic: pouzivame
    nejake prumyslove tlacitka, kde v krabici je dvojice switchu. Jeden klasicky,
    druhy rozpojovaci. Pouzivame jen klasicky, ale tlacitka se casem opotrebovavaji
    a kupujem fungl nove kusy. Ted ale bude stacit zmenit konfiguraci a budem
    moci vyuzivat i ty rozpinaci.
    """
    if BUTTON1.value() == BUTTON_CONFIG[0]:
        return 0
    if BUTTON2.value() == BUTTON_CONFIG[1]:
        return 1
    if BUTTON3.value() == BUTTON_CONFIG[2]:
        return 2
    if BUTTON4.value() == BUTTON_CONFIG[3]:
        return 3

    return -1