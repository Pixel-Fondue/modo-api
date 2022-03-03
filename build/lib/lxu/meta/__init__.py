#!/usr/bin/env python
#
# We want the lxu.meta module to be populated with all the metaclasses that are
# available for creating servers. Thus it imports from all the sub-modules.
#
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.

import sys

from .meta      import *
from .chanmod   import ChannelModifier,Meta_ChannelModifier
from .channel   import Channels,Meta_Channels
from .command   import Command,Meta_Command,CustomArgument
from .drop      import Drop,Meta_Drop,DropAction
from .falloff   import Falloff,Meta_Falloff
from .modifier  import EvalModifier,Meta_EvalModifier,ObjectEvaluation,Meta_ObjectEvaluation,Simulation
from .package   import Package,Meta_Package,ChannelUI,ViewItem3D,Meta_ViewItem3D
from .select    import SelectionType,Meta_SelectionType
from .schematic import SchematicConnection,Meta_SchematicConnection

from lxu.attrdesc import CustomChannelUI


