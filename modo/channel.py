#
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.
#

"""

.. module:: modo.channel
    :synopsis: A collection of channel related classes & functions.

.. moduleauthor:: Gwynne Reddick <gwynne.reddick@thefoundry.co.uk>


"""

import lx
import lxu
from . import constants as c
from . import util


class ChannelRead(object):
    def __init__(self, scene):
        """Channel Reader object. The new reader object defaults to "evaluation" mode and time = 0.0. A different
        action or time can be set using the reader's "set" method.

        :param scene: the scene that the channel reader object belongs to.
        :type scene: modo.Scene

        """

        # scene is supposed to be type modo.Scene, but there may be old code which is passing lxu.object.Scene
        try:
            self._scene = scene.scene
        except: 
            self._scene = scene
        self._currentAction = None
        self._channelRead = scene.Channels(None, 0.0)

    def __getattr__(self, attr):
        return getattr(self._channelRead, attr)

    def set(self, action=None, time=None):
        """Initialises the channel read object with a new action and/or an explicit time to read from. If no action is
        provided the last action set is used. If no time value is provided the current time is used.

        :param action: optional action to read from.
        :type action: basestring
        :param time: optional time (in seconds) to read at.
        :type time: float

        """
        if time is None:
            time = c.SEL_SVC.GetTime()
        if action == self._currentAction:
            if time != self._channelRead.Time():
                self._channelRead.SetTime(time)
        else:
            if hasattr(self, '_channelRead'):
                del self._channelRead
            self._channelRead = self._scene.Channels(action, time)
            self._currentAction = action


class ChannelWrite(object):
    def __init__(self, scene):
        """Channel Writer object. The new writer object defaults to "edit" action and current time. A different
        action or time can be set using the writer's "init" method.

        :param scene: the scene that the channel writer object belongs to.
        :type scene: modo.Scene

        """

        # scene is supposed to be type modo.Scene, but there may be old code which is passing lxu.object.Scene
        try:
            self._scene = scene.scene
        except: 
            self._scene = scene
        self._currentAction = lx.symbol.s_ACTIONLAYER_EDIT
        self._channelRead = scene.Channels(self._currentAction, c.SEL_SVC.GetTime())
        self._channelWrite = None
        self.set()

    def __getattr__(self, attr):
        return getattr(self._channelWrite, attr)

    def set(self, action=lx.symbol.s_ACTIONLAYER_EDIT, time=None):
        """Initialises the channel write object with an action and/or a time write to. Defaults to writing to the
        "edit" action if no action is provided and to the current time if no time is provided.

        :param action: the action to write to.
        :type action: basestring
        :param time: the time to write to in seconds.
        :type time: float

        """
        if time is None:
            time = c.SEL_SVC.GetTime()
        if action == self._currentAction:
            if time != self._channelRead.Time():
                self._channelRead.SetTime(time)
        if hasattr(self, '_channelWrite'):
            del self._channelWrite
        self._channelWrite = lx.object.ChannelWrite(self._scene.Channels(action, time))


class Envelope(object):
    def __init__(self, envelope):
        """Envelope object. Wraps an lx.object.Envelope object which has methods for setting various envelope properties
        and a pointer to a :class:`Keyframes` object for manipulating the individual keys. test.

        :param env: the envelope object to wrap.
        :type env: lx.object.Envelope

        """
        self._envelope = envelope

    def __getattr__(self, attr):
        return getattr(self._envelope, attr)

    @property
    def keyframes(self):
        """Returns a :class:`Keyframes` object that provides access to the keyframes set for the envelope and methods to
        manipulate them.

        :getter: Returns a :class:`Keyframes` object containing the keys for this envelope.
        :rtype: modo.channel.Keyframes

        """
        return Keyframes(self._envelope)

    @property
    def interpolation(self):
        """Returns the interpolation setting for the envelope.  Can be one of:

            | lx.symbol.iENVv_INTERP_CURVE
            | lx.symbol.iENVv_INTERP_LINEAR
            | lx.symbol.iENVv_INTERP_STEPPED

        :getter: Returns the interpolation setting for the envelope.
        :rtype: int

        """
        return self._envelope.Interpolation()

    @interpolation.setter
    def interpolation(self, interpolation):
        self._envelope.SetInterpolation(interpolation)

    def clear(self):
        """Clears (removes all keys from) the envelope."""
        self._envelope.Clear()

    @property
    def isInt(self):
        """Returns whether the envelope is integer-valued type, if not it's a float type.

        :Getter: Returns True if the envelope is integer-valued type, False otherwise.
        :rtype: bool

        """
        if self._envelope.IsInt():
            return True
        return False

    def value(self, time=None):
        """Returns the value of the envelope evaluated at the specified time. If no time is explicitly provided the
        value of the envelope at the current time is returned

        :param time: time to evaluate envelope at.
        :type time: float
        :returns: value of the envelope
        :rtype: float for float type envelopes, int for integer-valued type envelopes

        """
        if time is None:
            time = lx.service.Selection().GetTime()
        if self._envelope.IsInt():
            return self._envelope.EvaluateI(time)
        return self._envelope.EvaluateF(time)

    @property
    def preBehaviour(self):
        """gets/sets the behavior of times before the first keyframe in the envelope.

        - **RESET** A default value, or may be just zero.
        - **CONSTANT** The value of the first or last keyframe. For first or last keys set to "Auto" or "Auto Flat" \
          the slopes of the keys will be adjusted to provide a smooth interpolation to or from the behavior.
        - **REPEAT** The values in the keyframe range repeating continuously.
        - **OSCILLATE** Like repeat, but the values run forwards and backward alternately. For first or last keys set \
          to "Auto" or "Auto Flat" the slopes of the keys will be adjusted to provide a smooth interpolation to or \
          from the behavior.
        - **OFFSETREPEAT** Like repeat, but the values are offset in each cycle by the difference between the first \
          and last keyframes. For first or last keys set to "Auto" or "Auto Flat" the slopes of the keys will be \
          adjusted to provide a smooth interpolation to or from the behavior.
        - **LINEAR** Linear interpolation from the slope at the nearest keyframe.
        - **NONE** Indicates that the envelope does not exist before or after the explicit keyframe range. This can be \
          used by motion evaluation code to decide whether to use the envelope for a channel or to look up the parent \
          envelope or default value.
        - **CONSTANT_KEEP_SLOPE** As for constant except that the slopes of the first or last keys are not changed.
        - **OSCILLATE_KEEP_SLOPE** As for oscillate except that the slopes of the first or last keys are not changed.
        - **OFFSETREPEAT_KEEP_SLOPE** As for offset repeat except that the slopes of the first or last keys are not \
          changed.

        :setter: Sets the behavior
        :param behavior: the behaviour to set for the envelope. Can be one of:

                | lx.symbol.iENV_RESET
                | lx.symbol.iENV_CONSTANT
                | lx.symbol.iENV_REPEAT
                | lx.symbol.iENV_OSCILLATE
                | lx.symbol.iENV_OFFSETREPEAT
                | lx.symbol.iENV_LINEAR
                | lx.symbol.iENV_NONE
                | lx.symbol.iENV_CONSTANT_KEEP_SLOPE
                | lx.symbol.iENV_OSCILLATE_KEEP_SLOPE
                | lx.symbol.iENV_OFFSETREPEAT_KEEP_SLOPE

        :type behavior: int

        :getter: Returns envelope behavior
        :rtype: int

        """
        return self._envelope.EndBehavior(lx.symbol.iENVSIDE_IN)

    @preBehaviour.setter
    def preBehaviour(self, behavior):
        self._envelope.SetEndBehavior(behavior, lx.symbol.iENVSIDE_IN)

    @property
    def postBehaviour(self):
        """gets/sets the behavior of times after the last keyframe in the envelope.

        :setter: Sets the envelope post behavior
        :param behavior: the behaviour to set for the envelope. See :meth:`preBehaviour` for available options.
        :type behavior: int

        :getter: Returns the envelope post behavior
        :rtype: int
        """
        return self._envelope.EndBehavior(lx.symbol.iENVSIDE_OUT)

    @postBehaviour.setter
    def postBehaviour(self, behavior):
        self._envelope.SetEndBehavior(behavior, lx.symbol.iENVSIDE_OUT)

    @property
    def behavior(self):
        """gets/sets the behavior of times for both before the first keyframe and after the last keyframe in the
        envelope.

        :setter: Sets the envelope behavior
        :param behavior: the behaviour to set for the envelope. See :meth:`preBehaviour` for available options.
        :type behavior: int

        :getter: Returns the envelope behavior
        :rtype: int
        """
        return self._envelope.EndBehavior(lx.symbol.iENVSIDE_BOTH)

    @behavior.setter
    def behavior(self, behavior):
        self._envelope.SetEndBehavior(behavior, lx.symbol.iENVSIDE_BOTH)


class Keyframes(object):
    def __init__(self, envelope):
        """Represents the keyframes present in an :class:`Envelope` object.

        Features list-like access:

            frame = lx.service.Value().FrameToTime
            item = modo.scene.current().selected[0]
            envelope = item.position.y.envelope

            envelope.keyframes.add( val=0.666, time=frame(7))

            for time, value in envelope.keyframes:
                print time, value

            envelope.keyframes[0] = frame(3), 0.333

        :param envelope: the :class:`Envelope` object.
        :type envelope: modo.channel.Envelope

        """
        self._envelope = envelope
        self._keyframe = envelope.Enumerator()

    def __getattr__(self, attr):
        # pass any unknown attribute access on to the wrapped lxu.object.Keyframe class to see if
        # it's a recognised call there.
        return getattr(self._keyframe, attr)

    @property
    def numKeys(self):
        """
        :getter: Returns the number of keyframes found
        :rtype: int
        """
        # TODO: 1 if isAnimated, 0 otherwise
        numKeys = 1
        self._keyframe.First()
        while True:
            try:
                self._keyframe.Next()
                numKeys += 1
            except LookupError:
                return numKeys
        self._keyframe.First()
        return numKeys

    def __len__(self):
        return self.numKeys

    def __getitem__(self, item):
        self.setIndex(item)
        return self.time, self.value

    def __setitem__(self, key, value):
        self.setIndex(key)
        self.time, self.value = value
        self.setIndex(0)

    def __delitem__(self, key):
        self.setIndex(key)
        self._keyframe.Delete()

    def __iter__(self):
        for i in range(self.numKeys):
            self.setIndex(i)
            yield (self.time, self.value)

        self.setIndex(0)

    def setIndex(self, index):
        """Go to the keyframe by index"""
        self._keyframe.First()
        if index:
            for i in range(index):
                self._keyframe.Next()

    def first(self):
        """Go to the first keyframe."""
        self._keyframe.First()

    def last(self):
        """Go to the last keyframe."""
        self._keyframe.Last()

    def __next__(self):
        """Go to the next keyframe."""
        self._keyframe.Next()

    def prev(self):
        """Go to the previous keyframe."""
        self._keyframe.Previous()

    def add(self, val, time=None):
        """Adds a new keyframe at the specified time. If no time value is passed as an argument a keyframe is set at
        the current time.

        :param time: optional time (in seconds) to add a keyframe at.
        :type time: float
        :param val: the value to set for the keyframe
        :type val: int or float

        """
        if time is None:
            time = lx.service.Selection().GetTime()
        if self._envelope.IsInt():
            self.AddI(time, val)
        else:
            self.AddF(time, val)

    @property
    def value(self):
        """Convenience property to get & set value of the current keyframe for the 90% case of an unbroken key.

        :setter: Sets a value
        :param val: the value to set for the key.
        :type val: int or float

        :getter: Returns the value of an (unbroken) key.
        :rtype: int or float
        """
        if self._envelope.IsInt():
            return self._keyframe.GetValueI(lx.symbol.iENVSIDE_BOTH)
        return self._keyframe.GetValueF(lx.symbol.iENVSIDE_BOTH)

    @value.setter
    def value(self, val):
        if self._envelope.IsInt():
            self._keyframe.SetValueI(val, lx.symbol.iENVSIDE_BOTH)
        else:
            self._keyframe.SetValueF(val, lx.symbol.iENVSIDE_BOTH)

    @property
    def time(self):
        """Returns & sets the time for the current keyframe.

        :setter: Sets the time
        :param time: the time to move the key to.
        :type time: float

        :getter: Returns the time of the current keyframe
        :rtype: float

        """
        return self._keyframe.GetTime()

    @time.setter
    def time(self, time):
        self._keyframe.SetTime(time)

    def getSlopeType(self, side):
        """Returns the slope type for either side of a keyframe.

        :returns: a tuple of the slope type set for the side of the keyframe specified and whether the slope is \
        weighted or not.
        :rtype: (int, int)

        """
        return self._keyframe.GetSlopeType(side)

    def setSlopeType(self, stype, side):
        """ Sets the slope type for either side of a keyframe

        - **SLOPE_DIRECT** the slope of the tangent is set based on the value stored in the key.
        - **SLOPE_AUTO** the slope of the tangent is calculated automatically with regard to surrounding keys. \
        This is similar to the slope adjustments made by TCB curves.
        - **SLOPE_LINEAR_IN** the slope of the tangent is calculated to align with the previous key's value.
        - **SLOPE_LINEAR_OUT** the slope of the tangent is calculated to align with the next key's value.
        - **SLOPE_FLAT** The slope of the tangent is set to zero.
        - **SLOPE_AUTOFLAT** the same as auto but if a neighboring key has the same value as the key the slope \
        is set to zero.
        - **SLOPE_STEPPED** Maintains the value of the previous key between pairs of keys.

        :param stype: set the slope type for the current keyframe. Can be one of:

            | lx.symbol.iSLOPE_AUTO
            | lx.symbol.iSLOPE_AUTOFLAT
            | lx.symbol.iSLOPE_DIRECT
            | lx.symbol.iSLOPE_FLAT
            | lx.symbol.iSLOPE_LINEAR_IN
            | lx.symbol.iSLOPE_LINEAR_OUT
            | lx.symbol.iSLOPE_STEPPED

        :type stype: int
        :param side: the side of the key (in or out) the slope type is being set for
        :type side: int

        """
        self._keyframe.SetSlopeType(stype, side)

    def delete(self):
        """Deletes the current key"""
        self._keyframe.Delete()
        self.setIndex(0)

    def _indexFromTime(self, time):

        index = None
        for i, values in enumerate(self):
            if util.float_equals(values[0], time):
                return i
        return None


class Channel(object):
    def __init__(self, chan, item):
        """Wraps channel access as an object. Takes a channel index or name and the item it comes from as input.

        :param chan: the channel to wrap.
        :type chan: int or basestring
        :param item: the item the channel belongs to.
        :type item: modo.item.Item

        """
        # Throw a LookupError if the channel doesn't exist
        if isinstance(chan, str):
            item.ChannelLookup(chan)

        self._item = item
        self._chan = chan
        self._index = None
        self._chanRead = None
        self._chanWrite = None
        self._envelope = None
        self._graph = None

    def __repr__(self):
        return "modo.%s('%s', %s)" % (self.__class__.__name__, self._chan, self._item)

    @property
    def type(self):
        """Returns the channel type. The numeric and gradient types can be keyframed. The return type is an int which
        translates to the following types:

            | 0: none
            | 1: integer
            | 2: float
            | 3: gradient
            | 4: storage
            | 5: eval

        :getter: Returns the channel type.
        :rtype: int

        """
        return self.item.ChannelType(self.index)

    @property
    def storageType(self):
        """Returns the storage type of the channel, which can be valid exo-type name for numeric and stored
        custom types or None if no storage type is found.

        :getter: Returns the channel storage type
        :rtype: basestring

        """
        try:
            return self.item.ChannelStorageType(self.index)
        except LookupError:
            return None

    @property
    def evalType(self):
        """Returns the evaluation type of a channel, which is the type of slot allocated in the eval state
        vector. This will return the "gradstack" exo-type for gradient channels.

        :getter: Returns the evaluation type of the channel
        :rtype: basestring

        """
        try:
            return self.item.ChannelEvalType(self.index)
        except LookupError:
            return None

    @property
    def name(self):
        """The channel's name.

        :getter: Returns the channel's name.
        :rtype: basestring

        """
        if isinstance(self._chan, int):
            return self.item.ChannelName(self._chan)
        else:
            return self._chan

    @property
    def index(self):
        """The channel's index.

        :getter: Returns the channel's index.
        :rtype: int
        """
        if self._index is None:
            if isinstance(self._chan, int):
                self._index = self._chan
            else:
                self._index = self.item.ChannelLookup(self._chan)
        return self._index

    @property
    def graph(self):
        """The channel's channel graph.

        :getter: Returns the channel's channel graph.
        :rtype: lxu.object.ChannelGraph

        """
        if self._graph is None:
            # TODO: investigate the consequences of this.
            # self.item.scene is not available when self.item is an lx.object.Item
            if hasattr(self.item, 'scene'):
                self._graph = lx.object.ChannelGraph(self.item.scene.GraphLookup(lx.symbol.sGRAPH_CHANLINKS))
            else:
                self._graph = lx.object.ChannelGraph(self.item.Context().GraphLookup(lx.symbol.sGRAPH_CHANLINKS))
        return self._graph

    def get(self, time=None, action=None):
        """Returns a channel's value for an action at a specific time. Defaults to reading the channel's evaluated
        value at the current time.

        :param time: Optional time in seconds to read the value at.
        :type time: float
        :param action: The action to read the value from. Defaults to None (evaluation).
        :type action: basestring
        :returns: the channel's value.
        :rtype: depends on the type of the channel being read.

        """
        if self._chanRead is None:
            self._chanRead = self.item.scene.chanRead
        self._chanRead.set(action, time)
        
        return self._chanRead.Value(self.item, self.index)

    def set(self, value, time=None, key=False, action='edit'):
        """Sets a channel's value for an action at a specific time. Defaults to setting the channel's value
        for the "edit" action and at the current time.

        :param value: The value to set for the channel.
        :type value: depends on the type of the channel
        :param time: optional time in seconds to set the value for.
        :type time: float
        :param key: Specifies whether to set a key for the channel.
        :type key: bool
        :param action: The action to set the value on.
        :type action: basestring

        """
        action = 'edit' if action is None else action
        
        if self._chanWrite is None:
            self._chanWrite = self.item.scene.chanWrite
        self._chanWrite.set(action, time)
        datatype = self._chanWrite.Type(self.item, self.index)

        if datatype == lx.symbol.i_TYPE_FLOAT:
            if key:
                self._chanWrite.DoubleKey(self.item, self.index, float(value), True)
            else:
                self._chanWrite.Double(self.item, self.index, float(value))

        elif datatype == lx.symbol.i_TYPE_INTEGER:
            if isinstance(value, str):
                try:
                    if key:
                        self._chanWrite.EncodedIntKey(self.item, self.index, value)
                    else:
                        self._chanWrite.EncodedInt(self.item, self.index, value)

                # If the channel has no integer hint, an exception is raised and
                # we revert to using a simple string to integer conversion
                except RuntimeError:
                    if key:
                        self._chanWrite.IntegerKey(self.item, self.index, int(value), True)
                    else:
                        self._chanWrite.Integer(self.item, self.index, int(value))
            else:
                if key:
                    self._chanWrite.IntegerKey(self.item, self.index, int(value), True)
                else:
                    self._chanWrite.Integer(self.item, self.index, int(value))

        elif datatype == lx.symbol.i_TYPE_STRING:

            # This is a workaround for bug 46391 until it gets resolved.
            # The UI does not refresh when setting a texture effect using the edit action
            self._chanWrite.set('setup', time)
            if key:
                raise RuntimeError("Can't keyframe string channels.")

            self._chanWrite.String(self.item, self.index, str(value))

        else:
            raise RuntimeError("Can't set object channels.")

    @property
    def envelope(self):
        """ Returns the channel's animation envelope.

        :getter: Returns the channel's animation envelope.
        :rtype: modo.channel.Envelope
        :raises LookupError: if the channel isn't animated.
        """

        if not self.isAnimated and self.evalType != 'gradstack':
            raise LookupError("Envelope not found, channel not animated")
        if self._envelope is None:
            if self._chanWrite is None:
                self._chanWrite = self.item.scene.chanWrite
            if self.evalType == 'gradstack':
                # Workaround for bug 47584 - keyframe edits lost after re-opening scene
                # This happens when the keys were inserted with the 'edit' and the scene is saved while the scene is still in flux
                self._chanWrite.set(lx.symbol.s_ACTIONLAYER_SETUP, 0.0)
            else:
                self._chanWrite.set(lx.symbol.s_ACTIONLAYER_EDIT, 0.0)
            self._envelope = Envelope(self._chanWrite.Envelope(self.item, self.index))

        return self._envelope

    @property
    def isAnimated(self):
        """Returns whether the channel is animated.

        :getter: Returns whether the channel is animated or not.
        :rtype: bool

        """
        if self.item.scene.chanRead.IsAnimated(self.item, self.index):
            return True
        else:
            return False

    @property
    def fwdCount(self):
        """Returns the number of linked channels forward of this channel in this channel graph.

        :getter: Returns the number of linked channels forward of this channel in this channel graph.
        :rtype: int

        """
        return self.graph.FwdCount(self.item, self.index)

    @property
    def revCount(self):
        """Returns the number of linked channels that occur before this channel in the channel graph.

        :getter: Returns the number of linked channels that occur before this channel in the channel graph.
        :rtype: int

        """
        return self.graph.RevCount(self.item, self.index)

    def forward(self, index):
        """Returns the linked channel at the specified index forward of this channel in the channel graph.

        :param index: The index of the channel to return.
        :type index: int
        :returns: The channel at specified index forward of this channel.
        :rtype: modo.channel.Channel

        """
        item, channel = self.graph.FwdByIndex(self.item, self.index, index)
        name = item.ChannelName(channel)
        itemfunc = util.typeToFunc(item.Type())
        lxu_item = item.Context().ItemLookupIdent(item.Ident())
        return Channel(name, itemfunc(lxu_item))

    def reverse(self, index):
        """Returns the linked channel at the specified index before this channel in the channel graph.

        :param index: The index of the channel to return.
        :type index: int
        :returns: The channel at specified index before of this channel.
        :rtype: modo.channel.Channel

        """
        item, channel = self.graph.RevByIndex(self.item, self.index, index)
        name = item.ChannelName(channel)
        itemfunc = util.typeToFunc(item.Type())
        lxu_item = item.Context().ItemLookupIdent(item.Ident())
        return Channel(name, itemfunc(lxu_item))

    @property
    def fwdLinked(self):
        """Returns a list of the linked channels forward of this channel in the channel graph.

        :getter: Returns the forward channels in this item's channel graph.
        :rtype: list

        """
        linked = []
        for x in range(self.graph.FwdCount(self.item, self.index)):
            item, channel = self.graph.FwdByIndex(self.item, self.index, x)
            name = item.ChannelName(channel)
            itemfunc = util.typeToFunc(item.Type())
            lxu_item = item.Context().ItemLookupIdent(item.Ident())
            linked.append(Channel(name, itemfunc(lxu_item)))
        return linked

    @property
    def revLinked(self):
        """Returns a list of the linked channels that appear before this channel in the channel graph.

        :getter: Returns the linked channels that appear before this channel in the channel graph.
        :rtype: list

        """
        linked = []
        for x in range(self.graph.RevCount(self.item, self.index)):
            item, channel = self.graph.RevByIndex(self.item, self.index, x)
            name = item.ChannelName(channel)
            itemfunc = util.typeToFunc(item.Type())
            lxu_item = item.Context().ItemLookupIdent(item.Ident())
            linked.append(Channel(name, itemfunc(lxu_item)))
        return linked

    def addLink(self, to_channel):
        """Add a link between this channel and another.

        :param to_channel: The channel to link to.
        :type to_channel: modo.channel.Channel

        """
        self.graph.AddLink(self.item, self.index, to_channel.item, to_channel.index)

    def setLink(self, from_index, to_channel, to_index):
        """Set a link's position (from index, to index) in the channel graph.

        :param from_index: The index in the channel graph for the current (from) channel.
        :type from_index: int
        :param to_channel: The to channel.
        :type to_channel: modo.channel.Channel
        :param to_index: the index in the channel graph for the 'to' channel.
        :type to_index: int

        """
        self.graph.SetLink(self.item, self.index, from_index, to_channel.item, to_channel.index, to_index)

    def deleteLink(self, to_channel):
        """Delete a link from the channel graph.

        :param to_channel: The channel the link is to.
        :type to_channel: modo.channel.Channel

        """
        self.graph.DeleteLink(self.item, self.index, to_channel.item, to_channel.index)

    def __rshift__(self, other):
        """>> operator for connecting to another channel

        :param Channel other:
        """
        if not isinstance(other, Channel):
        # if not str(other.__class__) == str(Channel):
            raise AttributeError("The input type must be a channel")

        other.connectInput(self)

    def connectInput(self, other):

        if not isinstance(other, Channel):
        # if not str(other.__class__) == str(Channel):
            raise AttributeError("The input type must be a channel")
        self.graph.AddLink(other.item, other.index, self.item, self.index)

    def __lshift__(self, other):
        """<< operator for disconnecting from another channel

        :param Channel other: Connected channel to disconnect from
        """

        if not isinstance(other, Channel):
            raise AttributeError("The input type must be a channel")
        self.disconnectInput(other)

    def disconnectInput(self, other=None):
        """Removes an input connection from another channel if it exists.

        :param Channel other: Other channel to disconnect from. If it is None, all input connections are removed.
        """
        if other:
            if not isinstance(other, Channel):
                raise AttributeError("The input type must be a channel")
            self.deleteLink(other)
        else:
            for channel in self.revLinked:
                channel.deleteLink(self)

    @property
    def item(self):
        """

        :getter: Returns the item that is associated with this channel
        :rtype: Item
        """
        return self._item


class ChannelTriple(object):
    """Wrapper to allow setting and reading all three channels on a vector 'channel' at once

    :param basestring channelName: The channel name. eg 'diffCol'
    :param modo.item.Item item: The item the channel belongs to.

    :raises: LookUpError if no respective channel of the given name was found
    """
    def __init__(self, item, channelName):
        extension = None

        channels = set([item.ChannelName(index) for index in range(item.ChannelCount())])

        # XYZ
        if ('%s.X' % channelName) in channels:
            extension = ('X', 'Y', 'Z')

        # RGB
        elif ('%s.R' % channelName) in channels:
            extension = ('R', 'G', 'B')

        if extension:
            self._channels = [item.channel('%s.%s' % (channelName, extension)) for extension in extension]
            return

        # If nothing found raise error
        raise LookupError

    def get(self, *args, **kwargs):
        """Same arguments as Channel.get()
        """
        return tuple([channel.get(*args, **kwargs) for channel in self._channels])

    def set(self, values, time=None, action='edit'):
        """Sets three values for the three channels at once

        :param float time: Time in seconds for the value to be set at (optional)
        :param basestring action: Action to set the value for (optional)
        """
        for channel, value in zip(self._channels, values):
            channel.set(value, time, action=action)


