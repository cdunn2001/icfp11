#!/usr/bin/env python
import sys, re

class Move(object):
    def __repr__(me):
        return "%s %s" %(me.func, me.arg)
    def __init__(me, text):
        if not text: return
        #print repr(text)
        re_move = re.compile(r'''
            \*\*\*\ player\ \d's\ turn,\ with\ slots:\n
            (?P<slotsec>(?:\d+=\{[^}]*\}\n)*)
            .*
            player\ (?P<player>\d)\ applied\ \w+\ (?P<func>\S+)\ to\ \w+\ (?P<arg>\S+)\n
          ''', re.X|re.S|re.M)
        match = re_move.search(text)
        #print match.groups()
        #print match.groupdict()
        g = match.groupdict()
        func, arg = g['func'], g['arg']
        slotsec = g['slotsec']
        #print "slots:", slotsec
        re_slots = re.compile(r'''
            \d+=\{[^}]*\}\n
          ''', re.X|re.S|re.M)
        slots = set()
        for exp in re_slots.findall(slotsec):
            re_slot = re.compile(r'(\d)=\{([^,]*),([^}]*)\}')
            #print "exp:", exp
            slots.add(re_slot.search(exp).groups())
        #print "move:", func, arg
        #print "slots:", slots
        me.func = func; me.arg = arg
        me.slots = slots
            


class Turn(object):
    def __repr__(me):
        return "Turn(%d)" %me.turn
    def __init__(me, match):
        me.turn = int(match.group(1))
        me.move = [None]*2
        move0, move1 = match.group(2, 3)
        me.move[0] = Move(move0)
        me.move[1] = Move(move1) if move1 else None

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
def GetTurn(text):
    """Return a Turn obj."""
    re_turn = re.compile(r'turn (\d+).*(player 0 applied i[^\n])\n.*(player 1 applied [^\n])\n', re.DOTALL|re.MULTILINE)
    re_turn = re.compile(r'''
        turn\ (\d+)\n
        (
        \*\*\*\ player\ \d's\ turn,\ with\ slots:\n
        [^\*]*
        player\ \d\ applied\ \w+\ \S+\ to\ \w+\ \S+\n
        )
        (
        \*\*\*\ player\ \d's\ turn,\ with\ slots:\n
        [^\*]*
        player\ \d\ applied\ \w+\ \S+\ to\ \w+\ \S+\n
        )?
      ''', re.X|re.S|re.M)
    return Turn(re_turn.search(text))
def ProcessResult(text):
    """
    >>> '!! draw by 256:256 after turn 100000\n'
    !! draw by 256:256 after turn 100000
    """
    sys.stdout.write(text)
def Report(turn, prev):
    """Report diffs between turns."""
    print "###### turn %d" %turn.turn
    for ply in range(2):
        move = turn.move[ply]
        if not move: continue
        pmove = prev.move[ply]
        print "Changed:", move.slots - pmove.slots
        print "Player %d: %s" %(ply, move)

def Scan(s):
    turn = None
    for text in SplitTurn(s):
        if text.startswith('###'):
            prev = turn
            turn = GetTurn(text)
            if prev:
                Report(turn, prev)
        else:
            ProcessResult(text)
def main():
    Scan(sys.stdin)
main()
