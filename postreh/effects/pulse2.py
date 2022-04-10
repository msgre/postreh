from postreh.colors import rgb_to_hsv, hsv_to_rgb


# TODO: tohle pak vyresim importem s detekci DEBUG 
# - tj. nebudu tim konfigurovat tridu Firefly
def fill_led_debug(color):
    print('LEDs set to %s %s %s' % color)


class Pulse2:
    """
    TODO:
    """

    def __init__(self, period, color1, color2, cycles, fadeout=False, fadein=False, led_fn=None):
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
            self.step = ((self.color2[0] - self.color1[0]) / period, (self.color2[1] - self.color1[1]) / period, (self.color2[2] - self.color1[2]) / period)
        self.actual_cycle = 0
        self.tick = 0
        if led_fn and callable(led_fn):
            self.fill_led = led_fn
        else:
            self.fill_led = fill_led_debug

    def cycle(self):
        self.fill_led(hsv_to_rgb(*self.color))
        if self.actual_cycle >= self.cycles:
            return True

        self.color = self.get_new_color()

        self.tick += 1
        if self.tick < self.period:
            return False

        self.step = (-self.step[0], -self.step[1], -self.step[2])
        self.tick = 0
        self.actual_cycle += 1

        return False

    def get_new_color(self):
        return (self.color[0] + self.step[0], self.color[1] + self.step[1], self.color[2] + self.step[2])

    def debug(self):
        print('tick: %s' % self.tick)
        print('step: %s %s %s' % self.step)
        print('color: %s %s %s' % self.color)
        print('actual_cycle: %s' % self.actual_cycle)
        print('color1: %s %s %s' % self.color1)
        print('color2: %s %s %s' % self.color2)



