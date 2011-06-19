"""
For various static evaluators.

These will always evaluate from the point-of-view of the given player,
which may or not be current.
"""

def simple_evaluate(s, player):
    return sum(s.v[player]) - sum(s.v[1-player])


evaluate = simple_evaluate
