#!/usr/bin/python
from engines import killatron as e
import sys, os

def opp():
    try:
        lr = raw_input()
        func = raw_input()
        arg = raw_input()
        if lr == '1':
            return str(func), int(arg)
        else:
            return int(func), str(arg)
    except:
        sys.stderr.write("No more input. Quitting\n")
        sys.exit(0)

def move(func, arg):
    if isinstance(func, str):
        print 1
    else:
        print 2
    print func
    print arg
    sys.stdout.flush()

def main():
    #print>>sys.stderr, "argv:", sys.argv
    engine = e.engine()
    engine.next()
    func, arg = None, None
    if sys.argv[1] == "1":
        func, arg = opp()
    while True:
        #print>>sys.stderr, "Send:", func, arg
        func, arg = engine.send((func,arg))
        #print>>sys.stderr, "Move:", func, arg
        move(func, arg)
        func, arg = opp()

main()
