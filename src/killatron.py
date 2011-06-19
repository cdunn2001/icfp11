#!/usr/bin/python
import sys
from game.compose import *

def opp():
    sys.stdout.flush()
    try:
        raw_input()
        raw_input()
        raw_input()
    except:
        sys.stderr.write("No more input. Quitting\n");
        sys.exit(0);

def turn(left, right):
    print "1" if isinstance(left, str) else "2"
    print left
    print right
    opp()

def turns(apps):
    for app in apps:
        turn(*app)
        opp()

# Ocaml:
#   let S f g x = (f x) (g x)
#   let K x y = x

#   let A _ = B x
#   let A = S (K B) (K x)

#   let A _ = B x y
#   let A = S (S (K B) (K x)) (K y)

#   let A _ = B x y z
#   let A = S (S (S (K B) (K x)) (K y)) (K z)

#   let A _ = B (C x)
#   let A = S (K B) (S (K C) (K x))

# Goal:
#   let attack _ = attack 1 (get 0) (get 3)
#   let help _ = help 2 1 (get 3)

# Expanded:
#   let A = S (S (S (K attack) (K 1)) (S (K get) (K 0))) (S (K get) (K 3))
#   let H = S (S (S (K help) (K 2)) (K 1)) (S (K get) (K 3))


# I -> zero
# zero <- succ
# 1 <- succ
# 2 <- succ
# 3 <- K
# (K 3)

# Given: X
# Goal: X 3
# Back: X (succ (succ (succ zero)))

# X <- K
# K X <- S
# S (K X) 

# Heal wheel:

# a=10000, b=10000 : a -= 10000, b += 11000
# a=0,     b=21000 : b -= 10000, a += 11000
# a=11000, b=11000 : repeat

# I -> zero
# zero <- get
# A -> I
# <fun> -> I


def main():
    if sys.argv[0] == "1":
        opp()
    turns(n2s(0, 0))
    turns(n2s(3, 65535))
    turns(t2s(4, ((S, ((S, ((S, (K, attack)), (K, 1))), ((S, (K, get)), (K, 0)))), ((S, (K, get)), (K, 3)))))
    turns(t2s(5, ((S, ((S, ((S, (K, help)), (K, 2))), (K, 1))), ((S, (K, get)), (K, 3)))))
 
    while True:
        for i in range(256):
            turns(n2s(6, 4))
            turn("get", 6)
            turn("get", 6)
            turn(6, I)

main();
