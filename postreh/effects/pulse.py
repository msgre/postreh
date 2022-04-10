"""
Efekt pulzovani, vyuzitelny jak pro hlavni svetlo tak i cisla se skore.

Asi nejuniverzalnejsi efekt ve sbirce. Da se pouzit na:

* pulzovani svetla (definovany pocet prechod mezi dvema barvama)
* plynule roznuti svetla z cerne do libovolne barvy
* plynule zhasnuti svetla z libovolne barvy do cerne
* plynuly prechod mezi dvema barvami

Poznamka: Efekt je kreativne vyuzity ve win/fail stavu, kde namisto obvyklejsi
fill metody se vyuziva lambda funkce pro zablikani pouze jedne diody na skore.
"""

from postreh.colors import rgb_to_hsv, hsv_to_rgb


class Pulse:
    """
    Priklad pouziti:

        LED_MAIN.fill(BLACK)
        LED_MAIN.show()

        pulse = Pulse(26, BLACK, RED, 1, fadein=True, led_fn=LED_MAIN.fill)
        while True:
            if pulse.cycle():
                break
            LED_MAIN.show()
            utime.sleep_ms(10)
        del pulse
    """

    def __init__(
        self, period, color1, color2, cycles, fadeout=False, fadein=False, led_fill=None
    ):
        """
        Parametry
            period
                Pocet ticku, ktere musi probehnout aby se delo neco dalsiho
                (ticky se meni docela rychle a nekdy je potreba reagovat pomaleji).
            color1
                Z jake barvy bude efekt zacinat
            color2
                Do jake barvy ma efekt dojit
            cycles
                Parametr cycles definuje pocet cyklu, po jejichz uplynuti
                metoda .cycle() vrati True (tedy priznak, ze uz je hotovo).
                Jeden cyklus je to same jako uplynuti "period" ticku.
            fadeout/fadein
                Nepovinne priznaky. Pokud je NEKTERY (ne oba najednou) z nich
                nastaven, pak ke zmene barev mezi color1 a color2 dojde pouze
                aktualizaci hodnoty V (v HSV modelu), coz znamena prechod z/do
                plne barvy z/do cerne.
                Naopak, pokud ani jeden z techto flagu nastaven neni, pak je
                pro color1/color2 vypocitana trirozmerna delta a barva meni
                plynule parametry ve vsech rozmerech (tedy hue i saturation).
            led_fill
                Metoda na vyliti barvy do vsech diod v pasku
        """
        self.period = period
        self.color1 = rgb_to_hsv(*color1)
        self.color2 = rgb_to_hsv(*color2)
        if fadein:
            self.color = (self.color2[0], self.color2[1], 0)
        else:
            self.color = self.color1
        self.cycles = cycles
        if fadeout or fadein:
            self.step = (0, 0, (self.color2[2] - self.color1[2]) / period)
        else:
            self.step = (
                (self.color2[0] - self.color1[0]) / period,
                (self.color2[1] - self.color1[1]) / period,
                (self.color2[2] - self.color1[2]) / period,
            )
        self.actual_cycle = 0
        self.tick = 0
        self.fill_led = led_fill

    def cycle(self):
        # vykresleni barvy
        self.fill_led(hsv_to_rgb(*self.color))

        if self.actual_cycle >= self.cycles:
            return True

        # vypocet nove barvy
        self.color = self.get_new_color()

        self.tick += 1
        if self.tick < self.period:
            return False

        # otoceni prirustku barev na konci jednoho cyklu
        self.step = (-self.step[0], -self.step[1], -self.step[2])

        self.tick = 0
        self.actual_cycle += 1

        return False

    def get_new_color(self):
        """
        Vypocita novou barvu (stara + prirustek).
        """
        return (
            self.color[0] + self.step[0],
            self.color[1] + self.step[1],
            self.color[2] + self.step[2],
        )

    def debug(self):
        print("period: {}".format(self.period))
        print("color1: {}".format(self.color1))
        print("color2: {}".format(self.color2))
        print("color: {}".format(self.color))
        print("cycles: {}".format(self.cycles))
        print("step: {}".format(self.step))
        print("actual_cycle: {}".format(self.actual_cycle))
        print("tick: {}".format(self.tick))
