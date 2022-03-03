#!/usr/bin/env python
#
# ChannelModifier metaclasses
#
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.

import lx
import lxu
import lxu.object
import lxifc
from lxu.meta.meta import MetaServer, MetaInterface
from lxu.meta.channel import Channels, Meta_Channels
from lxu.meta.package import Package, Meta_Package


class ChannelModifier(Channels):
    """Base class for defining ChannelModifier servers. The client will
       subclass this base class, filling in the methods that they require.
       It's then instantiated as a metaclass to be promoted to server. This
       derives from the Channels base class so needs an init_chan() method.
    """
    def __init__(self):
        self.m_eval = None

    def eval(self, data):
        """
        """
        pass

    def post_alloc(self):
        """
        """
        pass


class impl_ChannelModOperator(lxifc.ChannelModOperator):
    """Internal ChannelModOperator implementation does the actual work of
       binding and evaluating. The metaclass is meta_ChannelModManager.
    """
    def __init__(self, meta, cmod):
        self._meta = meta
        self._inst = meta._cm_cls()
        self._inst.m_eval = lxu.object.Evaluation(lx.object.ChannelModSetup(cmod).GetEvaluation())

        self._data = self._meta._desc.chmod_bind(cmod)
        self._inst.post_alloc()

    def cmop_Evaluate(self):
        self._inst.eval(self._data)


class impl_ChannelModManager(lxifc.ChannelModManager):
    """Internal class implementing ChannelModManager interface on package.
    """
    def __init__(self, meta):
        self._meta = meta

    def cman_Define(self, cmod):
        self._meta._desc.chmod_define(cmod)

    def cman_Allocate(self, cmod):
        return impl_ChannelModOperator(self._meta, cmod)


class meta_ChannelModManager(MetaInterface):
    """Metaclass for the ChannelModManager defines an interface for a package.
    """
    def __init__(self, cls, chan):
        MetaInterface.__init__(self, lx.symbol.u_PACKAGE)
        self._cm_cls = cls
        self._chan = chan

    def alloc(self):
        """Internal metaclass method.
        """
        self._desc = self._chan.alloc()
        return impl_ChannelModManager


class Meta_ChannelModifier(Meta_Package):
    """This is the metaclass for the ChannelModifier server type. This is
       actually a Package server metaclass, which does most of the work
       for us. We just need to add the channels metaclass, and the
       manager inerface metaclass.
    """
    def __init__(self, name, modcls = ChannelModifier, pcls = Package):
        Meta_Package.__init__(self, name, pcls)
        self._cm_cls = modcls
        self.set_supertype(lx.symbol.sITYPE_CHANMODIFY)

        self._cm_chan = Meta_Channels(modcls)
        self.add(self._cm_chan)

        self.add(meta_ChannelModManager(modcls, self._cm_chan))



