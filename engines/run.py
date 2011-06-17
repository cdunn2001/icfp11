#!/usr/bin/env python
import sys

def opp():
	lr = input()
	if lr == 1:
		card = raw_input()
		slot = input()
	else:
		slot = input()
		card = raw_input()
	return card, slot

if sys.argv[1] == '1':
	opp()

while True:
    print "1"
    print "I"
    print "0"
    opp()
