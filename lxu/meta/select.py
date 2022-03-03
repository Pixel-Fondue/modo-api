#!/usr/bin/env python
#
# SeletionType metaclasses
#
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.

import lx
import lxu
import lxu.service
import lxu.utils
import lxifc
from lxu.meta.meta import MetaServer
import ctypes


class SelectionType(object):
    """Base class for defining SelectionType servers. The client will
       subclass this base class, filling in the methods that they require.
       It's then instantiated as a metaclass to be promoted to server.
       Selections are all given by numeric id code.
    """
    def __init__(self):
        pass

    def subtype(self, id):
        """Implement to return a subtype code for a given selected ID.
        """
        return 0


class impl_Server(lxifc.SelectionType):
    """This internal class implements the actual SelectionType server.
       It defers to the metaclass state and the client subclass for specific
       behaviors.
    """
    def __init__(self, meta):
        self._meta = meta
        self._inst = meta._cls_inst()

    def seltyp_Size(self):
        return ctypes.sizeof(ctypes.c_int)

    def seltyp_Flags(self):
        if self._meta._is_undo:
            return lx.symbol.f_SELPACKET_UNDOABLE
        else:
            return 0

    def seltyp_MessageTable(self):
        return self._meta._mtab

    def seltyp_Compare(self,pkey,pelt):
        key = self._meta.id_from_pkt(pkey)
        elt = self._meta.id_from_pkt(pelt)
        return (key < elt) - (key > elt)

    def seltyp_SubType(self,pkt):
        id = self._meta.id_from_pkt(pkt)
        return self._inst.subtype(id)


class Meta_SelectionType(MetaServer):
    """This is the metaclass for the SelectionType server type.
    """
    def __init__(self, name, code, cinst = SelectionType):
        lxu.meta.MetaServer.__init__(self, name, lx.symbol.u_SELECTIONTYPE)
        self._cls_inst = cinst
        self._code = lxu.utils.lxID4(code)
        self.add_tag (lx.symbol.sSELTYPE_CODE, code)

        self._is_undo = False
        self._mtab = name
        self._int_ptr = ctypes.POINTER(ctypes.c_int)
        self._pkt_int = ctypes.c_int()
        self._sel_S = lxu.service.Selection()

    def set_undoable(self, supportUndo = True):
        """Set the selection to be undoable. Default is non-undoable.
        """
        self._is_undo = supportUndo

    def get_ID4(self):
        """Get the type code for the selection.
        """
        return self._code

    def pkt_from_id(self, id):
        """Get a packet from a numeric id code. The packet is effectively a
           pointer to the int, and is valid until this is called again.
        """
        self._pkt_int.value = id
        return ctypes.addressof(self._pkt_int)

    def id_from_pkt(self, pkt):
        """Get an id from a selection packet. This dereferences the packet
           pointer and returns the int inside.
        """
        return ctypes.cast(pkt, self._int_ptr).contents.value

    def select(self, id, add = True):
        """Add this id to the selection, or if 'add' is false, set the selection
           to only this id.
        """
        if not add: self.clear()

        self._sel_S.Select(self._code, self.pkt_from_id(id))

    def deselect(self, id):
        """Deselect this id.
        """
        self._sel_S.Deselect(self._code, self.pkt_from_id(id))

    def remove(self, id):
        """Remove this id from the selection anywhere it might occur.
        """
        self._sel_S.Remove(self._code, self.pkt_from_id(id))

    def clear(self):
        """Set the current selection to empty.
        """
        self._sel_S.Clear(self._code)

    def drop(self):
        """Clear the selection and make this selection type topmost.
        """
        self._sel_S.Drop(self._code)

    def alloc(self):
        """ (internal) Return implementation class.
        """
        return impl_Server


