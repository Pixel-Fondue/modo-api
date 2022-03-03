
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.

import lx

class AnySelection(object):
    """Common subclass for selection objects.

    """
    def __init__(self, type_name, trans_name):
        self.selsvc  = lx.service.Selection()
        self.stype   = type_name
        self.spType  = self.selsvc.LookupType(self.stype)
        cls          = getattr(lx.object, trans_name + "PacketTranslation")
        self.spTrans = cls(self.selsvc.Allocate(self.stype))

    def pkt_list(self):
        """Return a list of raw selection packets.

        """
        a = []
        for i in range(self.selsvc.Count(self.spType)):
            a.append(self.selsvc.ByIndex(self.spType, i))

        return a

    def drop(self):
        """Drop the selection, changing the selection mode.

        """
        self.selsvc.Drop(self.spType)

    def clear(self):
        """Drop the selection without changing the selection mode.

        """
        self.selsvc.Clear(self.spType)


class SceneSelection(AnySelection):
    """This is equivalent to the CLxSceneSelection helper class in C++.

    """
    def __init__(self):
        AnySelection.__init__(self, lx.symbol.sSELTYP_SCENE, "Scene")

    def current(self):
        """Return the current scene.

        """
        return self.spTrans.Scene(self.selsvc.Recent(self.spType))


class ItemSelection(AnySelection):
    """This is equivalent to the CLxItemSelection helper class in C++.
    Selected items are returned as a list.

    """
    def __init__(self):
        AnySelection.__init__(self, lx.symbol.sSELTYP_ITEM, "Item")

    def current(self):
        """Returns the currently selected items are returned as a list.

        """
        a = []
        for pkt in self.pkt_list():
            item = self.spTrans.Item(pkt)
            a.append(item)

        return a

    def select(self, itemID, add=False):
        """Select an item by ID or name

            itemID - name or ID of item to select
            add    - add to current selection or replace, default = replace

        """
        scene = SceneSelection().current()
        item = scene.ItemLookup(itemID)
        if not add:
            self.selsvc.Clear(self.spType)
        sPacket = self.spTrans.Packet(item)
        self.selsvc.Select(self.spType, sPacket)


class ChannelSelection(AnySelection):
    """This is equivalent to the CLxChannrlSelection helper class in C++.

    """
    def __init__(self):
        AnySelection.__init__(self, lx.symbol.sSELTYP_CHANNEL, "Channel")

    def current(self):
        """Returns the currently selected channels as a list.
        Channels are given by an item / channel index pair.

        """
        a = []
        for pkt in self.pkt_list():
            item = self.spTrans.Item(pkt)
            chan = self.spTrans.Index(pkt)
            a.append((item, chan))

        return a


class PresetPathSelection(AnySelection):
    """Selected paths are returned as a list.

    """
    def __init__(self):
        AnySelection.__init__(self, lx.symbol.sSELTYP_PRESETPATH, "PresetPath")

    def current(self):
        a = []
        for pkt in self.pkt_list():
            path = self.spTrans.Path(pkt)
            id   = self.spTrans.Identifier(pkt)
            a.append((path,id))

        return a



