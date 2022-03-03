#!/usr/bin/env python
#
# Package metaclasses for implementing item type servers.
#
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.

import lx
import lxu
import lxu.meta
import lxifc
from lxu.meta.meta import MetaServer, MetaInterface


class Package(object):
    """Base class for defining Packages. The client will subclass this base
       class, filling in the methods that they require. It's then instantiated
       as a metaclass to be promoted to a server.
    """
    def __init__(self):
        self.m_item = None

    def initialize(self, super):
        """Initial package creation.
        """
        pass

    def newborn(self, item, flags):
        """Item initial creation.
        """
        pass

    def loading(self):
        """Item create on load.
        """
        pass

    def after_load(self):
        """Item finished loading.
        """
        pass

    def doomed(self):
        """Item final destroy.
        """
        pass

    def add(self):
        """Item added to scene -- either on create or on delete undo.
        """
        pass

    def remove(self):
        """Item removed from scene -- either on delete or on create undo.
        """
        pass

    def synth_name(self):
        """Return a synthetic name for the item when it has no other name.
        """
        return None

    def parent_ok(self, parent):
        """Return true if the parent is valid.
        """
        return True


class impl_Instance(lxifc.PackageInstance):
    """This class implements the PackageInstance using the client's
       Package sub-class.
    """
    def __init__(self, meta):
        self._meta = meta
        self._inst = meta._icls()

    def pins_Initialize(self,item,super):
        self._inst.m_item = lxu.object.Item(item)
        self._inst.initialize(super)

    def pins_SynthName(self):
        n = self._inst.synth_name()
        if (n):
            return n
        else:
            lx.notimpl()

    def pins_TestParent(self,item):
        return self._inst.parent_ok(lxu.object.Item(item))

    def pins_Newborn(self,original,flags):
        if (original.test()):
            self._inst.newborn(lxu.object.Item(original), flags)
        else:
            self._inst.newborn(None, flags)

    def pins_Loading(self):
        self._inst.loading()

    def pins_AfterLoad(self):
        self._inst.after_load()

    def pins_Doomed(self):
        self._inst.doomed()

    def pins_Add(self):
        self._inst.add()

    def pins_Remove(self):
        self._inst.remove()


class meta_Instance(object):
    """This is an internal metaclass object for the package instance. It just
       passes the client instance class as _icls, and the interfaces as _sub_ifcs.
    """
    def __init__(self, cls):
        self._icls     = cls
        self._sub_ifcs = None


# NOTE: defined here because it's referenced soon
#
class ChannelUI(object):
    """The base class for ChannelUI metaclass. It only has a couple of methods
       so often this class itself is all that's needed.
    """
    def item_enabled(self, item, message):
        """
        """
        return True

    def item_icon(self, item):
        """
        """
        return None


class impl_Server(lxifc.Package):
    """This class implements the Package server using a local version of the
       client's Package sub-class.
    """
    def __init__(self, meta):
        self._meta  = meta
        self._inst  = meta._icls()
        self.s_guid = lx.service.GUID()

    def pkg_SetupChannels(self,addChan):
        if (self._meta._desc):
            self._meta._desc.setup_channels(addChan)

    def pkg_Attach(self):
        return impl_Instance(self._meta._instmeta)

    def pkg_TestInterface(self,guid):
        return lx.testifc(impl_Instance, guid, self._meta._instmeta)

#    def pkg_PostLoad(self,scene):
#        lx.notimpl()
#    def pkg_CollectItems(self,collection,mode):
#        lx.notimpl()


class Meta_Package(MetaServer):
    """This is the metaclass for Packages. You allocate it with the server
       name and optional Package sub-class.
    """
    def __init__(self, name, cls = Package):
        lxu.meta.MetaServer.__init__(self, name, lx.symbol.u_PACKAGE)
        self._icls = cls
        self._desc = None
        self._hasui = False

    def set_supertype(self, typename = "."):
        """Set the supertype for this package, making it an item type. If the
           typename is omitted then this is a root type.
        """
        self.add_tag (lx.symbol.sPKG_SUPERTYPE, typename)

    def add_channelui(self, cls = ChannelUI):
        """Add a ChannelIU class
        """
        self.add(Meta_ChannelUI(cls))
        self._hasui = True

    def pre_init(self):
        """Internal method
        """
        m = self.find_any(self.types.ATTRDESC)
        if (m):
            self._desc = m.alloc()
            if not self._hasui and self._desc.need_chan_ui():
                self.add_channelui()

        return False

    def alloc(self):
        """Internal method
        """
        self._instmeta = meta_Instance(self._icls)
        self._instmeta._sub_ifcs = self.get_ifcs(lx.symbol.u_PACKAGEINSTANCE)

        self.init_ifcs()
        return impl_Server


class impl_ChannelUI(lxifc.ChannelUI):
    """Internal implementation class. Methods defer to client instance or attrdesc.
    """
    def __init__(self, meta):
        self._meta = meta
        self._inst = meta._icls()

    def inherit(self, pkgimpl):
        self._desc = pkgimpl._meta._desc

    def cui_ItemEnabled(self,msg,item):
        msg  = lxu.object.Message(msg)
        item = lxu.object.Item(item)
        return self._inst.item_enabled(item, msg)

    def cui_ItemIcon(self,item):
        item = lxu.object.Item(item)
        return self._inst.item_icon(item)

    def cui_DependencyCount(self, channelName):
        return self._desc.chan_dep_count(channelName)

    def cui_DependencyByIndexName(self, channelName, index):
        t, c = self._desc.chan_dep_byindex(channelName, index)
        if not t:
            t = self._meta._itemtype

        return (t, c)

    def cui_UIHints(self, channelName, hints):
        self._desc.chan_uihints(channelName, hints)

    def cui_Enabled(self,channelName,msg,item,chanRead):
        return self._desc.chan_enabled(channelName, item, chanRead, msg)

    def cui_UIValueHints(self,channelName):
        return self._desc.chan_uivalue(channelName)


class Meta_ChannelUI(MetaInterface):
    """Metaclass for ChannelUI. This is added under a package and modifies it.
    """
    def __init__(self, cls = ChannelUI):
        MetaInterface.__init__(self, lx.symbol.u_PACKAGE)
        self._icls = cls
        self._desc = None
        self._itemtype = None

    def alloc(self):
        m = self.find_any(self.types.ATTRDESC)
        if (m):
            self._desc = m.alloc()

        m = self.find_any(self.types.SERVER, lx.symbol.u_PACKAGE)
        if (m):
            self._itemtype = m._name

        return impl_ChannelUI



class ViewItem3D(object):
    """The base class for ViewItem3D metaclass. This class controls how a package
       will appear in 3D.
    """
    def __init__(self):
        self.m_item = None

    def draw(self, chanread, stroke, flags, color):
        """This method is called to draw the package in 3D, reading channels from
           the read object and drawing with the stroke object.
        """
        pass

    def drawtest(self, chanread, stroke, flags, color):
        """Hit testing can be done by drawing a different stroke pattern. This
           method has to be enabled with enable_test()
        """
        pass

    def drawbg(self, chanread, stroke, color):
        """Background drawing can also be optionally done. This method has to be
           enabled with enable_background().
        """
        pass


class impl_ViewItem3D(lxifc.ViewItem3D):
    def __init__(self, meta):
        self._meta  = meta
        self._inst  = meta._icls()

    def inherit(self, pkgimpl):
        self._inst.m_item = pkgimpl._inst.m_item

    def vitm_WorldSpace(self):
        return self._meta._world

    def vitm_Draw(self,chanRead,strokeDraw,sflags,itemColor):
        cr = lxu.object.ChannelRead(chanRead)
        st = lxu.object.StrokeDraw(strokeDraw)
        self._inst.draw(cr, st, sflags, itemColor)

    def vitm_DrawBackground(self,chanRead,strokeDraw,itemColor):
        if (self._meta._b_bg):
            cr = lxu.object.ChannelRead(chanRead)
            st = lxu.object.StrokeDraw(strokeDraw)
            self._inst.drawbg(cr, st,itemColor)
        else:
            lx.notimpl()

    def vitm_Test(self,chanRead,strokeDraw,sflags,itemColor):
        if (self._meta._b_test):
            cr = lxu.object.ChannelRead(chanRead)
            st = lxu.object.StrokeDraw(strokeDraw)
            self._inst.drawtest(cr, st, sflags,itemColor)
        else:
            lx.notimpl()

#    def vitm_HandleCount(self):
#        lx.notimpl()
#    def vitm_HandleMotion(self,handleIndex):
#        lx.notimpl()
#    def vitm_HandleChannel(self,handleIndex):
#        lx.notimpl()
#    def vitm_HandleValueToPosition(self,handleIndex):
#        lx.notimpl()
#    def vitm_HandlePositionToValue(self,handleIndex):
#        lx.notimpl()


class Meta_ViewItem3D(MetaInterface):
    """Metaclass for ViewItem3D. This is added under a package and modifies it.
    """
    def __init__(self, cls = ViewItem3D):
        MetaInterface.__init__(self, lx.symbol.u_PACKAGEINSTANCE)
        self._icls   = cls
        self._b_bg   = False
        self._b_test = False
        self._world  = False

    def set_world_space(self, world = True):
        """Set the package to draw in world space. Normally locators are drawn in
           their local coordinate space.
        """
        self._world = world

    def enable_background(self):
        """Enable background drawing.
        """
        self._b_bg = True

    def enable_test(self):
        """Enable alternate testing.
        """
        self._b_test = True

    def alloc(self):
        return impl_ViewItem3D



