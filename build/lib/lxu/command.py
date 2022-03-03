
#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.

import lx
import lxifc
import lxu.attributes
import lxu.service
import traceback


class BasicCommand(lxifc.Command, lxu.attributes.DynamicAttributes):
    def __init__(self):
        lxu.attributes.DynamicAttributes.__init__(self)
        self._flags = []
        self._has_varg = False
        self._msg = lx.service.Message().Allocate()


    def cmd_Message(self):
        """Returns our message object."""
        return self._msg


    def cmd_Flags(self):
        """Required method, but should be overridden by the client.
        The default retuns zero, which means this is a side-effect command.

        """
        return 0


    def cmd_ArgType(self, index):
        """The default retuns None, which means the argument type will be taken from it's definition."""
        return None


    def dyna_Add(self, name, type):
        """We override dyna_Add() to expand our flags array."""
        self._flags.append(0)
        lxu.attributes.DynamicAttributes.dyna_Add(self, name, type)


    def basic_SetFlags(self, index, flags):
        """Flags can be set by the client during initialization."""
        self._flags[index] = flags;
        if flags & lx.symbol.fCMDARG_VARIABLE:
            self._has_varg = True


    def basic_Enable(self, msg):
        """basic_Enable() gives the enable state (true/false) and reason.
        It can also return None if the command is not available at all.
        """
        return True

    def cmd_Enable(self, msg):
        msg = lx.object.Message(msg)
        res = self.basic_Enable(msg)
        if res == None:
            msg.SetCode(lx.result.CMD_NOT_AVAILABLE)
            lx.throw(lx.result.CMD_NOT_AVAILABLE)
        elif not res:
            msg.SetCode(lx.result.CMD_DISABLED)
            lx.throw(lx.result.CMD_DISABLED)
        else:
            msg.SetCode(lx.result.OK)

    def cmd_NotifyAddClient(self,argument,object):
        lx.notimpl()
    def cmd_NotifyRemoveClient(self,object):
        lx.notimpl()


    def cmd_ArgClear(self, index):
        """Clearing arguments has to deal with the vararg flags on all arguments."""
        self.dyna_SetType(index, None)
        if self._has_varg and (self._flags[index] & lx.symbol.fCMDARG_REQFORVARIABLE):
            
            for i in range(len(self._flags)):
                self._flags[i] = self._flags[i] & ~lx.symbol.fCMDARG_REQFORVAR_SET
                if self._flags[i] & lx.symbol.fCMDARG_VARIABLE:
                    self.cmd_ArgClear(i)


    def cmd_ArgResetAll(self):
        for i in range(len(self._flags)):
            self.cmd_ArgClear(i)


    def cmd_ArgFlags(self, index):
        """Get the flags, getting value_set from the dyna attrs."""
        f = self._flags[index]
        if self.dyna_IsSet(index):
           f = f | lx.symbol.fCMDARG_VALUE_SET

        return f


    def basic_ArgType(self, index):
        """Dynamic argument types can be supported with this method."""
        lx.notimpl()


    def cmd_ArgSetDatatypes(self):
        if not self._has_varg:
            return

        for i in range(len(self._flags)):
            if self._flags[i] & lx.symbol.fCMDARG_REQFORVARIABLE and not self.dyna_IsSet(i):
                lx.throw(lx.result.CMD_MISSING_ARG)

        for i in range(len(self._flags)):
            self._flags[i] = self._flags[i] | lx.symbol.fCMDARG_REQFORVAR_SET
            if self._flags[i] & lx.symbol.fCMDARG_VARIABLE:
                self.dyna_SetType(i, self.basic_ArgType(i))


    def basic_ButtonName(self):
        """Button name override."""
        pass


    def cmd_ButtonName(self):
        s = self.basic_ButtonName()
        if s:
            return s
        lx.notimpl()


    def basic_Icon(self):
        """Icon name override."""
        pass


    def cmd_Icon(self):
        s = self.basic_Icon()
        if s:
            return s
        lx.notimpl()


    def basic_PreExecute(self, msg):
        """Pre-Execution: failure is trapped by the message object."""
        pass

    def cmd_PreExecute(self):
        try:
            self.basic_PreExecute(self._msg)
        except:
            lx.outEx("basic_PreExecute failed")
            self._msg.SetCode(lx.result.FAILED)
            raise   # outEx doesn't work -- only way to see the error is to raise it again


    def basic_Execute(self, msg, flags):
        """Execution: failure is trapped by the message object."""
        lx.notimpl()


    def cmd_Execute(self, flags):
        try:
            self.basic_Execute(self._msg, flags)
        except:
            lx.out("basic_Execute failed")
            lx.out(traceback.format_exc())
            self._msg.SetCode(lx.result.FAILED)


class BasicHints(lxifc.UIValueHints):
    def uiv_Flags(self):
        if hasattr(self, "_popnames"):
            return lx.symbol.fVALHINT_POPUPS
        else:
            return 0

    def uiv_PopCount(self):
        if hasattr(self, "_popnames"):
            return len(self._popnames)
        else:
            return 0

    def uiv_PopUserName(self, index):
        return self._popnames[index]

    def uiv_PopInternalName(self, index):
        if hasattr(self, "_popinternal"):
            return self._popinternal[index]
        else:
            return self._popnames[index]

    def uiv_NotifierCount(self):
        if hasattr(self, "_notifiers"):
            return len(self._notifiers)

    def uiv_NotifierByIndex(self, index):
        return self._notifiers[index]


class NotifierHost(object):
    """Utility class for managing notifiers on a command.
    """
    def __init__(self):
        self._note_S = lxu.service.NotifySys()
        self._notifiers = []
        self._clients = {}
        self._has_arg = False

    def __del__(self):
        for c in keys(self._clients):
            for n in self._notifiers:
                 n.RemoveClient(c)

    def add(self, name, args):
        """Add a notifier by name and args. It's spawned and appended to the
           list, but only if there are no clients yet.
        """
        if self._clients:
            lx.throw(lx.result.NOACCESS)

        self._notifiers.append(self._note_S.Spawn(name, args))

    def set_arg(self, dyna, index):
        """Add the notifiers associated with an argument of the command. This can
           only be done before clients are added, and only once.
        """
        if self._has_arg:
            lx.throw(lx.result.NOACCESS)

        self._has_arg = True
        ui = dyna.atrui_UIValueHints (index)
        for i in range(ui.NotifierCount()):
            name, args = ui.NotifierByIndex(i)
            self.add(name, args)

    def add_client(self, object):
        """Add a client to all notifiers. It's placed into a dictionary to
           prevent adding more than once.
        """
        if object not in self._clients:
            self._clients[object] = 1
            for n in self._notifiers:
                 n.AddClient(object)

    def rem_client(self, object):
        """Remove a client from all notifiers.
        """
        if object in self._clients:
            del self._clients[object]
            for n in self._notifiers:
                 n.RemoveClient(object)


class StaticAnalysisCommand(BasicCommand):
    """Python Static Analysis Template
        This is a wrapped around BasicCommand. The user will just implement the "sa_" functions, 
        and the static analysis runner run the tests.
    """
    def __init__ (self):
        lxu.command.BasicCommand.__init__ (self)
        self.dyna_Add("item", "&item")
        self.basic_SetFlags(0,  lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_HIDDEN)
        self.dyna_Add('name', lx.symbol.sTYPE_STRING) 
        self.basic_SetFlags(1,  lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_QUERY | lx.symbol.fCMDARG_HIDDEN)
        self.dyna_Add('category', lx.symbol.sTYPE_STRING) 
        self.basic_SetFlags(2,  lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_QUERY | lx.symbol.fCMDARG_HIDDEN)
        self.dyna_Add('runFix', lx.symbol.sTYPE_BOOLEAN) 
        self.basic_SetFlags(3,  lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_QUERY | lx.symbol.fCMDARG_HIDDEN)
        self.dyna_Add('runTests', lx.symbol.sTYPE_STRING) 
        self.basic_SetFlags(4,  lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_QUERY | lx.symbol.fCMDARG_HIDDEN)
        self.dyna_Add('ignoreKey', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(5,  lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_QUERY | lx.symbol.fCMDARG_HIDDEN)
        self.dyna_Add('showIgnored', lx.symbol.sTYPE_BOOLEAN) 
        self.basic_SetFlags(6,  lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_QUERY | lx.symbol.fCMDARG_HIDDEN)
        self.dyna_Add('doSelect', lx.symbol.sTYPE_BOOLEAN) 
        self.basic_SetFlags(7,  lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_HIDDEN)
        self.dyna_Add('selectMode', lx.symbol.sTYPE_STRING) 
        self.basic_SetFlags(8,  lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_HIDDEN)
        self.dyna_Add('tooltip', lx.symbol.sTYPE_STRING) 
        self.basic_SetFlags(9,  lx.symbol.fCMDARG_OPTIONAL | lx.symbol.fCMDARG_QUERY | lx.symbol.fCMDARG_HIDDEN)

        self.DefaultArgumentsCount = 9 # track how many default args we have, so tests can easily get this value to test their own

    def cmd_Flags (self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable (self, msg):
        return True
    
    # run fixes for the tests
    def basic_Execute (self, msg, flags):
        # Execute the fix command
        myItem = self.__GetTestItem()
        runFix = self.dyna_Int(3, False)
        runTests = self.dyna_String(4, "")
        doSelect = self.dyna_Int(7, False)
        if runFix:
            self.sa_Fix(myItem)
        if doSelect and runTests is "":
            mode = self.dyna_String(8, "")
            self.sa_Select(myItem, mode)
        if runTests is not "":
            # fix all
            self.__RunTests(None)

    # The main part of the test
    def cmd_Query(self, index, vaQuery):
        va = lx.object.ValueArray(vaQuery)
        va.set(vaQuery)
        va.Reset()

        myItem = self.__GetTestItem()
        if index == 0:
            pass
        if index == 1:
            # Get the user defined test name
            va.AddString(self.sa_Name())
        if index == 2:
            # split the user defined categories into a list
            allCats = self.sa_Category().split(";")
            for cat in allCats:
                va.AddString(cat)
        if index == 3:
            # test the item
            va.AddString(self.sa_Test(myItem))
        if index == 4:
            # test all items
            self.__RunTests(va)
        if index == 6:
            va.AddInt(self.__IsIgnored(myItem))
        if index == 9:
            va.AddString(self.sa_ToolTip())
    
    # work out if the item has the ignore flag set       
    def __IsIgnored(self, item):
        bShowIgnore = self.dyna_Bool(6, False)
        if bShowIgnore:
            return False

        tagVal = ""
        tag = lx.object.StringTag(item)
        tagID = lxu.lxID4("SAIT")
        if tagID != None:
            try:
                tagVal = tag.Get(tagID)
            except:
                tagVal = ""
        allTags = []
        if tagVal is not "":
            allTags = tagVal.split(";")

        ignoreKey = self.dyna_String(5)
        allKeys = []
        allKeys = ignoreKey.split(";")
        
        bFoundIgnore = False
        for key in allKeys:
            if key in allTags:
                bFoundIgnore = True
                break
        return bFoundIgnore

    # find the items to test in the scene
    def __GetAllItems(self, itype=None, selected = False):
        # from the td sdk.
        srvScn = lx.service.Scene()
        scene = lxu.select.SceneSelection().current()
        all_items = []
        types = []
        if isinstance(itype, str):
            allUserTypes = []
            allUserTypes = itype.split(";")     
            for uType in allUserTypes:   
                itype = srvScn.ItemTypeLookup(uType)
                types.append(itype)
        if itype == None:
            types = []
            for i in range(srvScn.ItemTypeCount()):
                types.append(srvScn.ItemTypeByIndex(i) )

        types.append(0)

        item_types = lx.object.storage()
        item_types.setType('i')
        item_types.set(types)

        selSrv = lx.service.Selection()
        if selected < 2:
            idents = set()
            item_count = scene.ItemCountByTypes(item_types)

            for i in range(item_count):
                bDoAdd = True
                item = scene.ItemByIndexByTypes(item_types, i)
                ident = item.Ident()
                if ident not in idents:
                    if selected == 1:
                        spTrans = lx.object.ItemPacketTranslation(selSrv.Allocate(lx.symbol.sSELTYP_ITEM))
                        spType = selSrv.LookupType(lx.symbol.sSELTYP_ITEM)

                        pkt = spTrans.Packet(item)
                        if selected:
                            if selSrv.Test(spType, pkt):
                                bDoAdd = True
                            else:
                                bDoAdd = False
                    if bDoAdd:
                        idents.add(ident)
                        all_items.append(item)
        else:
            #graph
            grpCount = 0;
            grpType = srvScn.ItemTypeLookup("group")
            grpCount = scene.ItemCount(grpType)
            for grpIter in range(0, grpCount):
                myGroup = scene.ItemByIndex(grpType, grpIter);
                spTrans = lx.object.ItemPacketTranslation(selSrv.Allocate(lx.symbol.sSELTYP_ITEM))
                spType = selSrv.LookupType(lx.symbol.sSELTYP_ITEM)
                pkt = spTrans.Packet(myGroup)
                if selSrv.Test(spType, pkt):
                    ig = lx.object.ItemGraph(scene.GraphLookup("itemGroups"))
                    itemCount = ig.FwdCount(myGroup)
                    for linkedItemIter in range(0, itemCount):
                        groupItem = ig.FwdByIndex(myGroup, linkedItemIter)
                        if groupItem.TestTypes(item_types):
                            all_items.append(groupItem)
        return all_items



    # Run tests against all items of desired type
    def __RunTests(self, vaArray=None):
        testType = self.sa_ItemType()
        srvCmd = lx.service.Command()
        valSrv = lx.service.Value()
        cmd = srvCmd.Spawn(0, "StaticAnalysis.TestType")
        myAtt = lx.object.Attributes()
        myAtt.set(cmd)
        hints = myAtt.Hints(0)
        doSelection = lx.eval("StaticAnalysis.TestType ?")
        selectInt = valSrv.TextHintDecode(str(doSelection), hints)
        allItems = self.__GetAllItems(testType, selectInt)
        self.all_results = []
        for item in allItems:
            if self.__IsIgnored(item) == False:
                result = self.sa_Test(item)
                if result is not "":
                    if vaArray is not None:
                        vaArray.AddString(item.UniqueName())
                        vaArray.AddString(result)
                    else:
                        doSelect = self.dyna_Int(7, False)
                        if doSelect:
                            print (item)                   
                            self.sa_Select(item, "add")
                        else:
                            self.sa_Fix(item)


    
    # Get our test item
    def __GetTestItem(self):
        ident = self.dyna_String (0, '')
        scn = lxu.select.SceneSelection ().current ()
        MyItem = None
        if scn is None:
            return
        try:
            MyItem = scn.ItemLookupIdent (ident)
        except:
            pass
        return MyItem

    # Override the following in user tests
    # type of items to test eg "return 'mesh'"
    def sa_ItemType(self):
        return None

    # Test name eg return "My Test"
    def sa_Name(self):
        return ""

    # Categories for the tests eg "return catA;catB"
    def sa_Category(self):
        return ""

    # Tooltip to display in the tree for the test
    def sa_ToolTip(self):
        return ""

    # return a string if the test fails. if it passes return ""
    def sa_Test(self, item=None):        
        pass

    # Function to attempt a fix for the test
    def sa_Fix(self, item=None):
        pass

    # Function to select the item.
    # If doing a geometry based tst, you may need to override the function, otherwise you can leave it
    def sa_Select(self, item=None, mode=""):
        lx.eval("select.item {{{0}}} {1}".format(item.Ident(), mode))
        



# Function easily bless our command with the correct tag:
# eg modo.staticanalysis.RegisterStaticAnalysisTest(TestPython, "testingSA")
def RegisterStaticAnalysisTest(in_function, in_name):
    tags = {"StaticAnalysisTest":  in_name}
    try:
        lx.bless(in_function, in_name, tags)
    except:
        print("ERROR: Test Already Exists.")


