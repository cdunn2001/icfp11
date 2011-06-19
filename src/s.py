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

def turn(left, right):
    print "1" if isinstance(left, str) else "2"
    print left
    print right
    opp()

def main():
    if sys.argv[0] == "1":
        opp()
    turn(0, "S")
    turn(0, "I")
    turn(0, "I")
    turn(0, "K")
    while True:
        turn ("I", 0)

main()
