"""
Efekt svetluska pro Neopixel prouzek se skore.

Nahodne rozsveci cisla a pak je pomalinku pohasina. Trochu to pripomina
efekt na vanocnich stromcich co byva ve mestech.
"""

import random
from postreh.colors import WHITE, BLACK
from postreh.config import LED_NUMBERS_COUNT


class Firefly:
    """
    Priklad pouziti:

        LED_NUMBERS.fill(BLACK)
        LED_NUMBERS.show()

        firefly = Firefly(200, 2, LED_NUMBERS.set)
        while True:
            if firefly.cycle():
                break
            LED_NUMBERS.show()
            utime.sleep_ms(3)
        del firefly
    """

    def __init__(self, period, flies_per_period, led_set, dimming=True):
        """
        Parametry
            period
                Pocet ticku, ktere musi probehnout aby se delo neco dalsiho
                (ticky se meni docela rychle a nekdy je potreba reagovat pomaleji).
            flies_per_period
                Po uplynuti periody se rodi nove svetlusky. Tenhle parametr
                rika kolik jich bude.
            led_set
                Reference na metodu NeopixelStrip.set.
            dimming
                Nepovinny parametr, kterym je mozne zapnout alternativni rezim
                svetlusek.
                Defaultni hodnota dimming=True zajisti, ze na pasku diod se postupne
                nahodne objevuji svetlusky a pak pomalu hynou. Pasek proste
                poblikava a nic moc se nedeje.
                Pokud se dimming nastavi na hodnotu True, pak nedochazi k uhynu,
                tj. jednou rozsvicena dioda uz zustane svitit naporad. Jakmile
                se rozsviti vsechny diody, vrati metoda .cycle True, tj. priznak
                ze uz sviti vse a efekt skoncil.
        """
        self.period = period
        self.flies_per_period = flies_per_period
        self.dimming = dimming
        self.live_flies = {}
        self.all_flies = list(range(LED_NUMBERS_COUNT))
        self.tick = 0
        self.fadeout_delta = 255 / period
        self.led_set = led_set
        self.first = True
        self.newborn()

    def newborn(self):
        """
        Pomocna metoda, ktera se postara o narozeni novych svetlusek.
        """
        for _ in range(self.flies_per_period):
            if not self.all_flies:
                continue
            idx = random.randint(0, len(self.all_flies) - 1)
            fly = self.all_flies.pop(idx)
            if self.first:
                delay = 0
                self.first = False
            else:
                delay = random.randint(0, self.period - 1)
            self.live_flies[fly] = {
                "delay": delay,
                "count": 0,
            }
        self.tick = 0

    def care(self):
        """
        Hlavni metoda, ktera se stara o svetlusky:

        * kazda nove narozena svetluska ma urceny nahodny cas rozsviceni;
          pokud jeste nenastal jeji cas, casovac se zmensi
        * pokud nastal spravny cas, rozsviti svetlusku
        * pokud u svetlusky dobehl efekt ztmavovani, svetluska je odstranena
          z interniho seznamu

        Tento efekt je v defaultnim rezimu nekonecny. Neni zde zadny pocet cyklu,
        ktery by se hlidal a signalizoval konec. Pro tento rezim vraci metoda False.
        Pokud se ale prepne do rezimu "non-dimming" rezimu, pak narozene svetlusky
        nehynou, zustavaji svitit a metoda vrati True v momente, kdy jsou vsechny
        diody v prouzku rozsvicene.
        """
        to_remove = []
        for fly in self.live_flies:
            if self.live_flies[fly]["delay"] > 0:
                # cekani na narozeni svetlusky
                self.live_flies[fly]["delay"] -= 1
            elif self.live_flies[fly]["delay"] == 0:
                # narozeni svetlusky
                self.led_set(fly, WHITE)
                self.live_flies[fly]["delay"] = -1
            elif self.live_flies[fly]["count"] >= self.period:
                # umreta svetluska
                self.led_set(fly, BLACK)
                self.all_flies.append(fly)
                to_remove.append(fly)
            else:
                # pohasinajici beruska
                if self.dimming:
                    self.live_flies[fly]["count"] += 1
                    c = 255 - int(
                        round(self.fadeout_delta * self.live_flies[fly]["count"])
                    )
                    self.led_set(fly, (c, c, c))

        if not self.all_flies:
            count = len([k for k, v in self.live_flies.items() if v["delay"] == -1])
            if count == LED_NUMBERS_COUNT:
                return True

        # odstraneni umretych svetlusek
        if to_remove:
            for k in to_remove:
                del self.live_flies[k]

        return False

    def cycle(self):
        # obsluha narozenych svetlusek
        if self.care():
            return True

        self.tick += 1
        if self.tick < self.period:
            return False

        # ubehla perioda, cas na narozeni novych svetlusek
        self.newborn()

        return False

    def reconfigure(self, period=None, flies_per_period=None, dimming=None):
        """
        Unikatni metoda pro tento typ efektu. Umoznuje za chodu zmenit dulezite
        parametry, ktere zmeni chovani celeho hejna.

        Vyuziva se pro scenar, kdy se v defaultnim rezimu svetlusky nahodne
        objevuji a hynou, ale pak (po stisku tlacitka) se prepnout do "non-dimming"
        modu a zalijou vsechny diody svetlem.

        Ukazka je k nalezeni v testech.
        """
        if period is not None:
            self.period = period
        if flies_per_period is not None:
            self.flies_per_period = flies_per_period
        if dimming is not None:
            self.dimming = dimming

        if not self.dimming:
            for k in self.live_flies:
                self.live_flies[k] = {"delay": -1, "count": 0}
                self.led_set(k, WHITE)

    def debug(self):
        print("period: {}".format(self.period))
        print("flies_per_period: {}".format(self.flies_per_period))
        print("dimming: {}".format(self.dimming))
        print("live_flies: {}".format(self.live_flies))
        print("all_flies: {}".format(self.all_flies))
        print("tick: {}".format(self.tick))
        print("fadeout_delta: {}".format(self.fadeout_delta))
