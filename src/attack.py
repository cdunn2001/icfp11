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

def main():
    if sys.argv[0] == "1":
        opp()

    turns(n2s(0, 9999))
    turns(n2s(1, 1200))

    for i in range(128):
        j = 255 - i
        turns(t2s(2, (((attack, i*2), j), (get, 0))))
        turns(t2s(2, (((attack, i*2+1), j), (get, 1))))
    while True:
        turn(I, 0)

main();
