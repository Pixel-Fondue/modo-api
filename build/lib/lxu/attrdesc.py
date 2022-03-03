
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.

import lx
import lxu
import lxu.object


def _writable_attr_value(attr, index):
    """Helper function to get a Value object from attr index.
    """
    v = attr.Value(index, 1)
    try:
        val = lxu.object.Value(v)
    except:
        val = v

    return val


class AttributeDescVector(object):
    def __init__(self, attr, index, vector):
        self._output = []
        for i in range(len(vector)):
            val = _writable_attr_value(attr, index + i)
            self._output.append(val)
            setattr(self, vector[i], val)

    def Set(self, vector):
        for i in range(len(vector)):
            self._output[i].SetFlt(vector[i])


class AttributeDescData(object):
    pass


class CustomChannelUI(object):
    """This class can be specialized by the client for custom UI behaviors
       on specific channels.
    """
    def __init__(self):
        self.channel_name = None

    def enabled(self, item, read, msg):
        """Implement this method to return false when the channel is disabled.
           The message can also be set.
        """
        return True

    def hints(self, hints):
        """Implement this method to set hints on the UIHints object. If this
           returns true then it overrides any other default hints.
        """
        return False

    def uivalue(self):
        """Implement this method to return a new UIValueHints object for
           the channel.
        """
        pass


class AttributeDesc(object):
    """ This is equivalent to the CLxAttributeDesc class."""

    #
    # Attr object holds the state of a single attribute in the list.
    #
    class Attr(object):
        def __init__(self, name, type):
            self.name = name
            self.type = type
            self.index = -1
            self.is_channel = True
            self.vector = None
            self.text_hint = None
            self.def_val = None
            self.eval_ok = False
            self.chmod_type = 0
            self.nodal_ok = False
            self.vmin = None
            self.vmax = None
            self.chan_deps = []
            self.chan_cust = None
            self.chan_flags = 0
            self.arg_flag = 0

    #
    # General list setup methods. Client adds first then set more settings
    # on the current (last) attribute.
    #

    def __init__(self):
        self._attrs = []
        self._byname = {}
        self._cur = None
        self._val_S = lx.service.Value()
        self._need_ui = False

    def add(self, name, type):
        """Add an attribute to the end of the attribute list.
        Takes a name and value type string.

        """
        self._cur = self.Attr(name, type)
        self._cur.itype = self._val_S.ValueType(type)
        self._cur.index = len(self._attrs)
        self._attrs.append (self._cur)
        self._byname[name] = self._cur

    def default_val(self, val):
        """Set the default value for the attribute."""
        self._cur.def_val = val

    def vector_type(self, vtype):
        """Set the optional vector type for an attribute."""
        self._cur.vector = vtype
        for suffix in vtype:
            self._byname[self._cur.name + '.' + suffix] = self._cur

    def set_hint(self, hint):
        """Set the optional hint vector for an attribute."""
        self._cur.text_hint = hint

    def eval_flag(self, flag = lx.symbol.fECHAN_READ):
        """Set evaluation flags for a channel attribute."""
        self._cur.eval_ok = True
        self._cur.eval_flag = flag

    def arg_flag(self, flag):
        """Set argument flags for a command argument attribute."""
        self._cur.arg_flag = flag

    def eval_time(self):
        """Add time as an evaluation attribute."""
        self.add('_time', lx.symbol.sTYPE_TIME)
        self._cur.is_channel = False
        self._cur.eval_ok = True
        self._cur.eval_flag = lx.symbol.fECHAN_READ

    #
    # UI customization methods.
    #

    def chan_add_dependency(self, channel, itemtype = None):
        self._need_ui = True
        self._cur.chan_deps.append((itemtype, channel))

    def chan_set_custom(self, cust):
        self._need_ui = True
        self._cur.chan_cust = cust
        cust.channel_name = self._cur.name

    def chan_flags(self, fl = lx.symbol.fUIHINTCHAN_SUGGESTED):
        self._need_ui = True
        self._cur.chan_flags = fl

    def set_min(self, minval):
        self._need_ui = True
        self._cur.vmin = minval

    def set_max(self, maxval):
        self._need_ui = True
        self._cur.vmax = maxval

    #
    # Access methods
    #

    def count(self):
        """Get the number of attributes.
        """
        return len(self._attrs)

    def by_index(self, index):
        """Get the name of an attribute by index.
        """
        return self._attrs[index].name

    def by_name(self, name):
        """Get the index of an attribute by name.
        """
        return self._byname[name].index

    #
    # Channel methods -- the attributes are the channels on a package definition.
    #

    def need_chan_ui(self):
        return self._need_ui

    def setup_channels(self, add_obj):
        """Setup the channels for a package using the description."""
        ac = lxu.object.AddChannel(add_obj)

        for t in self._attrs:
            if not t.is_channel:
                continue

            ac.NewChannel(t.name, t.type)

            if (t.text_hint):
                ac.SetHint(t.text_hint)

            if (t.vector):
                ac.SetVector(t.vector)

            if (t.def_val):
                if (t.itype == lx.symbol.i_TYPE_STRING):
                    ac.SetStorage(t.type)
                    dv = ac.SetDefaultObj()
                    dv.SetString(t.def_val)
                else:
                    ac.SetDefault (float(t.def_val), int(t.def_val))

            if (t.type == lx.symbol.sTYPE_MATRIX4):
                ac.SetStorage(t.type)

    def eval_attach(self, eval, item):
        """Attach channels to an Evaluation, returing base index.
        """
        eval = lxu.object.Evaluation(eval)

        base = None
        for t in self._attrs:
            if not t.eval_ok:
                continue

            if not t.is_channel:
                idx = eval.ReadTime()
            elif t.vector:
                for suffix in t.vector:
                    idx = eval.AddChannelName(item, t.name + '.' + suffix, t.eval_flag)
                    if base is None:
                        base = idx
            else:
                idx = eval.AddChannelName(item, t.name, t.eval_flag)

            if base is None:
                base = idx

        return base

    def eval_read(self, attr, base):
        """Read eval channels from Attributes (already cast for speed) and base
           index, returing an object with named attributes. Types will match the
           intrinsic type for read, and will be value objects for write.
        """
        data = AttributeDescData()

        for t in self._attrs:
            if not t.eval_ok:
                continue

            step = 1

            if t.eval_flag & lx.symbol.fECHAN_WRITE:
                if t.vector:
                    val = AttributeDescVector(attr, base, t.vector)
                    step = len(t.vector)
                else:
                    val = _writable_attr_value(attr, base)

            elif t.vector:
                val = []
                step = len(t.vector)
                for i in range(step):
                    val.append(attr.GetFlt(base + i))

            elif t.itype == lx.symbol.i_TYPE_FLOAT:
                val = attr.GetFlt(base)

            elif t.itype == lx.symbol.i_TYPE_INTEGER:
                val = attr.GetInt(base)

            elif t.itype == lx.symbol.i_TYPE_STRING:
                val = attr.GetString(base)

            else:
                v = attr.Value(base, 0)
                try:
                    val = lxu.object.Value(v)
                except:
                    val = v

            setattr(data, t.name, val)
            base += step

        return data

    def chan_enabled(self, name, item, read, msg):
        if name not in self._byname:
            return

        attr = self._byname[name]
        if not attr.chan_cust:
            return

        item = lxu.object.Item(item)
        read = lxu.object.ChannelRead(read)
        msg = lxu.object.Message(msg)
        if attr.chan_cust.enabled(item, read, msg):
            return

        msg.SetCode(lx.result.CMD_DISABLED)
        lx.throw(lx.result.CMD_DISABLED)

    def chan_dep_count(self, name):
        if name not in self._byname:
            return 0

        attr = self._byname[name]
        return len(attr.chan_deps)

    def chan_dep_byindex(self, name, index):
        attr = self._byname[name]
        return attr.chan_deps[index]

    def chan_uihints(self, name, obj):
        if name not in self._byname:
            return

        attr = self._byname[name]
        hint = lxu.object.UIHints(obj)
        if attr.chan_cust:
            if attr.chan_cust.hints(hint):
                return

        isint = (attr.itype == lx.symbol.i_TYPE_INTEGER)

        if attr.vmin is not None:
            if isint:
                hint.MinInt(attr.vmin)
            else:
                hint.MinFloat(attr.vmin)

        if attr.vmax is not None:
            if isint:
                hint.MaxInt(attr.vmax)
            else:
                hint.MaxFloat(attr.vmax)

        if attr.chan_flags:
            hint.ChannelFlags(attr.chan_flags)

    def chan_uivalue(self, name):
        if name not in self._byname:
            return

        attr = self._byname[name]
        if attr.chan_cust is not None:
            return attr.chan_cust.uivalue()

    #
    # Channel modifier methods. The attributes are the channels on a chan mod.
    #

    def chmod_value(self, flags = 0):
        """Set the attribute to be accessed from a channel modifier as a Value."""
        self._cur.chmod_type = 1
        self._cur.chmod_flags = (flags & ~lx.symbol.fCHMOD_MULTILINK)

    def chmod_array(self, flags = 0):
        """Set the attribute to be accessed from a channel modifier as a ValueArray."""
        self._cur.chmod_type = 2
        self._cur.chmod_flags = (flags | lx.symbol.fCHMOD_MULTILINK)

    def chmod_matrix(self, flags = 0):
        """Set the attribute to be accessed from a channel modifier as a Matrix."""
        self._cur.chmod_type = 3
        self._cur.chmod_flags = flags

    def chmod_time(self):
        """Add time as a channel modifier input."""
        self.add('-time-', lx.symbol.sTYPE_TIME)
        self._cur.is_channel = False
        self._cur.chmod_type = 4

    def chmod_define(self, cmod):
        """Define the inputs and outputs of a channel modifier."""
        setup = lx.object.ChannelModSetup(cmod)

        for t in self._attrs:
            if (t.chmod_type == 4):
                setup.AddTime()
            elif (t.chmod_type != 0):
                if (t.vector):
                    for ext in t.vector:
                        setup.AddChannel(t.name + '.' + ext, t.chmod_flags)
                else:
                    setup.AddChannel(t.name, t.chmod_flags)

    def chmod_bind(self, cmod):
        """Bind the channel modifier to data object."""
        setup = lx.object.ChannelModSetup(cmod)

        data = AttributeDescData()

        for t in self._attrs:
            if (t.chmod_type == 0):
                continue

            isout = (t.chmod_flags & lx.symbol.fCHMOD_OUTPUT)

            if (t.chmod_type == 4):
                x = setup.ReadTimeValue()
            elif (t.chmod_type == 2):
                x = setup.ReadArray (t.name)
            elif (t.vector):
                a = []
                for ext in t.vector:
                    f = t.name + '.' + ext
                    if (isout):
                        x = setup.WriteValue (f)
                    else:
                        x = setup.ReadValue (f)

                    a.append(x)

                x = tuple(a)
            else:
                if (isout):
                    x = setup.WriteValue (t.name)
                else:
                    x = setup.ReadValue (t.name)

                if (t.chmod_type == 3):
                    x = lxu.object.Matrix(x)

            setattr(data, t.name, x)

        return data

    #
    # Command argument methods.
    #

    def setup_args(self, cmd):
        """Set command arguments from attributes.
        """
        for t in self._attrs:
            cmd.dyna_Add(t.name, t.type)
            cmd.dyna_SetFlags(t.index, t.arg_flag)
            if (t.text_hint):
                cmd.dyna_SetHint(t.index, t.text_hint)

    def read_args_isset(self, attr, data = None):
        """Read command argument "set" status into struct.
        """
        if not data:
            data = AttributeDescData()

        for t in self._attrs:
            val = attr.dyna_IsSet(t.index)
            setattr(data, t.name + "_isset", val)

        return data

    def read_args(self, attr):
        """Read command arguments into struct.
        """
        data = AttributeDescData()

        for t in self._attrs:
            if t.itype == lx.symbol.i_TYPE_FLOAT:
                val = attr.dyna_Float(t.index, t.def_val)

            elif t.itype == lx.symbol.i_TYPE_INTEGER:
                val = attr.dyna_Int(t.index, t.def_val)

            elif t.itype == lx.symbol.i_TYPE_STRING:
                val = attr.dyna_String(t.index, t.def_val)

            else:
                val = attr.attr_Value(t.index, 0)

            setattr(data, t.name, val)

        return self.read_args_isset(attr, data)

    def dialog_init(self, attr):
        """Initialize command dialog.
        """
        for t in self._attrs:
            if t.def_val and not attr.dyna_IsSet(t.index):
                if t.itype == lx.symbol.i_TYPE_FLOAT:
                    attr.attr_SetFlt(t.index, t.def_val)

                elif t.itype == lx.symbol.i_TYPE_INTEGER:
                    attr.attr_SetInt(t.index, t.def_val)

                elif t.itype == lx.symbol.i_TYPE_STRING:
                    attr.attr_SetString(t.index, t.def_val)



