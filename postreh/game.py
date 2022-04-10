"""
Hlavni trida starajici se o chod hry.
"""

from postreh.states import STATES, INTRO
from postreh.hw import PROBE


class Game:
    def __init__(self):
        self.tick = 0
        self.context = {'quick_wakeup': False}
        self.state = INTRO
        print('Game: Hra byla inicializovana')

    def process(self):
        fn = self.get_state_fn()
        new_state = fn(self.tick, self.context)
        if new_state:
            self.state = new_state
            self.tick = 0
        else:
            self.tick += 1
        if PROBE:
            PROBE.toggle()

    def get_state_fn(self):
        return STATES[self.state].process