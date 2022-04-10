from postreh.colors import rgb_to_hsv, hsv_to_rgb


# TODO: tohle pak vyresim importem s detekci DEBUG 
# - tj. nebudu tim konfigurovat tridu Firefly
def fill_led_debug(color):
    print('LEDs set to %s %s %s' % color)


class Pulse:
    """
    TODO:
    """

    def __init__(self, period, color1, color2, cycles, led_fn=None):
        self.period = period
        self.color1 = rgb_to_hsv(*color1)
        self.color2 = rgb_to_hsv(*color2)
        self.color = self.color1
        self.cycles = cycles
        self.step = (self.color2[2] - self.color1[2]) / period
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

        self.step *= -1
        self.tick = 0
        self.actual_cycle += 1

        return False

    def get_new_color(self):
        return (self.color[0], self.color[1], self.color[2] + self.step)

    def debug(self):
        print('tick: %s' % self.tick)
        print('step: %s' % self.step)
        print('color: %s %s %s' % self.color)
        print('actual_cycle: %s' % self.actual_cycle)