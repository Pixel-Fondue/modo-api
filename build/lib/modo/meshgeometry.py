#
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.
#

"""

.. module:: modo.meshgeometry
   :synopsis: Classes for mesh access and editing

.. moduleauthor:: Ivo Grigull <ivo.grigull@thefoundry.co.uk>

"""

import lx
import lxu
import lxifc
from .constants import *
import lxu.vector as vec3
from . import util
from fnmatch import fnmatch
from .mathutils import Vector3
import weakref
import collections
import sys


# Compatibility functions HACK to make sure python3 scripts using the modo tdsdk behave similar to what they do in python2.
# The more involved fix here is to make sure we don't rely on the differerence between int and long for point/edge/poly/map index args.
# See getIDAsLong() function below
def isPython2CompatibileLongInstance(val):
    if not isinstance(val, int):
        return False

    if (sys.platform == "win32"):
        return (val > 0x7fffffff)

    return (val > 0x7fffffffffffffff)

def isPython2CompatibileIntInstance(val):
    if not isinstance(val, int):
        return False

    if (sys.platform == "win32"):
        return (val <= 0x7fffffff)

    return (val <= 0x7fffffffffffffff)
 

def getIDAsLong(accessor):
    """ 
    Calls the ID() method on the accessor object passed in and returns it as long.
    This is required because the mesh editing system differentiates between int and long for point/edge/poly/map index arguments.
    Ints are treated as regular numbered indices and longs as memory address (ID).
    However the type returned from Modo's Python bindings is inconsistent between platforms (due the PyLong_FromVoidPtr function in Python's C API), 
    sometimes returning point ID's as int and sometimes as long.
    
    :param accessor: A point/edge/poly/map accessor
    :type accessor: lx.object.Point, lx.object.Edge, lx.object.Polygon or lx.object.MeshMap
    """
    return int(accessor.ID())

class MeshGeometry(object):
    """ A class wrapped around lx.object.Mesh that provides access to geometry of a given Mesh Item

    There have been new changes to this class in Modo 10.2, please read :ref:`meshediting102_`
    
    :param item: Input item
    :type item: type lx.object.Item
    :param mode: Mode in which to access the mesh. Possible values: "write", "read", "deformed"
    :type mode: string. Note: References are always read only.
    :return: Instance of MeshGeometry

    :raises LookupError: If item was passed as string and could not be found in the scene
    :raises TypeError: If the passed item is not of type lx.object.Item
    :raises TypeError: If the passed item is not compatible with the mesh type


    example::

        scene = modo.scene.current()

        # Get the selected mesh
        for mesh in scene.selectedByType("mesh")[:1]:

            # Print the number of vertices
            print (len(mesh.geometry.vertices))

            # Print point position by index
            print (mesh.geometry.vertices[4])

            # Set point position by index
            mesh.geometry.vertices[4] = (1,2,3)

            # Iterate all vertices and move them by 0.1 in x
            for point in mesh.geometry.vertices:
                point += (0.1, 0, 0)

            # Update to see mesh changes
            mesh.geometry.setMeshEdits()

    .. py:attribute:: vertices

        :rtype: :class:`MeshVertices<MeshVertices>`

    .. py:attribute:: edges

        :rtype: :class:`MeshEdges<MeshEdges>`

    .. py:attribute:: polygons

        :rtype: :class:`MeshPolygons<MeshPolygons>`

    .. py:attribute:: vmaps

        :rtype: :class:`MeshMaps<MeshMaps>`

    """

    _cache = weakref.WeakValueDictionary()
    _SEL_SVC = lx.service.Selection()
    _UNDO_SVC = lx.service.Undo()

    def __new__(cls, item=None, mode='write'):

        if isinstance(item, str):
            try:
                item = lxu.select.SceneSelection().current().ItemLookup(item)
            except LookupError:
                raise LookupError("Could not find %s" % item)

        elif not isinstance(item, (lx.object.Item)):
            raise TypeError("Item type is required")

        if not item.TestType(item_type('mesh')):
            raise TypeError("Item is not a Mesh")


        # Return a geometry object from cache if found
        for cachedItem, cachedGeometry in cls._cache.items():
            if cachedItem == item and cachedGeometry is not None:
                
                if not cachedGeometry:
                    raise ValueError('Invalid item')
                
                return cachedGeometry

        # ... else create a new object
        self = object.__new__(cls)

        self._scene = item.Context()
        self._item_ = item

        cls._cache[item] = self
        
        # This initializes our mesh and access-attributes
        self.provider = MeshProvider(self._item_, readOnly = (mode=='read'))
        mesh = self.provider.mesh
    
        self.vertices = MeshVertices(mesh, self, "Point")
        self.edges    = MeshEdges(mesh, self)
        self.polygons = MeshPolygons(mesh, self, "Polygon")
        self.vmaps    = MeshMaps(mesh, self, "MeshMap")
                
        return self

    @property
    def _item(self):
        if self._item_.Type() != 0:
            return self._item_
        else:
            raise ValueError("Invalid item")

    def __repr__(self):
        return "modo.%s('%s')" % (self.__class__.__name__, self._item.Ident())

    def __bool__(self):
        if self._item_.Type() == 0:
            return False

        return all([self._item.test(), self.provider.mesh.test(), self._scene.test()])

    @property
    def accessMode(self):
        #  Set or change the kind of access to the mesh.
        #
        # :param value: Mode in which to access the mesh. Possible values: "write", "read", "deformed"
        # :param time: Only relevant for "deformed" mode - will set the mesh up to read positions at the given time
        # """
        return self.__accessMode

    def setAccessMode(self, value='write', time=None):
        """ possible values: 'read', 'write' or 'deformed' """
        self.__accessMode = value
        self.provider.readOnly = (value == 'read')
        
        if value is not 'write':
            self.provider.readOnly = True
            self.provider.useMeshChannel(mode=value, time=time)            

    def setMeshEdits(self, editType=lx.symbol.f_MESHEDIT_GEOMETRY):
        """Updates mesh edits applying previous changes.

        :param lx.symbol.f_MESHEDIT_* editType: The type of change to set. Defaults to all.
        """
        self.provider.applyLayerScan(editType)

    @property
    def boundingBox(self):
        """Get the bounding box of this mesh

        :getter: Returns a tuple representing the two corners of the bounding box
        """
        return self.provider.mesh.BoundingBox(lx.symbol.iMARK_ANY)

    def getMeshCenter(self):
        """:return: Center position of the bounding box
        """
        v1, v2 = (Vector3 (v) for v in self.boundingBox)
        return v1.lerp (v2, 0.5)        

    def __getattr__(self, attr):
        # pass any unknown attribute access on to the wrapped lx.object.Item class to see if
        # it's a recognised call there.
        try:
            return getattr(self.provider.mesh, attr)
        except AttributeError:
            return None

    @property
    def internalMesh(self):
        """
        :getter: Returns the wrapped lx.object.Mesh object
        """
        return self.provider.mesh

    @property
    def numVertices(self):
        """:getter: returns the vertex count of this mesh"""
        return len(self.vertices)

    @property
    def numPolygons(self):
        """:getter: returns the polygon count of this mesh"""
        return len(self.polygons)

    @property
    def numEdges(self):
        """:getter: returns the vertex count of this mesh"""
        return len(self.edges)

    def __enter__(self):
        """This adds support for Pythons idiom of the 'with' statement.

        This is a nice way to guard a block from accessing an invalid geometry.
        """
        if not self:
            raise RuntimeError('Geometry not valid')
        self.provider.beginLayerScan(flags=lx.symbol.f_LAYERSCAN_EDIT)
        
        return self

    def __exit__(self, type, value, traceback):
        self.provider.applyLayerScan()
        return True


class MeshProvider(object):    
    '''
    Given an item, returns access to a mesh object.
    For read-only access (the initial default state), the mesh object obtained from the item's mesh-channel is used.    
    Edits to the geometry can be made after calling beginLayerScan()
    It is then required to call applyLayerScan() in order to finish the edits and release the LayerScan.
    Once the LayerScan is released, MeshProvider goes back to read-only state.
    
    '''
    
    def __init__(self, item, readOnly=False):
        self.item            = item
        self.layerEdit       = None
        self.readOnly        = readOnly
        
        accessMode = 'write' if self.item.Context().SetupMode() else 'read'
        self.useMeshChannel(mode=accessMode)

    @property
    def mesh(self):
        return self._mesh

    @property
    def point(self):
        return self.PointAccessor

    @property
    def polygon(self):
        return self.PolygonAccessor

    @property
    def edge(self):
        return self.EdgeAccessor
    
    @property
    def meshmap(self):
        return self.MeshMapAccessor
    
    def useMeshChannel(self, mode='read', time=None):
        self._mesh           = MeshProvider.meshFromMeshChannel(self.item, mode, time)
        self.PolygonAccessor = self._mesh.PolygonAccessor()
        self.PointAccessor   = self._mesh.PointAccessor()
        self.EdgeAccessor    = self._mesh.EdgeAccessor()
        self.MeshMapAccessor = self._mesh.MeshMapAccessor()

    def beginLayerScan(self, flags=lx.symbol.f_LAYERSCAN_EDIT):
        
        if self.readOnly is True:
            raise RuntimeError ("Attempted to access geometry which is set to read only mode")
        
        if self.layerEdit is not None:
            return
        
        self.layerEdit       = LayerScanItemEdit(self.item, flags)
        
        self._mesh           = self.layerEdit.getMesh()
        self.PolygonAccessor = self._mesh.PolygonAccessor()
        self.PointAccessor   = self._mesh.PointAccessor()
        self.EdgeAccessor    = self._mesh.EdgeAccessor()
        self.MeshMapAccessor = self._mesh.MeshMapAccessor()
    
    def applyLayerScan(self, flags=lx.symbol.f_MESHEDIT_GEOMETRY):
        if self.layerEdit is not None:
            
            # Apply edits and clear object, so it will be re-created by the next getMesh() call.
            self.layerEdit.apply(flags)
            self.layerEdit = None
                    
            # Go to read-only mode unless setup mode is active (
            accessMode = 'write' if self.item.Context().SetupMode() else 'read'            
            self.useMeshChannel(accessMode)
            
        else:
            flags = lx.symbol.f_MESHEDIT_GEOMETRY if flags is None else flags
            self._mesh.SetMeshEdits(flags)            

    @staticmethod
    def meshFromMeshChannel(item, value='write', time=None):
                
        if not value in ['write', 'read', 'deformed']:
            raise ValueError('Mode must be "write", "read" or "deformed"')
    
        time = lx.service.Selection().GetTime() if not time else time
        scene = item.Context()
        mesh = None
    
        if value is "write":
            # Get writeable mesh from channel
            chanWrite = lx.object.ChannelWrite(scene.Channels(lx.symbol.s_ACTIONLAYER_SETUP, time))
            write_mesh_obj = chanWrite.ValueObj(item, item.ChannelLookup(lx.symbol.sICHAN_MESH_MESH))
            mesh = lx.object.Mesh(write_mesh_obj)
    
        elif value is "read":
            # Get writeable mesh from channel
            chanRead = scene.Channels(lx.symbol.s_ACTIONLAYER_ANIM, time)
            read_mesh_obj = chanRead.ValueObj(item, item.ChannelLookup(lx.symbol.sICHAN_MESH_MESH))
            mesh = lx.object.Mesh(read_mesh_obj)
    
        # Fetch the mesh channel and filter to update for the case that deformers were added or removed
        elif value is "deformed":
            chanRead_deformed = scene.Channels(None, time)
            channelmesh = item.ChannelLookup(lx.symbol.sICHAN_MESH_MESH)
            read_deformed_mesh_obj = chanRead_deformed.ValueObj(item, channelmesh)
            mesh_filter = lxu.object.MeshFilter(read_deformed_mesh_obj)
            mesh = mesh_filter.Generate()
    
        if not mesh.test():
            raise LookupError("Invalid mesh")
        
        return mesh


class LayerScanItemEdit(object):
    '''
    Helper class for LayerScan based mesh editing of a single item
    
    It should be noted that the layerScan object in Modo is a global construct and should only be held on 
    for short periods of editing and immediately be released afterwards. This class keeps a reference
    only in order to maintain existing functionality (was doing edits via mesh channel object instead of layerScan before). 
    '''
    
    layerScanService = lx.service.Layer()
    layerScan = None
    
    def __init__(self, item, flags=lx.symbol.f_LAYERSCAN_EDIT):
        
        self._item = item
        self._flags = lx.symbol.f_MESHEDIT_GEOMETRY
        LayerScanItemEdit.release()
    
        if not self.isItemValid():
            raise RuntimeError('Invalid item')
                    
        layerScanService = type(self).layerScanService
        try:
            LayerScanItemEdit.layerScan = layerScanService.ScanAllocateItem(self._item, flags)
            if LayerScanItemEdit.layerScan.Count() == 0:
                raise RuntimeError("No valid mesh found during layer scan allocation")
            
        except RuntimeError:            
            # Clean up all potential previous layer scans
            LayerScanItemEdit.release()

            raise RuntimeError("Layer scan allocation failed. Did you forget to call setMeshEdits earlier?")
        
        self._mesh = LayerScanItemEdit.layerScan.MeshEdit(0)

    def apply(self, flags=lx.symbol.f_MESHEDIT_GEOMETRY):
        '''Pass None for the flags argument if no changes were made. Might fail otherwise'''
        
        if not self.isItemValid():
            LayerScanItemEdit.release()
            raise RuntimeError('Invalid item')
        
        if flags:
            LayerScanItemEdit.layerScan.SetMeshChange(0, lx.symbol.f_MESHEDIT_GEOMETRY)
                    
        LayerScanItemEdit.layerScan.Apply()        
        
    def getMesh(self):
        return self._mesh
    
    def isItemValid(self):
        if self._item.UniqueName() == '*BAD-NULL*':
            return False

        # Is the item still contained in the scene it was created in?
        try:
            sceneContext = self._item.Context()
            sceneContext.ItemLookupIdent (self._item.Ident())
        except LookupError:
            return False
        
        return True

    @staticmethod
    def release():
        del LayerScanItemEdit.layerScan
        LayerScanItemEdit.layerScan = None


class ListenerLayerScan(lxifc.SceneItemListener):
    '''
    Normally Modo's LayerScan is released when it's object goes out of scope, as it should only be held on shortly for performing edits.
    
    The MeshGeometry class initializes a LayerScan object which is held on to until the user releases it 
    by either calling MeshGeometry.setMeshEdits() or when it's context manager is released by using python's "with" statement.
    
    Accessing or releasing the LayerScan at a point where the associated item has become invalid leads to a crash.

    In order to avoid crashes after accidentally not releasing the LayerScan and then making further modifications to the scene,
    the LayerScan is automatically released on these events:
    
    - An item is removed from any scene
    - A scene is either cleared, destroyed or removed.
    '''
    
    def __init__(self):

        self.listenerService = lx.service.Listener()
        self.COM_object = lx.object.Unknown(self)
        self.listenerService.AddListener(self.COM_object)

    def __del__(self):
        self.listenerService.RemoveListener(self.COM_object)

    def sil_SceneClear(self, scene):
        LayerScanItemEdit.release()

    def sil_SceneDestroy(self, scene):
        LayerScanItemEdit.release()

    def sil_SceneCreate(self, scene):
        LayerScanItemEdit.release()
        
    def sil_ItemRemove(self, item):
        LayerScanItemEdit.release()
        
listener = ListenerLayerScan()


class MeshComponentContainer(object):
    """
        Base class for vertex, edge- and polygon containers to share common behaviour
    """
    def __init__(self, mesh, geometry, function_keyword="Point"):
        self.__accessorKeyword = function_keyword
        self._geometry = geometry
        self.provider = geometry.provider
        self.getAccessor = lambda : getattr(self.provider, self.__accessorKeyword + "Accessor")

    @property
    def _accessor(self):
        return self.getAccessor()
    
    def __len__(self):
        func_name = self.__accessorKeyword + "Count"
        func = getattr(self.provider.mesh, func_name)
        try:
            return func()
        except AttributeError:
            return None

    def _getitem(self, index, cls):
        """General access for angular brackets
        """
        # List access
        if isinstance(index, list):
            return [cls(i, self._geometry) for i in index if i >= 0]

        # Slice access
        if isinstance(index, slice):
            indices = index.indices(len(self))
            return (cls(i, self._geometry) for i in range(*indices))

        # Single access
        index = len(self) + index if index <0 else index
        return cls(index, self._geometry)

    def __bool__(self):
        if not self._geometry._item:
            return False
        return bool(len(self))

    @property
    def internalMesh(self):
        """
        :getter: returns the wrapped lx.object.Mesh object
        """
        return self.provider.mesh


class MeshVertex(object):
    """Class representing a single vertex

    example::

        #Supports operators

        v1 = mesh.geometry.vertices[1]
        v2 = mesh.geometry.vertices[2]

        v1 += v2
        v1 = v1 - v2

    """
    def __init__(self, index, geometry):
        """Initializes a vertex from a given MeshGeometry object

        :param int or long vertex: The index of the vertex to be obtained. If vertex is of type long,
        it will be looked up as pointer ID.
        :type: int
        :param geometry: The geometry to obtain the vertex from
        :type: MeshGeometry
        :return: An instance of MeshVertex
        
        Note that indices do not exist immediately after adding a vertex, the edits need to be applied with setMeshEdits to produce indices.        
        """

        if isinstance(geometry, str):
            geometry = MeshGeometry(geometry)
            
        self._geometry = geometry
        self._item = geometry._item
        self.provider = geometry.provider

        mesh  = self._geometry.provider.mesh
        point = self._geometry.provider.PointAccessor
        
        # If is ID (long)
        if isPython2CompatibileLongInstance(index):
            point.Select (index)
            self._id    = getIDAsLong(point)
            return
        
        # Else, if is index (int)
        if not 0 <= index < mesh.PointCount():
            raise LookupError("Index out of bounds")

        try:
            point.SelectByIndex(index)
        except TypeError:
            raise ValueError("Mesh has no vertices")
        
        self._index = point.Index()
        self._id    = getIDAsLong(point)

    @property
    def _accessor(self):
        # This selects the vertex by ID on the shared accessor
        point = self._geometry.provider.point
        point.Select(self._id)
        return point

    @property
    def accessor(self):
        """
        :getter: Returns the internal shared VertexAccessor object of the core SDK (lx.object.Polygon)
        """
        return self._accessor

    @classmethod
    def fromId(cls, id, geometry):
        """Initializes a vertex from a given MeshGeometry object

        :param int or long vertex: The index of the vertex to be obtained. If vertex is of type long, it will be looked up as pointer ID.
        :type: int
        :param geometry: The geometry to obtain the vertex from
        :type: MeshGeometry
        :return: An instance of MeshVertex
        """

        instance           = cls.__new__(cls)
        instance._geometry = geometry
        instance._mesh     = geometry.provider.mesh
        instance.provider  = geometry.provider

        point = geometry.provider.PointAccessor
        try:
            point.Select(id)
        except TypeError:
            raise LookupError('Vertex %i not found' % id)
        
        instance._id    = getIDAsLong(point)
        return instance

    @property
    def position(self):
        """Get or set the local position vector as tuple

        :getter: Returns position as a tuple
        :setter: Takes an Iterable as input to set the position from
        """
        point = self.provider.PointAccessor
        point.Select(self._id)
        return point.Pos()

    @position.setter
    def position(self, position):
        
        self.provider.beginLayerScan()
        
        point = self.provider.PointAccessor
        point.Select(self._id)
        point.SetPos(position)

    @property
    def x(self):
        """
        :getter: Returns the x position
        :setter: Takes a float value to set the x position from
        """
        return self.position[0]

    @x.setter
    def x(self, value):
        pos = self.position
        self.position = (value, pos[1], pos[2])

    @property
    def y(self):
        """
        :getter: Returns the y position
        :setter: Takes a float value to set the y position from
        """
        return self.position[1]

    @y.setter
    def y(self, value):
        pos = self.position
        self.position = (pos[0], value, pos[2])

    @property
    def z(self):
        """
        :getter: Returns the z position
        :setter: Takes a float value to set the z position from
        """
        return self.position[2]

    @z.setter
    def z(self, value):
        pos = self.position
        self.position = (pos[0], pos[1], value)

    def __repr__(self):
        indexOrId = None
        if self.provider.layerEdit is None:
            strIndexOrId = str(self.index)
        else :
            strIndexOrId = str(self._id)+'L'
        return 'modo.%s(%s, \'%s\')' % (self.__class__.__name__, strIndexOrId, self._geometry._item.Ident())

    def __add__(self, other):
        """Adds another position"""
        if isinstance(other, MeshVertex):
            other = other.position

        self.provider.beginLayerScan()            
        self.provider.PointAccessor.Select(self._id)
        pos = list(self.provider.PointAccessor.Pos())
        pos = [a+b for a, b in zip(pos, other)]
        self.provider.PointAccessor.SetPos(pos)
        return self

    def __sub__(self, other):
        """Subtracts from another position"""
        if isinstance(other, MeshVertex):
            other = other.position

        self.provider.beginLayerScan()            
        self.provider.PointAccessor.Select(self._id)
        pos = list(self.provider.PointAccessor.Pos())
        pos = [a-b for a, b in zip(pos, other)]
        self.provider.PointAccessor.SetPos(pos)
        return self

    def __mul__(self, other):
        """Multiplies by another position"""
        if isinstance(other, MeshVertex):
            other = other.position
            
        self.provider.beginLayerScan()                        
        self.provider.PointAccessor.Select(self._id)
        pos = list(self.provider.PointAccessor.Pos())
        pos = [a*b for a, b in zip(pos, other)]
        self.provider.PointAccessor.SetPos(pos)
        return self

    def __truediv__(self, other):
        """Divides by another position"""
        if isinstance(other, MeshVertex):
            other = other.position

        self.provider.beginLayerScan()                        
        self.provider.PointAccessor.Select(self._id)
        pos = list(self.provider.PointAccessor.Pos())
        pos = [a/b for a, b in zip(pos, other)]
        self.provider.PointAccessor.SetPos(pos)
        return self

    def __getattr__(self, attr):
        # pass any unknown attribute access on to the wrapped lx.object.Item class to see if
        # it's a recognised call there.
        return getattr(self._geometry.provider.PointAccessor, attr)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self._id == other._id

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def remove(self):
        """Removes this vertex from the mesh
        """
        self.provider.beginLayerScan()                        
        mesh = self.provider.mesh
        #accessor = mesh.PolygonAccessor()
        polygon = self.provider.polygon
        
        point = self.provider.point
        point.Select(self._id)
        

        # Deselect point first, Crashes otherwise
        self.deselect()

        # Deselect all edges. Deselecting individual edges appears to be broken
        if self._geometry.edges.selected:
            edge_selection = lxu.select.AnySelection(lx.symbol.sSELTYP_EDGE, 'Edge')
            edge_selection.clear()

        points_storage = lx.object.storage()

        # Needs to remove points from all polygons first
        for poly_index in reversed(list(range(mesh.PolygonCount()))):
            polygon.SelectByIndex(poly_index)

            ## See whether our vertex is part of this polygon
            try:
                polygon.PointIndex(self._id)
            except RuntimeError:
                continue

            vlist = []

            # Collect the polygon's points, without the one to be deleted
            for vi in range(polygon.VertexCount()):
                pt = int(polygon.VertexByIndex (vi))
                if not pt == self._id:
                    vlist.append (pt)
                                        

            # Delete the polygon if it would end up with less than 3 points
            if len(vlist) < 3:
                MeshPolygons._performSelectionOperation(getIDAsLong(polygon), mesh, operation='deselect')
                polygon.Remove()
                continue

            # Set the collected points to the storage object
            points_storage.setType('p')
            points_storage.setSize(len(vlist))
            points_storage.set(vlist)

            # Apply the new vertex list to the polygon
            polygon.SetVertexList(points_storage, len(vlist), 0)
                
        point.Remove()

    def __performSelectionOp(self, operation=0, polygon=None):
        if not self.provider.PointAccessor.test() or not self.provider.mesh.test():
            return

        MeshVertices._vertexSelectionOperation(getIDAsLong(self), self.provider.mesh, operation, polygon=polygon)

    def deselect(self):
        """Deselects this vertex
        """
        point = self._geometry.provider.point
        point.Select(self._id)
        self.__performSelectionOp(2)

    def select(self, polygon=None, replace=False):
        """Selects this vertex

        :param MeshPolygon polygon: Selects the vertex specific to this polygon, needed for UV selections
        :param bool replace: Clears the selection before selecting
        """
        point = self._geometry.provider.point
        point.Select(self._id)                
        self.__performSelectionOp(polygon=polygon, operation=int(replace))

    @property
    def index(self):
        """
        :getter: Returns the index of this vertex as integer.
        
        Note that indices do not exist immediately after adding a vertex, the edits need to be applied with setMeshEdits to produce indices.
        """
        point = self._geometry.provider.point
        point.Select(self._id)
        
        return int(point.Index())

    @property
    def id(self):
        """:getter: Returns the pointer ID of this vertex"""
        return getIDAsLong(self.provider.PointAccessor)

    def getUVs(self, uvmap=None):
        if uvmap is None and self._geometry.vmaps.uvMaps:
            uvmap = self._geometry.vmaps.uvMaps[0]

        if uvmap:
            return uvmap[self.index]
        return None

    def setUVs(self, values, polygon=None, uvmap=None):
        self.provider.beginLayerScan()
        if uvmap is None and self._geometry.vmaps.uvMaps:
            uvmap = self._geometry.vmaps.uvMaps[0]

        storage = lx.object.storage()
        storage.setType('f')
        storage.setSize(2)
        storage.set(values)

        if isinstance (polygon, MeshPolygon):
            
            #poly  = self.provider.PolygonAccessor
            
            self.provider.MeshMapAccessor.SelectByName (lx.symbol.i_VMAP_TEXTUREUV, 'Texture')
            mapID = getIDAsLong(self.provider.MeshMapAccessor)
            
            mapID = uvmap._id
            poly.SetMapValue (self._id, mapID, storage)
        else:
            point = self.provider.PointAccessor
            point.Select (self._id)
            point.SetMapValue (uvmap._id, storage)
            return
        
        if uvmap:
            uvmap[self.index] = values
        return None

    @property
    def vertices(self):
        """:getter: Returns the connected vertices"""
        ids = tuple(int(self.PointByIndex(i)) for i in range(self.PointCount()))
        return tuple(MeshVertex.fromId(id, self._geometry) for id in ids)

    @property
    def polygons(self):
        """:getter: Returns the connected polygons"""
        point = self.provider.PointAccessor
        point.Select(self._id)
        ids = tuple(int(point.PolygonByIndex(i)) for i in range( point.PolygonCount() ))
        return tuple(MeshPolygon.fromID(ID, self._geometry) for ID in ids)

    def nextPointByVector(self, direction, minAlign=-1.0):
        """
        :param Vector3 direction: A start vector
        :param float minAlign: A threshold between -1.0 and 1.0. The smaller the value, the bigger the angle range that is considered.
        :returns MeshVertex: The vertex closest to the given vector direction
        """
        self_pos = self.position

        if isinstance(direction, (list, tuple)):
            direction = Vector3(direction).normal()
        elif isinstance(direction, Vector3):
            direction.normalize()
        elif isinstance(direction, MeshVertex):
            other_vertex = direction
            direction = (Vector3(self_pos) - other_vertex.position).normal()
        elif isinstance(direction, int):
            index = direction
            other_vertex = self._geometry.vertices[index]
            direction = (Vector3(self_pos) - other_vertex.position).normal()

        candidate = [-1.0, None]

        for vertex in self.vertices:
            vertex_dir = (Vector3(vertex.position)-self_pos).normal()
            dotproduct = direction.dot(vertex_dir)
            if dotproduct > candidate[0]:
                candidate = [dotproduct, vertex]

        if candidate[0] <= minAlign:
            return None

        return candidate[1]


class MeshVertices(MeshComponentContainer):
    """Extension class of the point accessor that adds iteration methods.

    The individual vertex objects can be accessed through the built-in iterator function
    or angular brackets

    example::

        # Get the vertex count
        print ("Number of vertices: %i" % len(mesh.geometry.vertices))

        # Access first vertex
        print (mesh.geometry.vertices[0])

        # Iterates all vertices through a generator object
        for vertex in mesh.geometry.vertices:
            print (vertex)


    :param mesh: Input mesh to obtain PointAccessor from
    :param parent: MeshGeometry parent object
    """

    def __getitem__(self, index):
        """Quick read access to a point position via angular brackets.

        example::

            # Print point position by index
            print (mesh.geometry.vertices[4])

        """

        if isinstance(index, (list, tuple)):
            self.iterByList(index)

        return self._getitem(index, MeshVertex)

    def __setitem__(self, index, in_vertex):
        """Quick write access to a point position via angular brackets.

        example::

            mesh.geometry.vertices[0] = (1, 2, 3)

        """
        self.provider.beginLayerScan()
        
        self._accessor.SelectByIndex(index)

        if isinstance(in_vertex, tuple):
            self._accessor.SetPos(in_vertex)
        elif isinstance(in_vertex, MeshVertex):
            self._accessor.SetPos(in_vertex.position)

    def __delitem__(self, index):
        if isinstance(index, (list, tuple)):
            verts = index
            if len(verts) == 0:
                return
            if isinstance(verts[0], MeshVertex):
                for vert in verts:
                    vert.remove()
            elif isinstance(verts[0], int):
                indices = index
                indices = list(reversed((sorted(indices))))
                for i in indices:
                    del self[i]
        elif isinstance(index, int):
            self[index].remove()

    @staticmethod
    def _vertexSelectionOperation(vertex_id, mesh, operation=0, polygon=None):
        #TODO: replace/clear should only operate on this mesh
        """

        :param int operation: 0=select(add), 1=select(replace), 2=deselect, 3=clear
        """
        if operation not in [0, 1, 2, 3]:
            raise ValueError

        if polygon is None:
            polygon = 0
        elif isinstance(polygon, MeshPolygon):
            polygon = polygon.id
        elif isinstance(polygon, int):
            raise NotImplementedError

        # selSrv = lx.service.Selection()
        selSrv = MeshGeometry._SEL_SVC
        vertSelTypeCode = selSrv.LookupType(lx.symbol.sSELTYP_VERTEX)
        vTransPacket = lx.object.VertexPacketTranslation(selSrv.Allocate(lx.symbol.sSELTYP_VERTEX))

        if operation in [1, 3]:
            selSrv.Clear(vertSelTypeCode)

        if operation == 3:
            return

        pkt = vTransPacket.Packet(vertex_id, polygon, mesh)

        if operation in [0, 1]:
            selSrv.Select(vertSelTypeCode, pkt)

        elif operation == 2:
            selSrv.Deselect(vertSelTypeCode, pkt)

    def __iter__(self):
        """Iterate over all vertices.

        :return: Iterable MeshVertices generator object


        example::

            # Iterate all vertices and move them by 0.1 in x
            for point in mesh.geometry.vertices:
                pos = list(point.Pos())
                pos[0] += 0.1
                point.SetPos(pos)

            # Update to see mesh changes
            mesh.geometry.setMeshEdits()

        """

        for i in range(self.provider.mesh.PointCount()):
            self.provider.point.SelectByIndex(i)
            yield MeshVertex(i, self._geometry)

    def iterByList(self, vertex_list=None):
        """Iterate over vertices of a given list of point indices.

        :return: Iterable MeshVertices generator object
        :param vertex_list: List of point indices to visit

        example::

            # Iterate all vertices and move them by 0.1 in x
            for point in mesh.geometry.vertices.iterByList([1,3,6,7]):
                pos = list(point.Pos())
                pos[0] += 0.1
                point.SetPos(pos)

            # Update to see mesh changes
            mesh.geometry.setMeshEdits()

        """
        for i in vertex_list:
            self._accessor.SelectByIndex(i)
            yield MeshVertex(i, self._geometry)

    def new(self, position):
        """Adds a new vertex

        :param tuple: Position
        :returns MeshVertex: New vertex object
        """
        self.provider.beginLayerScan()
        
        point = self._accessor
        id = point.New (position)

        return MeshVertex.fromId(id, self._geometry)

    @property
    def selected(self):
        """
        :getter: Returns the currently selected vertices (tuple)
        """

        selSrv = lx.service.Selection()
        vertSelTypeCode = selSrv.LookupType(lx.symbol.sSELTYP_VERTEX)
        vTransPacket = lx.object.VertexPacketTranslation(selSrv.Allocate(lx.symbol.sSELTYP_VERTEX))

        numVerts = selSrv.Count(vertSelTypeCode)
        vertex_ids = []

        for vi in range(numVerts):
            packetPointer = selSrv.ByIndex(vertSelTypeCode, vi)
            if not packetPointer:
                continue

            vertexID = int(vTransPacket.Vertex(packetPointer))
            item_    = vTransPacket.Item(packetPointer)
            poly_    = vTransPacket.Polygon(packetPointer)

            if item_ == self._geometry._item:
                vertex_ids.append (vertexID)

        return tuple([MeshVertex(pid, self._geometry) for pid in vertex_ids])

    def select(self, vertices=None, replace=False):
        """Selects one or multiple vertices of this mesh

        :param int, list or tuple vertices: index, MeshVertex, or sequence of indices or MeshVertex objects. If None, the selection is cleared.
        :param bool replace: Clears the selection first
        """

        # Clear selection if vertices None
        if vertices is None or replace:
            for v in self:
                v.deselect()

        # Sequence
        if isinstance(vertices, collections.Iterable) and len(vertices) > 0:

            MeshGeometry._SEL_SVC.StartBatch()

            if isinstance(vertices[0], MeshVertex):
                for vertex in vertices:
                    vertex.select()

            if isPython2CompatibileIntInstance(vertices[0]):
                for index in vertices:
                    vertex = MeshVertex(index, self._geometry)
                    MeshVertices._vertexSelectionOperation(getIDAsLong(vertex), self.provider.mesh, 0)

            elif isinstance(vertices[0], int):
                for pid in vertices:
                    MeshVertices._vertexSelectionOperation(pid, self.provider.mesh, 0)

            MeshGeometry._SEL_SVC.EndBatch()

        # Single int (long?)
        elif isPython2CompatibileLongInstance(vertices):
            index = vertices
            vertex = MeshVertex(index, self._geometry)
            MeshVertices._vertexSelectionOperation(getIDAsLong(vertex), self.provider.mesh, 0)

        # Single MeshVertex
        elif isinstance(vertices, MeshVertex):
            vertices.select()

        # Single long
        elif isinstance(vertices, int):
            pid = vertices
            MeshVertices._vertexSelectionOperation(pid, self.provider.mesh, 0)

    def enumerate(self, mode, visitor, monitor=0):
        """Enumerate vertices using a visitor

        :param int mode: lx.symbol.iMARK_ANY
        :param lxifc.Visitor visitor: Visitor class instance to use
        :param monitor: Optional monitor (progress bar) to display
        """
        self.Enumerate(mode, visitor, monitor)

    def remove(self, vertices):
        """Removes a single vertex or a list of vertices

        :param int or list/tuple vertices: Vertices to remove
        """
        del self[vertices]


class MeshEdge(object):
    """Class representing an edge
    """

    def __init__(self, vertices, geometry):

        if isinstance(geometry, str):
            geometry = MeshGeometry(geometry)

        self._geometry = geometry

        if not self._geometry:
            raise ValueError("Geometry not found")

        mesh = self._geometry.provider.mesh
        self._mesh = mesh
        edge = geometry.provider.EdgeAccessor

        if isinstance(vertices, (list, tuple)):
            if len(vertices) <= 0:
                raise AttributeError("Empty list or tuple")
            if isPython2CompatibileIntInstance(vertices[0]):
                point = mesh.PointAccessor()
                if not point.test():
                    raise Exception("Vertex not found")
                point.SelectByIndex(vertices[0])
                id1 = getIDAsLong(point)
                point.SelectByIndex(vertices[1])
                id2 = getIDAsLong(point)
            elif isinstance(vertices[0], int):
                id1, id2 = vertices
            elif isinstance(vertices[0], MeshVertex):
                id1 = vertices[0].id
                id2 = vertices[1].id

            edge.SelectEndpoints(id1, id2)
            self._id = getIDAsLong(edge)

    @property
    def _accessor(self):
        edge = self._geometry.provider.edge
        edge.Select(self._id)
        return edge

    @classmethod
    def fromVertices(cls, vertices, geometry, mesh=None):
        # if int, if MeshVertex ...
        # if index vs. ID ...
        # Assuming int indices for now
        mesh = geometry.provider.mesh
        
        if isinstance(vertices, (list, tuple)):
            if len(vertices) <= 0:
                raise AttributeError("Empty list or tuple")
            if isinstance(vertices[0], int):
                point = geometry.provider.PointAccessor
                if not point.test():
                    return
                if isPython2CompatibileIntInstance(vertices[0]):
                    point.SelectByIndex(vertices[0])
                    id1 = getIDAsLong(point)
                    point.SelectByIndex(vertices[1])
                    id2 = getIDAsLong(point)
                elif isinstance(vertices[0], int):
                    id1, id2 = vertices

            elif isinstance(vertices[0], MeshVertex):
                id1 = vertices[0].id
                id2 = vertices[1].id

            instance = cls.__new__(cls)

            edge = geometry.provider.EdgeAccessor
            edge.SelectEndpoints(id1, id2)

            instance._geometry = geometry
            instance._mesh     = mesh
            instance._id       = getIDAsLong(edge)
            instance.provider  = geometry.provider
            return instance

        return None

    @classmethod
    def fromIDs(cls, id1, id2, geometry, mesh=None):
        # if int, if MeshVertex ...
        # if index vs. ID ...
        # Assuming int indices for now
        mesh = geometry.provider.mesh
        point = geometry.provider.PointAccessor
        if not point.test():
            raise ValueError

        instance = cls.__new__(cls)

        edge = geometry.provider.EdgeAccessor
        edge.SelectEndpoints(id1, id2)

        instance._geometry = geometry
        instance.provider  = geometry.provider
        instance._mesh     = mesh
        instance._id       = getIDAsLong(edge)
        return instance

    @classmethod
    def fromID(cls, id, geometry):
        # if int, if MeshVertex ...
        # if index vs. ID ...

        mesh = geometry.provider.mesh
        
        instance = cls.__new__(cls)

        edge = geometry.provider.EdgeAccessor
        edge.Select(id)
        instance._id       = id

        instance._geometry = geometry
        instance._mesh     = mesh
        instance.provider  = geometry.provider
        return instance

    @property
    def vertices(self):
        """:getter: Returns the connected :class:`vertices<MeshVertex>` as tuple
        """
        return tuple([MeshVertex(index, self._geometry) for index in self.vertex_indices])

    @property
    def vertex_indices(self):
        """:getter: Returns the connected vertex indices as tuple
        
        Note that indices do not exist immediately after adding a vertex, the edits need to be applied with setMeshEdits to produce indices.        
        """
        pac = self.provider.point

        ids = tuple(int(p) for p in self._accessor.Endpoints())
        if self.provider.layerEdit is not None:
            return ids

        vertexIndices = []
        for ID in ids:
            pac.Select(ID)
            vertexIndices.append (int (pac.Index()))
            
        return tuple(vertexIndices)

    def __getattr__(self, attr):
        # pass any unknown attribute access on to the wrapped lx.object.Item class to see if
        # it's a recognised call there.
        return getattr(self._accessor, attr)

    def __apply_operator(self, func_name, operand):
        """Helper function for operators """
        for vertex in self.vertices:
            getattr(vertex, func_name)(operand)
        return self

    def __add__(self, other):
        """Adds a position """
        self.__apply_operator("__add__", other)

    def __sub__(self, other):
        """Subtracts a position """
        self.__apply_operator("__sub__", other)

    def __mul__(self, other):
        """Multiplies by a position"""
        self.__apply_operator("__mul__", other)

    def __truediv__(self, other):
        """Divides by position"""
        self.__apply_operator("__truediv__", other)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self._id == other._id

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __repr__(self):
        ids = tuple(int(p) for p in self._accessor.Endpoints())
        return 'modo.%s(%s, \'%s\')' % (self.__class__.__name__, ids, self._geometry._item.Ident())

    @property
    def id(self):
        """:getter: Returns the pointer ID of this edge"""
        return getIDAsLong(self._accessor)

    def select(self, replace=False):
        op = 'replace' if replace else 'add'
        MeshEdges._performSelectionOperation(self._accessor, self._mesh, op)

    def deselect(self):
        MeshEdges._performSelectionOperation(self._accessor, self._mesh, 'deselect')

    @property
    def accessor(self):
        """
        :getter: Returns the internal shared EdgeAccessor object of the core SDK (lx.object.Edge)
        """
        return self._accessor

    @property
    def polygons(self):
        """:getter: Returns the polygons connected to this edge"""
        ids = tuple(int(self.PolygonByIndex(i)) for i in range(self.PolygonCount()))
        return tuple(MeshPolygon.fromID(id, self._geometry) for id in ids)


class MeshEdges(MeshComponentContainer):
    """Extension class of the Edge accessor lx.object.Edge that adds iteration methods.

        Note: Modo does not store edges by index, therefore they cannot be accessed by such.
        You can use the built-in python iterator however.

        :param mesh: Input mesh to obtain PointAccessor from
        :param parent: MeshGeometry parent object
    """

    def __init__(self, mesh, parent):
        super(MeshEdges, self).__init__(mesh, parent, "Edge")

    def __getitem__(self, vertexIndices):
        if not isinstance(vertexIndices, (list, tuple)):
            raise AttributeError("Must provide a list or tuple containing to vertex indices")

        return MeshEdge(vertexIndices, self._geometry)

    def fromVertices(self, vertices):
        return MeshEdge(vertices, self._geometry)

    def __iter__(self):
        IDs = self.__pollEdgeIDs()
        for id in IDs:
            yield MeshEdge.fromID(id, self._geometry)

    @property
    def selected(self):
        """
        :getter: Returns the currently selected edges as tuple
        """
        selSrv = lx.service.Selection()
        edgeSelTypeCode = selSrv.LookupType(lx.symbol.sSELTYP_EDGE)
        vTransPacket = lx.object.EdgePacketTranslation(selSrv.Allocate(lx.symbol.sSELTYP_EDGE))

        numEdges = selSrv.Count(edgeSelTypeCode)

        edges = []
        for i in range(numEdges):
            packetPointer = selSrv.ByIndex(edgeSelTypeCode, i)
            id1, id2 = vTransPacket.Vertices(packetPointer)
            item_ = vTransPacket.Item(packetPointer)

            if item_ == self._geometry._item:
                edges.append(MeshEdge.fromIDs(id1, id2, self._geometry))

        return tuple(edges)

    def select(self, edges=None, replace=False):
        """Selects one or multiple edges of this mesh

        :param list/tuple edges: Can be a list of MeshEdge, pairs of vertex indices or Mesh IDs (long). If None, the selection is cleared.
        :param bool replace: Clears the selection first
        """
        if edges is None or replace:
            for p in self:
                p.deselect()

        # Sequence
        if isinstance(edges, (list, tuple)) and len(edges) > 0:

            MeshGeometry._SEL_SVC.StartBatch()
            try:

                if isinstance(edges[0], MeshEdge):
                    for edge in edges:
                        edge.select()
    
                if len(edges) > 1 and isinstance(edges[0], int) and len(edges) % 2 == 0:
                    # iterate pair-wise
                    for vertices in zip(edges[::2], edges[1::2]):
                        edge = MeshEdge.fromVertices(vertices, self._geometry)
                        MeshEdges._performSelectionOperation(edge._accessor, edge._mesh, 'add')
    
                elif isinstance(edges[0], int):
                    for pid in edges:
                        edge = MeshEdge.fromID(pid, self._geometry)
                        MeshEdges._performSelectionOperation(edge._accessor, edge._mesh, 'add')
            
            # In case of an exception, terminate the Batch session and re-raise
            except:
                MeshGeometry._SEL_SVC.EndBatch()
                raise                

            MeshGeometry._SEL_SVC.EndBatch()

        # Single MeshEdge
        elif isinstance(edges, MeshEdge):
            edges.select()

    @staticmethod
    def _performSelectionOperation(edge_accessor, mesh, operation='add'):

        _edgeSelect = lxu.select.AnySelection(lx.symbol.sSELTYP_EDGE, 'Edge')
        edgeSelTypeCode = _edgeSelect.selsvc.LookupType(lx.symbol.sSELTYP_EDGE)
        vTransPacket = lx.object.EdgePacketTranslation(_edgeSelect.selsvc.Allocate(lx.symbol.sSELTYP_EDGE))

        operation_function = None

        if operation == 'clear':
            _edgeSelect.selsvc.Clear(edgeSelTypeCode)

        if edge_accessor is None:
            raise Exception('error')

        if not edge_accessor.PolygonCount():
            raise Exception('error')

        if operation is 'add':
            operation_function = _edgeSelect.selsvc.Select
        elif operation is 'replace':
            # Clear selection
            _edgeSelect.selsvc.Clear(edgeSelTypeCode)
            operation_function = _edgeSelect.selsvc.Select
        elif operation is 'deselect':
            operation_function = _edgeSelect.selsvc.Deselect

        id1, id2 = tuple(int(p) for p in edge_accessor.Endpoints())

        packet = _edgeSelect.spTrans.Packet(id1, id2, 0, mesh)
        operation_function(edgeSelTypeCode, packet)

    def __pollEdgeIDs(self):

        try:
            import lxifc
        except:
            raise Exception("This functionality is not available from the fire and forget python interpreter")

        class MeshEdgePollVisitor(lxifc.Visitor):
            def __init__(self, edge):
                self.edge = edge
                self.edge_ids = []

            def vis_Evaluate(self):
                ID = getIDAsLong(self.edge)
                self.edge_ids.append(ID)

            def getResults(self):
                return self.edge_ids

        visitor = MeshEdgePollVisitor(self._accessor)
        self._accessor.Enumerate(lx.symbol.iMARK_ANY, visitor, 0)
        return visitor.getResults()

    def enumerate(self, mode, visitor, monitor=0):
        """Enumerate edges using a visitor

        :param int mode: lx.symbol.iMARK_ANY
        :param lxifc.Visitor visitor: Visitor class instance to use
        :param monitor: Optional monitor (progress bar) to display
        """
        self.Enumerate(mode, visitor, monitor)


class MeshPolygon(object):
    """Class wrapped around lx.object.Polygon for polygon access.
    """

    def __init__(self, index, geometry):
        """Initializes a polygon from a given MeshGeometry object

        :param index: The polygon index to be obtained
        :type: int
        :param geometry: The geometry to obtain the polygon from
        :type: MeshGeometry
        :return: An instance of MeshPolygon
        """

        if isinstance(geometry, str):
            geometry = MeshGeometry(geometry)

        # Initializing static class members
        if not hasattr(MeshPolygon, '_polySelect'):
            MeshPolygon._polySelect = lxu.select.AnySelection(lx.symbol.sSELTYP_POLYGON, 'Polygon')
            MeshPolygon._polySelTypeCode = MeshPolygon._polySelect.selsvc.LookupType(lx.symbol.sSELTYP_POLYGON)


        self._geometry = geometry
        self.provider = geometry.provider
        mesh = geometry.provider.mesh
    
        if not 0 <= index < mesh.PolygonCount():
            raise LookupError("Index out of bounds")

        poly = geometry.provider.PolygonAccessor
        poly.SelectByIndex(index)
        self._id = getIDAsLong(poly)

    @classmethod
    def fromID(cls, ID, geometry):

        # Create instance
        instance = cls.__new__(cls)

        
        # Initializing static class members
        if not hasattr(MeshPolygon, '_polySelect'):
            MeshPolygon._polySelect = lxu.select.AnySelection(lx.symbol.sSELTYP_POLYGON, 'Polygon')
            MeshPolygon._polySelTypeCode = MeshPolygon._polySelect.selsvc.LookupType(lx.symbol.sSELTYP_POLYGON)

        instance._geometry = geometry
        instance.provider = geometry.provider
        
        mesh           = geometry.provider.mesh
        instance._mesh = mesh
        poly           = geometry.provider.PolygonAccessor

        poly.Select(ID)
        instance._id = getIDAsLong(poly)
        return instance

    @property
    def _accessor(self):
        # This selects the polygon by it's ID on the shared accessor
        poly = self._geometry.provider.polygon
        poly.Select (self._id)
        return poly

    @classmethod
    def fromMesh(cls, index, geometry):
        """Initializes a polygon from a given MeshGeometry object

        :param index: The polygon index to be obtained
        :type: int
        :param geometry: The geometry to obtain the polygon from
        :type: MeshGeometry
        :return: An instance of MeshPolygon
        """

        if isinstance(geometry, str):
            geometry = MeshGeometry(geometry)

        if not 0 <= index < geometry.provider.mesh.PolygonCount():
            raise LookupError("Index out of bounds")

        # Initializing static class members
        if not hasattr(MeshPolygon, '_polySelect'):
            MeshPolygon._polySelect = lxu.select.AnySelection(lx.symbol.sSELTYP_POLYGON, 'Polygon')
            MeshPolygon._polySelTypeCode = MeshPolygon._polySelect.selsvc.LookupType(lx.symbol.sSELTYP_POLYGON)

        # Create instance
        instance = cls.__new__(cls)
        instance._geometry = geometry
        instance._mesh     = geometry.provider.mesh
        instance.provider  = geometry.provider    
        
        poly = geometry.provider.mesh.PolygonAccessor()
        poly.SelectByIndex(index)
        instance._id = getIDAsLong(poly)
        return instance

    def __repr__(self):
        strIndexOrId = None
        if self.provider.layerEdit is None:
            strIndexOrId = str(self.index)
        else :
            strIndexOrId = str(self._id)+'L'
        
        return 'modo.%s(%s, \'%s\')' % (self.__class__.__name__, strIndexOrId, self._geometry._item.Ident())

    def __getattr__(self, attr):
        # pass any unknown attribute access on to the wrapped lx.object.Item class to see if
        # it's a recognised call there.
        return getattr(self.provider.PolygonAccessor, attr)

    @property
    def numVertices(self):
        """:getter: Returns the number of vertices of this polygon"""
        return self._accessor.VertexCount()

    def remove(self):
        self._accessor.Remove()

    @property
    def vertices(self):
        """:getter: Returns the connected :class:`vertices<MeshVertex>` of the polygon
        
        Note that indices do not exist immediately after adding a vertex, the edits need to be applied with setMeshEdits to produce indices.        
        """
        poly = self.provider.polygon
        poly.Select (self._id)
        
        num_verts = poly.VertexCount()
        vertices = []
        point = self.provider.point
        for i in range(num_verts):
            ID = int(poly.VertexByIndex(i))
            point.Select(ID)
            vertices.append(MeshVertex.fromId(ID, self._geometry))
        return vertices

    @property
    def edges(self):
        """:getter: Returns the :class:`edges<MeshEdge>` connected to this polygon
        """

        edges = []
        point = self._geometry.provider.point

        for v in range(self.VertexCount()):
            id = int(self.VertexByIndex(v))
            point.Select(id)
            for e in range(point.EdgeCount()):
                eid = point.EdgeByIndex(e)

                # Test if edge is part of this polygon
                try:
                    self.EdgeIndex(eid)
                    if eid not in edges:
                        edges.append(eid)

                except RuntimeError:
                    pass

        return tuple(MeshEdge.fromID(id, self._geometry) for id in edges)

    def __apply_operator(self, func_name, operand):
        """Helper function for operators """
        for vertex in self.vertices:
            getattr(vertex, func_name)(operand)
        return self

    def __add__(self, other):
        self.__apply_operator("__add__", other)

    def __sub__(self, other):
        self.__apply_operator("__sub__", other)

    def __mul__(self, other):
        self.__apply_operator("__mul__", other)

    def __truediv__(self, other):
        self.__apply_operator("__truediv__", other)

    def iterTriangles(self, asIndices=True):
        """

        :param bool asIndices: Indices are returned if True, MeshVertex instances if False
        :returns generator object: Tuples consisting of 3 vertices each
        """

        if asIndices:
            point = self.provider.point
            point.Select(self._id)            

        num = self.GenerateTriangles()
        for index in range(num):
            ids = self._accessor.TriangleByIndex(index)
            if asIndices:
                indices = []
                for id_ in ids:
                    point.Select(id_)
                    indices.append(int(point.Index()))
                yield tuple(indices)
            else:
                yield tuple(MeshVertex.fromId(ID, self._geometry) for ID in ids)

        self.ClearTriangles()

    @property
    def triangles(self):
        """
        :getter : Returns all triangle vertices as tuple
        """
        return tuple(self.iterTriangles(asIndices=True))

    def numTriangles(self, keepTriangles=False):
        """:returns: The number of triangles on the polygon"""
        num = self.GenerateTriangles()

        if not keepTriangles:
            self.ClearTriangles()

        return int(num)

    @property
    def area(self):
        """:getter: Returns the area of this polygon"""
        self._accessor.Select(self._id)
        return self.Area()

    @property
    def normal(self):
        """:getter: Returns the normal of this polygon face"""
        self._accessor.Select(self._id)
        return self.Normal()

    def vertexNormal(self, index):
        """
        :param int index: Vertex index on the polygon
        :returns tuple: The normal of the vertex
        """
        point = self.provider.point
        id = int(self._accessor.VertexByIndex(index))
        point.Select(id)
        return point.Normal(getIDAsLong(self._accessor))

    def iterVertexNormals(self):
        """Iterator for vertex normals
        :return: Generator object that returns a vertex normal per polygon vertex
        """
        for i in range(self.numVertices):
            yield self.vertexNormal(i)

    def tags(self):
        """List tags of this polygon
        """
        polytag = {}
        for attr in [i for i in dir(lx.symbol) if i.startswith('i_POLYTAG')]:

            id = attr.rfind('_')+1
            name = attr[id:].lower()

            polytag[name] = getattr(lx.symbol, attr)

        result = {}
        loc = lx.object.StringTag(self._accessor)

        for name, tagType in polytag.items():
            result[name] = loc.Get(tagType)
        return result

    def getTag(self, tagType):
        """Gets a polygon tag

        :param basestring tagType: Any out of lx.symbol.i_POLYTAG_*
        :return: Value of the tag
        """
        loc = lx.object.StringTag(self._accessor)
        return loc.Get(tagType)

    def setTag(self, tagType, value):
        """Sets a polygon tag

        :param basestring tagType: Any out of lx.symbol.i_POLYTAG_*
        :param value: Value to set
        """
        loc = lx.object.StringTag(self._accessor)
        loc.Set(tagType, value)

    @property
    def materialTag(self):
        """
        :getter: Get the value of the material tag
        :setter: Set the value of the material tag, taking a string argument
        """
        return self.getTag(lx.symbol.i_POLYTAG_MATERIAL)

    @materialTag.setter
    def materialTag(self, material):
        self.setTag(lx.symbol.i_POLYTAG_MATERIAL, material)

    def __lookupUVMap(self, uvmap):

        # If is UVMap type
        if isinstance(uvmap, UVMap):
            map_id = getIDAsLong(uvmap._accessor)
            return map_id

        # If string
        elif isinstance(uvmap, str):
            meshmap = self.provider.meshmap
            try:
                meshmap.SelectByName(lx.symbol.i_VMAP_TEXTUREUV, uvmap)
                map_id = getIDAsLong(meshmap)
                return map_id

            except LookupError:
                return None

        # If None
        elif uvmap is None:
            uvmaps = self._geometry.vmaps.uvMaps
            if uvmaps:
                map_id = getIDAsLong(uvmaps[0]._accessor)
                return map_id

            else:
                return None
        else:
            return None


    def getUV(self, vertex, uvmap=None):
        """Get a UV value pair from a vertex specific to this polygon.

        :param UVMap uvmap: The UVMap to read the value from
        :vertex int or MeshVertex: Vertex to read the uv value pair for. Can be a vertex index or a MeshVertex object.
        """
        map_id = self.__lookupUVMap(uvmap)

        if not map_id:
            return None

        point = self.provider.point;

        # Optionally, use the provided vertex's ID
        vertex_id = vertex._id if isinstance(vertex, MeshVertex) else int(self._accessor.VertexByIndex(vertex))

        values = lx.object.storage()
        values.setType('f')
        values.setSize(2)

        self._accessor.MapEvaluate(map_id, vertex_id, values)
        return values.get()

    def setUV(self, values, vertex, uvmap=None):
        """Set a UV value pair for a vertex specific to this polygon.
        Splitting UVs off their surrounding connections can be done this way.

        :param tuple values: A tuple containing the two uv floats to be set
        :vertex int or MeshVertex: Vertex to write the uv value pair for. Can be a vertex index or a MeshVertex object.
        :param UVMap uvmap: The UVMap to write the value to. Will look for the first found UV map if None
        """

        map_id = self.__lookupUVMap(uvmap)

        if not map_id:
            return None

        point = self.provider.point

        # Optionally, use the provided vertex's ID
        vertex_id = vertex._id if isinstance(vertex, MeshVertex) else int(self._accessor.VertexByIndex(vertex))

        storage = lx.object.storage()
        storage.setType('f')
        storage.setSize(2)
        storage.set(values)

        self._accessor.SetMapValue(vertex_id, map_id, storage)

    @property
    def id(self):
        """:getter: Returns the pointer ID of this polygon"""
        return getIDAsLong(self._accessor)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.id)

    def _performSelectionOperation(self, operation='add'):
        """

        :param basestring operation: 'add', 'replace' or 'deselect'
        """

        accessMode = 'write' if self.provider.item.Context().SetupMode() else 'read'
        mesh = MeshProvider.meshFromMeshChannel(self._geometry._item, accessMode)        
        MeshPolygons._performSelectionOperation(self._id, mesh, operation)
        
    def select(self, replace=False):
        """Selects this polygon

        :param bool replace: Deselects all polygons of this mesh before selecting
        """
        self._performSelectionOperation('replace') if replace else self._performSelectionOperation('add')

    def deselect(self):
        """Deselects this polygon
        """
        self._performSelectionOperation('deselect')

    @property
    def index(self):
        """:getter: Returns the index of this polygon
        
        Note that indices do not exist immediately after adding a polygon, the edits need to be applied with setMeshEdits to produce indices.        
        """
        return int(self._accessor.Index())

    @property
    def accessor(self):
        """
        :getter: Returns the internal shared PolygonAccessor object of the core SDK (lx.object.Polygon)
        """
        return self._accessor

    @property
    def neighbours(self):
        """
        :getter: Returns the neighbour polygons as tuple
        """
        polys = set()
        for i in self.vertices:
            for p in i.polygons:
                if not p == self:
                    polys.add(p)
        return tuple(polys)
    
    def getIsland(self):
        """
        Returns the all connected neighbour polygons found.
        """
        
        # Start queue with self
        queue = set([self,])
        
        island = set()
        
        while queue:
            poly = queue.pop()
            if poly not in island:
                island.add(poly)
                neighbours = set(poly.neighbours).difference(island)
                if neighbours:
                    queue.update(neighbours)
        
        return list(island)
        


class MeshPolygons(MeshComponentContainer):
    """
        Extension class of the Polygon accessor that adds iteration methods.

        The vertices of of individual vertices can be accessed through the built-in iterator function
        or angular brackets

        example::

            mesh, = modo.scene.current().selectedByType("mesh")

            # Get the number of polygon
            print ("Number of polygons: %i" % len(mesh.geometry.polygons))

            # Access the first polygon and print it's normal
            polygon = mesh.geometry.polygons[0]
            print (polygon.normal)

            # Iterates all polygons through a generator object and print it's vertices
            for polygon in mesh.geometry.polygons:
                print (polygon.vertices)

    """

    def __getitem__(self, index):
        """Quick read access to a point position via index and angular brackets.
        """
        return self._getitem(index, MeshPolygon)

    def __delitem__(self, index):
        self[index].remove()

    @staticmethod
    def _performSelectionOperation(polygon_id, mesh, operation='add'):

        _polySelect = lxu.select.AnySelection(lx.symbol.sSELTYP_POLYGON, 'Polygon')
        _polySelTypeCode = _polySelect.selsvc.LookupType(lx.symbol.sSELTYP_POLYGON)

        operation_function = None

        # if operation in ['deselect', 'replace']:
        if operation == 'clear':
            _polySelect.selsvc.Clear(_polySelTypeCode)

        if polygon_id is None:
            return

        if operation is 'add':
            operation_function = _polySelect.selsvc.Select
        elif operation is 'replace':
            # Clear selection
            _polySelect.selsvc.Clear(_polySelTypeCode)
            operation_function = _polySelect.selsvc.Select
        elif operation is 'deselect':
            operation_function = _polySelect.selsvc.Deselect

        packet = _polySelect.spTrans.Packet(polygon_id, mesh)
        operation_function(_polySelTypeCode, packet)

    def __iter__(self):
        """Iterate over all polygons.

        :return: Iterable MeshPolygon generator object

        example::

            for polygon in mesh.geometry.polygons:
                print (polygon)

        """
        for index in range(len(self)):
            yield MeshPolygon(index, self._geometry)

    def iterByIndices(self, poly_list=None):
        """Iterate over polygons of a given list of indices.

        Use this if you want to save memory for large meshes.

        :param poly_list: List of point indices to visit
        :return: Iterable MeshPolygon generator object

        example::

            for polygon in mesh.geometry.polygons.iterByIndices([1,4,2]):
                print (polygon)

        """
        for index in poly_list:
            yield MeshPolygon(index, self._geometry)

    def iterByType(self, polyType):
        """
        :param string polyType: Value in FACE, CURV, BEZR, SUBD, SPCH, TEXT, PSUB, LINE
        :returns: Generator object for polygons of specified type
        """
        for index in range(len(self)):
            self._accessor.SelectByIndex(index)
            if lxu.utils.decodeID4(self._accessor.Type()) == polyType:
                yield MeshPolygon(index, self._geometry)

    def iterFaces(self):
        """:returns: Iterable for curve polygons """
        for i in self.iterByType("FACE"):
            yield i

    def iterCurves(self):
        """This method currently broken, please use iterByType('CURV') instead

        :returns: Iterable for curve polygons """
        for i in self.iterByType("CURV"):
            yield i

    def iterSubdivs(self):
        """:returns: Iterable for subdiv polygons """
        for i in self.iterByType("SUBD"):
            yield i

    def iterSplinePatches(self):
        """:returns: Iterable for spline patch polygons """
        for i in self.iterByType("SPCH"):
            yield i

    def iterTexts(self):
        """:returns: Iterable for text polygons """
        for i in self.iterByType("TEXT"):
            yield i

    def iterPixarSubdivs(self):
        """:returns: Iterable for pixar subdiv polygons """
        for i in self.iterByType("PSUB"):
            yield i

    def iterLines(self):
        """:returns: Iterable for line polygons """
        for i in self.iterByType("LINE"):
            yield i

    def addFromPointIndices(self, indices, reversed):

        points = [getIDAsLong(self._geometry.vertices[i]._accessor) for i in indices]

        points_storage = lx.object.storage()
        points_storage.setType('p')
        points_storage.setSize(len(indices))
        points_storage.set(points)
        self._accessor.New(lx.symbol.iPTYP_FACE, points_storage, len(indices), 0)
        self._mesh.SetMeshEdits(lx.symbol.f_MESHEDIT_POLYGONS)

    def new(self, vertices=None, reversed=False, polyType=None):
        """Adds a polygon to the mesh
        
        :param list vertices: List containing or either MeshVertex objects or vertex indices
        :param bool reversed: Winding order is reversed when True. (Clockwise is the default)
        """
        if not vertices:
            raise AttributeError("No vertices specified")

        # Default polyType to a face when nothing was passed
        polyType = lx.symbol.iPTYP_FACE if not polyType else polyType
        
        if len(vertices) >= 3:
            pa = self.provider.point

            if isinstance(vertices[0], MeshVertex):
                ids = [v._id for v in vertices]
                
            elif isinstance(vertices[0], int):
                # Convert vertex indices to ids
                ids = []
                for index in vertices:
                    pa.SelectByIndex(index)
                    ids.append(getIDAsLong(pa))

            # Create storage object containing the ids
            points_storage = lx.object.storage()
            points_storage.setType('p')
            points_storage.setSize(len(ids))
            points_storage.set(ids)

            # Create face from storage
            newID = self._accessor.New(polyType, points_storage, len(ids), reversed)

            # Update mesh edits
            #self._mesh.SetMeshEdits(lx.symbol.f_MESHEDIT_POLYGONS)
            return MeshPolygon.fromID(newID, self._geometry)
        
        return None

    @property
    def selected(self):
        """
        :getter: Returns the selected polygons as tuple
        
        Note that indices do not exist immediately after adding a vertex, the edits need to be applied with setMeshEdits to produce indices.        
        """
        selSrv = lx.service.Selection()
        polySelTypeCode = selSrv.LookupType(lx.symbol.sSELTYP_POLYGON)
        vTransPacket = lx.object.PolygonPacketTranslation(selSrv.Allocate(lx.symbol.sSELTYP_POLYGON))

        numPolys = selSrv.Count(polySelTypeCode)
        poly_ids = []

        for vi in range(numPolys):
            packetPointer = selSrv.ByIndex(polySelTypeCode, vi)
            if not packetPointer:
                continue

            polygon = vTransPacket.Polygon(packetPointer)
            item_ = vTransPacket.Item(packetPointer)

            if item_ == self._geometry._item:
                tmp = self.provider.polygon
                tmp.Select(polygon)
                poly_ids.append(tmp.Index())

                # poly_ids.append(polygon)

        return tuple([MeshPolygon(pid, self._geometry) for pid in poly_ids])

    def select(self, polygons=None, replace=False):
        """Selects one or multiple polygons of this mesh

        :param int, list or tuple polygons: index, MeshPolygon, or sequence of indices or MeshPolygon objects. If None, the selection is cleared.
        :param bool replace: Clears the selection first
        """
        if polygons is None or replace:
            for p in self:
                p.deselect()

        # Sequence
        if isinstance(polygons, (list, tuple)) and len(polygons) > 0:

            MeshGeometry._SEL_SVC.StartBatch()

            if isinstance(polygons[0], MeshPolygon):
                for polygon in polygons:
                    polygon.select()

            if isPython2CompatibileIntInstance(polygons[0]):
                for index in polygons:
                    polygon = MeshPolygon(index, self._geometry)
                    MeshPolygons._performSelectionOperation(getIDAsLong(polygon), self.provider.mesh, 'add')

            elif isinstance(polygons[0], int):
                for pid in polygons:
                    MeshPolygons._performSelectionOperation(pid, self.provider.mesh, 'add')

            MeshGeometry._SEL_SVC.EndBatch()

        # Single int
        elif isinstance(polygons, int):
            index = polygons
            polygon = MeshPolygon(index, self._geometry)
            MeshPolygons._performSelectionOperation(getIDAsLong(polygon), self.provider.mesh, 'add')

        # Single MeshPolygon
        elif isinstance(polygons, MeshPolygon):
            polygons.select()

        # Single long
        elif isinstance(polygons, MeshPolygon):
            pid = polygons
            MeshPolygons._performSelectionOperation(pid, self.provider.mesh, 'add')

    def enumerate(self, mode, visitor, monitor=0):
        """Enumerate polygons using a visitor

        :param int mode: lx.symbol.iMARK_ANY
        :param lxifc.Visitor visitor: Visitor class instance to use
        :param monitor: Optional monitor (progress bar) to display
        """
        self.Enumerate(mode, visitor, monitor)

    @property
    def accessor(self):
        """
        :getter: Returns the internal shared PolygonAccessor object of the core SDK (lx.object.Polygon)
        """
        return self._accessor


class VertexMap(object):
    """A class representing a vertex map, accessible by point indices through angular brackets.

    Base class for other maps.

    """
    def __init__(self):
        raise NotImplementedError

    @classmethod
    def fromMesh(cls, geometry, accessor, ID=None, map_type=lx.symbol.i_VMAP_RGBA, name=None, **kwargs):
        instance = cls.__new__(cls)
        instance._geometry      = geometry
        instance._accessor_     = accessor
        instance._id            = ID
        instance.map_type       = map_type
        instance._name          = name
        instance.storage_format = ('f', 1)
        instance.provider       = geometry.provider
        return instance

    @property
    def name(self):
        """Get or set the name of this mesh map
    
            :getter: Returns name as string
            :setter: Sets name from string
        """
        
        return self._accessor.Name()
    
    @name.setter
    def name(self, text):
        self._accessor.SetName(text)
    
    @property
    def _accessor(self):
        self._accessor_.Select(self._id)
        return self._accessor_

    @property
    def accessor(self):
        """
        :getter: Returns the internal shared MeshMapAccessor object of the core SDK (lx.object.MeshMap)
        """
        return self._accessor

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, self.name)

    def __getitem__(self, index):

        # Get vertex accessor
        point_accessor = self._geometry.vertices._accessor
        point_accessor.SelectByIndex(index)

        # set up storage buffer
        storage = self.storage_format
        storageBuffer = lx.object.storage(storage[0], storage[1])

        # Retrieve value
        exists = point_accessor.MapValue(self._id, storageBuffer)
        if not exists:
            return None

        return storageBuffer.get()

    def __setitem__(self, index, value):

        self.provider.beginLayerScan ()
        
        # Get vertex accessor
        point_accessor = self._geometry.vertices._accessor
        point_accessor.SelectByIndex(index)

        if value is None:
            point_accessor.ClearMapValue(self._id)
            return

        # set up storage buffer
        datatype, datasize = self.storage_format
        storageBuffer = lx.object.storage(datatype, datasize)

        # Single values need to be turned into a sequence, hence the comma
        if isinstance(value, float):
            storageBuffer.set((value,))
        else:
            storageBuffer.set((value))

        # Set value
        point_accessor.SetMapValue(self._id, storageBuffer)

    def __getattr__(self, attr):
        # pass any unknown attribute access on to the wrapped lx.object.Item class to see if
        # it's a recognised call there.
        return getattr(self._accessor, attr)

    def __iter__(self):

        for i in range(len(self)):
            yield self[i]

    def __len__(self):
        return self.provider.mesh.PointCount()

    def __bool__(self):
        return len(self) != 0

    def clear(self, index=None):
        """
        :param int index: If not None, the vertex of this index is deallocated from the map. Otherwise all values of the map are deallocated.
        """
        if index:
            self[index] = None
        else:
            self.Clear()

    @property
    def id(self):
        return getIDAsLong(self.accessor)


class RGBMap(VertexMap):

    @classmethod
    def fromMesh(cls, *args, **kwargs):
        instance = super(RGBMap, cls).fromMesh(*args, **kwargs)
        instance.storage_format = ('f', 3)
        return instance


class RGBAMap(VertexMap):

    @classmethod
    def fromMesh(cls, *args, **kwargs):
        instance = super(RGBAMap, cls).fromMesh(*args, **kwargs)
        instance.storage_format = ('f', 4)
        return instance


class UVMap(VertexMap):
    """Access for UV-Map values
    """

    @classmethod
    def fromMesh(cls, *args, **kwargs):
        instance = super(UVMap, cls).fromMesh(*args, **kwargs)
        instance.storage_format = ('f', 2)
        return instance

    def __getitem__(self, item):
        return self.__get(item)

    def __setitem__(self, item, value):
        if isinstance(item, int) and isinstance(value, (list, tuple)):
            self._setValue(item, value, True)

    def disContinuousVertices(self):
        return tuple(self.iterDisContinuousVertices())

    def iterDisContinuousVertices(self):
        for i in range(len(self._geometry.vertices)):
            if self.__get(i, listContinuous=False, listNonContinuous=True):
                yield MeshVertex(i, self._geometry)

    def continuousVertices(self):
        return tuple(self.iterDisContinuousVertices())

    def iterContinuousVertices(self):
        for i in range(len(self._geometry.vertices)):
            if self.__get(i, listContinuous=True, listNonContinuous=False):
                yield MeshVertex(i, self._geometry)

    def __get(self, point_index, listContinuous=True, listNonContinuous=True):
        """Get the u and v value from a point

        A vertexuv pair is continuous if it's uv values are shared by multiple polygons.

        :param int point_index: Index of the vertex to get the uv value from. If it is a long, it is interpreted as ID
        :param bool listContinuous: Skips vertices with continuous uvs if False.
        :param bool listNonContinuous: Skips vertices with non-continuous uvs if False.
        :returns: A tuple containing the u and v values
        
        Note that map values are not accessible immediately after adding a vertex, the edits need to be applied with setMeshEdits to produce indices first.        
        """

        datatype, datasize = self.storage_format
        storageBuffer = lx.object.storage(datatype, datasize)

        point = self.provider.point
        if isPython2CompatibileIntInstance (point_index):
            point.SelectByIndex (point_index)
        elif isinstance (point_index, int):
            point.Select (point_index)

        poly = self.provider.polygon

        point_uvs = []
        polygon_indices = []
        polygons = []

        # Loop connected polygons
        for polygon_index in range(point.PolygonCount()):

            ID = int(point.PolygonByIndex(polygon_index))
            poly.Select(ID)
            polygon_indices.append(poly.Index())
            polygons.append (MeshPolygon(poly.Index(), self._geometry))

            # Read uv pair from this point of the polygon
            poly.MapEvaluate(getIDAsLong(self._accessor), getIDAsLong(point), storageBuffer)
            point_uvs.append(storageBuffer.get())

        isContinuous = point_uvs.count(point_uvs[0]) == len(point_uvs)

        if isContinuous and listContinuous and len(point_uvs) > 0:
            return point_uvs[0]

        elif not isContinuous and listNonContinuous:

            # Return a dict of uv value pair values with polygon indices as keys
            return tuple((polygon, uv_pair) for polygon, uv_pair in zip(polygons, point_uvs))

        return None

    def _setValue(self, vertexIndex, values, nonContinuous=False):
        """Sets UV values for this vertex.

        :param int vertexIndex: Index of vertex to change the UV values for
        :param tuple values: The u and v values to set (pair consisting of of 2 floats)
        :param bool nonContinuous: If True, the values are applied to all non-continuous occurrences on polygons found for this vertex.
        If False, Nothing happens when the vertex has non-continuous UVs.
        """

        if not len(values) == 2:
            raise ValueError("Value is not a UV pair")

        self.provider.beginLayerScan ()
        datatype, datasize = self.storage_format
        storageBuffer = lx.object.storage(datatype, datasize)
        storageBuffer.set((values[0], values[1]))

        point = self.provider.point
        point.SelectByIndex(vertexIndex)
        num_polys = point.PolygonCount()

        polygon = self.provider.polygon

        if not nonContinuous and num_polys >= 1:

            storageBuffer.set((values[0], values[1]))
            point.SetMapValue(getIDAsLong(self._accessor), storageBuffer)

        elif nonContinuous:
            for polygon_index in range(num_polys):

                # Select polygon by it's index
                polygon.Select(point.PolygonByIndex(polygon_index))

                polygon.SetMapValue(getIDAsLong(point), getIDAsLong(self._accessor), storageBuffer)


class MorphMap(VertexMap):
    """
    example::

        # Get first morph map if exists
        for morph in geo.vmaps.morphMaps[:1]:

            # Set position for vertex 10
            morph[10] = (1,2,3)

        # Update mesh
        geo.setMeshEdits()

    """
    @classmethod
    def fromMesh(cls, *args, **kwargs):
        instance = super(MorphMap, cls).fromMesh(*args, **kwargs)
        instance.storage_format = ('f', 3)
        return instance

    def setAbsolutePosition(self, index, value):
        """Sets the absolute position instead of the relative position

        :param int index: Vertex index to change
        :param tuple: xyz values
        """
        point = self.provider.point
        point.SelectByIndex(index)
        pos = point.Pos()
        storageBuffer = lx.object.storage('f', 3)
        if self.map_type == lx.symbol.i_VMAP_MORPH:
            storageBuffer.set((
                value[0]-pos[0],
                value[1]-pos[1],
                value[2]-pos[2]))
        elif self.map_type == lx.symbol.i_VMAP_SPOT:
            storageBuffer.set(value[0], value[1], value[2])

        point.SetMapValue(self._id, storageBuffer)

    def getAbsolutePosition(self, index):
        """Gets the absolute position instead of the relative position

        :param int index: Vertex index to read
        :returns tuple: position values
        """
        # TODO: if not static ...
        point = self.provider.point
        point.SelectByIndex(index)
        pos = point.Pos()
        storageBuffer = lx.object.storage('f', 3)

        point.MapEvaluate(self._id, storageBuffer)
        result = storageBuffer.get()
        if self.map_type == lx.symbol.i_VMAP_MORPH:
            result = [result[i]+pos[i] for i in range(3)]

        return tuple(result)


class WeightMap(VertexMap):
    """Provides access to weight map values.

    example::

        scene = modo.scene.current()

        # Get the first selected Mesh
        mesh = scene.selectedByType("mesh")[0]

        # Get the weight maps object
        vmaps = mesh.geometry.vmaps.weight_maps

        if vmaps:

            # Get the first weight map found
            weightMap = vmaps[0]

            # Set and get values
            weightMap[0] = 0.333
            print (weightMap[0])

            # Iterate and print all weight values
            if weightMap:
                for index, weight in enumerate(weightMap):
                    print (index, weight)

    """
    def __null(self):
        pass


class VertexNormalMap(VertexMap):
    """Vertex Normal Map class

    * Available from Modo 901 SP1 and upwards *

    Allows manipulation of a vertex normal map on either vertex or polygon basis.

    Example::

        import modo
        reload(modo)

        # Create a subdivided cube
        lx.eval('script.implicit {Unit Cube Item}')
        lx.eval('poly.subdivide ccsds')

        mesh = modo.Mesh('Cube')

        # Create a vertex normal map
        normals = mesh.geometry.vmaps.addVertexNormalMap()

        normalValue = (0, 0, -1)

        # Set the normal value on every vertex per polygon
        for polygon in mesh.geometry.polygons:
            for vert in polygon.vertices:
                normals.setNormal( normalValue, vert, polygon)

        # Update the mesh
        mesh.geometry.setMeshEdits(lx.symbol.f_MESHEDIT_MAP_OTHER)

        # Select the vertex normal map to see the effect
        lx.eval('select.vertexMap "%s" norm replace' % normals.name)

    """

    @classmethod
    def fromMesh(cls, *args, **kwargs):
        instance = super(VertexNormalMap, cls).fromMesh(*args, **kwargs)
        instance.storage_format = ('f', 3)
        instance.storage = lx.object.storage('f', 3)
        return instance

    def setNormal(self, values, vertex, polygon=None, normalize=True):
        # if not isinstance(values, (collections.Iterable, Vector3)):
        #     raise ValueError("Value must be iterable or vector")

        if values is not None:
            values = Vector3(values)
            if normalize:
                values.normalize()

            self.storage.set(values)

        # If an index was passed, turn it into a polygon now
        if isinstance(polygon, int):
            polygon = MeshPolygon(polygon, self._geometry)

        # Set the normal on the polygon if one was passed
        if isinstance(polygon, MeshPolygon):
            polygon.accessor.SetMapValue(getIDAsLong(vertex), getIDAsLong(self._accessor), self.storage)

        # Else set the normal for the vertex
        elif polygon is None:
            index = vertex.index if isinstance(vertex, MeshVertex) else vertex
            self[index] = values

    def getNormal(self, vertex, polygon=None):

        # If an index was passed, turn it into a polygon now
        if isinstance(polygon, int):
            polygon = MeshPolygon(polygon, self._geometry)

        # Set the normal on the polygon if one was passed
        if isinstance(polygon, MeshPolygon):
            polygon.accessor.MapValue(getIDAsLong(self._accessor), getIDAsLong(vertex), self.storage)
            return self.storage.get()

        # Else set the normal for the vertex
        elif polygon is None:
            index = vertex.index if isinstance(vertex, MeshVertex) else vertex
            print (index)
            return self[index]


class PickMap(VertexMap):

    @classmethod
    def fromMesh(cls, *args, **kwargs):
        instance = super(PickMap, cls).fromMesh(*args, **kwargs)
        # instance.storage_format = ('f', 1)
        return instance

    

class MeshMaps(MeshComponentContainer):
    """This module provides access to the various map types that a mesh holds.

        example::

            # By index
            myMap = geo.vmaps[0]

            # From string
            myMap = geo.vmaps['MyMap']

            # From string with wildcard
            myMap = geo.vmaps['MyMap*']

            # Get the first morph map if any and change vertex 36
            for morph in geo.vmaps.morphMaps[0:1]:
                morph[36] = (0, 0, 0)

            # Update changes on the mesh
            geo.setMeshEdits()


    Note: to remove a vertex map, use the Remove method of the accessor for now::

        myMap.accessor.Remove()

    """

    def __poll(self, types_list=None):
        """Enumerates and returns information about the mesh.

        :param list types_list: optional list of symbols (lx.symbol.i_VMAP_WEIGHT etc.)
        :returns: List of dictionaries with fields "name", "type_name", "ID" and "map_type"
        """

        try:
            import lxifc
        except:
            raise Exception("This functionality is not available from the fire and forget python interpreter")

        class QueryMapsVisitor(lxifc.Visitor):
            """Utility class to query information about a mesh's vertex maps.
            After enumerating the attribute 'mapInfos' contains a list of dictionaries per map,
            with the name, type name, ID and type string.
            """
            def __init__(self, meshmap, filter_types=None):
                self.meshmap = meshmap
                self.msv = lx.service.Mesh()
                self.mapInfos = []
                self.filter_types = filter_types

            def vis_Evaluate(self):
                name = self.meshmap.Name()
                if name:
                    map_type = self.meshmap.Type()
                    if self.filter_types:
                        if map_type not in self.filter_types:
                            return

                    type_name = self.msv.VMapLookupName(map_type)
                    vmap = {"name": name, "type_name": type_name, "ID": getIDAsLong(self.meshmap), "map_type": map_type}
                    self.mapInfos.append(vmap)

        if self._accessor.test():
            visitor = QueryMapsVisitor(self._accessor, types_list)
            self._accessor.Enumerate(lx.symbol.iMARK_ANY, visitor, 0)
        return visitor.mapInfos

    @staticmethod
    def __classFromSymbol(symbol):
        """Returns the class that corresponds to the given symbol

        :param lx.symbol symbol: VMap symbol, for example lx.symbol.i_VMAP_MORPH
        :returns: Class
        """

        cls = VertexMap

        if symbol in [lx.symbol.i_VMAP_MORPH, lx.symbol.i_VMAP_SPOT]:
            cls = MorphMap
        elif symbol == lx.symbol.i_VMAP_TEXTUREUV:
            cls = UVMap
        elif symbol == lx.symbol.i_VMAP_WEIGHT:
            cls = WeightMap
        elif symbol == lx.symbol.i_VMAP_RGB:
            cls = RGBMap
        elif symbol == lx.symbol.i_VMAP_RGBA:
            cls = RGBAMap
        elif symbol == lx.symbol.i_VMAP_NORMAL:
            cls = VertexNormalMap

        return cls

    # VertexMap Factory
    def getMapsByType(self, types_list=None):
        """

        :param types_list: List of lx.symbol types. If it is None, all map types will be retrieved
        :type types_list: list
        :returns: tuple containing the requested map objects of this mesh
        """
        if not isinstance(types_list, collections.Iterable):
            types_list = [types_list]

        mapInfos = self.__poll(types_list)

        out_maps = []
        for map_dict in mapInfos:

            self._accessor.Select(map_dict["ID"])

            cls = MeshMaps.__classFromSymbol(map_dict["map_type"])

            new_map = cls.fromMesh(self._geometry, self._accessor, **map_dict)
            out_maps.append(new_map)

        return tuple(out_maps)

    def __len__(self):
        return len(self.__poll())

    def __getitem__(self, item):
        li = self.__poll()

        if isinstance(item, int):
            infoDict = li[item]
            cls = MeshMaps.__classFromSymbol(infoDict["map_type"])
            return cls.fromMesh(self._geometry, self._accessor, **infoDict)

        elif isinstance(item, str):
            maps = [i for i in li if fnmatch(i["name"], item)]
            out = []
            for m in maps:
                cls = MeshMaps.__classFromSymbol(m["map_type"])
                out.append(cls.fromMesh(self._geometry, self._accessor, **m))
            return out

        return None

    def __delitem__(self, item):
        item.accessor.Remove()

    def addMap(self, mapType=lx.symbol.i_VMAP_WEIGHT, name='WeightMap'):
        """Add a new map

        :arg string name: Name
        :returns: New map
        """
        if mapType is None:
            return None

        cls = self.__classFromSymbol(mapType)
        self.provider.beginLayerScan()
        
        map_accessor = self.provider.MeshMapAccessor
        id = map_accessor.New(mapType, name)
        map_accessor.Select(id)

        return cls.fromMesh(self._geometry, map_accessor, ID=id, map_type=mapType, name=name)

    def addMorphMap(self, name='Morph', static=False):
        """Add a morph map

        :arg string name: Name
        :arg bool static: Creates a static (absolute) morph map if true and relative one if false
        :returns MorphMap:
        """
        map_type = lx.symbol.i_VMAP_SPOT if static else lx.symbol.i_VMAP_MORPH
        cls = self.__classFromSymbol(map_type)

        self.provider.beginLayerScan()
        
        map_accessor = self.provider.MeshMapAccessor
        id = map_accessor.New(map_type, name)
        map_accessor.Select(id)

        return cls.fromMesh(self._geometry, map_accessor, ID=id, map_type=map_type, name=name)

    def addWeightMap(self, name='WeightMap', initValue=None):
        map = self.addMap(lx.symbol.i_VMAP_WEIGHT, name)

        # Set initial values
        if initValue:
            for i in range(len(map)):
                map[i] = initValue

        return map

    def addUVMap(self, name='UVMap'):
        return self.addMap(lx.symbol.i_VMAP_TEXTUREUV, name)

    def edgePickMap(self, name='Edge Pick'):
        return self.addMap(lx.symbol.i_VMAP_EPCK, name)

    def addVertexNormalMap(self, name='Vertex Normal'):
        return self.addMap(lx.symbol.i_VMAP_NORMAL, name)

    # def addObjectPos(self, name='UVMap'):
    #     return self.addMap(lx.symbol.i_VMAP_OBJECTPOS, name)

    def addPickMap(self, name='Pick'):
        return self.addMap(lx.symbol.i_VMAP_PICK, name)

    def addRGBMap(self, name='Color'):
        return self.addMap(lx.symbol.i_VMAP_RGB, name)

    def addRGBAMap(self, name='Color'):
        return self.addMap(lx.symbol.i_VMAP_RGBA, name)

    def addSubdivMap(self, name='Subdivision'):
        return self.addMap(lx.symbol.i_VMAP_SUBDIV, name)

    def tangentBasisMap(self, name='Tangent Basis'):
        return self.addMap(lx.symbol.i_VMAP_TBASIS, name)

    def addVectorMap(self, name='Vector'):
        return self.addMap(lx.symbol.i_VMAP_VECTOR, name)

    @property
    def weightMaps(self):
        """:getter: Returns a list of weight maps"""
        return self.getMapsByType([lx.symbol.i_VMAP_WEIGHT])

    @property
    def morphMaps(self):
        """:getter: Returns a list of morph maps"""
        return self.getMapsByType([lx.symbol.i_VMAP_MORPH, lx.symbol.i_VMAP_SPOT])

    @property
    def uvMaps(self):
        """:getter: Returns a list of uv maps"""
        return self.getMapsByType([lx.symbol.i_VMAP_TEXTUREUV])

    @property
    def rgbMaps(self):
        """:getter: Returns a list of RGB maps"""
        return self.getMapsByType([lx.symbol.i_VMAP_RGB])

    @property
    def rgbaMaps(self):
        """:getter: Returns a list of RGBA maps"""
        return self.getMapsByType([lx.symbol.i_VMAP_RGBA])

    @property
    def pickMaps(self):
        """:getter: Returns a list of pick maps (aka selection sets)"""
        return self.getMapsByType([lx.symbol.i_VMAP_PICK])

    @property
    def accessor(self):
        """:getter: Returns the internal shared MeshMapAccessor object of the core SDK (lx.object.MeshMap)"""
        return self._accessor


