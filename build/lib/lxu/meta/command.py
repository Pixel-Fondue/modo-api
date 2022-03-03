#!/usr/bin/env python
#
# Command metaclasses
#
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.

import lx
import lxu
import lxu.attributes
import lxu.attrdesc
import lxu.object
import lxifc
import traceback
from lxu.meta.meta import MetaServer
from lxu.command import NotifierHost


class CustomArgument(object):
    """Base class for implementing custom command argument behaviors.
    """
    def query(self, cmd):
        """Implement to return a list of query results.
        """
        return []

    def type(self, cmd):
        """Implement to set the variable type.
        """
        return None

    def enabled(self, cmd):
        """Implement to enable or disable the argument.
        """
        return True


class Command(object):
    """Base class for defining Command servers. The client will
       subclass this base class, filling in the methods that they require.
       It's then instantiated as a metaclass to be promoted to server.
    """
    def __init__(self):
        self._e_flags = 0
        self._is_err = None
        self._meta = None
        self._desc = None
        self._msg = None
        self._tmpmsg = None

    def setup_args(self, desc):
        """Implement to define command arguments.
        """
        pass

    def enabled(self):
        """Implement to test if your command is enabled.
        """
        return True

    def interact(self):
        """Implement to do user interaction.
        """
        pass

    def preflight(self):
        """Implement to test your command for execution before starting.
        """
        pass

    def execute(self):
        """Implement to execute your command.
        """
        pass

    def notifiers(self):
        """Implement to add notifiers to your command.
        """
        pass

    def button_name(self):
        """Implement to return custom button or icon names.
        """
        return None

    def icon_name(self):
        """Implement to return custom button or icon names.
        """
        return None

    def cmd_arg_custom(self, cust):
        """Call during argument setup to customize the current argument.
        """
        self._meta._cust_map[self._desc.count() - 1] = cust

    def cmd_exec_flags(self):
        """Call to get execution flags.
        """
        return self._e_flags

    def cmd_interaction_ok(self, err = False):
        """Call to test if interaction is OK. If error is true the command fails.
        """
        if self._e_flags & lx.symbol.fCMD_EXEC_GETARGS or self._e_flags & lx.symbol.fCMD_EXEC_ALWAYSGETARGS:
            return True

        if err:
            lx.throw(lx.result.CMD_REQUIRES_USER_INTERACTION)

    def cmd_read_args(self):
        """Call to read all argument values.
        """
        return self._desc.read_args(self._args)

    def cmd_read_args_isset(self):
        """Call to read all argument 'isset' values.
        """
        return self._desc.read_args_isset(self._args)

    def cmd_set_arg(self, name, value):
        """Call to set the value of an argument.
        """
        self._args.attr_Set(value) // dyna_Set(value)

    def cmd_args(self):
        """Call to access arguments directly.
        """
        return self._args

    def cmd_message(self, key = None):
        """Call to get the message for the command, or -- if the key is set
           -- set the message key.
        """
        if self._tmpmsg:
            m = self._tmpmsg
        else:
            if not self._msg:
                self._msg = lx.service.Message().Allocate()
            m = self._msg

        if key is not None:
            m.SetMessage(self._meta._name, key, 0)

        return m

    def cmd_error(self, err = lx.result.FAILED, key = None):
        """Call to raise an error with optional message key.
        """
        self.cmd_message(key)
        self._is_err = True
        lx.throw(err)

    def cmd_add_notifier(self, name, args):
        """Call to add a notifier for this command.
        """
        self._nhost.add(name, args)


class impl_Command(lxifc.Command, lxu.attributes.DynamicArguments):
    """This internal class implements the actual Command server.
       It defers to the metaclass state and the client subclass for specific
       behaviors.
    """
    def __init__(self, meta):
        lxu.attributes.DynamicArguments.__init__(self)
        self._meta = meta
        self._inst = meta._cls_inst()
        self._inst._meta = meta
        self._inst._args = self
        self._nhost = None
        self._narg = -1

        if not meta._desc:
            meta._desc = lxu.attrdesc.AttributeDesc()
            self._inst._desc = meta._desc
            self._inst.setup_args(meta._desc)
        else:
            self._inst._desc = meta._desc

        meta._desc.setup_args(self)

    # Global state
    #
    def cmd_Flags(self):
        return self._meta._flags

    def cmd_Message(self):
        return self._inst.cmd_message()

    def cmd_ButtonName(self):
        return self._inst.button_name()

    def cmd_Icon(self):
        return self._inst.icon_name()

    # Argument methods
    #
    def cmd_ArgFlags(self, index):
        return self.dyna_GetFlags(index)

    def cmd_ArgClear(self, index):
        self.dyna_Clear(index)

    def cmd_ArgResetAll(self):
        self.dyna_ClearAll()

    def cmd_ArgSetDatatypes(self):
        self.dyna_SetVariable()

    def dyna_GetType(self, index):
        if index in self._meta._cust_map:
            cust = self._meta._cust_map[index]
            return cust.type(self._inst)

    def _enable_result(self, enab, msg = None):
        if not enab:
            if not msg:
                msg = self._inst.cmd_message()

            msg.SetCode(lx.result.CMD_DISABLED)
            lx.throw(lx.result.CMD_DISABLED)

    def cmd_ArgEnable(self, index):
        if index in self._meta._cust_map:
            cust = self._meta._cust_map[index]
            self._enable_result(cust.enabled(self._inst))

    # Execution cycle
    #
    def cmd_Enable(self, msg):
        self._inst._tmpmsg = lxu.object.Message(msg)
        try:
            enab = self._inst.enabled()
        except:
            self._inst._tmpmsg = None
        else:
            m = self._inst._tmpmsg
            self._inst._tmpmsg = None
            self._enable_result(enab, m)

    def cmd_DialogInit(self):
        self._meta._desc.dialog_init(self)

    def cmd_Interact(self):
        try:
            self._inst.interact()
        except:
            self._inst.cmd_message().SetCode(lx.excResult())

    def cmd_PreExecute(self):
        try:
            self._inst.preflight()
        except:
            self._inst.cmd_message().SetCode(lx.excResult())

    def cmd_Execute(self, flags):
        try:
            self._inst._e_flags = flags
            self._inst._is_err = False
            self._inst.execute()
        except:
            rc = lx.excResult()
            if not self._inst._is_err:
                lx.out(traceback.format_exc())

            self._inst.cmd_message().SetCode(rc)

    def cmd_Query(self, index, vaQuery):
        if index not in self._meta._cust_map:
            lx.throw(lx.result.NOTFOUND)

        cust = self._meta._cust_map[index]
        res = cust.query(self._inst)

        va = lxu.object.ValueArray(vaQuery)
        for r in res:
            va + r

    # Notifiers
    #
    def cmd_NotifyAddClient(self, argidx, object):
        if not self._nhost:
            self._nhost = NotifierHost()
            for p in self._meta._note_list:
                self._nhost.add(p[0], p[1])

            self._inst._nhost = self._nhost
            self._inst.notifiers()

        if argidx > -1:
            if self._narg > -1:
                lx.throw(lx.result.NOACCESS)

            self._narg = argidx
            self._nhost.set_arg(self, argidx)

        self._nhost.add_client(object)

    def cmd_NotifyRemoveClient(self, object):
        self._nhost.rem_client(object)


class Meta_Command(MetaServer):
    """This is the metaclass for the Command server type.
    """
    def __init__(self, name, cinst = Command):
        lxu.meta.MetaServer.__init__(self, name, lx.symbol.u_COMMAND)
        self._cls_inst = cinst
        self._note_list = []
        self._cust_map = {}
        self._flags = 0
        self._desc = None

    def set_type_flags(self, flags):
        self._flags = self._flags | flags

    def set_type_model(self):
        self.set_type_flags(lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO)

    def set_type_UI(self):
        self.set_type_flags(lx.symbol.fCMD_UI)

    def add_notifier(self, name, args):
        """Notifiers that don't vary with arguments can be added here.
        """
        self._note_list.append( (name, args) )

    def alloc(self):
        """Internal metaclass method.
        """
        return impl_Command



