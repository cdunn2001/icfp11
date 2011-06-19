#!/usr/bin/env python

from game.sim import Simulator
from game.evaluator import evaluate
from subprocess import Popen, PIPE
import sys, os

LTG_INTERVAL = int(os.getenv("LTG_INTERVAL", "1"))
print LTG_INTERVAL

def turn(sim, p0, p1, n):
    lr0 = p0.stdout.readline()[:-1]
    func0 = p0.stdout.readline()[:-1]
    arg0 = p0.stdout.readline()[:-1]
    move = "%s\n%s\n%s\n" %(lr0,func0,arg0)
    #print "move0:", repr(move)
    sim.move(int(lr0), func0, arg0)
    p1.stdin.write(move)
    p1.stdin.flush() # Does this matter?
    lr1 = p1.stdout.readline()[:-1]
    func1 = p1.stdout.readline()[:-1]
    arg1 = p1.stdout.readline()[:-1]
    move = "%s\n%s\n%s\n" %(lr1,func1,arg1)
    #print "move1:", repr(move)
    sim.move(int(lr1), func1, arg1)
    p0.stdin.write(move)
    p0.stdin.flush() # Does this matter?
    if not n%LTG_INTERVAL:
        print "#%05d: (%s %s %s)(%s %s %s) => %d" %(
            n, lr0, func0, arg0, lr1, func1, arg1, evaluate(sim, 0))

def match(e0, e1):
    p0 = Popen([e0, '0'], stdin=PIPE, stdout=PIPE, bufsize=1)
    p1 = Popen([e1, '1'], stdin=PIPE, stdout=PIPE, bufsize=1)
    sim = Simulator()
    try:
        for n in range(100000):
            turn(sim, p0, p1, n)
    finally:
        # Avoid hanging program from broken pipes.
        p0.kill()
        p1.kill()
        

def main(prog, *args):
    if args[0] == 'match':
        match(*args[1:])

main(*sys.argv)

