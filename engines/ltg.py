#!/usr/bin/env python

from game.sim import Simulator
from subprocess import Popen, PIPE
import sys, os

def turn(sim, p0, p1, n):
    lr0 = p0.stdout.readline()
    card0 = p0.stdout.readline()
    slot0 = p0.stdout.readline()
    sim.move(int(lr0), card0[:-1], int(slot0))
    p1.stdin.write(lr0+card0+slot0)
    p1.stdin.flush() # Does this matter?
    lr1 = p1.stdout.readline()
    card1 = p1.stdout.readline()
    slot1 = p1.stdout.readline()
    sim.move(int(lr1), card1[:-1], int(slot1))
    p0.stdin.write(lr1+card1+slot1)
    p0.stdin.flush() # Does this matter?
    if not n%200:
        print n, ": ", lr0, card0, slot0, " <-> ", lr1, card1, slot1

def match(e0, e1):
    p0 = Popen([e0, '0'], stdin=PIPE, stdout=PIPE)
    p1 = Popen([e1, '1'], stdin=PIPE, stdout=PIPE)
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

