#!/usr/bin/env python
# -*- Mode: python; indent-tabs-mode: t; -*-
# vim: set noexpandtab:
import sys
import os.path
import random

# when installed for the final submission, the "run"
# script MUST be top-level and source files will be
# in "src", so set up the search path accordingly
sys.path.insert(0, "./src/engines")

import game.cards as cards
import game.sim as simulator

from game.error import Error

# note: this invokes a simulator entirely through
# commands from memory, it does not perform I/O

if __name__ == "__main__":
	me = 0
	if len(sys.argv) > 1 and sys.argv[1] == '1':
		me = 1
	#stream = None
	stream = sys.stderr
	sim = simulator.Simulator(me, log_stream=stream)
	while 1:
		my_cards = cards.a_cards[sim.player]
		try:
			if sim.player == me:
				# player is active
				# TBD (test smart algorithms here)
				slot = int(random.random() * 256
				sim.apply_left(my_cards["dec"], slot)) # left: apply card (dec) to slot (random)
			else:
				# opponent is active
				# TBD (for now, do predictable moves)
				slot = 0
				sim.apply_left(cards.I, slot) # left: apply card (I) to slot (0)
				#sim.apply_right(cards.I, slot) # right: call whatever field card with card argument (I)
		except Error as e:
			sim.f[sim.player][slot] = cards.I

		sim.next_ply()
		if sim.turn_count > 100000:
			break
