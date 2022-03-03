
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.

import math


def vector(*a):
    """Return a 3-vector (tuple of three values):
    Vector(x,y,z) = (x,y,z)
    Vector(a) = (a,a,a)
    Vector() = (0,0,0)

    """
    n = len(a)
    if (n >= 3):
        return (a[0], a[1], a[2])

    if (n == 1):
        return (a[0], a[0], a[0])

    if (n == 0):
        return (0, 0, 0)

    raise RuntimeError('invalid vector initialization')


def add(a,b):
    """result = a + b"""
    return [ a[i] + b[i]  for i in range(len(a)) ]


def sub(a,b):
    """result = a - b"""
    return [ a[i] - b[i]  for i in range(len(a)) ]


def dot(a,b):
    """result = a . b"""
    return sum (a[i] * b[i]  for i in range(len(a)))


def length(v):
    """result = sqrt (v . v)"""
    return math.sqrt(sum( x * x for x in v ))


def scale(v,s):
    """result = v * s"""
    return [ x * s  for x in v ]


def cross(a,b):
    """result = a x b"""
    x = a[1] * b[2] - a[2] * b[1]
    y = a[2] * b[0] - a[0] * b[2]
    z = a[0] * b[1] - a[1] * b[0]
    return (x, y, z)


def normalize(v):
    """result = a / length(a)"""
    len = length(v)
    if len:
        return [ x / len for x in v ]
    else:
        return v


