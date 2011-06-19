import sys
from itertools import chain
from game.compose import *

def engine():
    first_opp = (yield)

    yield(0, "S")
    yield(0, "I")
    yield(0, "I")
    yield(0, "K")
    while True:
        yield ("I", 0)

