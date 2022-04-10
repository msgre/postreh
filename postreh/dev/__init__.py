"""
TODO:
    - ze tu resim fce, ktere bezi v rpi ale ne v dockeru
    - nebo aspon jinak
"""

from postreh.config import DEBUG

if DEBUG:
    import tty
    import sys
    import termios
    import select


    orig_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)

    BUTTON_TIMEOUT = 0.5


    def get_player_button():
        """
        Precte stav tlacitek v konzoli.

        Bylo to slozitejsi nez jsem si myslel, protoze stdin se normalne cte po radcich,
        tj. ocekava se stisknuti enteru.

        Zkombinoval jsem 2 informace na SO:
        * https://stackoverflow.com/a/34497639
          Tohle umi cist znaky i bez enteru
        * https://stackoverflow.com/a/21429655
          Tohle umi vyhodit timeout pokud se do nejake doby zadne tlacitko nezmackne
        """
        i, o, e = select.select( [sys.stdin], [], [], BUTTON_TIMEOUT)
        if i:
            val = sys.stdin.read(1)[0]
            if val in ('1', '2', '3', '4'):
                return int(val)

        return -1


    def cleanup():
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)


class Logging:    
    def __init__(self, level='info'):
        self.level = level
        
    def debug(self, message, *args):
        if self.level and self.level in ('debug'):
            print('debug: ' + message % args)

    def info(self, message, *args):
        if self.level and self.level in ('debug', 'info'):
            print('info: ' + message % args)

    def warning(self, message, *args):
        if self.level and self.level in ('debug', 'info', 'warning'):
            print('warning: ' + message % args)

    def error(self, message, *args):
        if self.level and self.level in ('debug', 'info', 'warning', 'error'):
            print('error: ' + message % args)

    def fatal(self, message, *args):
        if self.level:
            print('fatal: ' + message % args)


logger = Logging()