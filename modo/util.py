#
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.
#

"""

.. module:: modo.util
    :synopsis: A collection of support tools, decorators, functions etc used by the other modules in the package.

.. moduleauthor:: Gwynne Reddick <gwynne.reddick@thefoundry.co.uk>


"""

import lx
import functools
from . import constants as c
from . import item
import collections


def ensureModoItem():
    """Decorator - ensures that the argument passed as the first parameter
    to a function is an instance of the modo :class:`Item` class. Should only
    only be used to decorate methods where the first argument is meant to be
    an item and ensures that if for any reason an item of either type lx.object.Item
    or lxu.object.Item gets passed to the method it will get wrapped as an
    modo.item.Item object before being used.

    """
    def decorator(func):
        @functools.wraps(func)
        def item_check(*args, **kwargs):
            args = list(args)
            if not isinstance(args[1], item.Item):
                args[1] = item.Item(args[1])
            return func(*args, **kwargs)
        return item_check
    return decorator


# A dictionary relating types to constructors
_typeToFunc = {
  c.CAMERA_TYPE: item.Camera,
  c.GROUP_TYPE: item.Group,
  c.GROUPLOCATOR_TYPE: item.GroupLocator,
  c.LOCATOR_TYPE: item.Locator,
  c.LIGHT_TYPE: item.Light,
  c.LIGHTMATERIAL_TYPE: item.LightMaterial,
  c.AREALIGHT_TYPE: item.AreaLight,
  c.CYLINDERLIGHT_TYPE: item.CylinderLight,
  c.SUNLIGHT_TYPE: item.DirectionalLight,
  c.DOMELIGHT_TYPE: item.DomeLight,
  c.PHOTOMETRYLIGHT_TYPE: item.PhotometricLight,
  c.POINTLIGHT_TYPE: item.PointLight,
  c.PORTAL_TYPE: item.Portal,
  c.SPOTLIGHT_TYPE: item.SpotLight,
  c.MESH_TYPE: item.Mesh,
  c.ACTIONCLIP_TYPE: item.ActionClip,
  c.TXTRLOCATOR_TYPE: item.TextureLocator,
  c.DEFORMGROUP_TYPE: item.DeformerGroup,
  c.GENINFLUENCE_TYPE: item.GeneralInfluenceDeformer,
}

def typeToFunc(itype):
    """selects an item class constructor based on the item type passed as an argument and returns that as a class
    instantiation 'function' object to call the correct class in methods that eg select by item type or return items. In
    essence it acts as a sort of clearing house to try to ensure that any recognised but unwrapped items are wrapped
    with the correct modo.item.xxx type before being returned.

    example usage::

        # get a list of all the light items in a scene where each light in the list is returned as the correctly
        # wrapped modo version of each light sub-type.
        import modo
        scene = modo.Scene()
        lights = []
        for light in scene.ItemList(modo.c.LIGHT_TYPE):
            func = modo.c.typeToFunc(light.Type())
            lights.append(func(light))

        # or more succinctly as a list comprehension:
        lights = [modo.c.typeToFunc(light.Type())(light) for light in scene.ItemList(modo.c.LIGHT_TYPE)]

    """
    if itype in _typeToFunc:
      return _typeToFunc[itype]
    return item.Item


def makeQuickCommand(name, func,
                      arguments=None,
                      userName='myCmdName',
                      description='This command ...',
                      toolTip='Tooltip'):
    """Quick way to create a command.

    Note that a command can only be blessed (registered) once per modo session,
    so this command will fail when attempting to rebless a command.

    :param string name: Name that the command will be callable by. Example: cmds.myCommand
    :param function func: The function that the command should call
    :param iterable arguments: A sequence of name:defaultvalue pairs to make arguments that will be passed on to the function
    :param basestring userName: The user name
    :param basestring description: Summary of the command's purpose
    :param basestring toolTip: Text that appears when hovering over the button

    example::

        import modo

        def func_args(mystring, myint):
            print mystring, myint

        def func_simple():
            print 'simple function, no arguments'


        modo.util.makeQuickCommand('test.simple', func_simple)
        modo.util.makeQuickCommand('test.args', func_args, (('mystring', 'mesh021'), ('myint', 23)))

        lx.eval('test.simple')
        lx.eval('test.args mesh022 24')

    """
    if not testGlobalInterpreter():
        raise Exception("This functionality if not available from the fire and forget python interpreter")

    import lx
    import lxifc
    import lxu.command

    class CmdMyCustomCommand(lxu.command.BasicCommand):
        def __init__(self):
            lxu.command.BasicCommand.__init__(self)
            self._argumentList = None

            if not arguments:
                return

            self._numArgs = len(arguments)
            self._argumentList = collections.OrderedDict()

            for arg in arguments:
                argName, defaultValue = arg
                self._argumentList[argName] = defaultValue
                if isinstance(defaultValue, str):
                    self.dyna_Add(argName, lx.symbol.sTYPE_STRING)
                elif isinstance(defaultValue, int):
                    self.dyna_Add(argName, lx.symbol.sTYPE_STRING)

        def cmd_Flags(self):
            return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

        def basic_Enable(self, msg):
            return True

        def cmd_Interact(self):
            pass

        def basic_Execute(self, msg, flags):
            kwargs = {}

            if self._argumentList is not None:

                if not all([self.dyna_IsSet(i) for i in range(self._numArgs)]):
                    raise ValueError('Missing argument')

                for i, pair in enumerate(self._argumentList.items()):
                    name, defaultValue = pair
                    if isinstance(defaultValue, str):
                        value = self.dyna_String(i, defaultValue)
                        kwargs[name] = value
                    elif isinstance(defaultValue, int):
                        value = self.dyna_Int(i, defaultValue)
                        kwargs[name] = value

            func(**kwargs)

        def cmd_Query(self, index, vaQuery):
            lx.notimpl()

        def cmd_UserName(self):
            return userName

        def cmd_Desc(self):
            return description

        def cmd_Tooltip(self):
            return toolTip

    try:
        lx.bless(CmdMyCustomCommand, name)
    except RuntimeError:
        raise Exception('This command is already blessed')


def floatEquals(a, b, tolerance=0.00000001):
    """Test if two floats are equal

    :returns bool:
    """
    return abs(a - b) < tolerance


def paths(key=None):
    """Access to various system paths.

    :param basestring key: Specific path to return. Returns all if None.
    :returns dictionary or string: Dictionary containing all paths or single path as string
    """
    dict = {}
    psvc = lx.service.Platform()

    for i in range(psvc.PathCount()):
        k = psvc.PathNameByIndex(i)
        p = psvc.PathByIndex(i)
        if k == key:
            return p
        dict[k] = p
    return dict


def testGlobalInterpreter():
    try:
        import lxifc
        return True
    except:
        return False


