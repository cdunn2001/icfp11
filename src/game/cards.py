# -*- Mode: python; indent-tabs-mode: t; -*-
# vim: set noexpandtab:
"""
s is the global state.
"""

from error import Error

def RequireInt(n):
	if not isinstance(n, int):
		raise Error
def RequireSlot(i):
	if i<0 or i>255:
		raise Error
def RequireLiveSlot(v, i):
	RequireSlot(i)
	if not Alive(v, i):
		raise Error
def Alive(v, i):
	return v[i] not in (0,1)

I = lambda _, x: x

zero = 0

def succ(_, n):
	RequireInt(n)
	if n < 65535:
		return n+1
	else:
		return 65535

def dbl(_, n):
	RequireInt(n)
	if n>=32768:
		return 65535
	else:
		return n*2

def pget(pro):
	def get(s, i):
		RequireLiveSlot(s.v[pro], i)
		return s.f[pro][i]
	return get

put = lambda _, x: I
S = lambda _, f: lambda __, g: lambda s, x: f(s, x)(g(s, x))
K = lambda _, x: lambda __, y: x

def pinc(pro):
	def inc(s, i):
		RequireSlot(i)
		v = s.v[pro][i]
		if s.is_auto_app:
			if v > 0:
				s.v[pro][i] -= 1
		else:
			if v < 65535 and v > 0:
				s.v[pro][i] += 1
		return I
	return inc

def pdec(pro):
	def dec(s, i):
		opp = 1-pro
		RequireSlot(i)
		v = s.v[opp][255-i]
		if s.is_auto_app:
			if v < 65535 and v > 0:
				s.v[opp][255-i] += 1
		else:
			if v > 0:
				s.v[opp][255-i] -= 1
		return I
	return dec

def pattack(pro):
	opp = 1-pro
	def attack(_, i):
		RequireSlot(i)
		def attacki(__, j):
			def attackij(s, n):
				RequireSlot(i)
				RequireInt(n)
				v = s.v[pro][i]
				if n > v:
					raise Error
				s.v[pro][i] -= n
				RequireSlot(j)
				if Alive(s.v[opp], 255-j):
					w = s.v[opp][255-j]
					if s.is_auto_app:
						if w > 0:
							w += n*9//10
							if w >65535: w = 65535
					else:
						w -= n*9//10
						if w < 0: w = 0
					s.v[opp][255-j] = w
				return I
			return attackij
		return attacki

def phelp(pro):
	opp = 1-pro
	def help(_, i):
		def helpi(__, j):
			def helpij(s, n):
				RequireSlot(i)
				RequireInt(n)
				v = s.v[pro][i]
				if n > v:
					raise Error
				s.v[pro][i] -= n
				RequireSlot(j)
				if Alive(s.v[pro], j):
					w = s.v[pro][j]
					if s.is_auto_app:
						if w > 0:
							w -= n*11//10
							if w < 0: w = 0
					else:
						w += n*11//10
						if w > 65535: w = 65535
					s.v[pro][j] = w
				return I
			return helpij
		return helpi
	return help

def pcopy(pro):
	opp = 1-pro
	def copy(s, i):
		RequireSlot(i)
		return s.v[opp][i]
	return copy

def previve(pro):
	def revive(s, i):
		RequireSlot(i)
		if s.v[pro][i] <= 0:
			s.v[pro][i] = 1
		return I
	return revive

def pzombie(pro):
	opp = 1-pro
	def zombie(_, i):
		def zombiei(s, x):
			RequireSlot(i)
			if Alive(s.v[opp], 255-i):
				raise Error("Cannot apply zombiei to live slot %i." %(255-i))
			f1[255-i] = x
			s.v[opp][255-i] = -1
			return I
		return zombiei
	return zombie



def get_cards(pro):
	cards = dict()
	cards["I"] = I
	cards["zero"] = zero
	cards["succ"] = succ
	cards["dbl"] = dbl
	cards["get"] = pget(pro)
	cards["put"] = put
	cards["S"] = S
	cards["K"] = K
	cards["inc"] = pinc(pro)
	cards["dec"] = pdec(pro)
	cards["attack"] = pattack(pro)
	cards["help"] = phelp(pro)
	cards["copy"] = pcopy(pro)
	cards["revive"] = previve(pro)
	cards["zombie"] = pzombie(pro)
	return cards

a_cards = [get_cards(0), get_cards(1)]

card_names = dict()
for i in range(2):
	for name, func in a_cards[i].items():
		card_names[func] = name

