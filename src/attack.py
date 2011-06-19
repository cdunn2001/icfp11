#!/usr/bin/python
import sys
sys.path.append('src')
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
    turns(n2s(2, 8799))

    for i in range(128):
        j = 255 - i
        turns(t2s(129, (((attack, i*2), j), (get, 0))))
        turns(t2s(129, (((attack, i*2+1), j), (get, 1))))

    turn(put, 0)
    turn(put, 1)
    turns(n2s(0, 8799))
    turns(n2s(1, 8799))

    for i in range(64):
        j = 128 - i
        turns(t2s(129, (((attack, i*4+1), j), (get, 0))))
        turns(t2s(129, (((attack, i*4+3), j), (get, 1))))

    #for j in range(30):
    #    for i in range(128):
    #        turns(t2s(129, (((help, i*2+1), i*2), (get, 2))))
    #        turns(t2s(129, (((help, i*2), i*2+1), (get, 2))))
    while True:
        turn(I, 0)

main();
