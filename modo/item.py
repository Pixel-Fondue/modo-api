#
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.
#

"""

.. module:: modo.item
   :synopsis: Item classes.

.. moduleauthor:: Gwynne Reddick <gwynne.reddick@thefoundry.co.uk>

"""

import lxu
import lxu.select
import lxu.object
from . import scene
from .channel import *
from .mathutils import Vector3, Matrix4
from fnmatch import fnmatch
from .meshgeometry import MeshGeometry
from collections import Iterable

# Don't import util, it would be cyclic
# import util


class Item(object):
    """Base item class

    Takes an optional lx.object.Item object as an argument. If none is provided (the default) then the most
    recently selected item is used.

    :param item: Optional item object to wrap.
    :type item: an instance of lx.object.Item or lxu.object.item
    :raises ValueError: if no item is passed as an argument and no valid items are currently selected.
    :raises LookupError: if a string (item name or ID) is passed as the item argument and no item with that name or ID
        cane be found in the scene.
    :raises TypeError: if the object passed as the 'item' argument isn't an instance of lx.object.Item.

    """

    _sceneCache = {}

    def __init__(self, item=None):
        if not item:
            try:
                selected = lxu.select.ItemSelection().current()[0]
            except IndexError:
                raise ValueError('No valid item currently selected')
            self._item_ = selected
            
        elif isinstance(item, (lx.object.Item, lxu.object.Item) ):
            self._item_ = item
            
        elif isinstance(item, str):
            self._item_ = lxu.select.SceneSelection().current().ItemLookup(item)

        elif hasattr(item, '_item'):
            self._item_ = item._item
            if self._item_ is None:
                raise TypeError("Failed to create modo.Item from %s" % str(item))
            
        # Casting from lx.object.Unknown
        elif isinstance(item, lx.object.Unknown):
            try:
                lxitem = lx.object.Item(item)
            except:
                raise TypeError("Item type is required")
            self._item_ = lxu.select.SceneSelection().current().ItemLookup(lxitem.Ident())
        
        # Casting from modo.Item (fixes bug 55194)
        elif isinstance(item, Item):
            self._item_ = item._item_

        else:
            raise TypeError("Cannot create modo.Item from %s, incompatible type" % str(item))

        self._scene = None
        self._tag = None
    # Safety guard property to prevent crashes by accessing invalid 'zombie' COM objects
    @property
    def _item(self):
        if self._item_.Type() == 0:
            return None
            # raise Exception('Invalid Item')

        return self._item_

    def __getattr__(self, attr):
        # pass any unknown attribute access on to the wrapped lx.object.Item class to see if
        # it's a recognised call there.
        return getattr(self._item, attr)

    def __repr__(self):
        # The repr function generally returns a string representation of an object that can
        # be evaluated to create an instance from. Optionally, the __str__ function can return
        # A more readable representation.
        return "modo.%s('%s')" % (self.__class__.__name__, self.Ident())

    def __eq__(self, other):
        if not hasattr(other, 'test'):
            return False
        
        # Fix for 48937: Was not considering lx.object.Item and lxu.objet.Item.
        if isinstance(other, (lx.object.Item, lxu.object.Item)):
            return self._item_ == other
        elif isinstance(other, Item):
            return self._item_ == other._item_
        return False 

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.Ident() if self else None)

    def __bool__(self):
        """Test if the wrapped item is still valid

        If in doubt, add this extra check::

            item = scn.addItem('mesh')
            item._item = None
            if item:
                item.name = 'I am valid'

        :returns bool: Validity of the item
        """
        if self._item_.Type() == 0:
            return False

        if not isinstance(self._item_, lx.object.Item):
            return False
        if not self._item_.test():
            return False
        return True

    @property
    def _stringtag(self):
        if not self._tag:
            self._tag = lx.object.StringTag(self)
        return self._tag

    @property
    def scene(self):
        if self._scene is None:
            context = self.Context()
            scnPointer = context.__peekobj__()
            if scnPointer in Item._sceneCache:
                self._scene = Item._sceneCache[scnPointer]
            else:
                modoScene = scene.Scene (context)
                self._scene = modoScene
                Item._sceneCache[scnPointer] = modoScene
        return self._scene

    @property
    def index(self):
        """:getter: Index of the item in the collection of items of the same type in the scene.

        :return: Returns item index by type.
        :rtype: int

        """
        for x in range(self.scene.ItemCount(self.Type())):
            if self.Ident() == self.scene.ItemByIndex(self.Type(), x).Ident():
                return x

    @property
    def id(self):
        """:getter: Item's unique ID (Ident)

        :return: ID
        :rtype: basestring

        """
        return self.Ident()

    @property
    def name(self):
        """:getter: Item's name.

        :return: Item's unique (disambiguated) name
        :rtype: string
        :param name: Item's base name - before disambiguation.
        :type: basestring

        """
        return self.UniqueName()

    @name.setter
    def name(self, name):
        self.SetName(name)

    @property
    def baseName(self):
        """:getter: Item's base name.

        :return: item's base name before disambiguation.
        :rtype: basestring

        """
        return self.Name()

    @property
    def type(self):
        """:getter: Returns the type of the item as a string.

        :return: the type of the item.
        :rtype: basestring

        """
        return c.SCENE_SVC.ItemTypeName(self.Type())

    @property
    def superType(self):
        """:getter: Returns the parent type of the item as a string.

        :return: the type of the item.
        :rtype: basestring
        """
        result = c.SCENE_SVC.ItemTypeSuper(self.Type())
        return c.SCENE_SVC.ItemTypeName(result)

    @property
    def channelNames(self):
        """:getter: Returns a list of all the names of the channels belonging to an object.

        :returns: list of channel names.
        :rtype: list

        """
        return self.ChannelList()

    def channel(self, channelName):
        """Returns a channel object for the channel name provided.

        :param channelName: name of the channel.
        :type channelName: basestring
        :returns: a channel object for the specified channel
        :rtype: modo.channel.Channel.
        :raises LookupError: if the channel can not be found

        """
        try:
            return Channel(channelName, self)
        except:
          try:
              # See if the user is asking for a triple (i.e. a vector channel)
              return ChannelTriple(self, channelName)
          except:
              return None
        return None

    def iterChannels(self, name=None):
        """Returns a generator object for iterating all channels of this item

        :returns generator object: iterable of channel objects
        """

        name_filter = lambda ch: True
        if name:
            name_filter = lambda ch: bool(fnmatch(ch, name))

        for ch_name in self.channelNames:
            if name_filter(ch_name):
                yield self.channel(ch_name)

    def channels(self, name=None):
        """Returns a generator object for iterating all channels of this item

        :returns generator object: iterable of channel objects
        """
        return tuple(self.iterChannels(name))

    @property
    def parent(self):
        """:getter: Item parent

        When setting accepts either an item object (modo.Item or lx.object.Item) or a string (item ID or name).

        :return: parent item or None if the item has no parent
        :rtype: modo.item.Item
        :param parent: item to parent to
        :type parent: basestring, modo.Item or lx.object.Item
        :raises LookupError: if the argument was a string and no item with that name or id can be found.

        """
        try:
            return Item(self.Parent())
        except TypeError as e:
            if str(e) == 'no interface':
                return None
            else:
                raise

    @property
    def parentIndex(self):
        """:getter: Returns the index of this item from from the perspective of it's parent

        This correlates to the order items appear in the UI, i.e. the item view and Shader Tree.

        Returns None if the item has no parent. In that case, use rootIndex instead.

        :returns int: Index
        """
        return self.parent.children(asSubType=False).index(self) if self.parent else None

    def setParent(self, newParent=None, index=None):
        """Parents this item to another

        :param modo.item.Item newParent: Item to parent to. If None, the item is parented to root level.
        :param int index: Optionally sets the position the item appears in the item view for locatorSuperType items

        Note that this method does not preserve world transformations as in parenting in place.
        Please use the command 'item.parent' instead
        """
        if isinstance(newParent, str):
            newParent = Item(self.scene.ItemLookup(newParent))

        if newParent:
            if newParent.type == 'shaderFolder' and self.type == 'advancedMaterial':
                return None
            if newParent.type == 'shaderFolder' and self.superType == 'textureLayer':
    
                def shaderFolderType(item):
                    tags = item.getTags()
                    if 'CUE ' in tags:
                        return tags['CUE ']
    
                cueTag = shaderFolderType(newParent)
                if cueTag == 'lightShaders':
                    self.channel('effect').set('lightColor', action='setup')
                    newParent.itemGraph('localShader') >> self.itemGraph('localShader')
                elif cueTag == 'envShaders':
                    self.channel('effect').set('envColor', action='setup')
                    newParent.itemGraph('localShader') >> self.itemGraph('localShader')
    
                return

    # The following line was removed in Joota to fix this function but has been
    # restored due to it causing a change in behaviour (#56982).
        index = 0 if not index else index
        
        # Do the re-parenting
        if newParent is not None:
            if index is None:
                self.SetParent(newParent)
            else:
                graph = newParent.itemGraph('parent')
                graph.SetLink(self, 0, newParent, index)

        else:
            # Parenting to root level, removing the connection to the current parent
            graph = self.itemGraph('parent')
            if graph.FwdCount(self):
                current_parent = graph.FwdByIndex(self, 0)
                graph.DeleteLink(self, current_parent)
            
            # Set the root position
            if index is not None:
                sceneGraph = lx.object.SceneGraph(self.scene.GraphLookup(lx.symbol.sGRAPH_PARENT))
                sceneGraph.RootSetPos(self, index)

    @property
    def parents(self):
        """
        :getter: Returns list of all ancestor parents
        :rtype: tuple
        """
        myparent = self.parent
        if myparent is None:
            return None

        queue = [myparent]

        items = []

        while not len(queue) == 0:
            a = queue.pop()
            if a not in items:
                items.append(a)
            parent = a.parent
            if parent:
                queue.append(a.parent)

        return tuple(util.typeToFunc(i.Type())(i._item) for i in items)

    @property
    def rootIndex(self):
        """:getter: Returns the root index of this item

        This correlates to the order items appear in the UI, i.e. the item list and groups viewport,
        if the item has no parent. 

        Returns None if the item has a parent. In that case, use parentIndex instead.

        :returns int: Index
        """
        scene = self.Context()
        graph = scene.GraphLookup(lx.symbol.sGRAPH_PARENT)
        for x in range(graph.RootCount()):
            if graph.RootByIndex(x) == self:
                return x
        return None

    def __descendants(self, itemType, asSubType=True):
        """
        :returns list: list of all descendant children
        """
        queue = self.SubList()

        items = []

        while not len(queue) == 0:
            a = queue.pop()
            if a not in items and (itemType is None or (itemType is not None and a.Type() == itemType)):
                items.append(a)
            queue += a.SubList()

        if not asSubType:
            return [Item(i) for i in items]
        return [util.typeToFunc(i.Type())(i) for i in items]

    def children(self, recursive=False, itemType=None, asSubType=True):
        """Returns a list of the child items of this item. Each type of each of the returned child items
        will be one of the item types supported by the :meth:`modo.util.typeToFunc` method if
        possible, or an object of type lx.item.Item otherwise.

        :param bool recursive: Returns all childen's children if True.
        :param basestring itemType: Filter to return only specific item types. Can either be string or int
        :param bool asSubType: if False, all items are returned as modo.Item rather than relevant subtype to improve performance
        :returns: the children of the item.
        :rtype: list
        
        """
        if itemType and isinstance(itemType, str):
            itemType = c.SCENE_SVC.ItemTypeLookup(itemType)

        if recursive:
            return self.__descendants(itemType, asSubType=asSubType)

        if itemType:
            if not asSubType:
                return [Item(item) for item in self.SubList() if item.Type() == itemType]
            return [util.typeToFunc(item.Type())(item) for item in self.SubList() if item.Type() == itemType]

        if not asSubType:
            return [Item(item) for item in self.SubList()]
        return [util.typeToFunc(item.Type())(item) for item in self.SubList()]

    def iterChildren(self, itemType=None, asSubType=True, reverseIter=False):
        """Returns a generator of the child items of this item. Each type of each of the returned child items
        will be one of the item types supported by the :meth:`modo.util.typeToFunc` method if
        possible, or an object of type lx.item.Item otherwise.
    
        :param basestring itemType: Filter to return only specific item types. Can either be string or int
        :param bool asSubType: if False, all items are returned as modo.Item rather than relevant subtype to improve performance
        :param bool reverseIter: If False, children are iterated over in reverse.
        :returns: the children of the item.
        :rtype: generator
    
        """
        if itemType and isinstance(itemType, str):
            itemType = c.SCENE_SVC.ItemTypeLookup(itemType)
    
        indices = range (self.SubCount())
        if reverseIter:
            indices = reversed(indices)
    
        for x in indices:
            child = self.SubByIndex(x)
            if itemType:
                childType = child.Type()
            if (not itemType) or (childType == itemType):
                if not asSubType:
                    yield Item(child)
                else:
                    yield util.typeToFunc(childType)(child)

    def childCount(self):
        """returns the number of children an item has.

        :returns: the number of child items the item has.
        :rtype: int

        """
        return self.SubCount()

    def childAtIndex(self, index, asSubType=True):
        """Returns the child item at the specified index.

        :param index: the child's index.
        :type index: int
        :param asSubType: if False, all items are returned as modo.Item rather than relevant subtype to improve performance
        :type asSubType: bool
        :returns: the child item at the specified index.
        :rtype: an instance of one of the defined modo.Item subtypes or an modo.Item

        """
        child = self.SubByIndex(index)
        if not asSubType:
            return Item(child)
        return util.typeToFunc(child.Type())(child)

    def childrenByType(self, itype, asSubType=True):
        """Returns all the children of an item that are of the specified type.

        :param itype: the type of the children to return
        :type itype: int or basestring
        :param asSubType: if False, all items are returned as modo.Item rather than relevant subtype to improve performance
        :type asSubType: bool
        :returns: list of all the children of the specified type.
        :rtype: list

        """
        if isinstance(itype, str):
            itype = c.SCENE_SVC.ItemTypeLookup(itype)
        if not asSubType:
            return [Item(item) for item in self.SubList() if item.Type() == itype]
        return [util.typeToFunc(item.Type())(item) for item in self.SubList() if item.Type() == itype]

    def setTag(self, tagName, tagval):
        """ Create or set a string tag on to the item.

        :param tagName: the four character tagID.
        :type tagName: basestring
        :param tagval: The string value to be stored under the tag. Pass None to remove the tag.
        :type tagval: basestring

        """
        tagID = lxu.lxID4(tagName)
        if not tagID:
            raise ValueError("Can't create tagID, 4 character string required.")
        self._stringtag.Set(tagID, tagval)

    def readTag(self, tagName):
        """ Get the value of a string tag attached to the item.

            :param tagName: the four character tag ID.
            :type tagName: basestring
            :returns: the value of the specified tag.
            :rtype: string

        """
        tagID = lxu.lxID4(tagName)
        if not tagID:
            raise ValueError("Can't create tagID, 4 character string required.")
        return self._stringtag.Get(tagID)

    def getTags(self, values=True):
        """Get the string tags attached to an item.

        if 'values' is True (default) a dictionary of tag name/tag value pairs is returned,
        if 'values' is False a list of tag names is returned instead.

        :returns: the string tags attached to the item.
        :rtype: dictionary or list.

        """
        tags = {} if values else []
        for x in range(self._stringtag.Count()):
            tagID, tagData = self._stringtag.ByIndex(x)
            tagName = lxu.decodeID4(tagID)
            if values:
                tags[tagName] = tagData
            else:
                tags.append(tagName)
        return tags

    def hasTag(self, tagName):
        """Returns whether the tag with the specified name exists or not.

        :param tagName: the four character tag ID
        :type tagName: basestring
        :returns: True if the specified tag exists on the group, False if not.
        :rtype: bool

        """
        try:
            self._stringtag.Get(lxu.lxID4(tagName))
        except LookupError:
            return False
        return True

    @property
    def itemGraphNames(self):
        """:getter: Get connected ItemGraph names

        :returns list of strings: List of connected graph types
        :type: list
        """
        names = []

        for i in range(self.scene.GraphCount()):
            graph_name = self.scene.GraphByIndex(i).Name()

            try:
                graph = lx.object.ItemGraph(self.scene.GraphLookup(graph_name))
                if graph_name not in names:
                    if graph.FwdCount(self) or graph.RevCount(self):
                        names.append(graph_name)
            except TypeError:
                pass
        return names

    @property
    def itemGraphs(self):
        """
        :getter: Returns list of connected ItemGraphs
        :rtype: list
        """
        return [ItemGraph(self, graph_name) for graph_name in self.itemGraphNames]

    def itemGraph(self, graphType='deformers', reverse=True):
        """Retrieve ItemGraph by name

        :returns ItemGraph:
        """
        return ItemGraph(self, graphType, reverse)

    def packageNames(self):
        """

        :returns list: Package names that are attached to this item
        """
        hst_svc = lx.service.Host()
        hst_svc.SpawnForTagsOnly()

        all_packages = []
        contains_packages = []

        for i in range(hst_svc.NumServers(lx.symbol.a_PACKAGE)):
            factory = hst_svc.ServerByIndex(lx.symbol.a_PACKAGE, i)

            try:
                factory.InfoTag (lx.symbol.sPKG_SUPERTYPE)
                continue

            except:

                '''
                    We rely on the fact that this will fail if the super type
                    is undefined. If it is, the package is a true Package that
                    can be added to items, so we catch the error and add it to
                    the list.
                '''
                all_packages.append (factory.Name ())

        for package in all_packages:
            if self.PackageTest (package) == True:
                contains_packages.append (package)

        return contains_packages

    def isLocatorSuperType(self):
        """

        :returns bool: whether this item derives from the locator type.
        """
        return self.TestType(lx.symbol.i_CIT_LOCATOR)

    def __rshift__(self, other):
        """Connect this item to an ItemGraph

        :param other:
        :return:
        """
        if not self._item.test() or not other._item.test():
            raise ValueError("Invalid item")

        other.connectInput(self._item)

    @property
    def deformers(self, dtype=None):
        """:getter: Returns input connections of the 'deformers' graph

        :param basestring dtype: Optionally filter the result by this type.
        :returns tuple: Deformer items
        """
        if dtype:
            return tuple(deformer for deformer in self.itemGraph('deformers').reverse() if deformer.type == dtype)

        return self.itemGraph('deformers').reverse()

    @property
    def selected(self):
        """
        :getter: Returns True if this item is selected, False otherwise
        :type: bool
        """
        sv = c.SEL_SVC
        spTrans = lx.object.ItemPacketTranslation(sv.Allocate(lx.symbol.sSELTYP_ITEM))
        spType = sv.LookupType(lx.symbol.sSELTYP_ITEM)

        pkt = spTrans.Packet(self._item)
        return sv.Test(spType, pkt)

    def select(self, replace=False):
        """Selects this item

        :param bool replace: If True, the selection is cleared before selecting this item
        """
        lxu.select.ItemSelection().select(self._item.Ident(), not replace)

    def deselect(self):
        """Deselects this item
        """
        sv = c.SEL_SVC
        spTrans = lx.object.ItemPacketTranslation(sv.Allocate(lx.symbol.sSELTYP_ITEM))
        spType = sv.LookupType(lx.symbol.sSELTYP_ITEM)
        pkt = spTrans.Packet(self._item)
        sv.Deselect(spType, pkt)

    def _getChannelValuesAsDict(self, chNames=None, time=None, action=None):
        """Note: ignores non-numerical and non-string types

        This method is marked as private because it is likely to be moved somewhere else

        :arg list chNames: Optional list of channel names to receive. If None, all channels are retrieved.
        :arg float time: Time to get the values at. Default to the current time if None
        :arg string action: Action to get the values from (optional)
        :returns dict: A dictionary containing the values
        """
        kwargs = dict( locals() )
        kwargs.pop('self')
        kwargs.pop('chNames')

        result = {}

        if chNames:
            for chName in chNames:
                channel = self.channel(chName)
                if channel:
                    if channel.type in [lx.symbol.iCHANTYPE_INTEGER, lx.symbol.iCHANTYPE_FLOAT]:
                        result[channel.name] = channel.get(**kwargs)

        else:
            for channel in self.channels:
                if channel.type in [lx.symbol.iCHANTYPE_INTEGER, lx.symbol.iCHANTYPE_FLOAT]:
                    result[channel.name] = channel.get(**kwargs)

        return result

    def _setChannelValuesFromDict(self, pairs, time=None, key=False, action='edit'):
        """Set channel values from a provided dictionary

        This method is marked as private because it is likely to be moved somewhere else
        """
        kwargs = dict( locals() )
        kwargs.pop('self')
        kwargs.pop('pairs')

        for name, value in pairs.items():
            channel = Channel(name, self)
            channel.set(value, **kwargs)

    @property
    def internalItem(self):
        """:getter: Returns the internal Modo item embedded in this object"""
        return self._item

    @property
    def connectedGroups(self):
        """
        :getter: Returns a tuple of all Group objects that this item belongs to
        :rtype: tuple
        """
        graph = self.itemGraph('itemGroups')
        if not graph:
            return None
        return tuple(Group(item) for item in graph.reverse())

    @property
    def isAnInstance(self):
        """
        :getter: Returns True if item is an instance of another item, False otherwise.
        :rtype: bool
        """
        return True if self.itemGraph("source").forward() else False

    # This exists for performance reasons- ChannelLookup is called a *lot* and the __getattr__ mechanism is slow.
    def ChannelLookup(self, name):
        return self._item_.ChannelLookup(name)

class LocatorSuperType(Item):
    """The LocatorSuperType reflects all items that can be seen and transformed in the 3d view.
    Locators have transform items that hold the respective transform channels, such as position and rotation.

    """
    def __init__(self, item=None):
        Item.__init__(self, item)
        self._locator = lx.object.Locator(self._item)
        self._TransformItems = None

    @property
    def transforms(self):
        """

        :getter: Access to the stacked transform items.
        :rtype: :class:`TransformItems`
        """
        if not self._TransformItems:
            self._TransformItems = TransformItems(self._item)

        return self._TransformItems

    def __getTransformitem(self, symbol):
        """Utility function to get an 'internal' position, rotation or scale transform item
        """
        try:
            xfrm = lx.object.Locator(self._item).GetTransformItem(symbol)
        except LookupError:
            xfrm = lx.object.Locator(self._item).AddTransformItem(symbol)[0]
        return xfrm

    @property
    def position(self):
        """:getter: Returns a position TransformItem object. An appropriate channel is created if it does not exist.
        :rtype: :class:`TransformItem`
        """
        xfrm = self.__getTransformitem(lx.symbol.iXFRM_POSITION)
        return TransformItem(xfrm)

    @property
    def rotation(self):
        """:getter: Returns a rotation TransformItem object. An appropriate channel is created if it does not exist.
        :rtype: :class:`TransformItem`
        """
        xfrm = self.__getTransformitem(lx.symbol.iXFRM_ROTATION)
        return TransformItem(xfrm)

    @property
    def scale(self):
        """:getter: Returns a scale TransformItem object. An appropriate channel is created if it does not exist.
        :rtype: :class:`TransformItem`
        """
        xfrm = self.__getTransformitem(lx.symbol.iXFRM_SCALE)
        return TransformItem(xfrm)

    @property
    def pivot(self):
        """:getter: Returns a position TransformItem object. An appropriate channel is created if it does not exist.
        :rtype: :class:`TransformItem`
        """
        xfrm = self.__getTransformitem(lx.symbol.iXFRM_PIVOT)
        return TransformItem(xfrm)


# TODO: matrix access
class TransformItem(Item):
    """Contains a group of animatable transform channels of a locator object.

    It has convenience functions for access of the locator's position, rotation and scale.

    examples::

        # We retrieve two meshes from the current scene by name, assuming they exist
        cube = modo.Mesh('Cube')
        sphere = modo.Mesh('Sphere')

        # Set rotation values
        cube.rotation.set(10, 20, 30, degrees=True)

        # Link the position.x channel of the sphere to to the position.x channel of the cube
        cube.position.y.setLink(0, sphere.position.x, 0)

        # Set position values to zero
        cube.position.clear()

        # Insert keyframe for rotation on frame 21
        frame = lx.service.Value().FrameToTime(21)
        cube.rotation.insertKey(time=frame)

    """

    __translationType = c.SCENE_SVC.ItemTypeLookup(lx.symbol.sITYPE_TRANSLATION)
    __rotationType = c.SCENE_SVC.ItemTypeLookup(lx.symbol.sITYPE_ROTATION)
    __scaleType = c.SCENE_SVC.ItemTypeLookup(lx.symbol.sITYPE_SCALE)
    __types = {__translationType: 'pos', __rotationType: 'rot', __scaleType: 'scl'}

    def __init__(self, item=None):
        Item.__init__(self, item)

    def __transformType(self):
        """Utility function that returns the corresponding string value from __types, for later channel lookup
        """
        transform_str = None

        # Pick string arguments based on type
        for transformType, name in TransformItem.__types.items():

            if self._item.TestType(transformType):
                transform_str = name
                break
        else:
            raise TypeError('Unknown transform type')

        return transform_str

    @staticmethod
    def __toDegrees(kwargs, values=None):
        """Utility function to consume and process the 'degrees' argument for the set function
        """
        x, y, z = values
        if 'degrees' in kwargs:
            import math
            if kwargs['degrees']:
                x, y, z = (math.radians(i) for i in (x, y, z))

            # Remove argument to not confuse the set function call
            kwargs.pop('degrees')

        return kwargs, (x, y, z)

    # BUG: deletes all keys if 'key' is passed as False and action is None
    # TODO: make decorator that handles the input type of the three values accordingly
    def set(self, values, time=None, key=False, action='edit', degrees=False):
        """Function to set the x, y and z-values of the locator at once.

        :param values: either three floats, or a list/tuple containing the x, y, z values to set
        :param bool degrees: If set, values are interpreted as degrees instead of radians. Only relevant when setting rotation.
        :param keywords: Same as as :meth:`Channel.set<modo.channel.Channel.set>`

        """
        kwargs = dict( locals() )
        kwargs.pop('values')
        kwargs.pop('self')

        if len(values) is 3:
            x, y, z = values
        elif len(values) is 1:
            try:
                x, y, z = values
            except:
                raise LookupError('Wrong number of arguments')
        else:
            raise LookupError('Wrong number of arguments')

        if self.__transformType() == 'rot':
            kwargs, values = TransformItem.__toDegrees(kwargs, (x, y, z))
            x, y, z = values
        else:
            kwargs.pop('degrees')

        # Pass and set the values to the corresponding channels
        for axis, value in zip(('X', 'Y', 'Z'), (x, y, z)):
            self.channel('%s.%s' % (self.__transformType(), axis)).set(value, **kwargs)

    def get(self, time=None, action=None, degrees=False):
        """Function to get the x, y and z-values of the locator at once.

        :param bool degrees: If set, values are interpreted as degrees instead of radians. Only relevant when getting rotation.
        :param keywords: Same as as :meth:`Channel.get<modo.channel.Channel.get>`
        :returns tuple: x, y and z values

        """
        kwargs = dict( locals() )
        kwargs.pop('self')
        asDegrees = degrees
        kwargs.pop('degrees')

        transform_str = self.__transformType()

        # Pass and set the values to the corresponding channels
        out = [0.0] * 3
        for i, axis in enumerate(('X', 'Y', 'Z')):
            out[i] = self.channel('%s.%s' % (transform_str, axis)).get(**kwargs)

        if self.__transformType() == 'rot' and asDegrees:
            import math
            out = [math.degrees(i) for i in out]

        return tuple(out)

    def clear(self, *args, **kwargs):
        """Sets values to 1.0 if is a scaling transform and to 0.0 otherwise

        :param arguments: Same as :meth:`Channel.set<modo.channel.Channel.set>`

        """
        if not self._item.TestType(TransformItem.__scaleType):
            self.set((0, 0, 0), *args, **kwargs)
        else:
            self.set((1, 1, 1), *args, **kwargs)

    @property
    def x(self):
        """Shortcut to the x channel of the locator

        :getter: :class:`Channel<modo.channel.Channel>`
        :rtype: float
        """
        return self.channel('%s.X' % (self.__transformType() ))

    @property
    def y(self):
        """Shortcut to the y channel of the locator

        :getter: :class:`Channel<modo.channel.Channel>`
        :rtype: float
        """
        return self.channel('%s.Y' % (self.__transformType() ))

    @property
    def z(self):
        """Shortcut to the z channel of the locator

        :getter: :class:`Channel<modo.channel.Channel>`
        :rtype: float
        """
        return self.channel('%s.Z' % (self.__transformType() ))

    def insertKey(self, time=None, action='edit'):
        """Inserts a keyframe on the respective x, y and z channels.

        :param float time: Time in seconds to create the new keys
        :param action: Action to create keys in.
        """
        kwargs = dict( locals() )
        kwargs.pop('self')

        for channel in (self.x, self.y, self.z):
            value = channel.get(**kwargs)
            channel.set(value, key=True, **kwargs)

    def removeKey(self, time=None, action=None):
        """
        """
        time = lx.service.Selection().GetTime() if time is None else time

        for channel in (self.x, self.y, self.z):

            if not channel.isAnimated:
                continue

            keys = channel.envelope.keyframes

            index = keys._indexFromTime(time)
            if index:
                keys.setIndex(index)
                keys.delete()
                keys.setIndex(0)


class TransformItems(LocatorSuperType):
    """Container class for the stacked transform items of a Locator object.

    Transform items contain channels for either position, rotation or scale.
    The order of how they are processed can be changed and new transform items can be inserted or existing ones deleted.

    example::

        scene = modo.scene.current()

        # Grab first selected object
        for item in scene.selected[:1]:

            # Print the amount of transform items
            print len(item.transforms)

            # Add a new position transform item
            position = item.transforms.insert('position', values=(1,0,0), name='New_Position')

            # Add a new scale transform item
            scale = item.transforms.insert('scale', values=(2,2,2), name='Scaled')

            # Swap the indices of the first two transform items
            item.transforms.reposition(0,1)

            # Delete
            item.transforms.delete(scale)

            # Clear values of all transforms
            for i in item.transforms:
                i.clear()

    """
    def __init__(self, item):
        if isinstance(item, str):
            self._item_ = lxu.select.SceneSelection().current().ItemLookup(item)
        else:
            self._item_ = item

        self._scene = self._item.Context()
        self._graph = lx.object.ItemGraph(self._scene.GraphLookup(lx.symbol.sGRAPH_XFRMCORE))
        self._locator = lx.object.Locator(self._item)

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, self._item.Ident())

    def __len__(self):
        return self._graph.RevCount(self._item)

    def __getitem__(self, item):
        if isinstance(item, int):

            if len(self) <= item or item < 0:
                raise IndexError('Index out of range')

            index = item
            return TransformItem(self._graph.RevByIndex(self._item, index))

        raise ValueError

    def __iter__(self):
        for i in reversed(list(range(len(self)))):
            yield TransformItem(self._graph.RevByIndex(self._item, i))

    def idNames(self):
        return [item.Ident() for item in self]

    def names(self):
        return [item.UniqueName() for item in self]

    # Here a decorator/dings that does the lookup by ident and name and range
    # checking automatically.

    def delete(self, index):
        # note: [::-1] temporarily reverses the list
        
        if isinstance(index, TransformItem):
            if index.id in self.idNames():                
                index = self.idNames()[::-1].index(index.id)

        elif isinstance(index, str):
            idNames = self.idNames()
            names = self.names()
            if index in idNames:
                index = idNames[::-1].index(index)
            elif index in names:
                index = names[::-1].index(index)
            else:
                raise LookupError('%s not found' % index)

        if len(self) <= index or index < 0:
            raise IndexError('Index out of range')

        if self._item.TestType(c.LOCATOR_TYPE):
            locator = lx.object.Locator(self._item)
            xfrm = self._graph.RevByIndex(self._item, index)
            # self._graph.DeleteLink(xfrm, locator)
            scene = lx.object.Scene(self._scene)
            scene.ItemRemove(xfrm)

    def insert(self, xfrmType='position', placement='append', values=None, name=None):
        """Insert a new transform item into the transform chain.

        The 'prepend' and 'append' placement values place the new item at the top or bottom of the stack,
        where 'pre' and 'post' place it around the respective transform highlighted in black in the channel view.

        I am myself confused about the order though, is it bottom to top or the other way around?

        Note that modo always keeps at least one of each type of transform, so when you attempt to delete it
        a new one is created automatically.

        :param string xfrmType: 'position', 'rotation' or 'scale'
        :param string placement: 'prepend', 'append', 'pre' or 'post'
        :param tuple values: Initial xyz values to be optionally set
        :param string name: Optional name

        """
        # I have inverted these on purpose. Am I wrong about the order though?
        # This way it matches the top to bottom way in the channel view

        funcs = {'prepend'  : 'AppendTransformItem',
                 'append'   : 'PrependTransformItem',
                 'post'     : 'AddPreTransformItem',
                 'pre'      : 'AddPostTransformItem'}

        types = {'position' : lx.symbol.iXFRM_POSITION,
                 'rotation' : lx.symbol.iXFRM_ROTATION,
                 'pivot'    : lx.symbol.iXFRM_PIVOT,
                 'scale'    : lx.symbol.iXFRM_SCALE}

        if self._locator.test():
            func_ = getattr(self._locator, funcs[placement])
            type_ = types[xfrmType]
            writer = ChannelWrite(self._scene)

            # Default values
            if not values:
                values = (1,1,1) if xfrmType == 'scale' else (0,0,0)

            # Call the function to add the transform
            item_, index = func_(writer, type_, values)
            outItem = TransformItem(item_)

            # Set name
            outItem.name = name if name else outItem.name

            return outItem

        return None

    def reposition(self, indexFrom, indexTo):
        """Places a transform item to the provided index of the transform item stack

        :param int indexFrom: Source Index of the item that is to be moved
        :param int indexTo: Destination index to place item at
        """
        item = self[indexFrom]
        self._graph.SetLink(item, 0, self._locator, indexTo)


class Camera(LocatorSuperType):
    """Camera item class.

    Takes an optional 'camera' argument which can be either an item object (lx.object.Item or lxu.object.Item) of type
    'camera' or an item name or ID to look up. If no camera item is supplied as an argument an attempt will be made to
    wrap the most recently selected camera.

    :param camera: Optional camera item object (type lx.symbol.sITYPE_CAMERA) or string (item name or ID) to look up.
    :type camera: an instance of lx.object.Item, lxu.object.item or modo.item.Item
    :raises ValueError: if no valid camera item selected.
    :raises TypeError: if the item passed as an argument isn't either an instance of lx.object.Item of type 'camera'
        or an item name or ID string.
    :raises LookupError: if a name or ID is supplied as the camera argument but no item with that name/ID can
        be found.

    """
    def __init__(self, camera=None):
        # before calling the parent's __init__ method ensure that any incoming item is of the correct type for the
        # subclass, or, if no item is passed as an argument & we fall back to getting a selected item, that too is of
        # the correct type.
        if camera:
            if isinstance(camera, str):
                camera = scene.Scene().ItemLookup(camera)
            if not isinstance(camera, (lx.object.Item, Item)) or not camera.TestType(c.CAMERA_TYPE):
                raise TypeError("Camera item is required")
        if not camera:
            selection = lxu.select.ItemSelection().current()
            for sel in reversed(selection):
                if sel.Type() == c.CAMERA_TYPE:
                    camera = sel
                    break
            else:
                raise ValueError("No valid camera item selected")
        LocatorSuperType.__init__(self, camera)
        # Item.__init__(self, camera)


class Mesh(LocatorSuperType):
    """Mesh item class.

    Takes an optional 'mesh' argument which can be either an item object (lx.object.Item or lxu.object.Item) of type
    'mesh' or an item name or ID to look up. If no mesh item is supplied as an argument an attempt will be made to
    wrap the most recently selected mesh layer.

    :param mesh: Optional mesh item object (type lx.symbol.sITYPE_MESH) or string (item name or ID) to look up.
    :type mesh: an instance of lx.object.Item, lxu.object.item or modo.item.Item
    :raises ValueError: if no valid mesh item selected.
    :raises TypeError: if the item passed as an argument isn't either an instance of lx.object.Item of type 'mesh'
        or an item name or ID string.
    :raises LookupError: if a name or ID is supplied as the mesh argument but no item with that name/ID can
        be found.

    The mesh geometry can be accessed by the :class:`geometry<modo.meshgeometry.MeshGeometry>` attribute.

    .. py:attribute:: geometry

        :rtype: :class:`MeshGeometry<modo.meshgeometry.MeshGeometry>`


    """
    def __init__(self, mesh=None):
        # before calling the parent's __init__ method ensure that any incoming item is of the correct type for the
        # subclass, or, if no item is passed as an argument & we fall back to getting a selected item, that too is of
        # the correct type.
        if mesh:
            if isinstance(mesh, str):
                mesh = scene.Scene().ItemLookup(mesh)

            # Enforcing conversion to lx.object.Item in order to avoid boilerplate/cyclic import with MeshGeometry
            if isinstance(mesh, Item):
                mesh = mesh._item
            if not isinstance(mesh, (lx.object.Item, Item)) or not mesh.TestType(c.MESH_TYPE):
                raise TypeError("mesh item is required")
        if not mesh:
            selection = lxu.select.ItemSelection().current()
            for sel in reversed(selection):
                if sel.Type() == c.MESH_TYPE:
                    mesh = sel
                    break
            else:
                raise ValueError("No valid mesh item selected")
        LocatorSuperType.__init__(self, mesh)

        self._geometry = None

    @property
    def geometry(self):
        if not self._geometry:
            self._geometry = MeshGeometry(self._item)
        return self._geometry

    def __eq__(self, other):
        if isinstance(other, Mesh):
            return self.geometry == other.geometry
        elif isinstance(other, MeshGeometry):
            return self.geometry == other
        else:
            return super(Mesh, self).__eq__(other)

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __hash__(self):
        # Need to override __hash__ if we also override __eq__
        return LocatorSuperType.__hash__(self)

class Locator(LocatorSuperType):
    """Locator item class.

    Takes an optional 'locator' argument which can be either an item object (lx.object.Item or lxu.object.Item) of type
    'locator' or an item name or ID to look up. If no locator item is supplied as an argument an attempt will be made to
    wrap the most recently selected locator item.

    :param locator: Optional locator item object (type lx.symbol.sITYPE_LOCATOR) or string (item name or ID) to look up.
    :type locator: an instance of lx.object.Item, lxu.object.item or modo.item.Item
    :raises ValueError: if no valid locator item selected.
    :raises TypeError: if the item passed as an argument isn't either an instance of lx.object.Item of type 'locator'
        or an item name or ID string.
    :raises LookupError: if a name or ID is supplied as the locator argument but no item with that name/ID can
        be found.

    Hint: Items of other locator derived types should be casted as LocatorSuperType, casting to this class will fail.
    """
    def __init__(self, locator=None):
        # before calling the parent's __init__ method ensure that any incoming item is of the correct type for the
        # subclass, or, if no item is passed as an argument & we fall back to getting a selected item, that too is of
        # the correct type.
        if locator:
            if isinstance(locator, str):
                locator = scene.Scene().ItemLookup(locator)
            if not isinstance(locator, (lx.object.Item, Item)) or not locator.Type() == c.LOCATOR_TYPE:
                raise TypeError("Locator item is required")
        if not locator:
            selection = lxu.select.ItemSelection().current()
            for sel in reversed(selection):
                if sel.Type() == c.LOCATOR_TYPE:
                    locator = sel
                    break
            else:
                raise ValueError("No valid locator item selected")
        # Item.__init__(self, locator)
        LocatorSuperType.__init__(self, locator)


class Joint(Locator):

    def __init__(self, locator=None):
        Locator.__init__(self, locator)


class GroupLocator(LocatorSuperType):
    """Group locator item class.

    Takes an optional 'grploc' argument which can be either an item object (lx.object.Item or lxu.object.Item) of type
    'Group locator' or an item name or ID to look up. If no grploc item is supplied as an argument an attempt will be
    made to wrap the most recently selected group locator item.

    :param grploc: Optional group locator item object (type lx.symbol.sITYPE_GROUPLOCATOR) or string (item name or ID)
        to look up.
    :type grploc: an instance of lx.object.Item, lxu.object.item or modo.item.Item
    :raises ValueError: if no valid group locator item selected.
    :raises TypeError: if the item passed as an argument isn't either an instance of lx.object.Item of type 'group
        locator' or an item name or ID string.
    :raises LookupError: if a name or ID is supplied as the grploc argument but no item with that name/ID can
        be found.

    """
    def __init__(self, grploc=None):
        # before calling the parent's __init__ method ensure that any incoming item is of the correct type for the
        # subclass, or, if no item is passed as an argument & we fall back to getting a selected item, that too is of
        # the correct type.
        if grploc:
            if isinstance(grploc, str):
                grploc = scene.Scene().ItemLookup(grploc)
            if not isinstance(grploc, (lx.object.Item, Item)) or not grploc.Type() == c.GROUPLOCATOR_TYPE:
                raise TypeError("Group locator item is required")
        if not grploc:
            selection = lxu.select.ItemSelection().current()
            for sel in reversed(selection):
                if sel.Type() == c.GROUPLOCATOR_TYPE:
                    grploc = sel
                    break
            else:
                raise ValueError("No valid group locator item selected")
        # Item.__init__(self, grploc)
        LocatorSuperType.__init__(self, grploc)


class TextureLocator(LocatorSuperType):
    """Texture locator item class.

    Takes an optional 'texloc' argument which can be either an item object (lx.object.Item or lxu.object.Item) of type
    'Texture locator' or an item name or ID to look up. If no texloc item is supplied as an argument an attempt will be
    made to wrap the most recently selected group locator item.

    :param texloc: Optional texture locator item object (type lx.symbol.sITYPE_TEXTURELOC) or string (item name or ID)
        to look up.
    :type texloc: an instance of lx.object.Item, lxu.object.item or modo.item.Item
    :raises ValueError: if no valid texture locator item selected.
    :raises TypeError: if the item passed as an argument isn't either an instance of lx.object.Item of type 'texture
        locator' or an item name or ID string.
    :raises LookupError: if a name or ID is supplied as the texloc argument but no item with that name/ID can
        be found.

    """
    def __init__(self, texloc=None):
        # before calling the parent's __init__ method ensure that any incoming item is of the correct type for the
        # subclass, or, if no item is passed as an argument & we fall back to getting a selected item, that too is of
        # the correct type.
        if texloc:
            if isinstance(texloc, str):
                texloc = scene.Scene().ItemLookup(texloc)
            if not isinstance(texloc, (lx.object.Item, Item)) or not texloc.Type() == c.TXTRLOCATOR_TYPE:
                raise TypeError("Texture locator item is required")
        if not texloc:
            selection = lxu.select.ItemSelection().current()
            for sel in reversed(selection):
                if sel.Type() == c.TXTRLOCATOR_TYPE:
                    texloc = sel
                    break
            else:
                raise ValueError("No valid texture locator item selected")
        # Item.__init__(self, texloc)
        LocatorSuperType.__init__(self, texloc)


class Light(LocatorSuperType):
    """Base Light item class.

    Each light item encapsulates both an lx.object.Item object (via inheritance from the Item class) of a specific modo
    light type and a corresponding lx.object.Item of type 'lightMaterial' as a :class:`LightMaterial` object via the
    light's material property.

    example::

        # to set the diffuse color on the currently selected spotlight
        spotlight = modo.SpotLight()
        spotlight.material.ch_diffCol.set((0.7, 0.1, 0.5))

    .. note::

        Although "Light" isn't technically a base class since, like all other classes in modo.item, it inherits from
        "Item", it does encapsulate modo's 'Light" supertype and can be treated as a kind of 'pseudo' base class for
        all modo's light types. As such it should not be instantiated directly, create one of the specific light types
        instead.

    |

    :param light: Optional light item object to wrap. Must be a specific type of light, not the light supertype.
    :type light: an instance of lx.object.Item, lxu.object.item or modo.item.Item
    :raises ValueError: if no valid light item selected.
    :raises TypeError: if the item passed as an argument isn't an instance of a specific subclass of Light.

    """
    def __init__(self, light):
        # Check the supplied argument is an item of type 'Light' but since the Light class can't be instanced itself
        # also check supplied argument to make sure it isn't just an instance of the supertype
        if light.Type() == c.LIGHT_TYPE:
            raise TypeError("supplied item was a 'Light' supertype, a specific light type is required.")
        if not light.TestType(c.LIGHT_TYPE):
            raise TypeError("supplied item was not a light type.")
        # Item.__init__(self, light)
        LocatorSuperType.__init__(self, light)

    @property
    def material(self):
        """The light material item associated with this light

        :type material: modo.item.LightMaterial
        :getter: the base light material (ie the light material at the bottom of the stack if there are more than one)
            for the light item.
        :rtype: modo.item.LightMaterial

        :setter: Parents a material to the light
        :param material: a material item to parent to the light

        """
        parentGraph = lx.object.ItemGraph(self.scene.GraphLookup(lx.symbol.sGRAPH_PARENT))
        for x in range(parentGraph.RevCount(self)):
            item = parentGraph.RevByIndex(self, x)
            if item.Type() == c.SCENE_SVC.ItemTypeLookup(lx.symbol.sITYPE_LIGHTMATERIAL):
                return LightMaterial(item)

    @material.setter
    def material(self, material):
        material.SetParent(self)


class AreaLight(Light):
    """Area light item class.

    Takes an optional 'light' argument which can be either an item object (lx.object.Item or lxu.object.Item) of type
    'Area Light' or an item name or ID to look up. If no light item is supplied as an argument an attempt will be
    made to wrap the most recently selected Area Light item.

    :param light: Optional area light item object (type lx.symbol.sITYPE_AREALIGHT)  or string (item name or ID)
        to look up.
    :type light: an instance of lx.object.Item, lxu.object.item or modo.item.Item
    :raises ValueError: if no valid area light item selected.
    :raises TypeError: if the item passed as an argument isn't either an area light item or an item name or ID string.
    :raises LookupError: if a name or ID is supplied as the light argument but no item with that name/ID can
        be found.

    """
    def __init__(self, light=None):
        # before calling the parent's __init__ method ensure that any incoming item is of the correct type for the
        # subclass, or, if no item is passed as an argument & we fall back to getting a selected item, that too is of
        # the correct type.
        if light:
            if isinstance(light, str):
                light = scene.Scene().ItemLookup(light)
            if (isinstance(light, (lx.object.Item, Item))) and (light.Type() != c.AREALIGHT_TYPE):
                raise TypeError("Area light item is required")
        else:
            selection = lxu.select.ItemSelection().current()
            for sel in reversed(selection):
                if sel.Type() == c.AREALIGHT_TYPE:
                    light = sel
                    break
            else:
                raise ValueError("No valid area light item selected")
        Light.__init__(self, light)

class CylinderLight(Light):
    """Cylinder light item class.

    Takes an optional 'light' argument which can be either an item object (lx.object.Item or lxu.object.Item) of type
    'Cylinder Light' or an item name or ID to look up. If no light item is supplied as an argument an attempt will be
    made to wrap the most recently selected Cylinder Light item.

    :param light: Optional Cylinder light item object (type lx.symbol.sITYPE_CYLINDERLIGHT)  or string (item name or ID)
        to look up.
    :type light: an instance of lx.object.Item, lxu.object.item or modo.item.Item
    :raises ValueError: if no valid cylinder light item selected.
    :raises TypeError: if the item passed as an argument isn't either a cylinder light or an item name or ID string.
    :raises LookupError: if a name or ID is supplied as the light argument but no item with that name/ID can
        be found.

    """
    def __init__(self, light=None):
        # before calling the parent's __init__ method ensure that any incoming item is of the correct type for the
        # subclass, or, if no item is passed as an argument & we fall back to getting a selected item, that too is of
        # the correct type.
        cylinder_light_type = c.SCENE_SVC.ItemTypeLookup(lx.symbol.sITYPE_CYLINDERLIGHT)
        if light:
            if isinstance(light, str):
                light = scene.Scene().ItemLookup(light)
            if (isinstance(light, (lx.object.Item, Item))) and (light.Type() != cylinder_light_type):
                raise TypeError("Cylinder light item is required")
        else:
            selection = lxu.select.ItemSelection().current()
            for sel in reversed(selection):
                if sel.Type() == cylinder_light_type:
                    light = sel
                    break
            else:
                raise ValueError("No valid cylinder light item selected")
        Light.__init__(self, light)


class DirectionalLight(Light):
    """Directional light item class.

    Takes an optional 'light' argument which can be either an item object (lx.object.Item or lxu.object.Item) of type
    'Directional Light' or an item name or ID to look up. If no light item is supplied as an argument an attempt will be
    made to wrap the most recently selected Directional Light item.

    :param light: Optional Directional light item object (type lx.symbol.sITYPE_SUNLIGHT)  or string (item
        name or ID) to look up.
    :type light: an instance of lx.object.Item, lxu.object.item or modo.item.Item
    :raises ValueError: if no valid directional light item selected.
    :raises TypeError: if the item passed as an argument isn't either a Directional light item or an item name or ID
        string.
    :raises LookupError: if a name or ID is supplied as the light argument but no item with that name/ID can
        be found.

    """
    def __init__(self, light=None):
        # before calling the parent's __init__ method ensure that any incoming item is of the correct type for the
        # subclass, or, if no item is passed as an argument & we fall back to getting a selected item, that too is of
        # the correct type.
        if light:
            if isinstance(light, str):
                light = scene.Scene().ItemLookup(light)
            if (isinstance(light, (lx.object.Item, Item))) and (light.Type() != c.SUNLIGHT_TYPE):
                raise TypeError("Directional light item is required")
        else:
            selection = lxu.select.ItemSelection().current()
            for sel in reversed(selection):
                if sel.Type() == c.SUNLIGHT_TYPE:
                    light = sel
                    break
            else:
                raise ValueError("No valid directional light item selected")
        Light.__init__(self, light)


class DomeLight(Light):
    """Dome light item class

    Takes an optional 'light' argument which can be either an item object (lx.object.Item or lxu.object.Item) of type
    'Dome Light' or an item name or ID to look up. If no light item is supplied as an argument an attempt will be
    made to wrap the most recently selected Dome Light item.

    :param light: Optional Dome light item object (type lx.symbol.sITYPE_DOMELIGHT)  or string (item name or ID)
        to look up.
    :type light: an instance of lx.object.Item, lxu.object.item or modo.item.Item
    :raises ValueError: if no valid Dome light item selected.
    :raises TypeError: if the item passed as an argument isn't either a Dome light item or an item name or ID string.
    :raises LookupError: if a name or ID is supplied as the light argument but no item with that name/ID can
        be found.

    """
    def __init__(self, light=None):
        # before calling the parent's __init__ method ensure that any incoming item is of the correct type for the
        # subclass, or, if no item is passed as an argument & we fall back to getting a selected item, that too is of
        # the correct type.
        dome_light_type = c.SCENE_SVC.ItemTypeLookup(lx.symbol.sITYPE_DOMELIGHT)
        if light:
            if isinstance(light, str):
                light = scene.Scene().ItemLookup(light)
            if (isinstance(light, (lx.object.Item, Item))) and (light.Type() != dome_light_type):
                raise TypeError("Dome light item is required")
        else:
            selection = lxu.select.ItemSelection().current()
            for sel in reversed(selection):
                if sel.Type() == dome_light_type:
                    light = sel
                    break
            else:
                raise ValueError("No valid dome light item selected")
        Light.__init__(self, light)


class PhotometricLight(Light):
    """Photometric (ies) light item class.

    Takes an optional 'light' argument which can be either an item object (lx.object.Item or lxu.object.Item) of type
    'Photometric Light' or an item name or ID to look up. If no light item is supplied as an argument an attempt will be
    made to wrap the most recently selected Photometric Light item.

    :param light: Optional Photometric light item object (type lx.symbol.sITYPE_PHOTOMETRYLIGHT)  or string (item
        name or ID) to look up.
    :type light: an instance of lx.object.Item, lxu.object.item or modo.item.Item
    :raises ValueError: if no valid Photometric light item selected.
    :raises TypeError: if the item passed as an argument isn't either a Photometric light item or an item name or ID
        string.
    :raises LookupError: if a name or ID is supplied as the light argument but no item with that name/ID can
        be found.

    """
    def __init__(self, light=None):
        # before calling the parent's __init__ method ensure that any incoming item is of the correct type for the
        # subclass, or, if no item is passed as an argument & we fall back to getting a selected item, that too is of
        # the correct type.
        ies_light_type = c.SCENE_SVC.ItemTypeLookup(lx.symbol.sITYPE_PHOTOMETRYLIGHT)
        if light:
            if isinstance(light, str):
                light = scene.Scene().ItemLookup(light)
            if (isinstance(light, (lx.object.Item, Item))) and (light.Type() != ies_light_type):
                raise TypeError("Photometric light item is required")
        else:
            selection = lxu.select.ItemSelection().current()
            for sel in reversed(selection):
                if sel.Type() == ies_light_type:
                    light = sel
                    break
            else:
                raise ValueError("No valid photometric light item selected")
        Light.__init__(self, light)


class PointLight(Light):
    """Point light item class.

    Takes an optional 'light' argument which can be either an item object (lx.object.Item or lxu.object.Item) of type
    'Point Light' or an item name or ID to look up. If no light item is supplied as an argument an attempt will be
    made to wrap the most recently selected Point Light item.

    :param light: Optional Point light item object (type lx.symbol.sITYPE_POINTLIGHT)  or string (item name or ID)
        to look up.
    :type light: an instance of lx.object.Item, lxu.object.item or modo.item.Item
    :raises ValueError: if no valid Point light item selected.
    :raises TypeError: if the item passed as an argument isn't either a Point light item or an item name or ID string.
    :raises LookupError: if a name or ID is supplied as the light argument but no item with that name/ID can
        be found.

    """
    def __init__(self, light=None):
        # before calling the parent's __init__ method ensure that any incoming item is of the correct type for the
        # subclass, or, if no item is passed as an argument & we fall back to getting a selected item, that too is of
        # the correct type.
        if light:
            if isinstance(light, str):
                light = scene.Scene().ItemLookup(light)
            if (isinstance(light, (lx.object.Item, Item))) and (light.Type() != c.POINTLIGHT_TYPE):
                raise TypeError("Point light item is required")
        else:
            selection = lxu.select.ItemSelection().current()
            for sel in reversed(selection):
                if sel.Type() == c.POINTLIGHT_TYPE:
                    light = sel
                    break
            else:
                raise ValueError("No valid point light item selected")
        Light.__init__(self, light)


class Portal(Light):
    """Portal item class.

    Takes an optional 'light' argument which can be either an item object (lx.object.Item or lxu.object.Item) of type
    'Portal' or an item name or ID to look up. If no light item is supplied as an argument an attempt will be
    made to wrap the most recently selected Portal item.

    :param light: Optional Portal item object (type 'portal')  or string (item name or ID) to look up.
    :type light: an instance of lx.object.Item, lxu.object.item or modo.item.Item
    :raises ValueError: if no valid Portal item selected.
    :raises TypeError: if the item passed as an argument isn't either a Portal item or an item name or ID string.
    :raises LookupError: if a name or ID is supplied as the light argument but no item with that name/ID can
        be found.

    """
    def __init__(self, light=None):
        # before calling the parent's __init__ method ensure that any incoming item is of the correct type for the
        # subclass, or, if no item is passed as an argument & we fall back to getting a selected item, that too is of
        # the correct type.
        portal_type = c.SCENE_SVC.ItemTypeLookup("portal")
        if light:
            if isinstance(light, str):
                light = scene.Scene().ItemLookup(light)
            if (isinstance(light, (lx.object.Item, Item))) and (light.Type() != portal_type):
                raise TypeError("Portal item is required")
        else:
            selection = lxu.select.ItemSelection().current()
            for sel in reversed(selection):
                if sel.Type() == portal_type:
                    light = sel
                    break
            else:
                raise ValueError("No valid portal light item selected")
        Light.__init__(self, light)


class SpotLight(Light):
    """Spotlight item class.

    Takes an optional 'light' argument which can be either an item object (lx.object.Item or lxu.object.Item) of type
    'Spotlight' or an item name or ID to look up. If no light item is supplied as an argument an attempt will be
    made to wrap the most recently selected Spotlight item.

    :param light: Optional Spotlight item object (type lx.symbol.sITYPE_SPOTLIGHT)  or string (item name or ID)
        to look up.
    :type light: an instance of lx.object.Item, lxu.object.item or modo.item.Item
    :raises ValueError: if no valid Spotlight item selected.
    :raises TypeError: if the item passed as an argument isn't either a Spotlight item or an item name or ID string.
    :raises LookupError: if a name or ID is supplied as the light argument but no item with that name/ID can
        be found.

    """
    def __init__(self, light=None):
        # before calling the parent's __init__ method ensure that any incoming item is of the correct type for the
        # subclass, or, if no item is passed as an argument & we fall back to getting a selected item, that too is of
        # the correct type.
        if light:
            if isinstance(light, str):
                light = scene.Scene().ItemLookup(light)
            if (isinstance(light, (lx.object.Item, Item))) and (light.Type() != c.SPOTLIGHT_TYPE):
                raise TypeError("Spotlight light item is required")
        else:
            selection = lxu.select.ItemSelection().current()
            for sel in reversed(selection):
                if sel.Type() == c.SPOTLIGHT_TYPE:
                    light = sel
                    break
            else:
                raise ValueError("No valid spotlight item selected")
        Light.__init__(self, light)


class LightMaterial(Item):
    """Wraps a light material texture layer item.

        :param material: the light material item to be wrapped.
        :type material: lx.object.Item of type lx.symbol.sITYPE_LIGHTMATERIAL

        """
    def __init__(self, material):
        if not isinstance(material, (lx.object.Item, Item)):
            raise TypeError("Item type is required")
        if material.Type() != c.SCENE_SVC.ItemTypeLookup(lx.symbol.sITYPE_LIGHTMATERIAL):
            raise TypeError("A light material item is required")
        Item.__init__(self, material)

    @property
    def light(self):
        """:getter: The light item that the material belongs to.

        :param light_item: the light item to parent the material layer to.
        :type light_item: an instance of one of the modo.Light types or either lx.object.Item or lxu.object.Item of
            a specific light item type
        :returns: the parent light item.
        :rtype: one of the modo light types.

        """
        parent = self.Parent()
        func = util.typeToFunc(parent.Type())
        return func(parent)

    @light.setter
    def light(self, light_item):
        self.SetParent(light_item)

    @property
    def lightCol(self):
        """A wrapper property for the light material item's three diffuse color channels. Returns an
        :class:`modo.channel.Channel` object

        :getter: Returns a channelTriple object.
        :rtype: modo.channel.channelTriple

        """
        return self.channel('lightCol')

    @property
    def shadCol(self):
        """:getter: A wrapper property for the light material item's three shadow color channels. Returns an
        :class:`modo.channel.Channel` object

        :returns: a channelTriple object.
        :rtype: modo.channel.channelTriple

        """
        return self.channel('shadCol')

    @property
    def scatteringCol(self):
        """:getter: A wrapper property for the light material item's three scattering color channels. Returns an
        :class:`modo.channel.Channel` object

        :returns: a channelTriple object.
        :rtype: modo.channel.channelTriple

        """
        return self.channel('scatteringColor')


class Group(Item):
    """A group item.

    Takes an optional 'groupItem' argument which can be either an item object (lx.object.Item or lxu.object.Item) of
    type 'Group' or an item name or ID to look up. If no groupItem is supplied as an argument an attempt will be
    made to wrap the most recently selected Area Light item.

    NOTE: The 'gtype' argument is now deprecated and unused.
    
    :param groupItem: an optional group item (type lx.symbol.sITYPE_GROUP) or an item name/ID to look up.
    :type groupItem: an instance of lx.object.Item, lxu.object.item or modo.item.Item
    :raises TypeError: if an item is supplied as the groupItem argument but is not of type lx.symbol.sITYPE_GROUP.
    :raises ValueError: if no groupItem argument is supplied and no valid group item is selected in the scene.
    :raises LookupError: if a name or ID is supplied as the groupItem argument but no item with that name/ID can
        be found.

    Note that the children() method derived from the Item object will only list child groups.
    To iterate the contained items, use the method items.

    """
    def __init__(self, groupItem=None, gtype=''):
        if groupItem:
            if isinstance(groupItem, str):
                groupItem = scene.Scene().ItemLookup(groupItem)
            if (isinstance(groupItem, (lx.object.Item, Item))) and not groupItem.TestType(c.GROUP_TYPE):
                raise TypeError("A group item is required.")
        else:
            selection = lxu.select.ItemSelection().current()
            for sel in reversed(selection):
                if sel.Type() == c.GROUP_TYPE:
                    groupItem = sel
                    break
            else:
                raise ValueError("No valid group item selected")
        Item.__init__(self, groupItem)
        
        self._itemGraph = lx.object.ItemGraph(self.scene.GraphLookup(lx.symbol.sGRAPH_ITEMGROUPS))
        self._channel_graph = lx.object.ChannelGraph(self.scene.GraphLookup(lx.symbol.sGRAPH_CHANGROUPS))

    @property
    def type(self):
        """Get or set the group type.
        If the group is a general group it has no type so returns None.

        :getter: Returns the type of the group.
        :rtype: basestring or empty string
        :raises ValueError: if the supplied argument isn't one of the default group type strings.

        :setter: Sets the group type
        :param gtype: either one of the available group types - 'assembly', 'actor', 'render', 'keyset', 'chanset',
            'preset', 'shader' to define the group as one of the built in types or any other string to define the
            group as a custom type of your own.
        :type gtype: basestring
        """
        if self.hasTag('GTYP'):
            return self.readTag('GTYP')            
        
        return ''

    @type.setter
    def type(self, gtype):
        self.setTag('GTYP', gtype)

    def hasItem(self, item):
        """

        :param item:
        :type item:
        :returns: True if the item is in the group, False if not.
        :rtype: bool
        """
        for connection in range(self._itemGraph.RevCount(item)):
            groupItem = self._itemGraph.RevByIndex(item, connection)
            if groupItem == self:
                return True
        return False

    def addItems(self, items):
        """Add one or more items to the group if they're not already members.

        :param items: the item or items to add
        :type items: modo.item.Item or list of modo.item.Item objects

        """
        if not isinstance(items, Iterable):
            items = [items]
        for item in items:
            if not self.hasItem(item):
                self._itemGraph.AddLink(self, item)

    def removeItems(self, items):
        """Remove one or more items from the group, if they exis.

        :param items: the item or items to remove.
        :type items: modo.item.Item or list of modo.item.Item objects

        """
        if not isinstance(items, Iterable):
            items = [items]
        for item in items:
            if self.hasItem(item):
                self._itemGraph.DeleteLink(self, item)

    @property
    def itemCount(self):
        """The number of items in the group

        :getter: Returns the number of items
        :rtype: int

        """
        return self._itemGraph.FwdCount(self)

    @property
    def items(self):
        """Get a list of the items in the group.

        :returns: the items in the group.
        :rtype: list

        """
        item_list = [self._itemGraph.FwdByIndex(self, x) for x in range(self._itemGraph.FwdCount(self))]

        # Convert items to class instances
        for i, item in enumerate(item_list):
            cls = util.typeToFunc(item.Type())
            item_list[i] = cls(item)

        return item_list

    def getItemIndex(self, item):
        """Index of the item within the groups list of items.

        :return: item index in the group.
        :rtype: int

        """
        for x in range(self._itemGraph.FwdCount(self)):
            groupItem = self._itemGraph.FwdByIndex(self, x)
            if groupItem == item:
                return x

    def setItemIndex(self, item, index):
        """Set's the index for the specified item in the list of items within the group.

        :param item: the item to move
        :type item: modo.item.Item
        :param index: the index in the list of items belonging to the group to move the item to.
        :type index: int
        :raises ValueError: if index is less than zero.

        """
        if index < 0:
            raise ValueError("Must be a positive integer")
        for x in range(self._itemGraph.FwdCount(self)):
            groupItem = self._itemGraph.FwdByIndex(self, x)
            if groupItem == item:
                self._itemGraph.SetLink(self, index, item, -1)
                break

    def getItemAt(self, index):
        """Gets the item at the specified index.

        :returns: item at the specified index.
        :rtype: modo.item.Item
        :param index: index of the item in the group's list of items.
        :type index: int

        """
        return Item(self._itemGraph.FwdByIndex(self, index))

    def removeItemAt(self, index):
        """Removes the item at the specified index from the group's list of items.

        :param index: index of the item in the group's list of items.
        :type index: int

        """
        self._itemGraph.DeleteLink(self, self.getItemAt(index))

    def hasChannel(self, chan, item=None):
        """Check to see if the specified channel is a member of the group.
        The supplied channel argument be a :class:`modo.channel.Channel` object, in which case no item argument
        is required, a channel name (string) or index (int), both of which require an additional 'item' argument.

        :param chan: the channel to check
        :type chan: modo.channel.Channel, int or basestring
        :param item: the item to which the channel belongs. Not required if a Channel() object is provided as the
            first argument.
        :type item: modo.item.Item
        :returns: True if the channel is in the group, False if not.
        :rtype: bool
        """
        if isinstance(chan, str):
            chan = item.ChannelLookup(chan)
        if isinstance(chan, Channel):
            item = chan.item
            chan = chan.index
        for x in range(self._channel_graph.RevCount(item, chan)):
            group, channel = self._channel_graph.RevByIndex(item, chan, x)
            if group == self:
                return True
        return False

    def addChannel(self, chan, item=None):
        """Add a channel to the group.
        The supplied channel argument be a modo.channel.Channel() object, in which case no item argument is required or a channel
        name (string) or index (int), both of which require an additional 'item' argument.

        :param channel: the channel to add.
        :type channel: modo.channel.Channel() object, int or basestring
        :param item: the item to which the channel belongs. Not required if a Channel() object is provided as the
            first argument.
        :type item: modo.item.Item

        """
        if isinstance(chan, str):
            chan = item.ChannelLookup(chan)
        if isinstance(chan, Channel):
            item = chan.item
            chan = chan.index
        if not self.hasChannel(chan, item):
            self._channel_graph.AddLink(self, -1, item, chan)

    def removeChannel(self, chan, item):
        """Remove a channel from the group.
        The supplied channel argument can either be a channel name (string) or index (int).

        :param item: the item to which the channel belongs.
        :type item: modo.item.Item
        :param channel: the channel to remove.
        :type channel: int or basestring

        """
        if isinstance(chan, str):
            chan = item.ChannelLookup(chan)
        if isinstance(chan, Channel):
            item = chan.item
            chan = chan.index
        if self.hasChannel(chan, item):
            self._channel_graph.DeleteLink(self, -1, item, chan)

    @property
    def groupChannelCount(self):
        """The number of channels in the group.

        :getter: Returns the number of channels in the group.
        :rtype: int

        """
        return self._channel_graph.FwdCount(self, -1)

    @property
    def groupChannels(self):
        """returns a list of all the channels in the group.
        Each element of the list will be an modo.channel.Channel

        :getter: Returns a list of channels.
        :rtype: list of modo.channel.Channel items

        """
        channels = []
        for x in range(self._channel_graph.FwdCount(self, -1)):
            item, chan = self._channel_graph.FwdByIndex(self, -1, x)
            func = util.typeToFunc(item.Type())
            channels.append(Channel(chan, func(item)))
        return channels

    def groupGetChannelAt(self, index):
        """Gets the channel at the specified index.

        :returns: the channel at the specified index.
        :rtype: modo.channel.Channel
        :param index: index of the channel in the group's list of channels.
        :type index: int

        """
        item, channel = self._channel_graph.FwdByIndex(self, -1, index)
        func = util.typeToFunc(item.Type())
        return Channel(channel, func(item))

    def groupRemoveChannelAt(self, index):
        """Removes the channel at the specified index from the group's list of channels.

        :param index: index of the channel in the group's list of channels.
        :type index: int

        """
        item, channel = self._channel_graph.FwdByIndex(self, -1, index)
        self._channel_graph.DeleteLink(self, -1, item, channel)


class RenderPassGroup(Group):
    """Render pass group

    :param groupItem: either a group item or an item name/ID to look up.
    :type groupItem: lx.object.item or modo.item.Item
    :raises TypeError: if the item is not a 'Group" item.
    :raises LookupError: if a name or ID is supplied as the groupItem argument but no item with that name/ID can
        be found.

    """
    def __init__(self, groupItem):
        if isinstance(groupItem, str):
                groupItem = scene.Scene().ItemLookup(groupItem)
        if isinstance(groupItem, (lx.object.Item, Item)) and groupItem.Type() != c.GROUP_TYPE:
            raise TypeError("Group item is required")
        Group.__init__(self, groupItem, 'render')

    def addPass(self, name=None):
        """Add a render pass item to the group.

        :param name: optional name for the render pass
        :type name: basestring
        :return: the render pass item.
        :rtype: modo.item.ActionClip

        """
        rpass = self.scene.addItem(c.SCENE_SVC.ItemTypeLookup('actionclip'))
        rpass.name = name
        self._itemGraph.AddLink(self, rpass)
        return rpass

    @property
    def passes(self):
        """:getter: Returns a lst of render passes in the group.

        :returns: list of render pass items
        :rtype: list of modo.item.ActionClip

        """
        p = []
        for x in range(self._itemGraph.FwdCount(self)):
            try:
                p.append(ActionClip(self._itemGraph.FwdByIndex(self, x)))
            except TypeError:
                continue
        return p


class ActionClip(Item):
    """Action Clip and Render pass item.

    :param item: either an item of type 'actionclip' or an item name/ID to lookup.
    :type item: an instance of modo.item.Item

    """
    def __init__(self, clip):
        if isinstance(clip, str):
                clip = scene.Scene().ItemLookup(clip)
        if clip.Type() not in (c.SCENE_SVC.ItemTypeLookup('actionclip'), c.SCENE_SVC.ItemTypeLookup('actionpose')):
            raise TypeError("Item of type 'actionclip' or 'actionpose' is required")
        Item.__init__(self, clip)
        self.actionClip = lx.object.ActionClip(self)

    @property
    def name(self):
        """Name of the render pass.

        :getter: Returns the name of the render pass
        :rtype: basestring

        :setter: Assigns a new name to the render pass
        :param name: new name for the render pass.
        :type name: basestring
        """
        return self.UniqueName()

    @name.setter
    def name(self, name):
        self.SetName(name)

    @property
    def active(self):
        """Set or get the active state of the render pass.

        :getter: Returns the active state of the render pass.
        :rtype: bool

        :setter: Sets the active state of the renter pass
        :param state: active state.
        :type state: bool
        """
        return self.actionClip.Active()

    @active.setter
    def active(self, state):
        self.actionClip.SetActive(state)

    @property
    def enabled(self):
        """Get or set the enabled state of the render pass.

        :getter: Returns the enabled state.
        :rtype: bool

        :setter: Sets the enabled state of the render pass
        :param state: enabled state.
        :type state: bool

        """
        return self.actionClip.Enabled()

    @enabled.setter
    def enabled(self, state):
        self.actionClip.SetEnabled(state)

    @property
    def passGroup(self):
        """The render pass group that the render pass belongs to.

        :getter: Returns the render pass group
        :rtype: modo.item.RenderPassGroup

        :setter: Sets the render pass group
        :param group: render pass group to parent to.
        :type group: modo.item.RenderPassGroup

        """
        itemGraph = lx.object.ItemGraph(self.scene.GraphLookup(lx.symbol.sGRAPH_ITEMGROUPS))
        for x in range(itemGraph.RevCount(self)):
            item = itemGraph.RevByIndex(self, x)
            if isinstance(item, RenderPassGroup):
                return item

    @passGroup.setter
    def passGroup(self, group):
        if not isinstance(group, RenderPassGroup):
            raise ValueError("An instance of modo.item.RenderPassGroup is required.")
        itemGraph = lx.object.ItemGraph(self.scene.GraphLookup(lx.symbol.sGRAPH_ITEMGROUPS))
        itemGraph.AddLink(group, self)

    def setValue(self, chan, value, time=0.0, key=False):
        """Set a value on a channel for this render pass.

        :param chan: the channel to set the value on.
        :type chan: modo.channel.Channel object
        :param value: the value to set for the channel.
        :type value: any
        :param time: the time (in seconds) to set the value for, defaults to 0.0.
        :type time: float
        :param key: whether to set a key for the value or not, defaults to False.
        :param key: bool

        """
        if not isinstance(chan, Channel):
            raise TypeError("An modo.channel.Channel object is required")
        self.active = True
        chan.set(value, time, key, self.name)

    def getValue(self, chan, time=0.0):
        """Read a value set on a channel for this render pass.

        :param chan: the channel to read the value from.
        :type chan: modo.channel.Channel object
        :param time: the time (in seconds) to read the value for, defaults to 0.0.
        :type time: float

        """
        if not isinstance(chan, Channel):
            raise TypeError("An modo.channel.Channel object is required")
        self.active = True
        return chan.get(time, self.name)


class Actor(Group):
    """Wrapper class for actor groups.

    """

    def __addClip(self, name=None, pose=False):
        typ = c.ACTIONPOSE_TYPE if pose else c.ACTIONCLIP_TYPE
        action_item = self._scene.ItemAdd(typ)
        if name:
            action_item.SetName(name)
        action_clip = ActionClip(action_item)
        action_clip.actionClip.SetParenting(self._item)
        self.addItems(action_clip)
        return action_clip

    def addAction(self, name=None):
        """Adds an action to this actor

        Note: please avoid naming actions 'setup', 'edit' or 'scene'

        :returns ActionClip: ActionClip
        :param basestring name: Optional name for the action
        """
        if name in ['setup', 'edit', 'scene']:
            raise ValueError('This name is a reserved constant')

        return self.__addClip(name, pose=False)

    def addPose(self, name=None, activate=True):
        """Adds a pose to this actor

        :returns ActionClip: ActionClip
        :param basestring name: Optional name for the pose
        """
        return self.__addClip(name, pose=True)

    @property
    def actions(self):
        """
        :getter: Returns a list of ActionClip objects for this Actor
        :rtype: list
        """
        return [ActionClip(i) for i in super(Actor, self).items
                if i.TestType(c.ACTIONCLIP_TYPE) and not i.TestType(c.ACTIONPOSE_TYPE)]

    @property
    def poses(self):
        """
        :getter: Returns a list of ActionClip objects for this Actor
        :rtype: list
        """
        return [ActionClip(i) for i in super(Actor, self).items if i.TestType(c.ACTIONPOSE_TYPE)]

    def pose(self, poseName):
        """Return a pose by name

        :param basestring poseName: Name of the pose to look up
        :returns: Pose
        """
        for pose in self.poses:
            if pose.name == poseName:
                return pose

        return None

    @property
    def currentAction(self):
        """
        :getter: Returns the currently active action if any. None if no action is active
        :rtype: ActionClip
        """
        for action in self.actions:
            if action.active:
                return action
        else:
            return None

    @property
    def items(self):
        """
        :getter: Returns a list of LocatorSuperType items that are connected to this action.
        :rtype: list
        """
        return [i for i in super(Actor, self).items if i._item.TestType(c.LOCATOR_TYPE)]


class ItemGraph(object):
    """Utility container class for quick access to ItemGraph compatible graphs

    :param item:                            Item to look up graph for
    :param ls.symbol.sGRAPH_* graphType:    Graph to look up. Common ones are 'parent', 'deformers', 'groups', 'chanMods'
    :param bool reverse:                    Indices traverse the graph forwards if false or reverse if true
    """

    _graphCache = {}

    def __init__(self, item=None, graphType='parent', reverse=True):
        if isinstance(item, str):
            self._item = Item(item)
        else:
            self._item = lx.object.Item(item)

        scene = self._item.Context ()
        scnPointer = scene.__peekobj__()
        self._graph = None
        if scnPointer in ItemGraph._graphCache:
            graphs = ItemGraph._graphCache[scnPointer]
        else:
            ItemGraph._graphCache[scnPointer] = {}
            graphs = ItemGraph._graphCache[scnPointer]
        
        if graphType in graphs:
            self._graph = graphs[graphType]
        else:
            graph = lx.object.ItemGraph(scene.GraphLookup(graphType))
            graphs[graphType] = graph
            self._graph = graph

        if not self._graph.test():
            raise ValueError("graph invalid")

        self._reverse = reverse
        
        self._indexFunc = self._graph.RevByIndex if self._reverse else self._graph.FwdByIndex
        self._graphType = graphType

        self.setReverse(reverse)

    def __repr__(self):
        return "modo.%s('%s', '%s')" % (self.__class__.__name__, self._item.Ident(), self._graphType)

    @staticmethod
    def __toType(item):
        return util.typeToFunc(item.Type())(item)

    def __len__(self):
        if self._reverse:
            return self._graph.RevCount(self._item)
        return self._graph.FwdCount(self._item)

    def __getitem__(self, index):
        item_ = self._indexFunc(self._item, index)
        return ItemGraph.__toType(item_)

    def __getattr__(self, attr):
        return getattr(self._graph, attr)

    def __iter__(self):
        for i in range(len(self)):
            item_ = self._indexFunc(self._item, i)
            yield ItemGraph.__toType(item_)

    def __delitem__(self, key):
        if self._reverse:
            self.DeleteLink(self.reverse(key), self._item)
        else:
            self.DeleteLink(self._item, self.reverse(key))

    def _items(self, index=None, asSubType=True):
        if index is not None and isinstance(index, int):
            if not asSubType:
                result = Item(self._indexFunc(self._item, i))
            else:
                result = self[index]
        else:
            if not asSubType:
                result = [Item(self._indexFunc(self._item, i)) for i in range(len(self))]
            else:
                result = [self[i] for i in range(len(self))]
        return result

    def _iteritems(self, asSubType=True, reverseIter=False):
        indices = range(len(self))
        if reverseIter:
            indices = reversed(indices)
            
        for i in indices:
            if not asSubType:
                yield Item(self._indexFunc(self._item, i))
            else:
                yield self[i]

    def forward(self, index=None, asSubType=True):
        """
        :returns list: Items of the forward connections
        :param bool asSubType: if False, all items are returned as modo.Item rather than relevant subtype to improve performance
        """
        before = self._reverse
        self.setReverse(False)
        
        result = self._items(index, asSubType)
        
        self.setReverse(before)
        return result

    def reverse(self, index=None, asSubType=True):
        """
        :returns list: Items of the reverse connections
        :param bool asSubType: if False, all items are returned as modo.Item rather than relevant subtype to improve performance
        """
        before = self._reverse
        self.setReverse(True)
        
        result = self._items(index, asSubType)
        
        self.setReverse(before)
        return result

    def iterForward(self, asSubType=True, reverseIter=False):
        """
        :returns generator: Items of the forward connections
        :param bool asSubType: if False, all items are returned as modo.Item rather than relevant subtype to improve performance
        :param bool reverseIter: If True the graph is iterated backwards.
        """
        before = self._reverse
        self.setReverse(False)
        
        for i in self._iteritems(asSubType, reverseIter):
            yield i
        
        self.setReverse(before)

    def iterReverse(self, asSubType=True, reverseIter=False):
        """
        :returns generator: Items of the reverse connections
        :param bool asSubType: if False, all items are returned as modo.Item rather than relevant subtype to improve performance
        :param bool reverseIter: If True the graph is iterated backwards.
        """
        before = self._reverse
        self.setReverse(True)
        
        for i in self._iteritems(asSubType, reverseIter):
            yield i
        
        self.setReverse(before)

    @property
    def connectedItems(self):
        """
        :getter: Returns a dictionary that lists the input- and output items at once.
        :rtype: dictionary
        """
        return {key : value for key, value in zip( ('Reverse', 'Forward'), (self.reverse(), self.forward()) )}

    def setReverse(self, reverse):
        """Sets the direction that is used for lookup when using the angular brackets []

        :param bool reverse: If True the graph is looked up forwards, if False, backwards.
        """
        self._indexFunc = self._graph.RevByIndex if reverse else self._graph.FwdByIndex
        self._reverse = reverse

    @property
    def type(self):
        """
        :getter: Returns the name of the graph type that this instance represents.
        :return type: basestring
        """
        return self._graphType

    def deleteLink(self, *args, **kwargs):
        self._graph.DeleteLink(*args, **kwargs)

    # def setLink(self, itemFrom, fromIndex, itemTo, toIndex):
    #     self._graph.SetLink(itemFrom, fromIndexm, itemTo, toIndex)

    def setLink(self, *args, **kwargs):
        self._graph.SetLink(*args, **kwargs)

    def connectInput(self, other):
        """Connects the given item as input.

        This function is called by the >> operator.

        :param Item other: Can be any type derived from Item
        """
        self._graph.AddLink(other, self._item)

    def disconnectInput(self, other):
        """Removes the given item from the input connections if any.

        This function is called by the << operator.

        :param Item other: Can be any type derived from Item
        """        
        sceneService = lx.service.Scene()
        
        if isinstance(other, int):
            del self[other]
            
        else:
            if isinstance(other, (lx.object.Item, lxu.object.Item)):
                item = other
            elif hasattr(other, 'internalItem'):
                item = other

            elif isinstance(other, ItemGraph):
                item = other.item

            else:
                raise TypeError("Could not disonnect %s from graph" % self.item)

            self._graph.DeleteLink(item, self._item)

    @property
    def item(self):
        """
        :getter: Returns the Item that this ItemGraph instance is bound to.
        :return type: Item
        """
        return self._item

    def __rshift__(self, other):
        """Connect this item to an ItemGraph

        :param other:
        :return:
        """
        if not self._item.test() or not other._item.test():
            raise ValueError("Invalid item")

        other.connectInput(self._item)

    def __lshift__(self, other):
        """<< operator for disconnecting from another channel

        :param Channel other: Connected channel to disconnect from
        """
        if not isinstance(other, ItemGraph) and not ( hasattr(other, '_item') and other._item.test() ):
            raise AttributeError("The input type must be an ItemGraph or an item")
        self.disconnectInput(other)


class DeformerGroup(Item):

    def __init__(self, item):
        if isinstance(item, str):
                item = scene.Scene().ItemLookup(item)
        if not item.TestType(c.DEFORMGROUP_TYPE):
            raise TypeError("Item of type 'deformGroup' is required")
        Item.__init__(self, item)

        self._deformTreeGraph = ItemGraph(self._item, 'deformTree')

    def connectInput(self, other):
        """Connects an influence deformer into this deformGroup

        :param other:
        """
        self._deformTreeGraph.AddLink(other, self._item)

    def createJointLocator(self, name=None):
        mesh = self.mesh()
        if not mesh:
            return None

        joint = self.scene.addJointLocator(name)

        influence = self.scene.addItem('genInfluence', 'Transform: %s' % name)
        influence >> self
        influence.channel('type').set('mapWeight')
        influence.channel('name').set(joint.UniqueName())
        influence >> mesh.itemGraph('deformers')

        joint >> influence

        weightmap = mesh.geometry.vmaps.addWeightMap(joint.UniqueName(), initValue=0.0)
        mesh.geometry.setMeshEdits()

        return joint, influence, weightmap

    def mesh(self):
        for it in self.itemGraph('deformers').forward():
            if it.type == 'mesh':
                return it
        return None


class Deformer(Item):

    svc = lx.service.Deformer()

    def __init__(self, item):
        if isinstance(item, str):
                item = scene.Scene().ItemLookup(item)
        if not item.test():
            raise TypeError("Invalid item")

        Item.__init__(self, item)

    @property
    def numMeshes(self):
        """
        :getter: Returns the number of meshes connected to this deformer
        """
        return Deformer.svc.MeshCount(self)

    @property
    def meshes(self):
        """
        :getter: Returns a list of connected meshes
        """
        return [Mesh(Deformer.svc.MeshByIndex(self, i)) for i in range(self.numMeshes)]


class GeneralInfluenceDeformer(Deformer):

    def connectInput(self, other):
        self.itemGraph('deformers').AddLink(other, self._item)

    @property
    def mapName(self):
        """
        :getter: Returns the UI version of the map name as string
        """
        weightMapDeformerItem = lx.object.WeightMapDeformerItem(self)
        return weightMapDeformerItem.GetMapName(self.scene.chanRead)


