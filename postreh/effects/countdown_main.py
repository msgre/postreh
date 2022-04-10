import utime

from postreh.effects.countdown import Countdown
from postreh.hw import LED_NUMBERS
from postreh.colors import WHITE, BLACK


        
f = Countdown(50, 4, 9, WHITE, 50, led_fn=LED_NUMBERS.set)
LED_NUMBERS.fill(WHITE)
LED_NUMBERS.show()

while True:
    if f.cycle():
        break
    LED_NUMBERS.show()
    utime.sleep_ms(3)
    
LED_NUMBERS.fill(BLACK)
LED_NUMBERS.show()
utime.sleep_ms(2000)