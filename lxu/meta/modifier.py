#!/usr/bin/env python
#
# EvalModifier server metaclasses
#
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.

import lx
import lxu
import lxu.object
import lxu.utils
import lxifc
from lxu.meta.meta import Meta, MetaServer, MetaInterface


class EvalModifier(object):
    """Base class for defining EvalModifier server. The client will
       subclass this base class, filling in the methods that they require.
    """
    def include_item(self, item):
        """Implement this method for modifiers that apply to all items. Return a
           list of indices, if nodes are to be created for this item.
        """
        return []

    def bind(self, item, ident):
        """Implement this method to bind custom channels that aren't part of the
           channels metaclass. Call the next function to add them.
        """
        pass

    def mod_add_chan(self, item, chan, type = lx.symbol.fECHAN_READ):
        """Call this method to add a named custom channel.
        """
        self._custom.append((item, chan, type))

    def change_test(self):
        """Any changes to custom channels will automatically trigger modifier
           invalidation. Implement this method to invalidate for other changes.
        """
        return True

    def eval(self):
        """Implement this method to evaluate inputs and write outputs.
        """
        pass

    def mod_item(self):
        """Call this method to get the item for this modifier node.
        """
        return self._item

    def mod_index(self):
        """Call this method to get the identifing index for this modifier node.
        """
        return self._ident

    def mod_eval(self):
        """Call this method to get the Evaluation object.
        """
        return self._eval

    def mod_attr(self):
        """Call this method to get the Attributes object.
        """
        return self._attr

    def mod_read_attr(self):
        """Call this method to read channels defined in the Channels metaclass.
        """
        return self._desc.eval_read (self._attr, self._base_desc)

    def mod_cust_index(self, index):
        """Call this method to get the attribute index of a custom channel.
        """
        return self._attridx[index]

    def mod_cust_value(self, index):
        """Call this method to get the value of a custom channel.
        """
        v = self._attr.Value(self._attridx[index], 0)
        try:
            return lxu.object.Value(v)
        except:
            return v

    def mod_cust_write(self, index):
        """Call this method to get the writable value of a custom channel.
        """
        v = self._attr.Value(self._attridx[index], 1)
        try:
            return lxu.object.Value(v)
        except:
            return v

    def mod_result(self, res):
        """Call this method to return a result other than e_OK.
        """
        self._res = res


class Evaluator(object):
    """We can also implement alternate forms of evaluation, which can take
       over part of the eval process.
    """
    def bind(self, mod):
        pass

    def eval(self, mod):
        pass


class MetaEvaluator(Meta):
    """Alternate evaluators are under the eval modifier metaclass.
    """
    def __init__(self):
        Meta.__init__(self)
        self._type = self.types.EVALUATOR


class impl_Modifier(lxifc.Modifier):
    """This internal class implements the actual Modifier object.
    """
    def __init__(self, meta):
        self._meta = meta
        self._met2 = meta._meta
        self._inst = meta._meta._cls_inst()
        self._res  = 0
        if self._met2._alt_meta:
            self._alt = self._met2._alt_meta.alloc()
        else:
            self._alt = None

    def init_node(self, item, ident, eval):
        z = self._inst
        z._item  = lxu.object.Item(item)
        z._ident = ident
        z._eval  = lxu.object.Evaluation(eval)
        z._attr  = lxu.object.Attributes(eval)

        if self._alt:
            self._alt.bind(z)

        z._custom = []
        z.bind(z._item, ident)
        z._oldcust = z._custom
        z._attridx = []
        for c in z._custom:
            i = z._eval.AddChannelName(c[0], c[1], c[2])
            z._attridx.append(i)

        if self._met2._desc:
            z._desc = self._met2._desc
            z._base_desc = z._desc.eval_attach(z._eval, z._item)

    def mod_Evaluate(self):
        z = self._inst
        z._res = lx.result.OK

        if self._alt:
            self._alt.eval(z)
        else:
            z.eval()

        if z._res is not lx.result.OK:
            lx.throw(z._res)

    def mod_Test(self, item, index):
        z = self._inst
        if not z.change_test():
            return False

        if not z._oldcust:
            return True

        z._custom = []
        z.bind(z._item, z._ident)
        return z._custom == z._oldcust

#    def mod_Free(self,cache):
#        lx.notimpl()

#    def mod_Invalidate(self,item,index):
#        lx.notimpl()
#    def mod_Validate(self,item,index,rc):
#        lx.notimpl()
#    def mod_RequiredCount(self):
#        return 0
#    def mod_Required(self,index):
#        lx.notimpl()


class meta_Modifier(object):
    """This internal class is the metaclass for the Modifier nodes. Its
       _meta is the EvalModifier metaclass. Very meta.
    """
    def __init__(self, meta):
        self._meta = meta


class ItemsByType(object):
    """Iteration by item type: returns one node per item, all index 0
    """
    def __init__(self, scene, type):
        self._type = type
        self._scene = lxu.object.Scene(scene)
        self._n = self._scene.ItemCount(type)
        self._i = 0

    def __next__(self):
        if (self._i >= self._n):
            return (0,0)
        else:
            item = self._scene.ItemByIndex(self._type, self._i)
            self._i += 1
            return (item, 0)


class ItemsByTest(object):
    """Iteration by test function: walks all items in the scene and returns
       as many nodes as requested by the client.
    """
    def __init__(self, scene, inst):
        self._inst = inst
        self._scene = lxu.object.Scene(scene)
        self._n = self._scene.ItemCount(lx.symbol.iTYPE_ANY)
        self._i = 0
        self._list = []

    def __next__(self):
        while True:
            if (len(self._list)):
                return a.pop()

            if (self._i >= self._n):
                return (0,0)

            item = self._scene.ItemByIndex(self._type, self._i)
            self._i += 1
            lidx = self._inst.include_item(item)
            self._list = [ (item, x) for x in lidx ]


class impl_EvalModifier(lxifc.EvalModifier):
    """This internal class implements the actual EvalModifier server. It basically
       iterates through items to determine what noes to add, and allocates them.
    """
    def __init__(self, meta):
        self._meta = meta
        self._inst = meta._cls_inst()
        self._iter = None

    def eval_Reset(self, scene):
        if self._meta._getall:
            self._iter = ItemsByTest(scene, self._inst)
        else:
            self._iter = ItemsByType(scene, self._meta._itemtype.code())

    def eval_Next(self):
        return next(self._iter)

    def eval_Alloc(self, item, index, eval):
        mod = impl_Modifier(self._meta._mod_meta)
        mod.init_node(item, index, eval)
        return mod


def string_KeyNames(dict):
    s = ''
    for k in list(dict.keys()):
        if len(s):
            s += ' '

        s += k

    return s


class Meta_EvalModifier(MetaServer):
    """This is the metaclass for the Falloff object type.
    """
    def __init__(self, name, cinst = EvalModifier):
        lxu.meta.MetaServer.__init__(self, name, lx.symbol.u_EVALMODIFIER)
        self._cls_inst = cinst
        self._itemtype = lxu.utils.ItemType()
        self._dep_type = {}
        self._dep_graph = {}
        self._getall = False
        self._desc = None
        self._alt_meta = None
        self._mod_meta = None

    def set_itemtype(self, typename):
        """If there's a package server in the meta tree then that's automatically
           set as the main item type for the modifier. That can be overridden
           with this call.
        """
        self._itemtype.set(typename)

    def get_all_items(self):
        """A modifier associated with an item type will allocate one modifier
	       node for each item of that type. Calling get_all_items() will instead
           configure the modifier to process all items, adding zero or more
           nodes for each.
        """
        self._getall = True

    def add_dependent_type(self, typename):
        """Modifiers can be automatically invalidated for changes related to
	       other item types.
        """
        self._dep_type[typename] = 1

    def add_dependent_graph(self, graphname):
        """Modifiers can be automatically invalidated for changes related to
	       named graphs.
        """
        self._dep_graph[graphname] = 1

    def invalidate(self, scene, reset = False):
        """Any change (other than item types or graphs) that require the modifier
	       nodes to be refreshed should invalidate the modifier. If 'reset' is
	       true then the results of all modifier nodes are cleared regardless.
        """
        scene = lx.object.Scene(scene)
        if reset:
            scene.EvalModReset(self._name)
        else:
            scene.EvalModInvalidate(self._name)

    def set_simulation(self):
        """Call to set the modifier to be a simulation.
        """
        self.add(meta_Simulation())

    def alloc(self):
        """Internal metaclass method.
        """
        m = self.find_any(self.types.ATTRDESC)
        if (m):
            self._desc = m.alloc()

        self._alt_meta = self.find_sub(self.types.EVALUATOR)
        self._mod_meta = meta_Modifier(self)
        self._mod_meta._sub_ifcs = self.get_ifcs(lx.symbol.u_MODIFIER)

        if not self._itemtype:
            m = self.find_any(self.types.SERVER, lx.symbol.u_PACKAGE)
            if (m):
                self._itemtype.set(m._name)

        if self._itemtype:
            self._dep_type[self._itemtype.name()] = 1

        if (self._dep_type):
            self.add_tag(lx.symbol.sMOD_TYPELIST, string_KeyNames(self._dep_type))

        if (self._dep_graph):
            self.add_tag(lx.symbol.sMOD_GRAPHLIST, string_KeyNames(self._dep_graph))

        if (self._itemtype and not self._getall):
            self.add_tag(lx.symbol.sMOD_REQUIREDTYPE, self._itemtype.name())

        return impl_EvalModifier


class Simulation(object):
    """Co-class for evaluating an EvalModifier in a simulation context.
    """
    def enabled(self, chanRead):
        return True

    def init_sim(self, time, sample):
        pass

    def cleanup_sim(self):
        pass

    def step_size(self):
        return 0.0

    def step(self, dt):
        pass

class impl_Simulation(lxifc.SimulationModifier):
    """Implementation for Simulation. This just gets the instance from the
       Modifier implementation.
    """
    def __init__(self, meta):
        self._meta = meta

    def inherit(self, modimpl):
        self._inst = modimpl._inst

    def sim_Enabled(self, chanRead):
        return self._inst.enabled(lxu.object.ChannelRead(chanRead))

    def sim_Initialize(self, time, sample):
        self._inst.init_sim(time, sample)

    def sim_Cleanup(self):
        self._inst.cleanup_sim()

    def sim_StepSize(self):
        s = self._inst.step_size()
        if s <= 0.0:
            lx.notimpl()
        else:
            return s

    def sim_Step(self,dt):
        self._inst.step(dt)

class meta_Simulation(MetaInterface):
    """Metaclass for Simulation. This is added under a Modifier.
    """
    def __init__(self):
        MetaInterface.__init__(self, lx.symbol.u_MODIFIER)

    def alloc(self):
        return impl_Simulation


class ObjectEvaluation(object):
    """One alternate form of evaluation is to create an object and write it
       to an OBJREF channel. The object can be allocated directly or using a
       metaclass.
    """
    def alloc_obj(self, mod):
        """Implement this method to allocate and return a new object.
        """
        pass

    def init_obj(self, mod, obj):
        """Implement this method to initialize an object alloced by metaclass.
        """
        pass


class impl_ObjectEvaluation(Evaluator):
    def __init__(self, meta):
        self._chan = meta._name
        self._inst = meta._cls_inst()
        self._obj_meta = meta._obj_meta

    def bind(self, mod):
        eval = mod.mod_eval()
        item = mod.mod_item()
        self._chidx = eval.AddChannelName(item, self._chan, lx.symbol.fECHAN_WRITE)

    def eval(self, mod):
        if self._obj_meta:
            obj = self._obj_meta.spawn()
            self._inst.init_obj(mod, self._obj_meta.extract(obj))
        else:
            obj = self._inst.alloc_obj(mod)

        ref = mod.mod_attr().Value(self._chidx, 1)
        ref = lx.object.ValueReference(ref)
        ref.SetObject(obj)


class Meta_ObjectEvaluation(MetaEvaluator):
    """This is the metaclass for the Object evaluator.
    """
    def __init__(self, chan, cinst = ObjectEvaluation):
        MetaEvaluator.__init__(self)
        self._name = chan
        self._cls_inst = cinst
        self._obj_meta = None

    def alloc(self):
        if not self._obj_meta:
            self._obj_meta = self.find_sub(self.types.OBJECT)

        return impl_ObjectEvaluation(self)




