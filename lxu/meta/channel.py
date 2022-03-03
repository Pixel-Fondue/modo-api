#!/usr/bin/env python
#
# Channel metaclasses for packages & package-like servers
#
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.

import lx
import lxu.attrdesc
import lxifc
from lxu.meta.meta import Meta


class Channels(object):
    """Base class for defining Channels. The client will subclass this base
       class, filling in the methods that they require. It's then instantiated
       as a metaclass to be used by servers.
    """
    def init_chan(self, desc):
        """This is passed an AttributeDesc object which is used to init the
           channels.
        """
        pass


class Meta_Channels(Meta):
    """This is the metaclass for Channels.
    """
    def __init__(self, cls):
        lxu.meta.Meta.__init__(self)
        self._type = self.types.ATTRDESC
        self._ccls = cls
        self._desc = None

    def alloc(self):
        if (not self._desc):
            self._desc = lxu.attrdesc.AttributeDesc()
            self._ccls().init_chan(self._desc)
        return self._desc


