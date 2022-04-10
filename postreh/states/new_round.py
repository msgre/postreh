"""
Hra zacala. Vygeneruje dobu, za jakou se rozsviti hlavni svetlo.
"""

import random

from postreh import states
from postreh.config import (
    NEW_ROUND_RANDOM_BASE,
    NEW_ROUND_RANDOM_MAX,
    NEW_ROUND_RANDOM_MIN,
)


def process(tick, context):
    # prvni dioda ve hre se musi rozsvitit relativne brzo, protoze lidi si jinak
    # mysli ze hra nefunguje
    max_timeout = NEW_ROUND_RANDOM_MAX // 4 if context["first_round"] else NEW_ROUND_RANDOM_MAX
    round_timeout = (
        random.randrange(NEW_ROUND_RANDOM_MIN, max_timeout)
        * NEW_ROUND_RANDOM_BASE
    )
    context["round_timeout"] = round_timeout
    context["first_round"] = False
    print("NEW_ROUND: svetlo se rozsviti za {} cyklu".format(round_timeout))
    return states.KEYS
