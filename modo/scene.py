#
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.
#

"""

.. module:: modo.scene
   :synopsis: Scene class and scene level utility functions.

.. moduleauthor:: Gwynne Reddick <gwynne.reddick@thefoundry.co.uk>

"""

import lx
import lxu
import lxu.select
from . import constants as c
from . import item
from . import util
from .channel import ChannelRead, ChannelWrite
from fnmatch import fnmatch


def current():
    return Scene(lxu.select.SceneSelection().current())


def sceneList():
    """Get a list of all the currently open scenes.

    :returns: Collection of currently open scenes as modo.scene.Scene objects.
    :rtype: list

    """
    rootCinema = c.SCENE_SVC.Root()
    return [Scene(rootCinema.SubSceneByIndex(c.MESH_TYPE, x)) for x in range(rootCinema.SubSceneCount(c.MESH_TYPE))]


class Scene(object):
    """The main scene class.

    Takes an optional lx.object.Scene object as an argument. If none is provided (the default) then the currently
    selected scene is used which will mostly be the general case. The module function :func:`sceneList` makes use of
    the scene parameter to return a list of open scenes as modo.scene.Scene objects.

    :param scene: Optional scene object to wrap.
    :type scene: lx.object.Scene

    """

    def __init__(self, scene=None):
        if not scene:
            self.scene = lxu.select.SceneSelection().current()
        else:
            if not isinstance(scene, lx.object.Scene):
                raise TypeError("Scene type is required")
            self.scene = scene

        self.selSvc = lx.service.Selection()
        if not hasattr(self.scene, '_item'):
            self._item = item.Item(self.scene.AnyItemOfType(c.SCENE_TYPE))

        self.chanRead = ChannelRead(self)
        self.chanWrite = ChannelWrite(self)

    def __getattr__(self, attr):
        try:
            return getattr(self.scene, attr)
        except AttributeError:
            return getattr(self._item, attr)

    @property
    def sceneItem(self):
        """The scene's 'scene item'

        :getter: Returns the scene's scene item.
        :rtype: lxdt.item.Item (type lx.symbol.sITYPE_SCENE)
        """
        return self._item

    @property
    def name(self):
        """Friendly name of the scene.

        :getter: Returns the name of the scene.
        :rtype: basestring

        """
        return self.FriendlyFilename(0)

    @property
    def filename(self):
        """File path of the scene.

        :getter: Returns the file path of the scene or 'None' if not yet saved.
        :rtype: basestring or None

        """
        return self.Filename()

    @property
    def fps(self):
        """Scene frames per second.

        .. note::
            There is no way to set the fps value from the Python API for any scene other than the currently selected
            one. Therefore, for any other scene the property will be read only and attempts to write to it will throw
            an AttributeError.

        |

        :getter: Returns the Frames Per Second
        :rtype: float

        :setter: Sets the Frames Per Second
        :param fps: Scene frames per second.
        :type fps: float
        :raises: AttributeError

        """
        return lx.eval('time.fpsCustom ?')

    @fps.setter
    def fps(self, fps):
        if self == lxu.select.SceneSelection().current():
            lx.eval('time.fpsCustom %s' % fps)
        else:
            raise AttributeError("Unable to set FPS on non-selected scene")

    @property
    def sceneRange(self):
        """Set or read the scene's frame range
        start and end frame value should be passed in as a tuple.

        :setter: Sets the range
        :param frange: frame range - a tuple of ints (start, end).
        :type frange: tuple

        :getter: Returns the start and end frames.
        :rtype: tuple
        :exception ValueError: if supplied start frame is higher than end frame.

        """
        start = int(round(lx.eval('time.range scene in:?') * self.fps))
        end = int(round(lx.eval('time.range scene out:?') * self.fps))
        return (start, end,)

    @sceneRange.setter
    def sceneRange(self, frange):
        start, end = frange
        if start > end:
            raise ValueError('start value should be less than or equal to end value')
        currStart, currEnd = self.sceneRange
        if end < currStart:
            lx.eval('time.range scene in:%s' % float(start / self.fps))
            lx.eval('time.range scene out:%s' % float(end / self.fps))
        else:
            lx.eval('time.range scene out:%s' % float(end / self.fps))
            lx.eval('time.range scene in:%s' % float(start / self.fps))

    @property
    def currentRange(self):
        """Set or read the current frame range
        start and end frame value should be passed in as a tuple.

        :setter: Sets the range
        :param frange: frame range - a tuple of ints (start, end).
        :type frange: tuple

        :Getter: Returns the start and end frames.
        :rtype: tuple
        :exception ValueError: if supplied start frame is higher than end frame.

        """
        start = int(round(lx.eval('time.range current in:?') * self.fps))
        end = int(round(lx.eval('time.range current out:?') * self.fps))
        return (start, end,)

    @currentRange.setter
    def currentRange(self, frange):
        start, end = frange
        if start > end:
            raise ValueError('start value should be less than or equal to end value')

        currStart, currEnd = self.currentRange
        if end < currStart:
            lx.eval('time.range current in:%s' % float(start / self.fps))
            lx.eval('time.range current out:%s' % float(end / self.fps))
        else:
            lx.eval('time.range current out:%s' % float(end / self.fps))
            lx.eval('time.range current in:%s' % float(start / self.fps))

    @property
    def selected(self):
        """Selected items in the scene.

        :getter: Returns the selected items
        :rtype: list

        """
        return [util.typeToFunc(selected.Type())(selected) for selected in lxu.select.ItemSelection().current()]

    def selectedByType(self, itype, superType=False):
        """Returns the selected items of a specific type as modo.item.Item objects.

        :param itype: item type to filter on.
        :type itype: int or string
        :return: selcted items of specified type.
        :param bool superType: If True, all items derived fom itype are listed. Otherwise only items of the exact type of itype.
        :rtype: list of modo.item.Item

        """
        if isinstance(itype, str):
            itype = c.SCENE_SVC.ItemTypeLookup(itype)

        # Function to use to convert the item to it's corresponding class instance
        typefunc = util.typeToFunc(itype)

        # Test against 'Type()' by default, but use 'TestType()' when superType is True
        filter_func = lambda itm, typ: itm.Type() == typ
        if superType:
            filter_func = lambda itm, typ: itm.TestType(typ)

        items = []
        for selected in lxu.select.ItemSelection().current():
            if filter_func(selected, itype):
                if superType is True:
                    typefunc = util.typeToFunc(selected.Type())

                items.append(typefunc(selected))

        return items

    def select(self, itemObj, add=False):
        """
        :param itemObj: the item to select.
        :type item: basestring (item name or ID) or instance of either lx.object.Item or modo.item.Item
        :param add: whether to add to the current selection, False replaces the current selection.
        :type add: bool

        Note::

            To clear the selection of the scene, please use deselect() instead.

        """

        if not add:
            self.deselect()

        if not itemObj:
            return

        if not isinstance(itemObj, (list, tuple)):

            if isinstance(itemObj, (item.Item, lx.object.Item)):
                itemObj = itemObj.Ident()

            lxu.select.ItemSelection().select(itemObj, add)

        # If itemObj is a list
        # Optimized for performance, fixing bug 49122
        else:                        
            selsvc = lx.service.Selection()            
            spType = selsvc.LookupType(lx.symbol.sSELTYP_ITEM)
            spTrans = lx.object.ItemPacketTranslation(selsvc.Allocate(lx.symbol.sSELTYP_ITEM))
            
            selsvc.StartBatch()            
            
            for it in itemObj:
                sPacket = spTrans.Packet(it)
                selsvc.Select(spType, sPacket)
                
            selsvc.EndBatch()

    def deselect(self, itemObj=None):
        """Deselect an item.

        :param itemObj: the item to deselect. Clears the entire selection if None
        :type itemObj: basestring (item name or ID) or instance of either lx.object.Item or modo.item.Item

        """
        if itemObj is None:
            c.SEL_SVC.Clear(lx.symbol.iSEL_ITEM)
            return

        if isinstance(itemObj, str):
            itemObj = self.ItemLookup(itemObj)
        seltype = lx.symbol.sSELTYP_ITEM
        spkttype = self.selSvc.LookupType(seltype)
        sptrans = lx.object.ItemPacketTranslation(self.selSvc.Allocate(seltype))
        spacket = sptrans.Packet(itemObj)
        self.selSvc.Deselect(spkttype, spacket)

    @property
    def cameraCount(self):
        """Number of cameras in the scene.

        :getter: Returns the number of camera items.
        :rtype: int

        """
        return self.ItemCount(c.CAMERA_TYPE)

    @property
    def cameras(self):
        """Returns a list of all the camera items in the scene as modo.item.Camera objects.

        :getter: Returns a list of the camera items in the scene.
        :rtype: list of modo.item.Camera

        """
        return [item.Camera(camera) for camera in self.ItemList(c.CAMERA_TYPE)]

    @property
    def renderCamera(self):
        """Get & set the scene's current render camera

        :setter: Set the scene's current render camera
        :param camera: the camera item to set as the current render camera.
        :type camera: lx.object.Item of type 'Camera'

        :getter: Returns the current render camera.
        :rtype: modo.Item.Camera
        """
        return item.Camera(self.RenderCameraByIndex(
            self.renderItem.channel("cameraIndex").get()))

    @renderCamera.setter
    def renderCamera(self, camera):
        if not isinstance(camera, item.Camera):
            raise TypeError("modo Camera item is required")
        # renderItem = item.Item(self.AnyItemOfType(c.RENDER_TYPE))
        renderItem = self.renderItem
        if renderItem:
            renderItem.renderItem.channel('cameraIndex').set(camera.index)
        # renderItem.WriteAction()
        # renderItem.SetChannel('cameraIndex', camera.index)

    @property
    def renderItem(self):
        """
        :getter: Returns the first found render item of the scene
        :rtype: Item
        """
        return item.Item(self.AnyItemOfType(c.RENDER_TYPE))

    def camera(self, cam):
        """Returns a camera item in the scene.
        The supplied argument can be either a string (camera ID or name) or an integer
        (camera index in the scene's collection of cameras)

        :param cam: the camera
        :type cam: basestring or int
        :returns: camera item
        :rtype: modo.item.Camera

        """
        if isinstance(cam, str):
            return item.Camera(self.ItemLookup(cam))
        elif isinstance(cam, int):
            return item.Camera(self.ItemByIndex(c.CAMERA_TYPE, cam))

    def addCamera(self, name=None):
        """Add a new camera item to the scene

        :returns: camera item
        :rtype: modo.item.Camera
        :param name: optional name for the camera.
        :type name: basestring

        """
        camera = item.Camera(self.ItemAdd(c.CAMERA_TYPE))
        if name:
            camera.name = name
        return camera

    def __setupTextureLayerType(self, newItem):

        render = self.renderItem
        index = 0

        try:
            defaultShader = self.AnyItemOfType(c.DEFAULTSHADER_TYPE)
            index = item.Item(defaultShader).parentIndex-1
        except LookupError:
            pass

        if render:
            newItem.setParent(render, index=index)
        else:
            raise Exception("No render item found")

    def __createItem(self, itype, asSubType):
        if isinstance(itype, str):
            itype = c.SCENE_SVC.ItemTypeLookup(itype)
        func = util.typeToFunc(itype)
        newitem = self.ItemAdd(itype)
        if not asSubType:
            newitem = item.Item(newitem)
        else:
            newitem = util.typeToFunc(itype)(newitem)
        newitem._scene = self # This improves performance by reducing the number of new Scene objects created   
        return newitem

    def addItem(self, itype, name=None, asSubType=True):
        """Add a new item to the scene

        :returns: item
        :rtype: modo.item.item
        :param itype: item type
        :type itype: modo.Constant
        :param name: optional name for the item.
        :type name: basestring
        :param asSubType: if False, item is returned as modo.Item rather than relevant subtype
        :type asSubType: bool
        :raises TypeError: When failing

        """
        # Avoid adding a new scene to an existing scene
        if itype in ['scene']:
            raise TypeError('Cannot add a scene to a scene')

        # Create the new item.
        newitem = self.__createItem(itype, asSubType)

        # Parent to the render item if appropriate
        if newitem.superType == 'textureLayer':
            self.__setupTextureLayerType(newitem)   

        if name:
            newitem.name = name

        return newitem

    def addShaderItem(self, itype, name=None, parentToRender=True, asSubType=True):
        """Add a new item to the scene

        :returns: item
        :rtype: modo.item.item
        :param itype: item type
        :type itype: modo.Constant
        :param name: optional name for the item.
        :type name: basestring
        :param parentToRender: When creating a shading-related item (items of superType "textureLayer") it can be optionally parented to the render item so that it shows up in the shader tree view.
        :type parentToRender: bool
        :param asSubType: if False, item is returned as modo.Item rather than relevant subtype
        :type asSubType: bool
        :raises TypeError: When failing

        """
        # Avoid adding a new scene to an existing scene
        if itype in ['scene']:
            raise TypeError('Cannot add a scene to a scene')

        # Test that the item type passed in is derived from the textureLayer type.
        itypeTexLayer = c.SCENE_SVC.ItemTypeLookup(lx.symbol.sITYPE_TEXTURELAYER)
        itypeNewItem = c.SCENE_SVC.ItemTypeLookup(itype)
        if not c.SCENE_SVC.ItemTypeTest(itypeNewItem, itypeTexLayer):
            raise TypeError('Item type is not derived from textureLayer')
        
        # Create the new item.
        newitem = self.__createItem(itype, asSubType)

        if name:
            newitem.name = name

        # Parent to the render item if requested.
        if parentToRender:
            self.__setupTextureLayerType(newitem)

        return newitem

    def addJointLocator(self, name=None, parent=None):
        """Adds a new joint to the scene

        """

        channelValues = {'lsOffsetS': 0.0, 'isRadius': 0.25, 'isAuto': 0, 'isSize.Y': 1.0,
                         'lsShape': 'rhombus', 'isSize.X': 1.0, 'isSize.Z': 1.0, 'lsRadius': 0.5, 'lsWidth': 0.5,
                         'isOffset.Y': 0.0, 'isOffset.X': 0.0, 'isOffset.Z': 0.0, 'isAlign': 0, 'isShape': 'sphere',
                         'isSolid': 0, 'lsAuto': 1, 'lsOffsetE': 0.0, 'isStyle': 'replace', 'lsSolid': 1,
                         'lsHeight': 0.5, 'isAxis': 'z', 'drawShape': 'custom', 'link': 'custom'}

        joint = self.addItem(c.LOCATOR_TYPE)
        joint.setTag('BONE', 'Joint')
        joint.setTag('STAL', '6')
        joint.setTag('STPX','Skeleton_')

        joint.PackageAdd('glItemShape')
        joint.PackageAdd('glLinkShape')

        joint._setChannelValuesFromDict(channelValues, action='setup')

        if name:
            joint.name = name

        if parent:
            if parent.test():
                joint.parent = parent

        # Add 'Rotation Zero' transform
        lx.object.Locator(joint).ZeroTransform(self.chanRead, self.chanWrite, lx.symbol.iXFRM_ROTATION)

        return joint


    def itemCount(self, itype):
        """The number of items of a specified type in the scene.

        :param itype: type of the items.
        :type itype: int or basestring
        :returns: the number of items of the specified type in the scene.
        :rtype: int
        """
        if isinstance(itype, str):
            itype = c.SCENE_SVC.ItemTypeLookup(itype)
        return self.ItemCount(itype)

    def _allItems(self):
        """Utility function to get all items of a scene
        """
        types = []
        for i in range(c.SCENE_SVC.ItemTypeCount()):
            types.append( c.SCENE_SVC.ItemTypeByIndex(i) )

        types.append(0)

        item_types = lx.object.storage()
        item_types.setType('i')
        item_types.set(types)

        idents = set()

        item_count = self.ItemCountByTypes(item_types)

        for i in range(item_count):
            item = self.ItemByIndexByTypes(item_types, i)
            ident = item.Ident()
            if ident not in idents:
                idents.add(ident)
                yield item

    def items(self, itype=None, name=None, superType=True):
        """List of items of the specified type in the scene.

        :param itype: the item type.
        :type itype:
        :param basestring name: Optionally filter result by this text. Can use * and ? wildcards for globbing.
        :param bool superType: If True, all items that have 'itype' as superType are listed. Else, only items of specifically that type are returned.
        :returns: list of the items of the specified type in the scene. If itype is None, all items in the scene are returned.
        :rtype: list
        """
        return list(self.iterItems(itype, name, superType))

    def iterItems(self, itype=None, name=None, superType=True):
        """Same as items(), but returns a generator object.

        """
        if name :
            namefilter = lambda itm: bool(fnmatch(itm.UniqueName(), name))
        else:
            namefilter = lambda itm: True

        typecast = lambda itm: util.typeToFunc(itm.Type())(itm)

        if itype is not None:
            if isinstance(itype, str):        
                itype = c.SCENE_SVC.ItemTypeLookup(itype)

            for item in self.ItemList (itype):
                if namefilter(item) and (superType or item.Type() == itype):
                    yield typecast(item)
        else:
            for item in self._allItems():
                if namefilter(item):
                    yield typecast(item)

    def iterItemsFast(self, itype):
        """Stripped down alternative for the iterItems method to be used in large scenes where performance is crucial. 
        
            All objects are returned as type "modo.Item" instead of being cast to specialized sybtypes as in iterItems()
    
            :param itype: the item type. (i.e. lx.symbol.sITYPE_MESH)
            :type itype: basestring or int
            :returns: Generator object with objects of type Item
            :rtype: generator
        """
        if isinstance(itype, str):
            itype = c.SCENE_SVC.ItemTypeLookup(itype)

        for i in range(self.ItemCount(itype)):
            yield item.Item (self.ItemByIndex(itype, i))

    def item(self, name, asSubType=True):
        """Look up item by name

        :param string name: Name to look for
        :param bool asSubType: if False, item is returned as modo.Item rather than relevant subtype
        :returns item: Found item
        """
        item_ = self.ItemLookup(name)
        if not asSubType:
            return item.Item(item_)
        return util.typeToFunc(item_.Type())(item_)

    def addMesh(self, name=None):
        """Add a new mesh item to the scene

        :returns: mesh item
        :rtype: modo.item.Mesh
        :param name: optional name for the mesh.
        :type name: basestring

        """
        mesh = item.Mesh(self.ItemAdd(c.MESH_TYPE))
        if name:
            mesh.name = name
        return mesh

    @property
    def meshes(self):
        """Returns a list of all the mesh items in the scene as modo.item.Mesh objects.

        :getter: Returns a list of the mesh items in the scene.
        :rtype: list of modo.item.Mesh

        """
        return [item.Mesh(mesh) for mesh in self.ItemList(c.MESH_TYPE)]

    def __ItemAdd(self, groupType):
        # Lukasz pointed out that ItemAdd fails to add the group channels package.
        # This replacement function adds it.
        item_ = self.ItemAdd(groupType)
        lx.object.Item(item_).PackageAdd('uistate')
        return item_

    def addGroup(self, name=None, gtype=''):
        """Add a new group item to the scene

        :returns: group item
        :rtype: modo.item.Group
        :param name: optional name for the group item.
        :type name: basestring
        :param gtype: optional group type, can be one of the default group types ('assembly', 'actor', 'render',
            'keyset', 'chanset', 'preset', 'shader') or any other string to create a custom group type. Default is an
            empty string which creates a 'Genera' group type.
        :type gtype: basestring

        """
        if gtype == 'actor':
            grp = item.Actor(self.__ItemAdd(c.GROUP_TYPE))
        else:
            grp = item.Group(self.__ItemAdd(c.GROUP_TYPE))

        if gtype != '':
            grp.type = gtype

        if name:
            grp.name = name
        return grp

    def addActor(self, name=None, items=None, makeActive=True):
        """Add a new actor to the scene

        :returns modo.item.Actor: Actor item object
        :param basestring name: optional name
        :param list items: list of items for the actor to contain

        """
        group = self.addGroup(name, gtype='actor')
        if items:
            group.addItems(items)

        return group

    @property
    def groups(self):
        """Returns a list of all the group items in the scene as modo.item.Group objects.

        :getter: Returns a list of the group items in the scene.
        :rtype: list of modo.item.Group

        """
        return [item.Group(group) for group in self.ItemList(c.GROUP_TYPE)]

    def getGroups(self, gtype=''):
        """Returns all groups of the given kind
        
        :param gtype: optional group type, can be one of the default group types ('assembly', 'actor', 'render',
            'keyset', 'chanset', 'preset', 'shader') or any other string to create a custom group type. Default is an
            empty string which creates a 'Genera' group type. You can also pass a list of multiple group types.
        :returns list: List of groups matching the type
        """
        gtype = '' if gtype is None else gtype
        multi = True if isinstance(gtype, (list, tuple)) else False
        
        if gtype == '':
            return [item.Group(group) for group in self.ItemList(c.GROUP_TYPE)]
        else:
            result = []
            for group in self.ItemList(c.GROUP_TYPE):
                
                groupItem = item.Group(group)

                if multi:
                    if groupItem.type in gtype:
                        result.append(groupItem)
                else:
                    if groupItem.type == gtype:
                        result.append(groupItem)
                
            return result

    @property
    def actors(self):
        """Returns a list of all actors in the scene

        :getter: Returns a list of Actor objects found in this scene
        :rtype: list

        """
        groups = [item.Actor(group) for group in self.ItemList(c.GROUP_TYPE)]
        return [actor for actor in groups if ('GTYP', 'actor') in list(actor.getTags().items())]

    def addRenderPassGroup(self, name=None):
        """Add a render pass group to the scene

        :returns: render pass group.
        :rtype: modo.item.RenderPassGroup
        :param name: optional name for the render pass group.
        :type name: basestring

        """
        grp = item.RenderPassGroup(self.__ItemAdd(c.GROUP_TYPE))
        if name:
            grp.name = name
            
        grp.setTag ('GTYP', 'render')
        
        return grp

    @property
    def renderPassGroups(self):
        """Returns a list of all the render pass group items in the scene as modo.item.RenderPassGroup objects.

        :getter: Returns a list of the render pass group items in the scene.
        :rtype: list of modo.item.Group

        """
        return [item.RenderPassGroup(group._item) for group in self.groups
                if (group.hasTag('GTYP')) and (group.readTag('GTYP') == 'render')]

    @property
    def lightCount(self):
        """Number of lights in the scene.

        :getter: Returns the number of light items.
        :rtype: int

        """
        return self.ItemCount(c.LIGHT_TYPE)

    @property
    def meshCount(self):
        """Number of mesh items in the scene.

        :getter: Returns the number of mesh items.
        :rtype: int

        """
        return self.ItemCount(c.MESH_TYPE)

    def duplicateItem(self, item, instance=False):
        """Creates and returns a duplicate of the passed item

        :returns item: Item
        """
        if not item.test():
            return None

        if instance:
            duplicate = self.scene.ItemInstance(item)
        else:
            duplicate = self.scene.ItemCopy(item)
        return util.typeToFunc(duplicate.Type())(duplicate)

    def addMaterial(self, matType='advancedMaterial', name=None, index=None):
        """Adds a new material to the scene

        :param modo.c.MATERIAL_* matType: Type of material to create
        :param name: Optional name for the material
        :returns Item: The material item
        """
        render = self.renderItem
        material = self.addItem(matType, name)

        self.__setupTextureLayerType(material)

        return material

    def _addShadeLocItems(self, itm, items, checkReverse=False):
        graph = itm.itemGraph("shadeLoc")
        for other in graph.connectedItems["Forward"]:
            if other in items:
                continue
            # (484715) Check that all reversed items are in items.
            if checkReverse is True:
                notAdd = False
                graph2 = other.itemGraph("shadeLoc")
                for rItem in graph2.connectedItems["Reverse"]:
                    if rItem in items:
                        continue
                    notAdd = True
                    break
                if notAdd is True:
                    continue
            items.add(other)
            self._addShadeLocItems(other, items, checkReverse)

    def removeItems(self, itm, children=False):
        """

        :param Item: Item to remove from the scene
        :param bool children: If True, all found children are deleted also
        """
        
        if itm is None:
            return

        if isinstance(itm, str):
            itm = self.ItemLookup(itm)

        if children:
            if isinstance(itm, (list, tuple)):
                queue = [item.Item(i) for i in itm]
            else:
                queue = [item.Item(itm)]

            items = set()

            while not len(queue) == 0:
                a = queue.pop()
                if a not in items:
                    items.add(a)
                    if a.superType == lx.symbol.sITYPE_TEXTURELAYER:
                        self._addShadeLocItems(a, items, True)
                queue += a.children(recursive=False)

            
            
            # First pass - disconnect instanced objects from their source if any
            for itm in items:
                
                if itm.isAnInstance:
                    graph = itm.itemGraph('source')
                    for sourceItem in graph.forward():
                        graph << sourceItem

            # Second pass - delete the items from the scene
            itemCol  = lx.service.Scene().AllocEmptyCollection()
            for itm in items:                                    
                itemCol.Add(itm)
            self.DeleteCollection(itemCol, lx.symbol.iCOLLECT_DEL_SHALLOW)

        else:
            if isinstance(itm, (list, tuple)):
                for it in itm:
                    if isinstance(it, str):
                        it = self.ItemLookup(it)
                    self.ItemRemove(it)

            else:
                self.ItemRemove(itm)

    def deformers(self):

        result = []
        dvc = lx.service.Deformer()
        for item_ in self._allItems():
            try:
                if dvc.DeformerFlags(item_):
                    result.append(item_)
            except LookupError:
                pass

        return [util.typeToFunc(item_.Type())(item_) for item_ in result]

    @property
    def locators(self):
        # Not in SP0
        # """
        # :getter: Returns all locator items of the scene
        # :rtype: tuple
        # """
        return self.items(itype='locator', superType=True)

    def __contains__(self, obj):
        """
        :returns bool: True if the given item is part of this scene, else False.
        
        example::
        
            print modo.Item('Mesh') in modo.Scene()
            # Result: True
        
        """
        ident = None
        
        if isinstance(obj, str):
            ident = obj
        
        elif isinstance(obj, (item.Item, lx.object.Item, lxu.object.Item) ):
            ident = obj.Ident()
        
        if ident:
            try:
                it = self.ItemLookup(ident)
                return True
            except LookupError:
                return False
        
        return False


