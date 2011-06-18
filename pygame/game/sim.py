# -*- Mode: python; indent-tabs-mode: t; -*-
# vim: set noexpandtab:
"""
simulator; provides access to game data and tracks movements
"""

import cards

class _TooManyFuncs(Exception):
	# flags the "more than 1000 functions" case of auto-app
	pass

class Simulator:
	"""Manages state for both players of the game, and also
	provides behavior for switching turns.
	
	A new Simulator initializes vitalities to 10000 and
	fields to the Identity function, as in the spec.
	
	To run a simulator, call next_turn() repeatedly.  This
	automatically manages auto-application mode, and the
	"player" and "opponent" data members reflect indices
	into the "v" and "f" data structures.
	
	So, s.v[s.player][slot] accesses the specified slot's
	vitality for the current player, and a field can be
	accessed by s.f[s.player][slot].  If the field is a
	function, then hasattr(s.f[s.player][slot], '__call__')
	returns True and the syntax s.f[s.player][slot](args)
	calls the function.  Alternately, "try" an int(...) on
	the field and if that fails treat it as a function.
	
	Card classes are not directly exposed by the simulator,
	although the "cards" module's "I" (Identity) function
	is relied upon for initializations and any field can
	have instances of any card type.  See "pydoc cards".
	
	CARD IMPLEMENTATIONS:
	
	The is_auto_app field is True only if the simulator is
	currently performing auto-application as part of a new
	player's turn.  According to the spec, this means that
	cards can only receive the Identity function as input,
	and the "inc", "dec", "attack" and "help" cards have
	special behavior as outlined in the spec.  This should
	be used in card code to alter behavior automatically.
	While in this mode ONLY, cards should keep track of
	when they apply functions and call the simulator's
	applying_slot() method each time.  When this is used
	more than 1000 times, the simulator stops the current
	slot's auto-application, as stated in the spec.
	"""

	slot_range = range(256)

	def __init__(self):
		"""Every card named in the spec should be defined,
		associating the case-sensitive name from the spec with
		a value or function as appropriate.
		"""
		self.player = 0
		self.opponent = 1
		self.is_auto_app = False
		self.turn_count = 0
		self.auto_appl_count = 0
		self.v = [[10000] * 256, [10000] * 256] # 10000 is spec init. value
		self.f = [[cards.I] * 256, [cards.I] * 256] # Identity is spec init. value

	def _auto_app():
		"""Change the behavior of certain cards, iterate over
		every dead slot of the current player, make field changes
		and then return card behavior to normal.  While changes
		are being applied, the is_auto_app field is True.
		"""
		self.is_auto_app = True
		ai = self.player # actor index
		for slot in Simulator.slot_range:
			self.auto_appl_count = 0
			try:
				slot_field = self.f[ai][slot]
				if not hasattr(slot_field, '__call__'):
					# errors are NOT raised, they don't affect other auto-applications
					next
				if (self.v[ai][slot] == -1):
					# call the card
					self.applying_slot()
					slot_field(cards.I) # FIXME: check...result is apparently not used?
					self.f[ai][slot] = cards.I # from spec; overwrite with Identity now
					self.v[ai][slot] = 0 # from spec; overwrite with 0 now
			except _TooManyFuncs as e:
				# errors are NOT raised, they don't affect other auto-applications
				next
		self.is_auto_app = False

	def applying_slot():
		"""Raise if called more than 1000 times since the last reset.
		This must only be called by card implementations, and only
		when the "is_auto_app" field is True.
		"""
		if self.is_auto_app:
			self.auto_appl_count = self.auto_appl_count + 1
			if (self.auto_appl_count > 1000): # as in spec
				raise _TooManyFuncs()

	def next_turn():
		"""Implicitly changes the current player and current opponent,
		and applies auto-application to all of the new player's data.
		After this returns, you may start instructing the simulator on
		the actions that the player is taking.
		"""
		self.player = 1 - self.player
		self.opponent = 1 - self.opponent
		self.turn_count = self.turn_count + 1
		self._auto_app()

if __name__ == "__main__":
	# basic test...see what's defined
	s = Simulator()
	print s.__dict__