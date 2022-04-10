"""
Efekt vyhasinani diod pro ukazatele skore.

Podsvicena cisla zacnou pomalinku hasnout, az nesviti zadne.
Efekt je mozne nakonfigurovat tak, ze pohasinani probehne jen u protihracu
(ne u viteze).
"""


from postreh.colors import rgb_to_hsv, hsv_to_rgb
from postreh.config import SCORES_PER_PLAYER


class Fadeout:
    """
    Priklad pouziti:

        LED_NUMBERS.fill(WHITE)
        LED_NUMBERS.show()

        fadeout = Fadeout(2, 120, LED_NUMBERS)
        while True:
            if fadeout.cycle():
                break
            LED_NUMBERS.show()

    Poznamka: Priklad varianty s vitezem je v testech.
    """

    def __init__(self, period, cycles, strip, winner=None):
        """
        Parametry
            period
                Pocet ticku, ktere musi probehnout aby se delo neco dalsiho
                (ticky se meni docela rychle a nekdy je potreba reagovat pomaleji).
            cycles
                Rika jak rychle bude fadeout probihat. Cim nizsi cislo,
                tim rychleji.
            strip
                Instance NeopixelStrip (pres ni se LED ovladaji).
            winner
                Nepovinny parametr, kterym je mozne zapnout alternativni rezim
                ztmavovani.
                Defaultni hodnota winner=None zajisti, ze dojde ke ztmaveni
                uplne vsech diod v prouzku (vezme se aktualni stav a ztmavuje se).
                Pokud se ale nastavi na hodnotu 0, 1, 2 nebo 3, pak diody
                u hrace 0..3 zustanou nedotcene a ztmaveni probehne jen u vsech
                ostatnich protihracu.
        """
        self.period = period
        self.cycles = cycles
        self.strip = strip
        self.tick = 0
        self.delta = 256 / cycles
        self.actual_cycle = 0
        if winner is not None:
            self.min_idx = winner * SCORES_PER_PLAYER
            self.max_idx = self.min_idx + SCORES_PER_PLAYER - 1
        else:
            self.min_idx = None
            self.max_idx = None
        self.winner = winner
        self.indices = {}
        self.colors = {}
        self.precalculate()

    def precalculate(self):
        """
        Pomocna metoda, ktera projede interni buffer Neopixel prouzku,
        pixel po pixelu zjisti barvu a vytvori si 2 pomocne struktury:

        * self.indices je slovnik, kde klic je HSV barva a hodnota seznam
          pozic, na kterych se barva vyskytuje
        * self.colors je slovnik, kde klic je HSV barva (tedy ten samy
          co v self.indices) a hodnotou je vypocitana barva, kterou efekt
          postupne meni (tmavne)

        Oba atributy jsou nasledne vyuzity v metode .cycle pro efektivnejsi
        vykreslovani diod v pasku.

        Poznamka: pokud jede efekt v rezimu "winner", tak LED diody vitezneho
        hrace jsou zamerne preskoceny; efekt se jim nebude venovat a ony
        zustanou svitit tak jak jsou.
        """
        for i in range(self.strip.count):
            if self.max_idx and self.min_idx <= i <= self.max_idx:
                continue
            color = rgb_to_hsv(*self.strip.get(i))
            if color not in self.indices:
                self.indices[color] = []
            self.indices[color].append(i)
            self.colors[color] = color

    def cycle(self):
        # test na ukonceni efektu
        if self.actual_cycle >= self.cycles:
            return True

        self.tick += 1
        if self.tick < self.period:
            return False

        # prekresleni diod
        for key, color in self.colors.items():
            # vypocteme novou hodnotu V (0=cerna)
            v = max(color[2] - self.delta, 0)
            # ulozime nove vypocitanou barvu do pomocneho slovniku
            self.colors[key] = (color[0], color[1], v)
            # prevedeme barvu z HSV do RGB prostoru
            new_color = hsv_to_rgb(*self.colors[key])
            # postupne u vsech LED kterych se to tyka zmenime barvu na novou
            # tohle je klic k efektivite: drahy prepocet mezi barevnymi prostory
            # se dela jen jednou a jednorazove zmeni jen ty diody, kterych se to tyka
            for i in self.indices[key]:
                self.strip.set(i, new_color)

        self.actual_cycle += 1
        self.tick = 0

        return False

    def debug(self):
        print("period: {}".format(self.period))
        print("cycles: {}".format(self.cycles))
        print("strip: {}".format(self.strip))
        print("tick: {}".format(self.tick))
        print("delta: {}".format(self.delta))
        print("actual_cycle: {}".format(self.actual_cycle))
        print("min_idx: {}".format(self.min_idx))
        print("max_idx: {}".format(self.max_idx))
        print("winner: {}".format(self.winner))
        print("indices: {}".format(self.indices))
        print("colors: {}".format(self.colors))
