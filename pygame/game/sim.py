# -*- Mode: python; indent-tabs-mode: t; -*-
# vim: set noexpandtab:
"""
simulator; provides access to game data and tracks movements
"""

import cards

class ActorState:
	"""A state corresponds to one player (or the opponent).
	To look up data in slots, use any of the following:
		state.vits[slot]
		state.fields[slot]
		state.is_alive(slot)
		state.is_auto_applied(slot)
		state.slot_range()
	"""

	slot_range = range(256)

	def __init__(self):
		self.vits = [[None] * 256]
		self.fields = [[0] * 256] # type: int or Python def

	def is_alive(self, slot):
		return (self.vits[slot] > 0)

	def is_auto_applied(self, slot):
		return (self.vits[slot] == -1)

	def slot_range(self):
		return ActorState.slot_range

class Simulator:
	"""To look up a card in this structure, simply refer to
	its name as if it were a data member, e.g. "sim.I" or
	"sim.zero" or "sim.inc".
	
	To read slots, use sim.player() or sim.opponent() and
	then apply any of the idioms documented in ActorState.
	"""

	def __init__(self, **cards):
		"""Every card named in the spec should be defined,
		associating the case-sensitive name from the spec with
		a value or function as appropriate.
		
		Cards directly become member variables of the same
		name, therefore member variables with all of the card
		names from the spec are reserved: "I", "zero", "succ",
		"dbl", "get", "put", "S", "K", "inc", "dec", "attack",
		"help", "copy", "revive", and "zombie".
		"""
		for key in cards:
			self.__dict__[key] = cards[key]
		self._states = [ActorState(), ActorState()]
		self._actor = 0
		self._turn_count = 0
		self._is_auto_app = False

	def _auto_app():
		"""Change the behavior of certain cards, iterate over
		every dead slot of the current player, make field changes
		and then return card behavior to normal.  While changes
		are being applied, is_auto_app() returns True.
		"""
		self._is_auto_app = True
		state = player()
		for slot in state.slot_range():
			slot_field = state.fields[slot]
			if not hasattr(slot_field, '__call__'):
				# errors are NOT raised, they don't affect other auto-applications
				next
			# FIXME: how to count for max. 1000 function applications?
			if state.is_auto_applied(slot):
				slot_field(self.I) # FIXME: result is apparently not used?
				state.fields[slot] = self.I # from spec; overwrite with Identity now
				state.vits[slot] = 0 # from spec; overwrite with 0 now
		self._is_auto_app = False

	def next_turn():
		"""Implicitly changes the current player and current opponent,
		and applies auto-application to all of the new player's data.
		After this returns, you may start instructing the simulator on
		the actions that the player is taking.
		"""
		self._actor = 1 - self._actor
		self._turn_count = self._turn_count + 1
		self._auto_app()

	def is_auto_app():
		"""Return True only if the simulator is currently performing
		auto-application as part of a new player's turn.  According to
		the spec, this means that cards can only receive the Identity
		function as input, and the "inc", "dec", "attack" and "help"
		cards have special behavior as outlined in the spec.
		"""
		return self._is_auto_app

	def player():
		"""Return the ActorState for the current player.  Note that if
		you call next_turn() exactly once, player() will then return
		what was previously returned by opponent().
		"""
		return _states[self._actor]

	def opponent():
		"""Return the ActorState for the current opponent.  Note that
		if you call next_turn() exactly once, opponent() will then
		return what was previously returned by player().
		"""
		return _states[1 - self._actor]
