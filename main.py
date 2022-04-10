import utime

from postreh.config import MAIN_SLEEP
from postreh.game import Game


game = Game()

while True:
    game.process()
    utime.sleep_us(MAIN_SLEEP)
