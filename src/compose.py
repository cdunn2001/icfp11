#!/usr/bin/python
import sys
from game.compose import *

goal = "(((attack, 1), (get, 0)), zero))"
goal = "((S, ((S, (K, (attack, 2))), ((S, (K, get)), (K, 0)))), (K, 0))"

print>>sys.stderr, "S(S(K(attack(2)))(S(K(get))(K(1))))(K(65535))"

print>>sys.stderr, goal
s2g(0, eval(goal))
