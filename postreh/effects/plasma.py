"""
Efekt plasmy pro hlavni svetlo.

Lampa uprostred stolu se rozzari vsema barvama, ktere se organicky
prelivaji jedna pres druhou.

Vykradeny plasma efekt znamy z demoscen: https://lodev.org/cgtutor/plasma.html
"""

import math
from postreh.colors import hsv_to_rgb
from postreh.config import LED_MAIN_COLUMNS, LED_MAIN_HEIGHT


class Plasma:
    """
    Priklad pouziti:

        LED_MAIN.fill(BLACK)
        LED_MAIN.show()

        plasma = Plasma(1, 10, LED_MAIN)
        while True:
            if plasma.cycle():
                break
            LED_MAIN.show()
            utime.sleep_ms(1)
        del plasma
    """

    def __init__(self, period, cycles, strip, fadeout=None):
        """
        Parametry
            period
                Pocet ticku, ktere musi probehnout aby se delo neco dalsiho
                (ticky se meni docela rychle a nekdy je potreba reagovat pomaleji).
            cycles
                Parametr cycles definuje pocet cyklu, po jejichz uplynuti
                metoda .cycle() vrati True (tedy priznak, ze uz je hotovo).
                Jeden cyklus je definovan jako LED_MAIN_COLUMNS*LED_MAIN_HEIGHT
                zmen period (ono to je ale jedno, proste to je nejaka doba, stejne
                je treba to dycky odzkouset)
            strip
                Instance NeopixelStrip (pres ni se LED ovladaji).
            fadeout
                Nepovinny priznak, s jehoz pomoci je mozne zapnout alternativni
                mod plazmy. Typicky se pouziva v ramci .prepare_fadeout metody
                kdy se plazme rekne at se zacne ztmavovat az do uplneho vypnuti.
                Hodnota je ve stejnych jednotkach jako cycles.

        Poznamka: pote co efekt skonci, je treba na prouzku nastavit zpet
        puvodni hodnotu brightness, docasne ulozenou v self.brightness.
        """
        self.period = period
        self.cycles = cycles
        self.fadeout = fadeout
        if fadeout is not None:
            self.prepare_fadeout(fadeout)
        self.actual_cycle = 0
        self.tick = 0
        self.shift = 0
        self.strip = strip
        self.brightness = None
        self.fadeout_delta = None

    def prepare_fadeout(self, fadeout):
        """
        Prepne efekt to ztmavovaciho rezimu, ktery bude probihat `fadeout` cyklu.

        Poznamka: narozdil od efektu Fadeout se tady pohasinani resi na urovni
        LED prouzku, ve kterem pomalu menime parametr brightness na nulu.
        """
        self.fadeout = True
        self.cycles = fadeout
        self.actual_cycle = 0
        self.brightness = self.strip.get_brightness()
        self.fadeout_delta = self.brightness / (
            fadeout * LED_MAIN_COLUMNS * LED_MAIN_HEIGHT
        )
        self.tick = 0

    def cycle(self):
        if self.actual_cycle >= self.cycles:
            return True

        self.tick += 1
        if self.tick < self.period:
            return False

        # nastavi barvy na "zarovce" podle predem vypocitaneho patternu, barev
        # a aktualni hodnoty posunu po barvach `shift` (tohle dela animaci)
        for idx, item in enumerate(PATTERN):
            color = PALLETTE[(item + self.shift) % 256]
            self.strip.set(idx, color)

        # fadeout rezim
        if self.fadeout is not None:
            if self.brightness <= 0:
                self.brightness = 0
            else:
                self.brightness -= self.fadeout_delta
            self.strip.set_brightness(self.brightness)

        self.shift += 1
        if (self.shift % (LED_MAIN_COLUMNS * LED_MAIN_HEIGHT)) == 0:
            self.actual_cycle += 1
        self.tick = 0

        return False

    def debug(self):
        print("period: {}".format(self.period))
        print("cycles: {}".format(self.cycles))
        print("fadeout: {}".format(self.fadeout))
        print("actual_cycle: {}".format(self.actual_cycle))
        print("tick: {}".format(self.tick))
        print("shift: {}".format(self.shift))
        print("brightness: {}".format(self.brightness))
        print("fadeout_delta: {}".format(self.fadeout_delta))


def get_plasma_value(x, y, w, h):
    """
    Pomocna fce pro vypocet plasma patternu.

    Proste bordel nekolika goniometrickych funkci do sebe, ktere ve vysledku
    vygeneruji neco co vypada nahodne, ale zaroven je to dostatecne spojite,
    takze barevne zmeny vypadaji hladce.
    """
    v = (
        128
        + (127 * math.sin(2 * 3.14 * x / 16))
        + 128
        + (127 * math.sin(8 * 3.14 * y / 7))
        + 128
        + (127 * math.sin(math.sqrt(x * x + y * y)))
    )

    return int(round(v / 3))


def generate_pattern():
    """
    Vygeneruje plasma pattern na plochu LED_MAIN_COLUMNS x LED_MAIN_HEIGHT.

    Jednotlive hodnoty jsou cisla v rozsahu 0-255. Predstav si to jako moare
    nekolika kruhu do sebe v odstinech sedi.

    Pattern je predem vypocitany a v prubehu animace se nemeni. Plasma animace se
    pak provadi trikem -- namisto narocne zmeny patternu dochazi k pomalemu posunu
    po predem vypocitane tabulce s barvama (hodnoty v patternu udavaji pozici
    v color tabulce, a ta se pomalinku meni).
    """
    out = []
    for x in range(LED_MAIN_COLUMNS):
        for y in range(LED_MAIN_HEIGHT):
            v = int(round(get_plasma_value(x, y, LED_MAIN_HEIGHT, LED_MAIN_COLUMNS)))
            out.append(v)
    return out


def generate_pallette():
    """
    Vygeneruje seznam 256 barev, ktere budou "putovat" po plasma patternu.

    Zadna veda, pouzivame HSV model, s maximalne vysaturovanyma barvama,
    cele dostupne spektrum.
    """
    out = []
    for i in range(256):
        h = 65535 * i / 256
        out.append(hsv_to_rgb(h, 255, 255))
    return out


# predem vypocitane struktury, podle kterych se generuje plasma animace
PALLETTE = generate_pallette()
PATTERN = generate_pattern()
