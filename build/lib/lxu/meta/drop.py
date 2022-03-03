#!/usr/bin/env python
#
# Drop metaclasses
#
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.

import lx
import lxu
import lxu.object
import lxifc
from lxu.meta.meta import MetaServer


class DropAction(object):
    """Base class for defining Drop actions.
    """
    def __init__(self):
        self._drop = None
        self._name = None
        self._index = None
        self._custom = None
        self._cust_base = None
        self._cust_num = None

    def enabled(self, dest):
        """Tests if this action is enabled relative to this destination. Simple
           actions just return true or false; custom actions call add_custom().
        """
        return True

    def name_str(self):
        """Get the name for the action if it's different from the name in the
           message table. The string version is called first, and if that returns
           null then the message version is used.
        """
        return None

    def name_msg(self, msg):
        """Get the name for the action if it's different from the name in the
           message table. The string version is called first, and if that returns
           null then the message version is used.
        """
        return None

    def exec_act(self):
        """Implement to execute the action.
        """
        pass

    def exec_custom(self, index):
        """Implement to execute a custom action given by index.
        """
        pass


class Drop(object):
    """Base class for defining Drop servers. The client will
       subclass this base class, filling in the methods that they require.
       It's then instantiated as a metaclass to be promoted to server.
    """
    def __init__(self):
        self._add = None
        self._icur = None
        self._cur = None

    def recognize_any(self, source):
        """Called once on the start of drag/drop to detect if this drop server
           supports this source.
        """
        return False

    def recognize_array(self, array):
        """Called once on the start of drag/drop to detect if this drop server
           supports this array source.
        """
        return False

    def enabled(self, dest):
        """Called multiple times during drag to determine if this drop server
           supports the destination under the mouse.
        """
        return True

    def add_custom(self, name):
        self._add.AddAction(self._icur, name)
        self._icur = self._icur + 1
        self._cur._cust_num = self.icur._cust_num + 1


class impl_Server(lxifc.Drop):
    """This internal class implements the actual Drop server.
       It defers to the metaclass state and the client subclass for specific
       behaviors.
    """
    def __init__(self, meta):
        self._meta = meta
        self._inst = meta.alloc_inst()

    def drop_Recognize(self,source):
        if self._inst.recognize_any(source):
            return

        if self._meta._is_array and self._inst.recognize_array(lxu.object.ValueArray(source)):
            return

        lx.throw(lx.result.NOTFOUND(True))

    def drop_ActionList(self,source,dest,add):
        if not self._inst.enabled (dest):
            return

        self._inst._add = lxu.object.AddDropAction(add)
        self._inst._icur = 0

        for act in self._meta._actions:
            self._inst._cur = act
            act._cust_base = self._inst._icur
            act._cust_num = 0

            enab = act.enabled(dest)
            if act._custom or not enab:
                continue

            name = act.name_str()
            if not name:
                pass
                #get message
                #call name_msg

            if not name:
                name = '@' + self._meta._name + '@' + act._name + '@'

            self._inst._add.AddAction(act._index, name)

        self._inst._add = None

    def drop_Drop(self,source,dest,action):
        for act in self._meta._actions:
            if act._custom:
                if action >= act._cust_base and action < act._cust_base + act._cust_num:
                    act.exec_custom(action - act._cust_base)
                    return
            else:
                act.exec_act()
                return

        lx.throw(lx.result.NOTFOUND)


class Meta_Drop(MetaServer):
    """This is the metaclass for the Drop server type.
    """
    def __init__(self, name, cinst = Drop):
        lxu.meta.MetaServer.__init__(self, name, lx.symbol.u_DROP)
        self._cls_inst = cinst
        self._actions = []
        self._is_array = False
        self._inst = None

    def set_source_type(self, type):
        """
        """
        self.add_tag (lx.symbol.sDROP_SOURCETYPE, type)
        if type == lx.symbol.sDROPSOURCE_FILES or type == lx.symbol.sDROPSOURCE_FILES_SYNTH or type == lx.symbol.sDROPSOURCE_ITEMS or type == lx.symbol.sDROPSOURCE_CHANNELS or type == lx.symbol.sDROPSOURCE_COMMANDS or type == lx.symbol.sDROPSOURCE_FORMCONTROLS:
            self._is_array = True

    def add_action(self, name, action, custom = False):
        """Actions are added one at a time. The name is the key used for the
           default action name in the message table. Custom drop actions can
           add their own actions, but are not mappable.
        """
        action._name = name
        action._custom = custom
        self._actions.append(action)

    def alloc_inst(self):
        """(internal) Allocate the instance and set actions to use it.
        """
        if not self._inst:
            self._inst = self._cls_inst()
            for act in self._actions:
                act._drop = self._inst

        return self._inst

    def alloc(self):
        """(internal) We set the index of each action and build
           the tag string that identifies non-custom actions
        """
        self._imax = 0
        tag = None
        for act in self._actions:
            if act._custom:
                act._index = None
            else:
                act._index = self._imax
                self._imax = self._imax + 1

                if tag:
                    tag = tag + ' '
                else:
                    tag = ''

                tag += str(act._index) + '@' + act._name

        self.add_tag(lx.symbol.sDROP_ACTIONNAMES, tag)

        return impl_Server


