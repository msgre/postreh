"""
Pomocnici pro praci s barvama.
"""

# nejcastejsi RGB barvy
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 90, 5)
BLUE = (0, 0, 255)


def rgb_to_hsv(r, g, b):
    """
    Prevede RGB na HSV, r/g/b=0..255.
    """

    r, g, b = r / 255, g / 255, b / 255
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / df) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / df) + 120) % 360
    elif mx == b:
        h = (60 * ((r - g) / df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df / mx) * 255
    v = mx * 255
    return int(round(h * 182.04)), int(round(s)), int(round(v))


def hsv_to_rgb(hue, sat, val):
    """
    Prevede HSV na RGB. hue=0..65535, sat=0..255, val=0..255.

    V online kalkulackach je hue ve stupnich, sat/val v procentech. Musi se proto prepocitat:
        hue = 65536/360 * uhel
        sat = 255/100 * sat
        hue = 255/100 * hue

    Reimplementace funkcionality z https://github.com/adafruit/Adafruit_NeoPixel/blob/master/Adafruit_NeoPixel.cpp
    """
    hue = int(round(hue))
    sat = int(round(sat))
    if hue >= 65536:
        hue %= 65536

    hue = (hue * 1530 + 32768) // 65536
    if hue < 510:
        b = 0
        if hue < 255:
            r = 255
            g = hue
        else:
            r = 510 - hue
            g = 255
    elif hue < 1020:
        r = 0
        if hue < 765:
            g = 255
            b = hue - 510
        else:
            g = 1020 - hue
            b = 255
    elif hue < 1530:
        g = 0
        if hue < 1275:
            r = hue - 1020
            b = 255
        else:
            r = 255
            b = 1530 - hue
    else:
        r = 255
        g = 0
        b = 0

    v1 = int(round(1 + val))
    s1 = 1 + sat
    s2 = 255 - sat

    r = ((((r * s1) >> 8) + s2) * v1) >> 8
    g = ((((g * s1) >> 8) + s2) * v1) >> 8
    b = ((((b * s1) >> 8) + s2) * v1) >> 8

    return r, g, b
