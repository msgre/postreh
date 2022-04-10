from postreh.colors import rgb_to_hsv, hsv_to_rgb, BLACK

# TODO: tohle pak vyresim importem s detekci DEBUG 
# - tj. nebudu tim konfigurovat tridu Firefly
def display_led_debug(idx, color):
    print('LED %s set to %s' % (idx, color))


class Countdown:
    """
    TODO:
    """

    def __init__(self, period, strip_count, per_strip_count, color, wait, led_fn=None):
        self.period = period
        self.strip_count = strip_count
        self.per_strip_count = per_strip_count
        self.color = rgb_to_hsv(*color)
        self.actual_color = self.color[:]
        self.delta_v = -self.color[2] / period
        self.wait = wait
        self.actual_wait = wait

        self.tick = 0
        self.number = 9 - 1
        if led_fn and callable(led_fn):
            self.display_led = led_fn
        else:
            self.display_led = display_led_debug

    def cycle(self):
        if self.actual_wait > 0:
            self.actual_wait -= 1
            return False
        
        for i in range(self.strip_count):
            idx = i * self.per_strip_count + self.number
            self.display_led(idx, hsv_to_rgb(*self.actual_color))

        self.actual_color = self.get_new_color()

        self.tick += 1
        if self.tick < self.period:
            return False

        for i in range(self.strip_count):
            idx = i * self.per_strip_count + self.number
            self.display_led(idx, BLACK)
            
        self.actual_wait = self.wait
        self.number -= 1
        if self.number == -1:
            return True
        self.tick = 0
        self.actual_color = self.color[:]
        
        return False

    def get_new_color(self):
        return (self.actual_color[0], self.actual_color[1], self.actual_color[2] + self.delta_v)

    def debug(self):
        print('tick: %s' % self.tick)