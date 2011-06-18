#!/usr/bin/env python
import sys

valid_cards = {
  "I": {},
  "zero": {},
  "succ": {},
  "dbl": {},
  "get": {},
  "put": {},
  "S": {},
  "K": {},
  "inc": {},
  "dec": {},
  "attack": {},
  "help": {},
  "copy": {},
  "revive": {},
  "zombie": {},
}

def validate_card(card):
	if card not in valid_cards:
		raise ValueError("invalid card '%s'" % card)

def validate_slot(slot):
	n = int(slot) # raises for non-numbers
	if n not in range(256):
		raise ValueError("slot not in [0,255]")

def dump_left_app(card, slot):
	validate_card(card)
	validate_slot(slot)
	print "1"
	print card
	print slot

def dump_right_app(card, slot):
	validate_card(card)
	validate_slot(slot)
	print "2"
	print slot
	print card

def opp():
	card, slot = None, None
	validate = False # don't incur runtime penalty by default
	try:
		lr = raw_input()
		sys.stderr.write("lr=%r\n" %lr)
		lr = eval(lr)
		if lr == 1:
			card = raw_input()
			if validate:
				validate_card(card)
			sys.stderr.write("card=%r\n" %card)
			slot = raw_input()
			if validate:
				validate_slot(slot)
			sys.stderr.write("slot=%r\n" %slot)
		else:
			slot = raw_input()
			if validate:
				validate_slot(slot)
			sys.stderr.write("Slot=%r\n" %slot)
			card = raw_input()
			if validate:
				validate_card(card)
			sys.stderr.write("Card=%r\n" %card)
	except EOFError as e:
		pass
	return card, slot

if __name__ == "__main__":
	card, slot = None, None
	if sys.argv[1] == '1':
		card, slot = opp()
	while card is not None:
		dump_left_app("I", 0)
		sys.stdout.flush()
		card, slot = opp()
