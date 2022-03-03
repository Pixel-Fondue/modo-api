#
# Package implementations for easy package creation.
#
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.

import lx
import lxu
import lxu.object
import lxifc


class DefaultPackageInstance(lxifc.PackageInstance):
    """The DefaultPackageInstance class implements a default PackageInstance
    object that does nothing.
    """
    pass


class DefaultPackage(lxifc.Package):
    """The DefaultPackage class implements the Attach() and TestInterface() methods
    for a package. The PackageInstance does nothing remarkable.
    """
    def pkg_Attach(self):
        return DefaultPackageInstance()

    def pkg_TestInterface(self,guid):
        return (guid == lx.symbol.u_PACKAGEINSTANCE)


class BasicItemBehaviors(object):
    """The BasicItemBehaviors class can be subclassed by the client to override
    the common item behaviors in a BasicPackage.
    """
    def newborn(self, item, original, flags):
        pass

    def loading(self, item):
        pass

    def after_load(self, item):
        pass

    def doomed(self, item):
        pass

    def add(self, item):
        pass

    def remove(self, item):
        pass

    def synth_name(self, item):
        return None

    def parent_ok(self, item, parent):
        return True


class BasicPackageInstance(lxifc.PackageInstance):
    """The BasicPackageInstance class implements a PackageInstance that can be
    overridden using a BasicItemBehaviors object.
    """
    def __init__(self, acts):
        self.acts = acts
        self.item = None

    def pins_Initialize(self,item,super):
        self.item = lxu.object.Item(item)

    def pins_SynthName(self):
        if (self.acts):
            str = self.acts.synth_name(self.item)
            if (str):
                return str;

        lx.notimpl()

    def pins_TestParent(self,item):
        if (self.acts):
            return self.acts.test_parent(self.item, item)

    def pins_Newborn(self,original,flags):
        if (self.acts):
            self.acts.newborn(self.item,original,flags)

    def pins_Loading(self):
        if (self.acts):
            self.acts.loading(self.item)

    def pins_AfterLoad(self):
        if (self.acts):
            self.acts.after_load(self.item)

    def pins_Doomed(self):
        if (self.acts):
            self.acts.doomed(self.item)

    def pins_Add(self):
        if (self.acts):
            self.acts.add(self.item)

    def pins_Remove(self):
        if (self.acts):
            self.acts.remove(self.item)


class BasicPackage(lxifc.Package):
    """The BasicPackage class implements the Attach() and TestInterface() methods,
    and can be overridden using a BasicItemBehaviors class.
    """
    def __init__(self, acts = None):
        if (acts and isinstance(acts, BasicItemBehaviors)):
            self.acts = acts
        elif (isinstance(self, BasicItemBehaviors)):
            self.acts = self
        else:
            self.acts = None

    def pkg_Attach(self):
        return BasicPackageInstance(self.acts)

    def pkg_TestInterface(self,guid):
        return (guid == lx.symbol.u_PACKAGEINSTANCE)



