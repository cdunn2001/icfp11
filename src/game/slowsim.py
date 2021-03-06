# -*- Mode: python; indent-tabs-mode: nil; -*-
# vim: set expandtab:
"""
deubbuging simulator
"""
from copy import deepcopy

def vital(slot, delta):
    old = slot.vitality
    #print "Changing vitality %d by %d" %(old, delta)
    slot.vitality += delta
    if slot.vitality < 0:
        slot.vitality = 0
    if slot.vitality > 65535:
        slot.vitality = 65535
    if old > 0 and slot.vitality <= 0:
        slot.parent.aliveCount -= 1
    if old <= 0 and slot.vitality > 0:
        slot.parent.aliveCount += 1

tuples = [1]

def as_calls(name, *args):
    r = name
    for arg in args:
        if arg is not None:
            r += "(%s)" %arg
    return r

def as_tuples(name, *args):
    r = name
    for arg in args:
        if arg is not None:
            r = "(%s, %s)" %(r, arg)
    return r

def Repr(name, *args):
    return as_tuples(name, *args) if tuples[0] else as_calls(name, *args)

class I:
    def __repr__(self): return "I"
    def __call__(self, x): return x
def zero(): return 0
class succ:
    def __repr__(self): return "succ"
    def __call__(self, n): return n + 1 if n < 65535 else 65535
class dbl:
    def __repr__(self): return "dbl"
    def __call__(self, n): return n * 2 if n < 32768 else 65535
class get:
    def __repr__(self): return "get"
    def __call__(self, i): return deepcopy(pro.slots[i].field)
class put:
    def __repr__(self): return "put"
    def __call__(self, x): return I()
class S:
    def __init__(self): self.f = self.g = None
    def __repr__(self): return Repr("S", self.f, self.g)
    def __call__(self, x):
        if self.f is None:
            self.f = x
            return self
        if self.g is None:
            self.g = x
            return self
        return self.f(x)(self.g(deepcopy(x)))
class K:
    def __init__(self): self.x = None
    def __repr__(self): return Repr("K", self.x)
    def __call__(self, y):
        if self.x is None:
            self.x = y
            return self
        return self.x
class inc:
    def __repr__(self): return "inc"
    def __call__(self, i):
        vital(pro.slots[i], autosign * 1)
        return I()
class dec:
    def __repr__(self): return "dec"
    def __call__(self, i):
        #print "INDEX: %d" %i
        vital(opp.slots[255-i], autosign * -1)
        return I()
class attack:
    def __init__(self): self.i = self.j = None
    def __repr__(self): return Repr("attack", self.i, self.j)
    def __call__(self, n):
        if self.i is None:
            self.i = n
            return self
        if self.j is None:
            self.j = n
            return self
        vital(pro.slots[self.i], -n)
        vital(opp.slots[255-self.j], autosign * -n * 9 // 10)
        return I()
class help:
    def __init__(self): self.i = self.j = None
    def __repr__(self): return Repr("help", self.i, self.j)
    def __call__(self, n):
        if self.i is None:
            self.i = n
            return self
        if self.j is None:
            self.j = n
            return self
        vital(pro.slots[self.i], -n)
        vital(pro.slots[self.j], autosign * n * 11 // 10)
        return I()
class copy:
    def __repr__(self): return "copy"
    def __call__(self, i): return deepcopy(opp.slots[i].field)
class revive:
    def __repr__(self): return "revive"
    def __call__(self, i):
        vital(pro.slots[i], 1 - pro.slots[i].vitality)
        return I()
class zombie:
    def __init__(self): self.i = None
    def __repr__(self): return Repr("zombie", self.i)
    def __call__(self, x):
        if self.i is None:
            self.i = x
            return self
        i = 255 - self.i
        opp.slots[i].field = x
        vital(opp.slots[i], -1 - opp.slots[i].vitality)
        return I()

class Slot:
    def __init__(self, parent):
        self.parent = parent
        self.field = I()
        self.vitality = 10000
class Player:
    def __init__(self):
        self.slots = [Slot(self) for i in range(256)]
        self.aliveCount = 256

player1 = Player()
player2 = Player()
autosign = 1
pro = player1
opp = player2

def test():
    """
    >>> S()(I())(I())(K())

    >>> S()(I())(I())

    >>> S()(K())(K())(help())

    >>> attack()(zero())(succ()(succ()(zero())))

    >>> S()(K()(S()(K()(S()(K()(dec()))))(K())))(get())

    >>> S()(K()(dec()))(S()(K()(get()))(K()(1)))

    >>> opp.slots[0].vitality

    >>> pro.slots[1].field = 255
    >>> S()(K()(dec()))(S()(K()(get()))(K()(1)))(I())

    >>> opp.slots[0].vitality

    >>> S()(K()(S()(K()(attack()(2)))(S()(K()(get()))(K()(1)))))(K()(65535))

    >>> S()(K()(S()(K()(attack()(2)))(S()(K()(get()))(K()(1)))))(K()(65535))(I())

    >>> S()(K()(attack()(2)(get()(1))))(K()(65535))

    >>> S()(K()(attack()(2)(get()(1))))(K()(65535))(I())

    >>> opp.slots[0].vitality

    >>> opp.slots[1].vitality

    >>> pro.slots[1].field = 254

    >>> S()(S()(K()(attack()(2)))(S()(K()(get()))(K()(1))))(K()(65535))

    >>> tuples[0] = 0

    >>> S()(S()(K()(attack()(2)))(S()(K()(get()))(K()(1))))(K()(65535))

    >>> S()(S()(K()(attack()(2)))(S()(K()(get()))(K()(1))))(K()(65535))(I())

    >>> opp.slots[1].vitality

    """

if __name__ == "__main__":
    import doctest
    doctest.testmod()

