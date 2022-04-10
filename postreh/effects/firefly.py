import random
from postreh.colors import WHITE, BLACK


# TODO: tohle pak vyresim importem s detekci DEBUG 
# - tj. nebudu tim konfigurovat tridu Firefly
def display_led_debug(idx, color):
    print('LED %s set to %s' % (idx, color))


class Firefly:
    """
    TODO:
    """

    def __init__(self, count, period, flies_per_period, dimming=True, led_fn=None):
        self.count = count
        self.period = period
        self.flies_per_period = flies_per_period
        self.dimming = dimming
        self.live_flies = {}
        self.all_flies = list(range(count))
        self.tick = 0
        self.fadeout_delta = 255 / period
        if led_fn and callable(led_fn):
            self.display_led = led_fn
        else:
            self.display_led = display_led_debug

    def newborn(self):
        for _ in range(self.flies_per_period):
            if not self.all_flies:
                continue
            idx = random.randint(0, len(self.all_flies) - 1)
            fly = self.all_flies.pop(idx)
            self.live_flies[fly] = {'delay': random.randint(0, self.period - 1), 'count': 0}

        self.tick = 0

    def care(self):
        to_remove = []
        for fly in self.live_flies.keys():
            if self.live_flies[fly]['delay'] > 0:
                # cekani na narozeni svetlusky
                self.live_flies[fly]['delay'] -= 1
            elif self.live_flies[fly]['delay'] == 0:
                # narozeni svetlusky
                self.display_led(fly, WHITE)
                self.live_flies[fly]['delay'] = -1
            elif self.live_flies[fly]['count'] >= self.period:
                # umreta svetluska
                self.display_led(fly, BLACK)
                self.all_flies.append(fly)
                to_remove.append(fly)
            else:
                # pohasinajici beruska
                if self.dimming:
                    self.live_flies[fly]['count'] += 1
                    c = 255 - int(round(self.fadeout_delta * self.live_flies[fly]['count']))
                    self.display_led(fly, (c, c, c))
                    
        if not self.all_flies:
            count = len([k for k, v in self.live_flies.items() if v['delay'] == -1])
            if count == self.count:
                return True

        # odstraneni umretych svetlusek
        if to_remove:
            for k in to_remove:
                del self.live_flies[k]

        return False

    def cycle(self):
        if self.care():
            return True

        self.tick += 1
        if self.tick < self.period:
            return False

        self.newborn()

        return False

    def reconfigure(self, period=None, flies_per_period=None, dimming=None):
        if period is not None:
            self.period = period
        if flies_per_period is not None:
            self.flies_per_period = flies_per_period
        if dimming is not None:
            self.dimming = dimming
        
        if not self.dimming:
            for k, v in self.live_flies.items():
                self.live_flies[k] = {'delay': -1, 'count': 0}
                self.display_led(k, WHITE)

    def debug(self):
        print('tick: %s' % self.tick)
        print('live_flies: %s' % self.live_flies)
        print('all_flies: %s' % self.all_flies)
