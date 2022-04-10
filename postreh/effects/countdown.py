"""
Odpocet skore, efekt pro prouzek zobrazujici skore hracu.

U kazdeho hrace je ukazatel skore, podsvicene cislice 1-9.
Technicky 9 neopixelu, u stolku jsou mista pro 4 hrace,
jednotlive pasky jsou propojene za sebou.

Tento efekt zaridi, ze plne rozsvicene cislice (tj. signalizujici
skore 9) se postupne zhasina: 9, 8, 7, ... 1. Proste odpocet
do zacatku nove hry.
"""

from postreh.colors import rgb_to_hsv, hsv_to_rgb, BLACK
from postreh.config import PLAYERS, SCORES_PER_PLAYER


class Countdown:
    """
    Priklad pouziti:

        LED_NUMBERS.fill(WHITE)
        LED_NUMBERS.show()

        countdown = Countdown(50, WHITE, 100, LED_NUMBERS.set)
        while True:
            if countdown.cycle():
                break
            LED_NUMBERS.show()
            utime.sleep_ms(3)
    """

    def __init__(self, period, color, wait, led_set):
        """
        Parametry
            period
                Pocet ticku, ktere musi probehnout aby se delo neco dalsiho
                (ticky se meni docela rychle a nekdy je potreba reagovat pomaleji).
            color
                Barva ze ktere probiha ztmaveni.
            wait
                Jakmile cislo v poradi ztmavne, nastane chvile pauza,
                behem ktere se nic nedeje (jakoze: ztmavne cislo 9, pauza,
                ztmavne cislo 8, pauza, ...)
            strip
                Reference na metodu pro nastaveni barvy pixelu v prouzku
                (typicky NeopixelStrip.set)
        """
        self.period = period
        self.color = rgb_to_hsv(*color)
        self.actual_color = self.color[:]
        self.delta_v = -self.color[2] / period
        self.wait = wait
        self.actual_wait = wait
        self.tick = 0
        self.number = SCORES_PER_PLAYER - 1
        self.led_set = led_set

    def cycle(self):
        # pauza
        if self.actual_wait > 0:
            self.actual_wait -= 1
            return False

        # pohasinani cisla
        for i in range(PLAYERS):
            idx = i * SCORES_PER_PLAYER + self.number
            self.led_set(idx, hsv_to_rgb(*self.actual_color))

        # vypocet barvy do dalsiho cyklu
        self.actual_color = self.get_new_color()

        self.tick += 1
        if self.tick < self.period:
            return False

        # cislo zhaslo, pro zichr jej jeste prepisem cernou barvou
        for i in range(PLAYERS):
            idx = i * SCORES_PER_PLAYER + self.number
            self.led_set(idx, BLACK)

        # posun na dalsi cislo, reset promennych
        self.actual_wait = self.wait
        self.number -= 1
        if self.number == -1:
            return True
        self.tick = 0
        self.actual_color = self.color[:]

        return False

    def get_new_color(self):
        """
        Vypocita novou barvu diody kterou utlumujeme.
        Protoze jsme si barvu interne ulozili v HSV modelu, menime pouze
        jeji V hodnotu (0=cerna).
        """
        return (
            self.actual_color[0],
            self.actual_color[1],
            self.actual_color[2] + self.delta_v,
        )

    def debug(self):
        print("period: {}".format(self.period))
        print("color: {}".format(self.color))
        print("actual_color: {}".format(self.actual_color))
        print("delta_v: {}".format(self.delta_v))
        print("wait: {}".format(self.wait))
        print("actual_wait: {}".format(self.actual_wait))
        print("tick: {}".format(self.tick))
        print("number: {}".format(self.number))
