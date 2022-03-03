#!/usr/bin/env python
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.

import lx
import lxguid
import string
import sys

if sys.version_info[0] > 2:
    from .utils import decodeID4, lxID4
else:
    from .utils import decodeID4, lxID4

def lookupGuidName(guid):
    if guid.upper() not in lxguid.GUIDs:
        return guid
    name = lxguid.GUIDs[guid.upper()]
    isService = False
    if name.endswith("Service"):
        isService = True
        name = name[:-len("Service")]
    if isService:
        name = "lx.service.{}".format(name)
    else:
        name = "lx.object.{}".format(name)

    return name.rstrip(string.digits)
    
def unknownInfo(unknown):
    try:
        object = lx.object.Object(unknown)
        
        identifier = object.Identifier()
        lx.out("Identifier: {}\n".format(identifier))
        
        string = "Interfaces:\n"
        
        count = object.InterfaceCount()
        for i in range(count):
            try:
                guid = object.InterfaceByIndex(i)
                name = lookupGuidName(guid)
                string = string + "    {}\n".format(name)
            except:
                continue

        lx.out(string)

    except:
        return

if not hasattr(lx.object, "info"):
    setattr(lx.object, "info", unknownInfo)


