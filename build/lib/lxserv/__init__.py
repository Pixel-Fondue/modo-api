# Import Python-based plug-in servers. We're going to scan 'lxserv' subdirectories
# for any modules that might be servers and import them. Naturally these scripts
# could do bad things, so let's hope they don't.
#
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.
#
import lx
import os
import sys
import traceback
import collections

# Context manager for altering the system path. We want to temporarily append
# and remove the temp path in every case, normal or exceptional.
#
class ImportPath(object):
    def __init__(self, dirpath):
        self._dir = dirpath

    def __enter__(self):
        sys.path.append(self._dir)

    def __exit__(self, xt, xv, tb):
        sys.path.pop()
        return False


# Return list of all the modules in a single directory.
#
def ScanOne(dirpath):
    if not os.path.exists(dirpath):
        return None

    ls = []
    for filename in os.listdir(dirpath):
        module,extension = os.path.splitext(filename)
        if extension == '.py' or extension == '.pyc' and module not in ls:
            ls.append(module)

    return ls


# Return a list of all modules that can be found on any script or config path.
# This is the same search path used for scripts, but we look for the "lxserv"
# sub-directory. The result of this function is a list of tuples: directory
# name, list of modules.
#
def ScanAll():
    ml = []
    ps = lx.service.Platform()
    dirhash = collections.OrderedDict()
    for i in range(ps.ImportPathCount()):
        dirhash[ ps.ImportPathByIndex(i) ] = 1

    for dir in list(dirhash.keys()):
        path = os.path.join(dir, "lxserv")
        mods = ScanOne(path)
        if (mods):
            ml.append( (path, mods) )

    return ml


# Do the actual import. We want the modules in the root namespace for this
# module, so we have to do the import here rather than in a function.
#
# NOTE: not sure what happens to servers that have already been blessed if
# the import fails...
#
for _d,_l in ScanAll():
    with ImportPath(_d):
        for _m in _l:
            try:
                exec("import " + _m)
            except Exception:
                _e = lx.service.Message().Allocate()
                _e.SetCode(lx.symbol.e_STARTUP)
                _e.SetMessage('pythonintr','bad_import', 0)
                _e.SetArgumentString(1,str(_m))
                _e.SetArgumentString(2,traceback.format_exc())

                _lS = lx.service.Log()
                _e = _lS.CreateEntryMessageFromMsgObj(_e)
                _lS.SubSystemLookup('python').AddEntry(_e)


# Metaclasses may have only been put into a list for later intialization.
# This executes the global list, if any.
#
import lxu.meta.meta
lxu.meta.meta.InitAll()


