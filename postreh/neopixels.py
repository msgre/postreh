"""
Ovladani NeoPixel prouzku.
"""

import array
import rp2

from machine import Pin


@rp2.asm_pio(
    sideset_init=rp2.PIO.OUT_LOW,
    out_shiftdir=rp2.PIO.SHIFT_LEFT,
    autopull=True,
    pull_thresh=24,
)
def ws2812():
    """
    PIO rutina pro ovladani Neopixelu (WS2812).
    Copy/paste z https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf,
    kapitola 3.9.2

    Poznamka: jedna PIO rutina muze byt pouzita ve vice StateMachines
    (napr. pro ovladani vice prouzku v jednom projektu).
    """
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1).side(0)[T3 - 1]
    jmp(not_x, "do_zero").side(1)[T1 - 1]
    jmp("bitloop").side(1)[T2 - 1]
    label("do_zero")
    nop().side(0)[T2 - 1]
    wrap()


class NeopixelStrip:
    """
    Pomocna trida ovladajici prouzek Neopixelu.

    Index LED diod se pocita od 0, barvy se zadavaji v RGB prostoru
    jako tuple (R, G, B).

    Pouziti:
        # prouzek 20ti diod ovladany pres GPIO5, stavova masina ID=0
        LED_NUMBERS = NeopixelStrip(5, 20, 0)

        # zhasni vsecky diody
        LED_NUMBERS.fill((0, 0, 0))

        # jedenactou diodu rozsvit cervene
        LED_NUMBERS.set(10, (255, 0, 0))

        # teprem ted se to ukaze
        LED_NUMBERS.show()

    """

    def __init__(self, gpio, count, sm_id, brightness=0.2):
        """
        Parametry:
            gpio
                GPIO cislo pinu, pres ktery se Neopixely budou ovladat
            count
                pocet diod v prouzku
            sm_id
                ID stavove masiny; BACHA! pokud se v projektu vyskytne vice prouzku,
                kazdy musi mit sve vlastni ID
            brightness
                jas diod
        """
        self.count = count
        self.brightness = brightness
        self.sm = rp2.StateMachine(
            sm_id, ws2812, freq=8_000_000, sideset_base=Pin(gpio)
        )
        self.sm.active(1)
        self.array = array.array("I", [0 for _ in range(count)])

    def set(self, i, color):
        """
        Nastavi pixel na pozici "i" na barvu "color".
        """
        self.array[i] = (color[1] << 16) + (color[0] << 8) + color[2]

    def get(self, i):
        """
        Vrati RGB barvu ktera je nastavena na pozici "i".
        """
        c1 = self.array[i] >> 16
        c0 = (self.array[i] >> 8) & 255
        c2 = self.array[i] & 255
        return (c0, c1, c2)

    def fill(self, color):
        """
        Nastavi cely prouzek na barvu "color".
        """
        val = (color[1] << 16) + (color[0] << 8) + color[2]
        for i in range(self.count):
            self.array[i] = val

    def show(self):
        """
        Posle obsah internniho bufferu do Neopixelu, tj. teprve po zavolani
        teto metody se prouzek skutecne rozsviti.
        """
        dimmer_ar = array.array("I", [0 for _ in range(self.count)])
        for i, c in enumerate(self.array):
            r = int(((c >> 8) & 0xFF) * self.brightness)
            g = int(((c >> 16) & 0xFF) * self.brightness)
            b = int((c & 0xFF) * self.brightness)
            dimmer_ar[i] = (g << 16) + (r << 8) + b
        self.sm.put(dimmer_ar, 8)

    def set_brightness(self, value):
        """
        Aktualizuje hodnotu jasu prouzku.
        """
        self.brightness = value

    def get_brightness(self):
        """
        Vrati aktualni hodnotu jasu prouzku.
        """
        return self.brightness
