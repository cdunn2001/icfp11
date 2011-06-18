#!/usr/bin/python
import sys

def opp():
    sys.stdout.flush()
    try:
        raw_input()
        raw_input()
        raw_input()
    except:
        sys.stderr.write("No more input. Quitting\n")
        sys.exit(0)

def move(rl, card, slot):
    print rl
    print card
    print slot
    opp()

def main():
    if sys.argv[0] == "1":
        opp()
    while True:
        move(2, 0, "zero")
        for i in range(256):
            move(2, 1, "zero")
            move(1, "get", 1)
            move(1, "dec", 1)
            move(1, "succ", 0)
        move(2, 0, "zero")

main()
