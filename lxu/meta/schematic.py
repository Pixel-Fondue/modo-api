#!/usr/bin/env python
#
# SchematicConnection metaclasses
#
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.

import lx
import lxu
import lxu.utils
import lxifc
from lxu.meta.meta import MetaServer


class SchematicConnection(object):
    """Base class for defining SchematicConnection servers. The client will
       subclass this base class, filling in the methods that they require.
       It's then instantiated as a metaclass to be promoted to server.
    """
    def __init__(self):
        self._tmpflag = 0

    def test_item(self, item):
        """Test if an item should have a connection point. If it should then
           call set_single() for a single connection, or set_multiple() for
           multiple (perhaps ordered) connections.
        """
        pass

    def set_single(self):
        self._tmpflag = lx.symbol.fSCON_SINGLE

    def set_multiple(self, ordered = False):
        self._tmpflag = lx.symbol.fSCON_MULTIPLE
        if (ordered):
            self._tmpflag |= lx.symbol.fSCON_ORDERED

    def allow(self, ifrom, ito):
        """Return true if a link between these items is legal.
        """
        return True

    def get_list(self, item):
        """Get the list of items with incoming connections. This is only called
           if no graph is specified, or if the graph is manual.
        """
        return []

    def connect(self, ifrom, ito, toIndex):
        """Make a connection between two items. This is only called if no graph
           is specified.
        """
        pass

    def disconnect(self, ifrom, ito):
        """Break a connection between two items. This is only called if no graph
           is specified.
        """
        pass


class impl_Server(lxifc.SchematicConnection):
    """This internal class implements the actual SchematicConnection server.
       It defers to the metaclass state and the client subclass for specific
       behaviors.
    """
    def __init__(self, meta):
        self._meta = meta
        self._inst = meta._cls_inst()
        self._last = ""
        self._list = []
        self._ival = meta._valcount

    def item_flags(self, item):
        self._inst._tmpflag = 0
        self._inst.test_item(item)
        return self._inst._tmpflag

    def schm_ItemFlags(self,item):
        item = lx.object.Item(item)
        if (self._meta._bytype):
            if (item.TestType (self._meta._itemtype.code ())):
                return self._meta._typeflag
            return 0
        else:
            return self.item_flags(item)

    def schm_AllowConnect(self,from_obj,to_obj):
        ifrom = lx.object.Item(from_obj)
        ito   = lx.object.Item(to_obj)
        return self._inst.allow(ifrom, ito)

    def schm_AllowConnectType(self,from_obj,type):
        lx.notimpl()

    def schm_GraphName(self):
        if (self._meta._graph):
            return self._meta._graph
        else:
            lx.throw(lx.result.NOTFOUND)

    def refresh_list(self, item):
        item = lx.object.Item(item)
        if (item.Ident() != self._last):
            self._last = item.Ident()
            self._list = self._inst.get_list(item)

    def schm_Count(self,item):
        if (not self._meta._manual):
            lx.notimpl()

        refresh_list(lx.object.Item(item))
        return self._list.size()

    def schm_ByIndex(self,item,index):
        if (not self._meta._manual):
            lx.notimpl()

        refresh_list(lx.object.Item(item))
        return self._list[index]

    def schm_Connect(self,from_obj,to_obj,toIndex):
        if (not self._meta._manual):
            lx.notimpl()

        self._last = ""
        ifrom = lx.object.Item(from_obj)
        ito   = lx.object.Item(to_obj)
        self._inst.connect(ifrom,ito,toIndex)

    def schm_Disconnect(self,from_obj,to_obj):
        if (not self._meta._manual):
            lx.notimpl()

        self._last = ""
        ifrom = lx.object.Item(from_obj)
        ito   = lx.object.Item(to_obj)
        self._inst.disconnect(ifrom,ito)

    def schm_BaseFlags(self):
        f = 0
        if (self._meta._reverse): f |= lx.symbol.fSCON_REVERSE
        if (self._meta._manual):  f |= lx.symbol.fSCON_USESERVER
        if (self._meta._dynamic): f |= lx.symbol.fSCON_PERITEM
        return f

    def schm_PerItemFlags(self,item):
        if (not self._meta._dynamic):
            lx.notimpl()

        return item_flags(lx.object.Item(item))

    def schm_ItemFlagsValid(self):
        if (self._ival == self._meta._valcount):
            return 1

        self._ival = self._meta._valcount
        return 0


class Meta_SchematicConnection(MetaServer):
    """This is the metaclass for the SchematicConnection server type.
    """
    def __init__(self, name, cinst = SchematicConnection):
        lxu.meta.MetaServer.__init__(self, name, lx.symbol.u_SCHEMATICCONNECTION)
        self._cls_inst = cinst
        self._dynamic  = False
        self._bytype   = False
        self._reverse  = False
        self._manual   = True
        self._graph    = None
        self._itemtype = lxu.utils.ItemType()
        self._typeflag = 0
        self._valcount = 0

    def set_graph(self, name, reverse = False, manual = False):
        """Set the graph name for normal, graph-based connections. The graph can
           be set to be reversed. 'manual' can be True to use the computed list
           for the contents of the links.
        """
        self._graph    = name
        self._reverse  = reverse
        self._manual   = manual

    def set_itemtype(self, name, multiple = False, ordered = False):
        """Set an item type to limit connections to exactly items matching this type.
        """
        self._itemtype.set(name)
        self._dynamic = False
        if (not self._itemtype):
            self._bytype = False
            return

        self._bytype   = True
        self._typeflag = 0
        if (multiple):
            self._typeflag |= lx.symbol.fSCON_MULTIPLE
        else:
            self._typeflag |= lx.symbol.fSCON_SINGLE

        if (ordered):
            self._typeflag |= lx.symbol.fSCON_ORDERED

    def set_dynamic(self):
        """Set the connections to be tested for each individual item.
        """
        self._dynamic = True
        self._bytype  = False

    def invalidate(self):
        """Invalidate the dynamic state of item connections.
        """
        if (self._valcount > 4000000):
            self._valcount = 0
        else:
            self._valcount += 1

    def alloc(self):
        """Internal metaclass method.
        """
        return impl_Server


