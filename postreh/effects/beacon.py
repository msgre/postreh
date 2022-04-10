"""
TODO:
    - zoptimalizovat
    - namisto fill premazat puvodni mista cernou
    - bude to rychlejsi
    - on ten fill je stejne hack


    - mam podezreni, ze tam je nejaka bota
    - je to prekvapive pomale na to jak malo to dela...
        - viz nizke cisla period
"""
from postreh.colors import BLACK


class Beacon:
    def __init__(self, period, color1, color2, cycles, strip, sectors=2):
        self.period = period
        self.color1 = color1
        self.color2 = color2
        self.cycles = cycles
        self.tick = 0
        self.pos = 0
        self.prev_pos = None
        self.actual_cycle = 0
        self.sectors = sectors
        self.sectors_delta = 8 // sectors

        self.set_led = strip.set
        self.fill = strip.fill

    def cycle(self):
        # smazani predchoziho prouzku
        if self.prev_pos is not None:
            for sector in range(self.sectors):
                self.draw_sector(sector * self.sectors_delta, self.prev_pos, self.color2)

        # vykresleni noveho prouzku
        for sector in range(self.sectors):
            self.draw_sector(sector * self.sectors_delta, self.pos, self.color1)

        # koncime s majakem?
        if self.actual_cycle >= self.cycles:
            return True

        self.tick += 1
        if self.tick < self.period:
            return False
        self.tick = 0

        self.prev_pos = self.pos
        self.pos += 1
        if self.pos > 7:
            self.pos = 0

        if self.pos == 0:
            self.actual_cycle += 1

        return False

    def draw_sector(self, sector, pos, color):
        """
        sectors=2
        sectors_delta=4
            0
            4
        """
        for i in range(7):
            self.set_led((pos * 7 + sector * 7 + i) % 56, color)

    def debug(self):
        print('period: %s' % self.period)
        print('cycles: %s' % self.cycles)
        print('tick: %s' % self.tick)
        print('pos: %s' % self.pos)
        print('actual_cycle: %s' % self.actual_cycle)
        print('sectors: %s' % self.sectors)
        print('sectors_delta: %s' % self.sectors_delta)