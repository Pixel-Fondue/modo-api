#!/usr/bin/env python

#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.

import lx


class Meta(object):
    """The base class for metaclass nodes defines their core features. They have a
       type given by one of the pre-defined type strings, they have an optional
       name, and an optional guid. The are arranged into a tree, and the tree
       can be searched for matching meta nodes.
    """
    class Types(object):
        def __init__(self):
            self.ROOT = "(root)"
            self.SERVER = "server"
            self.OBJECT = "object"
            self.INTERFACE = "interface"
            self.ATTRDESC = "attrdesc"
            self.EVALUATOR = "evaluator"

    def __init__(self):
        self.types     = Meta.Types()
        self._type     = None
        self._name     = None
        self._guid     = None
        self._parent   = None
        self._sub_list = []

    def add(self, sub):
        """Add another meta object as a child of this one.
        """
        self._sub_list.append(sub)
        sub._parent = self

    def flatten(self):
        """Return this meta and all sub-metas in a list.
        """
        list = [self]
        for sub in self._sub_list:
            list += sub.flatten()
        return list

    def test(self, type, guid):
        """Test this meta node against a type and guid and return true for match.
           All testing allows for type or guid to be None for wildcard.
        """
        if (type and type != self._type):
            return False

        return (not guid or guid == self._guid)

    def find_sub(self, type, guid = None):
        """Find first node with a matching type/guid under this node.
        """
        for sub in self._sub_list:
            if (sub.test(type, guid)):
               return sub

        for sub in self._sub_list:
            f = sub.find_sub(type, guid)
            if (f):
                return f

        return None

    def find_any(self, type, guid = None, miss = None):
        """Find a node with matching type/guid, searching first inside this node
           but searching higher up the tree until somthing matches.
        """
        if (self.test(type, guid)):
            return self

        for sub in self._sub_list:
            if (sub is miss):
                continue

            if (sub.test(type, guid)):
                return sub

            f = sub.find_sub(type, guid)
            if (f):
                return f

        if (self._parent):
            return self._parent.find_any(type, guid, self)

        return None

    def get_ifcs(self, guid):
        """Get the list of interfaces matching the given guid under this node.
           The list is returned as tuples: ((class, meta), ...)
        """
        t = []
        for sub in self.flatten():
            if (sub is not self and sub._type == self.types.INTERFACE and sub._guid == guid):
                t.append( (sub.alloc(), sub) )

        if (len(t) == 0):
            return None
        else:
            return tuple(t)

    def init_ifcs(self, guid = None):
        """Initialize the _sub_ifcs attribute as a list of interfaces. If no
           guid is given we use the metaclass guid itself.
        """
        if (not guid):
            guid = self._guid

        self._sub_ifcs = self.get_ifcs(guid)

    def pre_init(self):
        """Do any self-modification or other steps before initialization. Return
           true as long as there is more to do.
        """
        return False

    def alloc(self):
        """Return the signature for this metaclass. Depends on type.
        """
        return None

    def __str__(self):
        """Convert node to string based on standard parameters.
        """
        s = self._type
        if (self._name):
            s += ':' + self._name
        if (self._guid):
            s += ' [' + self._guid + ']'
        return s

    def dump(self, prefix = ""):
        """Output the contents of the meta node tree with indenting.
        """
        lx.out(prefix + str(self))
        prefix = prefix + '    '
        for sub in self._sub_list:
            sub.dump(prefix)


class MetaServer(Meta):
    """The server meta node defines a plug-in server. The name and class guid
       must be specified, and the alloc() method (defined by the client, returns
       the server class. There is also a dictionary of server tags.
    """
    def __init__(self, name, guid):
        Meta.__init__(self)
        self._type     = self.types.SERVER
        self._name     = name
        self._guid     = guid
        self._tag_dict = {}

    def add_tag(self, key, value):
        self._tag_dict[key] = value

    def set_username(self, base, key = None):
        if key:
            if not base:
                base = self._name

            base = '@' + base + '@' + key + '@'

        self.add_tag(lx.symbol.sSRV_USERNAME, base)


class MetaInterface(Meta):
    """The interface meta node is a sub-interface for an object or server
       of the same guid.
    """
    def __init__(self, guid):
        Meta.__init__(self)
        self._type = self.types.INTERFACE
        self._guid = guid


class MetaObject(Meta):
    """The object meta node creates standalone objects that aren't servers.
    """
    def __init__(self, guid):
        Meta.__init__(self)
        self._type = self.types.OBJECT
        self._guid = guid

    def spawn(self):
        """Allocate a new instance of the COM object.
        """
        cls = self.alloc()
        return cls(self)

    def extract(self, com):
        """Get the implementation class object from the COM object.
        """
        return com._inst


root_list = []

class MetaRoot(Meta):
    """The root meta node is the ultimate parent of all other nodes, and it
       has an additional method to initialize all other sub-nodes. This can
       be called manually, or if not it will be called automatically.
    """
    def __init__(self, *subs):
        """Creating the root can take a list of the sub metaclasses to add.
        """
        Meta.__init__(self)
        self._type = self.types.ROOT
        self._done = False
        self._dbg  = None
        root_list.append(self)
        for sub in subs:
            self.add(sub)

    def debug(self, text):
        """Debuging can be enabled to see the tree in the event log.
        """
        self._dbg = text

    def initialize(self):
        if (self._done):
            return

        self._done = True

        isdone = {}
        any = True
        while any:
            any = False
            for m in self.flatten():
                if m not in isdone:
                    any = True
                    if not m.pre_init():
                        isdone[m] = 1

        if (self._dbg):
            lx.out("+-- init " + self._dbg)
            self.dump("|   ")

        for m in self.flatten():
            if (m._type == self.types.SERVER):
                mcls = m.alloc()
                lx.bless(mcls, m._name, m._tag_dict, m)


def InitAll():
    """This is called to init all root metaclasses. Called from lxserv after
       importing all lxserv modules.
    """
    for root in root_list:
        root.initialize()


