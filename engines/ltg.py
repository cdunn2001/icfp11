#!/usr/bin/env python

from game.sim import Simulator
from game.evaluator import evaluate
from subprocess import Popen, PIPE
import sys, os

def turn(sim, p0, p1, n):
    lr0 = p0.stdout.readline()
    func0 = p0.stdout.readline()
    arg0 = p0.stdout.readline()
    #print "%r-%r-%r" %(lr0, func0, arg0)
    sim.move(int(lr0), func0[:-1], arg0[:-1])
    p1.stdin.write(lr0+func0+arg0)
    p1.stdin.flush() # Does this matter?
    lr1 = p1.stdout.readline()
    func1 = p1.stdout.readline()
    arg1 = p1.stdout.readline()
    #print "%r-%r-%r" %(lr1, func1, arg1)
    sim.move(int(lr1), func1[:-1], arg1[:-1])
    p0.stdin.write(lr1+func1+arg1)
    p0.stdin.flush() # Does this matter?
    if not n%1:
        print n, ": ", lr0, func0, arg0, " <-> ", lr1, func1, arg1, " =>", evaluate(sim, 0)

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

