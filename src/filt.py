#!/usr/bin/env python
from cStringIO import StringIO
import sys, re

def SplitTurn(s):
    """Return text for the turn, or the final result text."""
    s.next() # Skip header.
    text = ""
    for line in s:
        if line.startswith('###'):
            yield text # This is a turn.
            text = ""
        text += line
    yield text # This will be the game result, plus last turn.

re_player_turn = re.compile(r'\*\*\* player (\d)')
prev_slots = [set(), set()]

def Filter(s, text):
    """
    Skip anything we do not want to see.
    For now, we neglect to show reversion to I.
    """
    global prev_slots
    ply = 0
    slots = [set(), set()]
    for line in StringIO(text):
        if '?' in line or 'omit' in line:
            continue
        mo = re_player_turn.search(line)
        if mo: ply = int(mo.group(1))
        if '=' in line:
            slots[ply].add(line)
            if line in prev_slots[ply]:
                continue
        s.write(line)
    prev_slots = slots

def Scan(si, so):
    turn = None
    for text in SplitTurn(si):
        Filter(so, text)

def main():
    Scan(sys.stdin, sys.stdout)
main()
