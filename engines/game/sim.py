# -*- Mode: python; indent-tabs-mode: t; -*-
# vim: set noexpandtab:
"""
simulator; provides access to game data and tracks movements
"""

from .error import Error
from .cards import a_cards
from . import cards

import sys, traceback

class _TooManyFuncs(Exception):
	# flags the "more than 1000 functions" case of auto-app
	pass

class Simulator(object):
	"""Manages state for both players of the game, and also
	provides behavior for switching turns.
	
	A new Simulator initializes vitalities to 10000 and
	fields to the Identity function, as in the spec.
	
	To run a simulator, call next_ply() repeatedly.  This
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

	def __init__(self, player=None, log_stream=None):
		"""Every card named in the spec should be defined,
		associating the case-sensitive name from the spec with
		a value or function as appropriate.
		"""
		if player is None:
			self.player = 0
		else:
			self.player = player
		self.opponent = 1
		self.is_auto_app = False
		self.turn_count = 0
		self.appl_count = 0
		self.v = [[10000] * 256, [10000] * 256] # 10000 is spec init. value
		self.f = [[cards.I] * 256, [cards.I] * 256] # Identity is spec init. value
		self.log_stream = log_stream

	def _auto_app(self):
		"""Change the behavior of certain cards, iterate over
		every dead slot of the current player, make field changes
		and then return card behavior to normal.  While changes
		are being applied, the is_auto_app field is True; at any
		other time, it is False.
		"""
		self.is_auto_app = True
		ai = self.player # actor index
		for slot in Simulator.slot_range:
			self.appl_count = 0
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

	def applying_slot(self):
		"""Raise if called more than 1000 times since the last reset
		of the appl_count field.
		
		This must be called ANY time a function from a card is applied
		ANYWHERE.  If is_auto_app mode is True, the count will reset
		for every slot; otherwise, it is reset by next_ply().
		"""
		self.appl_count = self.appl_count + 1
		if (self.appl_count > 1000): # as in spec (either regular turns or auto-apps)
			raise _TooManyFuncs()

	def apply_left(self, card, slot):
		"""Invoke the specified function (card), passing in the slot's
		field as an argument.  Raise an error if the slot is dead or
		the card cannot be invoked.
		"""
		ai = self.player # actor index
		try:
			if (self.v[ai][slot] in (0, -1)):
				raise Error("slot %i for apply_left() is dead" %slot)
			elif slot not in Simulator.slot_range:
				raise Error("slot %i for apply_left() is out of range" %slot)
			elif not hasattr(card, '__call__'):
				raise Error("card %r for apply_left() is not a function" %card)
			if self.log_stream is not None:
				print >>self.log_stream, "apply_left", card, slot
			self.applying_slot()
			fs = self.f[ai]
			fs[slot] = card(self, fs[slot]) # may raise and abort assignment (OK, in spec)
		except (Error, TypeError) as e:
			self.f[ai][slot] = cards.I

	def apply_right(self, card, slot):
		"""Invoke the specified function (slot field), passing in the
		given card as an argument.  Raise an error if the slot is dead
		or the slot's field cannot be invoked.
		"""
		ai = self.player # actor index
		try:
			if (self.v[ai][slot] in (0, -1)):
				raise Error("slot %i for apply_right() is dead" %slot)
			elif slot not in Simulator.slot_range:
				raise Error("slot %i for apply_right() is out of range" %slot)
			elif not hasattr(self.f[ai][slot], '__call__'):
				raise Error("slot %i for apply_right() is not a function" %slot)
			if self.log_stream is not None:
				print >>self.log_stream, "apply_right", card, slot
			self.applying_slot()
			fs = self.f[ai]
			if isinstance(fs[slot], int):
				pass #raise Error("
			fs[slot] = fs[slot](self, card) # may raise and abort assignment (OK, in spec)
		except (Error, TypeError) as e:
			print "error, slot:", e, slot
			print traceback.format_exc()
			self.f[ai][slot] = cards.I

	def next_ply(self):
		"""Implicitly changes the current player and current opponent,
		and applies auto-application to all of the new player's data.
		After this returns, you may start instructing the simulator on
		the actions that the player is taking.
		"""
		self.player = 1 - self.player
		self.opponent = 1 - self.opponent
		self.turn_count = self.turn_count + 1
		self._auto_app()
		self.appl_count = 0
		if self.log_stream is not None:
			print >>self.log_stream, "new turn:", self.turn_count

	def move(self, lr, func, arg):
		"""
		If lr==1: func is a card-name, arg is a slot-num.
		If lr==2: func is a slot-num, arg is a card-name.
		"""
		p = self.player; o = 1-p
		#prevp = self.v[p][:]
		#fp = self.f[p][:]
		#prevo = self.v[o][:]
		#op = self.f[o][:]
		try:
			if lr == 1:
				card = a_cards[self.player][func]
				slot = int(arg)
				self.apply_left(card, slot)
			else:
				card = a_cards[self.player][arg]
				slot = int(func)
				self.apply_right(card, slot)
		except:
			# We moved the exception-handler into apply_left/right.
			raise
		#print p, ":", diff(prevp, self.v[p]), diff(fp, self.f[p])
		#print o, ":", diff(prevo, self.v[o]), diff(op, self.f[o])
		self.next_ply()
def fov(v):
	if v in cards.card_names:
		return cards.card_names[v]
	return v
def diff(aold, anew):
	for i in range(len(anew)):
		if aold[i] != anew[i]:
			ao = fov(aold[i])
			an = fov(anew[i])
			return "%i:%r=>%r" %(i, ao, an)
	return "="

if __name__ == "__main__":
	# basic test...see what's defined
	s = Simulator()
	print s.__dict__
