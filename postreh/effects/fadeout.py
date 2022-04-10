from postreh.colors import rgb_to_hsv, hsv_to_rgb, BLACK

# TODO: tohle pak vyresim importem s detekci DEBUG 
# - tj. nebudu tim konfigurovat tridu Firefly
def display_led_debug(idx, color):
    print('LED %s set to %s' % (idx, color))


class Fadeout:
    """
    TODO:
    """

    def __init__(self, period, cycles, strip, winner=None):
        self.period = period
        self.cycles = cycles
        self.strip = strip
        self.tick = 0
        self.delta = 256 / cycles
        self.actual_cycle = 0
        if winner is not None:
            self.min_idx = winner * 9
            self.max_idx = self.min_idx + 8
        else:
            self.min_idx = None
            self.max_idx = None
        self.winner = winner
        self.indices = {}
        self.colors = {}
        self.precalculate()

    def precalculate(self):
        for i in range(self.strip.count):
            if self.max_idx and i >= self.min_idx and i <= self.max_idx:
                continue
            color = rgb_to_hsv(*self.strip.get(i))
            if color not in self.indices:
                self.indices[color] = []
            self.indices[color].append(i)
            self.colors[color] = color

    def cycle(self):
        if self.actual_cycle >= self.cycles:
            return True
        
        self.tick += 1
        if self.tick < self.period:
            return False

        for key, color in self.colors.items():
            v = color[2] - self.delta
            if v < 0:
                v = 0
            self.colors[key] = (color[0], color[1], v)
            new_color = hsv_to_rgb(*self.colors[key])
            for i in self.indices[key]:
                self.strip.set(i, new_color)
                     
        self.actual_cycle += 1
        self.tick = 0
        
        return False

    def debug(self):
        print('tick: %s' % self.tick)
        print('tick: %s' % self.tick)

