#!/usr/bin/env python
#
# Falloff object metaclasses
#
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.

import lx
import lxu
import lxu.object
import lxifc
from lxu.meta.meta import MetaObject


class Falloff(object):
    """Base class for defining Falloff objects. The client will
       subclass this base class, filling in the methods that they require.
    """
    def __init__(self):
        self._val = lx.service.Value().CreateValue(lx.symbol.sTYPE_MATRIX4)
        self._invxfrm = lxu.object.Matrix(self._val)

    def set_local(self, xfrm):
        """Call this method to set the world transform for a local falloff.
        """
        try:
            m4 = lx.object.Matrix(xfrm).Get4()
        except:
            m4 = xfrm

        self._invxfrm.Set4(m4)
        self._invxfrm.Invert()

    def valid(self):
        """Implement this method if the weight can be non-zero anywhere.
        """
        return True

    def bounded(self):
        """Implement this method if the weight can be bounded.
        """
        return False

    def bounds(self):
        """Implement this to return the bounding box for the bounded region.
        """
        return ((-1,-1,-1), (1,1,1))

    def weight_world(self, pos):
        """Implement this to get the weight computed in world coordinates.
        """
        return 0.0

    def weight_local(self, pos):
        """Implement this to get the weight computed in local coordinates.
        """
        return 0;0


class impl_Falloff(lxifc.Falloff):
    """This internal class implements the actual Falloff object.
    """
    def __init__(self, meta):
        self._meta = meta
        self._inst = meta._cls_inst()
        if (self._meta._local):
            self.fall_WeightF = self.local_weight
        else:
            self.fall_WeightF = self.world_weight

    def fall_Bounds(self):
        if not self._inst.valid():
            lx.throw(lx.result.DISABLED)

        if not self._inst.bounded():
            lx.throw(lx.result.INFINITE_BOUND)

        return self._inst.bounds()

    def local_weight(self, position):
        loc = self._inst._invxfrm.MultiplyVector(position)
        return self._inst.weight_local(loc)

    def world_weight(self, position):
        return self._inst.weight_world(position)


class Meta_Falloff(MetaObject):
    """This is the metaclass for the Falloff object type.
    """
    def __init__(self, cinst = Falloff):
        lxu.meta.MetaObject.__init__(self, lx.symbol.u_FALLOFF)
        self._cls_inst = cinst
        self._local = False

    def set_local(self, local = True):
        """Set the falloff to operate in local coordinates.
        """
        self._local = local

    def alloc(self):
        """Internal metaclass method.
        """
        return impl_Falloff



