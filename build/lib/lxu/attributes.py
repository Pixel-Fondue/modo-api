
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.

import lx
import lxifc


class DynamicAttributes(lxifc.Attributes, lxifc.AttributesUI):
    """ This is equivalent to the CLxDynamicAttributes class."""
    def __init__(self):
        self.val_svc = lx.service.Value()
        self._attrs = []
        self._index = {}
        self._hints = {}
        self._flags = {}

    def dyna_Add(self, name, type):
        """Add an attribute to the end of the attribute list.
        Takes a name and value type string.

        """
        self._index[name] = len(self._attrs)
        self._attrs.append( (name, type, None) )

    def dyna_SetType(self, index, type):
        """Change the value type for an attribute by index.
        Setting it to None clears the stored value without changing the type.

        """
        t = self._attrs[index]
        if type == None:
            type = t[1]
        self._attrs[index] = (t[0], type, None)

    def dyna_SetHint(self, index, hint):
        """Set the optional hint vector for an attribute."""
        if index < 0 or index >= len(self._attrs):
            raise IndexError('hint index out of range')

        self._hints[index] = hint

    def dyna_SetFlags(self, index, flags):
        """Set the optional flags int for an attribute."""
        if index < 0 or index >= len(self._attrs):
            raise IndexError('flags index out of range')

        self._flags[index] = flags

    def dyna_GetFlags(self, index):
        """Returns flags for an attribute by index."""
        if index in self._flags:
            return self._flags[index]
        return 0

    def dyna_IsSet(self, index):
        """Returns true if the attribute value is set."""
        return self._attrs[index][2] != None

    def attr_Count(self):
        """Returns number of attributes."""
        return len(self._attrs)

    def attr_Name(self,index):
        """Returns name of an attribute by index."""
        return self._attrs[index][0]

    def attr_Lookup(self,name):
        """Returns the index of an attribute given the name."""
        return self._index[name]

    def attr_TypeName(self,index):
        """Returns value type string of an attribute by index."""
        return self._attrs[index][1]

    def attr_Type(self,index):
        """Returns basic type of an attribute by index."""
        t = self._attrs[index]
        v = t[2]
        if v == None:
            v = self.val_svc.CreateValue(t[1])

        return v.Type()

    def attr_Hints(self, index):
        """Returns hint vector for an attribute by index."""
        if index in self._hints:
            return self._hints[index]
        return None

    def attr_Value(self,index,writeOK):
        """Get value object for an attribute.
        If writeOK is true the value will be created if it doesn't exist.
        """
        t = self._attrs[index]
        v = t[2]
        if v == None:
            if writeOK:
                v = self.val_svc.CreateValue(t[1])
                self._attrs[index] = (t[0], t[1], v)
            else:
                raise LookupError('attribute ' + str(index) + ' not found.')

        return v

    def attr_GetInt(self,index):
        return self.attr_Value(index,0).GetInt()
    def attr_SetInt(self,index,val):
        return self.attr_Value(index,1).SetInt(val)

    def attr_GetFlt(self,index):
        return self.attr_Value(index,0).GetFlt()
    def attr_SetFlt(self,index,val):
        return self.attr_Value(index,1).SetFlt(val)

    def attr_GetString(self,index):
        return self.attr_Value(index,0).GetString()
    def attr_SetString(self,index,val):
        return self.attr_Value(index,1).SetString(val)

    def dyna_Bool(self,index,value=False):
        if not self.dyna_IsSet(index):
            return value
        return self.attr_GetInt(index) != 0

    def dyna_Int(self,index,value=0):
        if not self.dyna_IsSet(index):
            return value
        return self.attr_GetInt(index)

    def dyna_Float(self,index,value = 0.0):
        if not self.dyna_IsSet(index):
            return value
        return self.attr_GetFlt(index)

    def dyna_String(self,index,value = ""):
        if not self.dyna_IsSet(index):
            return value
        return self.attr_GetString(index)

    def arg_DisableMsg(self, index, message):
        """Return true if the argument is disabled, and set the message if any.
        """
        lx.notimpl()

    def atrui_DisableMsg(self,index,message):
        message = lx.object.Message(message)
        if self.arg_DisableMsg(index, message):
            message.SetCode(lx.result.DISABLED)
            lx.throw(lx.result.DISABLED)

    def arg_UIHints(self, index, hints):
        """Set hints for the argument.
        """
        lx.notimpl()

    def atrui_UIHints(self,index,hints):
        self.arg_UIHints(index, lx.object.UIHints(hints))

    def arg_UIValueHints(self,index):
        """Return a UIValueHints object for the argument.
        """
        lx.notimpl()

    def atrui_UIValueHints(self,index):
        return self.arg_UIValueHints(index)


class DynamicArguments(DynamicAttributes):
    """ This is equivalent to the CLxDynamicArguments class."""
    def __init__(self):
        DynamicAttributes.__init__(self)

    def dyna_GetFlags(self, index):
        """Get the argument flags. This computes the VALUE_SET flag dynamically."""
        f = DynamicAttributes.dyna_GetFlags(self, index)
        if self.dyna_IsSet(index):
            f = f | lx.symbol.fCMDARG_VALUE_SET

        return f

    def dyna_HasVariable(self):
        """Test if any arguments have variable type."""
        for i in range(len(self._attrs)):
            if self.dyna_GetFlags(i) & lx.symbol.fCMDARG_VARIABLE:
                return True

        return False

    def dyna_SetVariable(self):
        """Set the type of all arguments that have variable type."""
        if not self.dyna_HasVariable():
            return

        for i in range(len(self._attrs)):
            k = self.dyna_GetFlags(i)
            if (k & lx.symbol.fCMDARG_REQFORVARIABLE) and not (k & lx.symbol.fCMDARG_VALUE_SET):
                lx.throw(lx.result.CMD_MISSING_ARGS)

        for i in range(len(self._attrs)):
            k = self.dyna_GetFlags(i)
            self.dyna_SetFlags (i, k | lx.symbol.fCMDARG_REQFORVAR_SET)
            if (k & lx.symbol.fCMDARG_VARIABLE):
                self.dyna_SetType(i, self.dyna_GetType(i))

    def dyna_GetType(self):
        """Return the type of variable type arguments (for override)."""
        return None

    def dyna_Clear(self, index):
        """Clear a single argument."""
        self.dyna_SetType(index, None)
        if not self.dyna_HasVariable() or not (self.dyna_GetFlags(index) & lx.symbol.fCMDARG_REQFORVARIABLE):
            return

        for i in range(len(self._attrs)):
            k = self.dyna_GetFlags(i)
            self.dyna_SetFlags(i, k & ~lx.symbol.fCMDARG_REQFORVAR_SET)
            if (k & lx.symbol.fCMDARG_VARIABLE):
                self.dyna_Clear(i)

    def dyna_ClearAll(self):
        """Clear all arguments."""
        for i in range(len(self._attrs)):
            self.dyna_Clear(i)




