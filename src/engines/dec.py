import sys
def dec():
    tup = (yield)
    #print>>sys.stderr, "Got", tup
    while True:
        tup = (yield 0, "zero")
        #print>>sys.stderr, tup, "was gotten1"
        tup = (yield "dec", 0)
        #print>>sys.stderr, tup, "was gotten1"
