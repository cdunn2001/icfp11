import sys

def engine():
    tup = (yield)
    print>>sys.stderr, "First opp move:", tup
    while True:
        tup = (yield 0, "zero")
        #print>>sys.stderr, tup, "was gotten1"
        tup = (yield "dec", 0)
        #print>>sys.stderr, tup, "was gotten1"
