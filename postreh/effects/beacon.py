"""
Efekt majaku pro hlavni svetlo.

Uprostred stolu je hlavni svetlo, na ktere hraci reaguji.
Technicky je slozeno z 8 Neopixel prouzku po 7 diodach, zapojenych
za sebou, takze se ovladaji jako jeden dlouhy pruh diod.

Tento efekt postupne zapina a vypina jednotlive pruhy, takze rozsviceny
prouzek jakoby putuje dokola a vytvari tak efekt majaku (jaky kdysi meli
cajti, hasici, sanity).
"""

from postreh.config import LED_MAIN_COLUMNS, LED_MAIN_COUNT, LED_MAIN_HEIGHT


class Beacon:
    """
    Priklad pouziti:

        beacon = Beacon(5, RED, BLACK, 20, 1, LED_MAIN)
        while True:
            if b.cycle():
                break
            LED_MAIN.show()
            utime.sleep_ms(3)
    """

    def __init__(self, period, color1, color2, cycles, sectors, strip):
        """
        Parametry
            period
                Pocet ticku, ktere musi probehnout aby se delo neco dalsiho
                (ticky se meni docela rychle a nekdy je potreba reagovat pomaleji).
            color1
                Barva prouzku, ktery po majaku putuje.
            color2
                Barva kterou se premazava stara pozice prouzku. Typicky cerna.
            cycles
                Jeden cyklus je protoceni prouzku pres vsech 8 sloupcu zarovky.
                Parametr cycles definuje pocet cyklu, po jejichz uplynuti
                metoda .cycle() vrati True (tedy priznak, ze uz je hotovo).
            sectors
                Kolik prouzku se na majaku vykresli, tj. kolik jich behem animace
                bude dokola obihat. Typicky jen jeden, ale je mozne zadat i 2 nebo 4.
                Nevypada to ale moc dobre.
            strip
                Instance NeopixelStrip (pres ni se LED ovladaji).

        Poznamka: s barvama jdou delat triky. Napr. ve hre roztocim majak klasicky,
        tj. color1=RED, color2=BLACK, cycles=20 (roztoci se cerveny prouzek).
        Jakmile ale dobehne roztocim hned po sobe dalsi 2 verze majaku:

        * color1=RED, color2=RED, cycles=2
          Prouzek se neumazava a zustava svitit. Tj. majak se jakoby najednou rozsviti
          (behem prvniho cyklu), a zustane chvili svitit (druhy cyklus).
          Jako kdyby se otevrel kvet.
        * color1=BLACK, color2=BLACK, cycles=1
          Rozsviceny majak se zas zabali, tj. postupne se budou vykreslovat cerne
          pruhy, takze po prvnim cyklu cely zhasne.

        Je to takove prijemnejsi ukonceni celeho efektu, nez jen proste vypnuti
        po prvni fazi.
        """
        self.period = period
        self.color1 = color1
        self.color2 = color2
        self.cycles = cycles
        self.tick = 0
        self.pos = 0
        self.prev_pos = None
        self.actual_cycle = 0
        self.sectors = sectors
        self.sectors_delta = LED_MAIN_COLUMNS // sectors
        self.set_led = strip.set

    def cycle(self):
        # koncime s majakem?
        if self.actual_cycle >= self.cycles:
            return True

        # interni hodiny
        self.tick += 1
        if self.tick < self.period:
            return False

        self.tick = 0

        # smazani predchoziho prouzku
        if self.prev_pos is not None:
            for sector in range(self.sectors):
                self.draw_sector(
                    sector * self.sectors_delta, self.prev_pos, self.color2
                )

        # vykresleni noveho prouzku
        for sector in range(self.sectors):
            self.draw_sector(sector * self.sectors_delta, self.pos, self.color1)

        # posunuti prouzku v majaku
        self.prev_pos = self.pos
        self.pos += 1
        if self.pos > LED_MAIN_COLUMNS - 1:
            self.pos = 0
        if self.pos == 0:
            self.actual_cycle += 1

        return False

    def draw_sector(self, sector, pos, color):
        """
        Vykresli prouzek na majaku.
        """
        base_pos = pos * LED_MAIN_HEIGHT + sector * LED_MAIN_HEIGHT
        for i in range(LED_MAIN_HEIGHT):
            self.set_led((base_pos + i) % LED_MAIN_COUNT, color)

    def debug(self):
        print("period: {}".format(self.period))
        print("color1: {}".format(self.color1))
        print("color2: {}".format(self.color2))
        print("cycles: {}".format(self.cycles))
        print("tick: {}".format(self.tick))
        print("pos: {}".format(self.pos))
        print("prev_pos: {}".format(self.prev_pos))
        print("actual_cycle: {}".format(self.actual_cycle))
        print("sectors: {}".format(self.sectors))
        print("sectors_delta: {}".format(self.sectors_delta))
