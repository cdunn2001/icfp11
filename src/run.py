#!/usr/bin/python
import sys

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
    engine = Engine(sys.argv[0])
    if sys.argv[0] == "1":
        func, arg = opp()
        engine.notify(func, arg)
    while True:
        func, arg = engine.next()
        move(func, arg)
        func, arg = opp()
        engine.notify(func, arg)

main()
