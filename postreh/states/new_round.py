"""
Hra zacala. Vygeneruje dobu, za jakou se rozsviti hlavni svetlo.
"""

import random

from postreh import states
from postreh.config import NEW_ROUND_RANDOM_BASE, NEW_ROUND_RANDOM_MAX, NEW_ROUND_RANDOM_MIN


def process(tick, context):    
    round_timeout = random.randrange(NEW_ROUND_RANDOM_MIN, NEW_ROUND_RANDOM_MAX) * NEW_ROUND_RANDOM_BASE  # TODO: do konstant
    context['round_timeout'] = round_timeout
    print('NEW_ROUND: svetlo se rozsviti za {} cyklu'.format(round_timeout))
    return states.KEYS