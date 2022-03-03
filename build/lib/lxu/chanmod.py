#
# Channel Modifier helper classes and implementations
#
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.

import lx
import lxu.attrdesc
import lxu.package
import lxifc


class Operator(object):
    """Clients sub-class this Operator class when they want to implement
       their own channel modifier.
    """

    def initialize(self, desc):
        """The intialize() method takes an AttributeDesc object and should define
        the channels and the channel modifier inputs and outputs.
        """
        pass

    def eval(self, chans):
        """The eval() method reads from input channels and writes to output channels.
        This computes the result of the modifier.
        """
        pass

    def post_alloc(self, chans):
        """The post_alloc() method is optional, and is called right after the values
        are bound.
        """
        pass


class InternalChanModOperator(lxifc.ChannelModOperator):
    """This internal class implements a ChannelModOperator using the client's op.
    """
    def __init__(self, sub):
        self.sub = sub

    def cmop_Evaluate(self):
        self.sub.eval(self.data)


class MetaPackage(lxu.package.BasicPackage, lxifc.ChannelModManager):
    """The client declares their own package class as a sub-class of this one.
       The only required method is "operator()", but the client can also derive
       from BasicItemBehaviors to override their item's behaviors.
    """
    def __init__(self):
        lxu.package.BasicPackage.__init__(self)

        self._desc = lxu.attrdesc.AttributeDesc()
        op = self.operator()
        op.initialize(self._desc)

    def operator(self):
        """The sub-class must implement this and return a new instance of their
        Operator.
        """
        pass

    def pkg_SetupChannels(self, add_obj):
        self._desc.setup_channels (add_obj)

    def cman_Define(self,cmod):
        self._desc.chmod_define (cmod)

    def cman_Allocate(self,cmod):
        sub = self.operator()
        op = InternalChanModOperator(sub)
        op.data = self._desc.chmod_bind (cmod)
        sub.post_alloc(op.data)
        return op


def bless_server(classref, name):
    """This is a replacement for blessing channel modifier classes that just provides
       standard tags.
    """
    tags = { lx.symbol.sPKG_SUPERTYPE: lx.symbol.sITYPE_CHANMODIFY }
    lx.bless(classref, name, tags)



