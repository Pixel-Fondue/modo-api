#!/usr/bin/env python

#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.

import lx
from struct import pack, unpack

class ThreadBody(object):
    """Used to maintain the state for a python thread allowing it to use
       lx functions and methods. Used with the 'with' keyword:
       
           with ThreadBody():
               do_threaded_stuff()
    """
    def __init__(self):
        self.t_S = lx.service.Thread()

    def __enter__(self):
        self.t_S.InitThread()

    def __exit__(self, xt, xv, tb):
        self.t_S.CleanupThread()


def lxID4(tagID):
    if len(tagID) == 4:
        return unpack(">I", tagID.encode(encoding='UTF-8'))[0]


def decodeID4(val):
    return pack(">I", val)

def item_type(name):
    return lx.service.Scene().ItemTypeLookup(name)

class ItemType(object):
    def __init__(self, name = None):
        self.set(name)

    def set(self, name):
        self._name = name
        self._code = None

    def __bool__(self):
        return self._name is not None

    def name(self):
        if (self._name):
            return self._name

        raise LookupError("name not set")

    def code(self):
        if (self._code):
            return self._code

        if (not self._name):
            lx.throw(lx.result.NOTFOUND)

        self._code = item_type(self._name)
        return self._code



