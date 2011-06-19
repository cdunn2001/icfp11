# -*- Mode: python; indent-tabs-mode: nil; -*-
# vim: set expandtab:
"""
function composition
"""

I = "I"
zero = "zero"
succ = "succ"
dbl = "dbl"
get = "get"
put = "put"
S = "S"
K = "K"
inc = "inc"
dec = "dec"
attack = "attack"
help = "help"
copy = "copy"
revive = "revive"
zombie = "zombie"

def n2t(num):
    """return a tree that evaluates to the number given
    >>> n2t(0)
    'zero'
    >>> n2t(7)
    ('succ', ('dbl', ('succ', ('dbl', ('succ', 'zero')))))
    >>> n2t(9)
    ('succ', ('dbl', ('dbl', ('dbl', ('succ', 'zero')))))

    #>>> n2s(0, 32768)
    """
    #if num < 0 or 65535 > num:
    #    raise
    s = zero
    p = 32768
    d = 0
    while p:
        if d:
            s = (dbl, s)
        if num & p:
            s = (succ, s)
            d = 1
        p = p >> 1
    return s

def n2s(slot, num):
    """return a sequence of apps that constuncts the num given, starting at I
    >>> n2s(0, 0)
    [(0, 'zero')]
    >>> n2s(0, 7)
    [(0, 'zero'), ('succ', 0), ('dbl', 0), ('succ', 0), ('dbl', 0), ('succ', 0)]
    >>> n2s(0, 9)
    [(0, 'zero'), ('succ', 0), ('dbl', 0), ('dbl', 0), ('dbl', 0), ('succ', 0)]

    """
    #if num < 0 or 65535 > num:
    #    raise
    s = [(slot, zero)]
    p = 32768
    d = 0
    while p:
        if d:
            s.append((dbl, slot))
        if num & p:
            s.append((succ, slot))
            d = 1
        p = p >> 1
    return s

def t2s(slot, tree):
    """return a sequence of apps that constructs the tree given, starting at I
    >>> t2s(0, (dec, zero) )
    [(0, 'dec'), (0, 'zero')]
    >>> t2s(0, ('dec', 1) )
    [(0, 'dec'), ('K', 0), ('S', 0), (0, 'succ'), (0, 'zero')]
    >>> t2s(1, (((S, I), I), I))
    [(1, 'S'), (1, 'I'), (1, 'I'), (1, 'I')]
    >>> t2s(1, (((S, I), I), (K, I)))
    [(1, 'S'), (1, 'I'), (1, 'I'), ('K', 1), ('S', 1), (1, 'K'), (1, 'I')]
    >>> t2s(1, (((S, I), I), (K, I)))
    [(1, 'S'), (1, 'I'), (1, 'I'), ('K', 1), ('S', 1), (1, 'K'), (1, 'I')]
    >>> t2s(0, n2t(5))
    [(0, 'succ'), ('K', 0), ('S', 0), (0, 'dbl'), ('K', 0), ('S', 0), (0, 'dbl'), ('K', 0), ('S', 0), (0, 'succ'), (0, 'zero')]
    """
    if isinstance(tree, int):
        return t2s(slot, n2t(tree))
    elif isinstance(tree, str):
        return [(slot, str)]

    left, right = tree[0], tree[1]
    s = []
    if isinstance(left, int):
        left = n2t(left)
    if isinstance(right, int):
        right = n2t(right)

    if isinstance(left, tuple):
        s.extend(t2s(slot, left))
    else:
        s.append((slot, left))

    if isinstance(right, tuple):
        s.extend([('K', slot), ('S', slot)])
        s.extend(t2s(slot, right))
    else:
        s.append((slot, right))

    return s

def turn(left, right):
    print "1" if isinstance(left, str) else "2"
    print left
    print right

def s2g(slot, tree):
    """print game input to construct tree
    >>> s2g(0, 1)
    2
    0
    succ
    2
    0
    zero
    >>> s2g(0, (dec, 2))
    2
    0
    dec
    1
    K
    0
    1
    S
    0
    2
    0
    dbl
    1
    K
    0
    1
    S
    0
    2
    0
    succ
    2
    0
    zero
    """
    for app in t2s(slot, tree):
        turn(*app)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

