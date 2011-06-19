#!/usr/bin/env python
import sys

def opp():
	lr = raw_input()
	sys.stderr.write("lr=%r\n" %lr)
	lr = eval(lr)
	if lr == 1:
		card = raw_input()
		sys.stderr.write("card=%r\n" %card)
		slot = raw_input()
		sys.stderr.write("slot=%r\n" %slot)
	else:
		slot = raw_input()
		sys.stderr.write("Slot=%r\n" %slot)
		card = raw_input()
		sys.stderr.write("Card=%r\n" %card)
	return card, slot

if sys.argv[1] == '1':
	opp()

while True:
	print "1"
	print "I"
	print "0"
	sys.stdout.flush()
	opp()
