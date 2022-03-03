#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.
#
import lx

class Modifier(object):
    def mod_Evaluate(self):
        lx.notimpl()
    def mod_Test(self,item,index):
        return True
    def mod_Invalidate(self,item,index):
        lx.notimpl()
    def mod_Validate(self,item,index,rc):
        lx.notimpl()
    def mod_RequiredCount(self):
        return 0
    def mod_Required(self,index):
        lx.notimpl()
    def mod_Free(self,cache):
        lx.notimpl()

class SimulationModifier(object):
    def sim_Enabled(self,chanRead):
        return True
    def sim_Initialize(self,time,sample):
        lx.notimpl()
    def sim_Cleanup(self):
        lx.notimpl()
    def sim_StepSize(self):
        lx.notimpl()
    def sim_Step(self,dt):
        lx.notimpl()
    def sim_Bake(self,time):
        lx.notimpl()

class EvalModifier(object):
    def eval_Reset(self,scene):
        lx.notimpl()
    def eval_Next(self):
        return (0,0)
    def eval_Alloc(self,item,index,eval):
        lx.notimpl()

class ActionListener(object):
    def actl_ActionChannelSignal(self,item,channel):
        lx.notimpl()
    def actl_ActionChannelConstantChange(self,item,channel):
        lx.notimpl()
    def actl_ActionChannelConstantPreChange(self,item,channel):
        lx.notimpl()

lx.bless(Modifier,":Modifier")
lx.bless(SimulationModifier,":SimulationModifier")
lx.bless(EvalModifier,":EvalModifier")
lx.bless(ActionListener,":ActionListener")


class AnimListener(object):
    def animevent_TimeChange(self):
        lx.notimpl()
    def animevent_PlayStart(self):
        lx.notimpl()
    def animevent_PlayEnd(self):
        lx.notimpl()
    def animevent_ScrubTime(self):
        lx.notimpl()
    def animevent_ScrubEnd(self):
        lx.notimpl()
    def animevent_EnterSetup(self):
        lx.notimpl()
    def animevent_LeaveSetup(self):
        lx.notimpl()

lx.bless(AnimListener,":AnimListener")



class ChannelModOperator(object):
    def cmop_Evaluate(self):
        lx.notimpl()

class ChannelModItem(object):
    # Allocate skipped
    def cmod_Flags(self,item,index):
        lx.notimpl()
    def cmod_Evaluate(self,cmod,attr,data):
        lx.notimpl()
    def cmod_Cleanup(self,data):
        lx.notimpl()

class ChannelModManager(object):
    def cman_Define(self,cmod):
        lx.notimpl()
    def cman_Allocate(self,cmod):
        lx.notimpl()

lx.bless(ChannelModOperator,":ChannelModOperator")
lx.bless(ChannelModItem,":ChannelModItem")
lx.bless(ChannelModManager,":ChannelModManager")

class ChannelUI(object):
    def cui_Enabled(self,channelName,msg,item,chanRead):
        lx.notimpl()
    def cui_DependencyCount(self,channelName):
        lx.notimpl()
    def cui_DependencyByIndex(self,channelName,index):
        lx.notimpl()
    def cui_DependencyByIndexName(self,channelName,index):
        lx.notimpl()
    def cui_ItemEnabled(self,msg,item):
        lx.notimpl()
    def cui_ItemIcon(self,item):
        lx.notimpl()
    def cui_UIHints(self,channelName,hints):
        lx.notimpl()
    def cui_UIValueHints(self,channelName):
        lx.notimpl()
    def cui_Cookie(self,channelName,requestedFor):
        lx.notimpl()

lx.bless(ChannelUI,":ChannelUI")

class VideoClipItem(object):
    # PrepFilter skipped
    def vclip_AllocFilter(self,attr,cache):
        lx.notimpl()
    def vclip_Cleanup(self,cache):
        lx.notimpl()

lx.bless(VideoClipItem,":VideoClipItem")

class ClipDest(object):
    def locd_Item(self):
        lx.notimpl()
    def locd_Type(self):
        lx.notimpl()
    def locd_Location(self):
        lx.notimpl()

lx.bless(ClipDest,":ClipDest")

class ColorModel(object):
    def colm_NumComponents(self):
        lx.notimpl()
    def colm_ComponentType(self,component):
        lx.notimpl()
    def colm_ComponentRange(self,component):
        lx.notimpl()
    def colm_ToRGB(self,vector,rgb):
        lx.notimpl()
    def colm_FromRGB(self,rgb,vector):
        lx.notimpl()
    def colm_DrawSlice(self,image,xAxis,yAxis,vec):
        lx.notimpl()
    def colm_DrawSliceMarker(self,image,xAxis,yAxis,downVec,vec):
        lx.notimpl()
    def colm_CanSliceBeReused(self,xAxis,yAxis,oldVec,newVec):
        lx.notimpl()
    def colm_ToSlicePos(self,xAxis,yAxis,imgW,imgH,vec):
        lx.notimpl()
    def colm_FromSlicePos(self,xAxis,yAxis,imgW,imgH,imgX,imgY,downVec,vec):
        lx.notimpl()
    def colm_StripBaseVector(self,axis,dynamic,vec):
        lx.notimpl()

class Color(object):
    def color_Color(self):
        lx.notimpl()
    def color_Alpha(self):
        lx.notimpl()
    def color_ColorModel(self):
        lx.notimpl()
    def color_ColorInModelSpace(self):
        lx.notimpl()

lx.bless(ColorModel,":ColorModel")
lx.bless(Color,":Color")

class ColorMappingModule(object):
    def cmapmod_Flags(self):
        lx.notimpl()

class ColorMapping(object):
    def cmap_Setup(self,toLinear):
        lx.notimpl()
    def cmap_ToLinear(self,sourceValues,length):
        lx.notimpl()
    def cmap_FromLinear(self,linearValues,length):
        lx.notimpl()
    def cmap_ToLinearFast(self,length):
        lx.notimpl()
    def cmap_FromLinearFast(self,length):
        lx.notimpl()
    # GetLUTImage skipped
    # GetShaderSource skipped
    def cmap_GetName(self):
        lx.notimpl()
    def cmap_GetCMServerName(self):
        lx.notimpl()
    # GenerateICCProfile skipped

lx.bless(ColorMappingModule,":ColorMappingModule")
lx.bless(ColorMapping,":ColorMapping")

class Object(object):
    def obj_Identifier(self):
        lx.notimpl()
    def obj_InterfaceCount(self):
        lx.notimpl()
    def obj_InterfaceByIndex(self,index):
        lx.notimpl()
    def obj_AddObserver(self,visitor):
        lx.notimpl()
    def obj_RemoveObserver(self,visitor):
        lx.notimpl()

lx.bless(Object,":Object")

class CmdSysListener(object):
    def cmdsysevent_SystemReady(self):
        lx.notimpl()
    def cmdsysevent_UndoLockout(self,isLockedOut):
        lx.notimpl()
    def cmdsysevent_CommandAdded(self,name):
        lx.notimpl()
    def cmdsysevent_AliasAdded(self,name,isOverride):
        lx.notimpl()
    def cmdsysevent_AliasRemoved(self,name,isOverride):
        lx.notimpl()
    def cmdsysevent_ExecutePre(self,cmd,type,isSandboxed,isPostCmd):
        lx.notimpl()
    def cmdsysevent_ExecuteResult(self,cmd,type,isSandboxed,isPostCmd,wasSuccessful):
        lx.notimpl()
    def cmdsysevent_ExecutePost(self,cmd,isSandboxed,isPostCmd):
        lx.notimpl()
    def cmdsysevent_BlockBegin(self,block,isSandboxed):
        lx.notimpl()
    def cmdsysevent_BlockEnd(self,block,isSandboxed,wasDiscarded):
        lx.notimpl()
    def cmdsysevent_BlockEndedPostMode(self,name,isSandboxed):
        lx.notimpl()
    def cmdsysevent_RefireBegin(self):
        lx.notimpl()
    def cmdsysevent_RefireEnd(self):
        lx.notimpl()
    def cmdsysevent_RefiringNext(self):
        lx.notimpl()
    def cmdsysevent_PostModeBegin(self):
        lx.notimpl()
    def cmdsysevent_PostModeEnd(self):
        lx.notimpl()
    def cmdsysevent_PostModeRestart(self):
        lx.notimpl()
    def cmdsysevent_PostModeUndoNext(self):
        lx.notimpl()
    def cmdsysevent_UserUndo(self):
        lx.notimpl()
    def cmdsysevent_UserRedo(self):
        lx.notimpl()

class AttributesUI(object):
    def atrui_UIHints(self,index,hints):
        lx.notimpl()
    def atrui_UIValueHints(self,index):
        lx.notimpl()
    def atrui_DisableMsg(self,index,message):
        lx.notimpl()

class CommandEvent(object):
    def cevt_Event(self,flags):
        lx.notimpl()

class Command(object):
    def cmd_Tag(self):
        lx.notimpl()
    def cmd_Name(self):
        lx.notimpl()
    def cmd_UserName(self):
        lx.notimpl()
    def cmd_ButtonName(self):
        lx.notimpl()
    def cmd_Desc(self):
        lx.notimpl()
    def cmd_Tooltip(self):
        lx.notimpl()
    def cmd_Help(self):
        lx.notimpl()
    def cmd_Example(self):
        lx.notimpl()
    def cmd_Icon(self):
        lx.notimpl()
    def cmd_Flags(self):
        lx.notimpl()
    def cmd_PostExecFlags(self):
        lx.notimpl()
    def cmd_PostExecBehaviorFlags(self):
        lx.notimpl()
    def cmd_PostExecHints(self):
        lx.notimpl()
    def cmd_SandboxGUID(self):
        lx.notimpl()
    def cmd_Message(self):
        lx.notimpl()
    def cmd_Enable(self,msg):
        lx.notimpl()
    def cmd_ContainedEnable(self):
        lx.notimpl()
    def cmd_Interact(self):
        lx.notimpl()
    def cmd_PreExecute(self):
        lx.notimpl()
    def cmd_Execute(self,flags):
        lx.notimpl()
    def cmd_ToggleArg(self):
        lx.notimpl()
    def cmd_ArgFlags(self,index):
        lx.notimpl()
    def cmd_ArgClear(self,index):
        lx.notimpl()
    def cmd_ArgResetAll(self):
        lx.notimpl()
    def cmd_ArgSetDatatypes(self):
        lx.notimpl()
    def cmd_ArgUserName(self,index):
        lx.notimpl()
    def cmd_ArgDesc(self,index):
        lx.notimpl()
    def cmd_ArgExample(self,index):
        lx.notimpl()
    def cmd_ArgType(self,index):
        lx.notimpl()
    def cmd_ArgTypeUserName(self,index):
        lx.notimpl()
    def cmd_ArgTypeDesc(self,index):
        lx.notimpl()
    def cmd_ArgOptionUserName(self,index,optIndex):
        lx.notimpl()
    def cmd_ArgOptionDesc(self,index,optIndex):
        lx.notimpl()
    def cmd_DialogInit(self):
        lx.notimpl()
    def cmd_DialogArgChange(self,arg):
        lx.notimpl()
    def cmd_ArgEnable(self,arg):
        lx.notimpl()
    def cmd_ArgParseString(self,argIndex,argString):
        lx.notimpl()
    def cmd_Copy(self,sourceCommand):
        lx.notimpl()
    def cmd_Query(self,index,vaQuery):
        lx.notimpl()
    def cmd_NotifyAddClient(self,argument,object):
        lx.notimpl()
    def cmd_NotifyRemoveClient(self,object):
        lx.notimpl()
    def cmd_DialogFormatting(self):
        lx.notimpl()
    def cmd_IconImage(self,w,h):
        lx.notimpl()

class UIValueHints(object):
    def uiv_Flags(self):
        lx.notimpl()
    def uiv_PopCount(self):
        lx.notimpl()
    def uiv_PopUserName(self,index):
        lx.notimpl()
    def uiv_PopInternalName(self,index):
        lx.notimpl()
    def uiv_PopToolTip(self,index):
        lx.notimpl()
    def uiv_PopIconSize(self):
        lx.notimpl()
    def uiv_PopIconImage(self,index):
        lx.notimpl()
    def uiv_PopIconResource(self,index):
        lx.notimpl()
    def uiv_PopFlags(self,index):
        lx.notimpl()
    def uiv_PopCategory(self):
        lx.notimpl()
    def uiv_ItemTest(self,item):
        lx.notimpl()
    def uiv_ColorPickerCommands(self,rgb,alpha,rgbAlt,alphaAlt,useAlt,bufLens):
        lx.notimpl()
    def uiv_NotifierCount(self):
        lx.notimpl()
    def uiv_NotifierByIndex(self,index):
        lx.notimpl()
    def uiv_FormCommandListCount(self):
        lx.notimpl()
    def uiv_FormCommandListByIndex(self,index):
        lx.notimpl()
    def uiv_CueText(self):
        lx.notimpl()
    def uiv_TextValidate(self,value):
        lx.notimpl()

lx.bless(CmdSysListener,":CmdSysListener")
lx.bless(AttributesUI,":AttributesUI")
lx.bless(CommandEvent,":CommandEvent")
lx.bless(Command,":Command")
lx.bless(UIValueHints,":UIValueHints")

class CustomView(object):
    def customview_Init(self,pane):
        lx.notimpl()
    def customview_Cleanup(self,pane):
        lx.notimpl()
    def customview_StoreState(self,pane):
        lx.notimpl()
    def customview_RestoreState(self,pane):
        lx.notimpl()

lx.bless(CustomView,":CustomView")

class ItemInfluence(object):
    def iinf_HasItems(self):
        lx.notimpl()
    def iinf_Enumerate(self,visitor):
        lx.notimpl()
    def iinf_GetItem(self):
        lx.notimpl()
    def iinf_AllowTransform(self,index):
        lx.notimpl()

class Deformer(object):
    def dinf_Flags(self):
        lx.notimpl()
    def dinf_PartitionCount(self):
        return 0
    def dinf_EnumeratePartition(self,visitor,part):
        lx.notimpl()
    def dinf_Element(self):
        lx.notimpl()
    def dinf_SetPartition(self,part):
        lx.notimpl()
    def dinf_Weight(self,elt,pos):
        return 1
    def dinf_Offset(self,elt,weight,pos):
        lx.notimpl()
    # WeightRun skipped
    # OffsetRun skipped

class MeshInfluence(object):
    def minf_MeshCount(self):
        return 0
    def minf_MeshByIndex(self,index):
        lx.notimpl()
    def minf_PartitionIndex(self,index):
        return index
    def minf_SetMesh(self,index,mesh,item):
        lx.notimpl()
    def minf_SetTransform(self,index):
        lx.notimpl()
    def minf_MeshChange(self,index,change):
        lx.notimpl()

class WeightMapDeformerItem(object):
    def wmd_GetMapName(self,chanRead):
        lx.notimpl()
    def wmd_GetColor(self,chanRead):
        lx.notimpl()

class Falloff(object):
    def fall_Bounds(self):
        lx.notimpl()
    def fall_WeightF(self,position,point,polygon):
        lx.notimpl()
    # WeightRun skipped
    def fall_SetMesh(self,mesh):
        lx.notimpl()

class Deformation(object):
    def deform_Flags(self):
        return 0
    def deform_Transform(self):
        lx.notimpl()
    def deform_OffsetF(self,position,weight):
        lx.notimpl()
    def deform_OBSOLETE(self):
        lx.notimpl()
    # OffsetRun skipped

lx.bless(ItemInfluence,":ItemInfluence")
lx.bless(Deformer,":Deformer")
lx.bless(MeshInfluence,":MeshInfluence")
lx.bless(WeightMapDeformerItem,":WeightMapDeformerItem")
lx.bless(Falloff,":Falloff")
lx.bless(Deformation,":Deformation")

class DirCacheFileMetrics(object):
    def dcfilemetrics_Metadata(self):
        lx.notimpl()
    def dcfilemetrics_Markup(self):
        lx.notimpl()
    def dcfilemetrics_Flags(self):
        lx.notimpl()

class DirCacheSynthetic(object):
    def dcsyn_Lookup(self,path):
        lx.notimpl()
    def dcsyn_Root(self):
        lx.notimpl()

class DirCacheSyntheticEntry(object):
    def dcsyne_Path(self):
        lx.notimpl()
    def dcsyne_Name(self):
        lx.notimpl()
    def dcsyne_DirUsername(self):
        lx.notimpl()
    def dcsyne_FileExtension(self):
        lx.notimpl()
    def dcsyne_IsFile(self):
        lx.notimpl()
    def dcsyne_DirBuild(self):
        lx.notimpl()
    def dcsyne_DirCount(self,listMode):
        lx.notimpl()
    def dcsyne_DirByIndex(self,listMode,index):
        lx.notimpl()
    def dcsyne_ModTime(self):
        lx.notimpl()
    def dcsyne_Size(self):
        lx.notimpl()

class DirEntryThumbAsync(object):
    def detasync_Ready(self,dirCacheEntry,idealW,idealH,image):
        lx.notimpl()
    def detasync_Failed(self,dirCacheEntry):
        lx.notimpl()
    def detasync_Ident(self):
        lx.notimpl()

lx.bless(DirCacheFileMetrics,":DirCacheFileMetrics")
lx.bless(DirCacheSynthetic,":DirCacheSynthetic")
lx.bless(DirCacheSyntheticEntry,":DirCacheSyntheticEntry")
lx.bless(DirEntryThumbAsync,":DirEntryThumbAsync")


class DrawingOverride(object):
    def drov_Flags(self):
        lx.notimpl()
    def drov_AffectedItems(self,scene,collection):
        lx.notimpl()
    def drov_SetItem(self,item):
        lx.notimpl()
    # GetColor skipped
    def drov_InitContext(self):
        lx.notimpl()
    def drov_CleanupContext(self):
        lx.notimpl()
    def drov_DrawVisitor(self,scene,view):
        lx.notimpl()

lx.bless(DrawingOverride,":DrawingOverride")

class Drop(object):
    def drop_Recognize(self,source):
        lx.notimpl()
    def drop_ActionList(self,source,dest,addDropAction):
        lx.notimpl()
    def drop_Preview(self,source,dest,action,draw):
        lx.notimpl()
    def drop_Drop(self,source,dest,action):
        lx.notimpl()

lx.bless(Drop,":Drop")

class GradientFilter(object):
    def grfilt_Type(self):
        lx.notimpl()
    def grfilt_Generate(self,time):
        return 0
    def grfilt_Evaluate(self,time,value):
        return 0
    def grfilt_MultiSample(self,time,other):
        return 0

lx.bless(GradientFilter,":GradientFilter")

class ExternalRenderNotifier(object):
    # Notify skipped
    def ntf_SetStatusText(self,text):
        lx.notimpl()

class ExternalRender(object):
    def rend_Start(self):
        lx.notimpl()
    def rend_Stop(self):
        lx.notimpl()
    def rend_Pause(self):
        lx.notimpl()
    def rend_Reset(self):
        lx.notimpl()
    # SelectedPixelAt skipped
    def rend_SetNotifier(self,notifier):
        lx.notimpl()
    def rend_SetBufferQueue(self,bufferQueue):
        lx.notimpl()

lx.bless(ExternalRenderNotifier,":ExternalRenderNotifier")
lx.bless(ExternalRender,":ExternalRender")

class VirtualDevice(object):
    def vdev_Initialize(self,path):
        lx.notimpl()
    def vdev_Select(self,sub):
        lx.notimpl()
    def vdev_Extract(self,dest):
        lx.notimpl()
    def vdev_Scan(self,visitor):
        lx.notimpl()
    def vdev_Type(self):
        lx.notimpl()
    def vdev_Name(self):
        lx.notimpl()
    def vdev_Date(self):
        lx.notimpl()
    def vdev_Size(self):
        lx.notimpl()

lx.bless(VirtualDevice,":VirtualDevice")

class StackFilter(object):
    def filt_Type(self):
        lx.notimpl()
    def filt_Compare(self,other):
        return lx.symbol.iSTACK_DIFFERENT
    def filt_Convert(self,other):
        lx.notimpl()
    def filt_Identifier(self):
        lx.notimpl()

class CacheData(object):
    def cache_Size(self):
        lx.notimpl()

lx.bless(StackFilter,":StackFilter")
lx.bless(CacheData,":CacheData")

class Force(object):
    def force_Flags(self):
        return 0
    def force_Force(self,pos):
        lx.notimpl()
    def force_ForceV(self,pos,velocity):
        lx.notimpl()
    def force_ForceM(self,pos,mass):
        lx.notimpl()
    def force_ForceVM(self,pos,velocity,mass):
        lx.notimpl()
    # ForceRun skipped
    # ForceRunAng skipped

lx.bless(Force,":Force")



class GroupDest(object):
    def grpd_Group(self):
        lx.notimpl()
    def grpd_Location(self):
        lx.notimpl()

class GroupMemberChanDest(object):
    def grpmcd_Group(self):
        lx.notimpl()
    def grpmcd_Channel(self):
        lx.notimpl()
    def grpmcd_Location(self):
        lx.notimpl()

class GroupMemberItemDest(object):
    def grpmid_Group(self):
        lx.notimpl()
    def grpmid_Item(self):
        lx.notimpl()
    def grpmid_Location(self):
        lx.notimpl()

lx.bless(GroupDest,":GroupDest")
lx.bless(GroupMemberChanDest,":GroupMemberChanDest")
lx.bless(GroupMemberItemDest,":GroupMemberItemDest")



class Movie(object):
    def mov_BeginMovie(self,fname,w,h,flags):
        lx.notimpl()
    def mov_SetFramerate(self,frate):
        lx.notimpl()
    def mov_AddImage(self,image):
        lx.notimpl()
    def mov_EndMovie(self):
        lx.notimpl()
    def mov_AddAudio(self,audio):
        lx.notimpl()

class ImageFilter(object):
    def imf_Type(self):
        lx.notimpl()
    def imf_Generate(self,width,height,monitor):
        lx.notimpl()
    def imf_MultiSample(self,monitor,image):
        lx.notimpl()
    def imf_SingleSample(self,src):
        lx.notimpl()
    def imf_SingleSampleN(self,src,num):
        lx.notimpl()

class TileImage(object):
    def tileimg_LevelCount(self):
        lx.notimpl()
    def tileimg_GetTile(self,level,tileX,tileY):
        lx.notimpl()
    def tileimg_GetTileSize(self,level,tileX,tileY):
        lx.notimpl()
    def tileimg_GetLevelSize(self,level):
        lx.notimpl()
    def tileimg_DetermineTile(self,level,x,y):
        lx.notimpl()
    def tileimg_DeterminePixel(self,level,x,y):
        lx.notimpl()

class LayeredImageWrite(object):
    def limgw_AddLayer(self,image,name):
        lx.notimpl()
    def limgw_SetType(self,index,flags,type):
        lx.notimpl()
    def limgw_SetOffset(self,index,x,y):
        lx.notimpl()
    def limgw_SetBlending(self,index,blend,mode):
        lx.notimpl()
    def limgw_AddAttribute(self,name,type):
        lx.notimpl()

class ImageBlockCodec(object):
    # Compress skipped
    # Free skipped
    # Decompress skipped
    pass

class LayeredImage(object):
    def limg_Size(self):
        lx.notimpl()
    def limg_Count(self):
        lx.notimpl()
    def limg_Image(self,index):
        lx.notimpl()
    def limg_Name(self,index):
        lx.notimpl()
    def limg_Type(self,index):
        lx.notimpl()
    def limg_Offset(self,index):
        lx.notimpl()
    def limg_Blend(self,index):
        lx.notimpl()
    def limg_ChannelName(self,layerIndex,channelIndex):
        lx.notimpl()
    def limg_Parent(self,layerIndex):
        lx.notimpl()
    def limg_IsGroup(self,layerIndex):
        lx.notimpl()

class ImageFilterMetrics(object):
    # Generate skipped
    # Evaluate skipped
    pass

class Image(object):
    def img_Size(self):
        lx.notimpl()
    def img_Format(self):
        lx.notimpl()
    def img_GetPixel(self,x,y,type,pixel):
        lx.notimpl()
    def img_GetLine(self,y,type,buf):
        lx.notimpl()

class ImageWrite(object):
    def imgw_Size(self):
        lx.notimpl()
    def imgw_Format(self):
        lx.notimpl()
    def imgw_AddAttribute(self,name,type):
        lx.notimpl()
    def imgw_SetPixel(self,x,y,type,pixel):
        lx.notimpl()
    def imgw_SetLine(self,y,type,line):
        lx.notimpl()

class ImageLevelSample(object):
    def level_Count(self):
        lx.notimpl()
    def level_GetLevelSize(self,level):
        lx.notimpl()
    # SampleLevel skipped
    def level_GetPixel(self,level,x,y,type,pixel):
        lx.notimpl()
    def level_GetLine(self,level,y,buf):
        lx.notimpl()

class ImageSegment(object):
    def imgs_GetSegment(self,y,left,right,rgba):
        lx.notimpl()
    def imgs_SetSegment(self,y,left,right,type,line):
        lx.notimpl()

lx.bless(Movie,":Movie")
lx.bless(ImageFilter,":ImageFilter")
lx.bless(TileImage,":TileImage")
lx.bless(LayeredImageWrite,":LayeredImageWrite")
lx.bless(ImageBlockCodec,":ImageBlockCodec")
lx.bless(LayeredImage,":LayeredImage")
lx.bless(ImageFilterMetrics,":ImageFilterMetrics")
lx.bless(Image,":Image")
lx.bless(ImageWrite,":ImageWrite")
lx.bless(ImageLevelSample,":ImageLevelSample")
lx.bless(ImageSegment,":ImageSegment")

class ImageMonitor(object):
    def imon_Image(self,imageToAnalyze,frameBufferToAnalyze,bufferIndex,x1,y1,x2,y2,imageProcessingRead,processedThumbnail):
        lx.notimpl()
    def imon_ImageProcChanged(self):
        lx.notimpl()
    def imon_AspectRange(self):
        lx.notimpl()
    def imon_Draw(self,imageForDrawing):
        lx.notimpl()
    def imon_ImageSource(self,source):
        lx.notimpl()
    def imon_MouseDown(self,startx,starty,w,h):
        lx.notimpl()
    def imon_MouseMove(self,startx,starty,cx,cy,w,h):
        lx.notimpl()
    def imon_MouseUp(self,startx,starty,cx,cy,w,h):
        lx.notimpl()
    def imon_MouseTrackEnter(self):
        lx.notimpl()
    def imon_MouseTrack(self,cx,cy,w,h):
        lx.notimpl()
    def imon_MouseTrackExit(self):
        lx.notimpl()
    def imon_ToolTip(self,cx,cy,w,h):
        lx.notimpl()

lx.bless(ImageMonitor,":ImageMonitor")

class InputDevices(object):
    def indev_DeviceCount(self):
        return 0
    def indev_DeviceNameByIndex(self,index,name):
        lx.notimpl()
    def indev_DeviceInstanceByIndex(self,index):
        lx.notimpl()

class InputDeviceInstance(object):
    def indevinst_Name(self,name):
        lx.notimpl()
    def indevinst_IsConnected(self):
        lx.notimpl()
    def indevinst_ButtonCount(self):
        return 0
    def indevinst_ButtonName(self,index):
        lx.notimpl()
    def indevinst_ButtonUserName(self,index):
        lx.notimpl()
    def indevinst_ButtonIsDown(self,index):
        lx.notimpl()
    def indevinst_AnalogCount(self):
        return 0
    def indevinst_AnalogName(self,index):
        lx.notimpl()
    def indevinst_AnalogUserName(self,index):
        lx.notimpl()
    def indevinst_AnalogMetrics(self,index):
        lx.notimpl()
    def indevinst_AnalogValue(self,index):
        lx.notimpl()

lx.bless(InputDevices,":InputDevices")
lx.bless(InputDeviceInstance,":InputDeviceInstance")

class Interviewer(object):
    def intrv_Title(self):
        lx.notimpl()
    def intrv_Description(self):
        lx.notimpl()
    def intrv_ButtonLabel(self):
        lx.notimpl()
    def intrv_ButtonCommand(self):
        lx.notimpl()

lx.bless(Interviewer,":Interviewer")


class Saver(object):
    def sav_Verify(self,source,message):
        lx.notimpl()
    def sav_Save(self,source,filename,monitor):
        lx.notimpl()

class Monitor(object):
    def mon_Initialize(self,count):
        lx.notimpl()
    def mon_Increment(self,count):
        lx.notimpl()

class LoaderInfo(object):
    def linf_TestClass(self,clsGUID):
        lx.notimpl()
    def linf_SetClass(self,clsGUID):
        lx.notimpl()
    def linf_SetFlags(self,flags):
        lx.notimpl()
    def linf_SetFormat(self,format):
        lx.notimpl()

class StreamIO(object):
    def io_Write(self,stream):
        lx.notimpl()
    def io_Read(self,stream):
        lx.notimpl()

class Loader(object):
    def load_Recognize(self,filename,loadInfo):
        lx.notimpl()
    def load_LoadInstance(self,loadInfo,monitor):
        lx.notimpl()
    def load_LoadObject(self,loadInfo,monitor,dest):
        lx.notimpl()
    def load_Cleanup(self):
        lx.notimpl()
    def load_SpawnOptions(self):
        lx.notimpl()

lx.bless(Saver,":Saver")
lx.bless(Monitor,":Monitor")
lx.bless(LoaderInfo,":LoaderInfo")
lx.bless(StreamIO,":StreamIO")
lx.bless(Loader,":Loader")

class InstanceAssets(object):
    def instass_Count(self):
        lx.notimpl()
    def instass_IdentByIndex(self,index):
        lx.notimpl()
    def instass_Category(self,index):
        lx.notimpl()
    def instass_GetPath(self,ident):
        lx.notimpl()
    def instass_SetPath(self,ident,newPath):
        lx.notimpl()

class SceneSubset(object):
    def scnsub_GetScene(self):
        lx.notimpl()
    def scnsub_GetCollection(self):
        lx.notimpl()

lx.bless(InstanceAssets,":InstanceAssets")
lx.bless(SceneSubset,":SceneSubset")

class MeshOpDest(object):
    def locd_Item(self):
        lx.notimpl()
    def locd_ItemDeformer(self):
        lx.notimpl()
    # ItemHG skipped
    def locd_Graph(self):
        lx.notimpl()
    def locd_Location(self):
        lx.notimpl()

class MeshDest(object):
    def meshd_Item(self):
        lx.notimpl()
    def meshd_HitPosition(self):
        lx.notimpl()
    def meshd_HitNormal(self):
        lx.notimpl()

class ShaderDest(object):
    def locd_Item(self):
        lx.notimpl()
    def locd_Type(self):
        lx.notimpl()
    def locd_Location(self):
        lx.notimpl()

class ItemTypeDest(object):
    def ityped_Item(self):
        lx.notimpl()
    def ityped_Location(self):
        lx.notimpl()

class LocatorDest(object):
    def locd_Item(self):
        lx.notimpl()
    def locd_Location(self):
        lx.notimpl()

class ChannelDest(object):
    def chand_Channel(self):
        lx.notimpl()
    def chand_Location(self):
        lx.notimpl()

class ChannelDropPreview(object):
    def chandp_MarkChannel(self):
        lx.notimpl()

lx.bless(MeshOpDest,":MeshOpDest")
lx.bless(MeshDest,":MeshDest")
lx.bless(ShaderDest,":ShaderDest")
lx.bless(ItemTypeDest,":ItemTypeDest")
lx.bless(LocatorDest,":LocatorDest")
lx.bless(ChannelDest,":ChannelDest")
lx.bless(ChannelDropPreview,":ChannelDropPreview")


class ItemListType(object):
    def ilt_SetArgument(self,arg):
        lx.notimpl()
    def ilt_SetRootItem(self,item):
        lx.notimpl()
    def ilt_GenerateList(self,scene,collection):
        lx.notimpl()

lx.bless(ItemListType,":ItemListType")

class ListenerPort(object):
    def lport_AddListener(self,object):
        lx.notimpl()
    def lport_RemoveListener(self,object):
        lx.notimpl()

lx.bless(ListenerPort,":ListenerPort")


class LogInfoBlock(object):
    def lb_Name(self):
        lx.notimpl()
    def lb_FieldCount(self):
        lx.notimpl()
    def lb_FieldName(self,index):
        lx.notimpl()
    def lb_FieldType(self,index):
        lx.notimpl()

class LogListener(object):
    def logevent_SystemAdded(self,system):
        lx.notimpl()
    def logevent_EntryAdded(self,system,entry):
        lx.notimpl()
    def logevent_ChildEntryAdded(self,entry,parentEntry):
        lx.notimpl()
    def logevent_EntryDropped(self,system,entry):
        lx.notimpl()
    def logevent_RollingEntryAdded(self,system,entry):
        lx.notimpl()
    def logevent_RollingChildEntryAdded(self,entry,parentEntry):
        lx.notimpl()
    def logevent_RollingEntryDropped(self,system,entry):
        lx.notimpl()

lx.bless(LogInfoBlock,":LogInfoBlock")
lx.bless(LogListener,":LogListener")

class Audio(object):
    def audio_Channels(self):
        lx.notimpl()
    def audio_Type(self):
        lx.notimpl()
    def audio_Frequency(self):
        lx.notimpl()
    def audio_TrimStart(self):
        lx.notimpl()
    def audio_Duration(self):
        lx.notimpl()
    def audio_Filename(self):
        lx.notimpl()
    def audio_Size(self):
        lx.notimpl()
    def audio_Data(self):
        lx.notimpl()
    def audio_Sample(self,time,type,value):
        lx.notimpl()
    def audio_Seek(self,frame):
        lx.notimpl()
    def audio_Tell(self):
        lx.notimpl()
    def audio_Read(self,buff):
        lx.notimpl()
    # Metrics skipped

class AudioWrite(object):
    # WriteBegin skipped
    def audiow_Write(self,data):
        lx.notimpl()
    def audiow_WriteEnd(self):
        lx.notimpl()
    def audiow_SetSample(self,time,type,value):
        lx.notimpl()
    def audiow_SetStart(self,start):
        lx.notimpl()
    def audiow_SetDuration(self,duration):
        lx.notimpl()

lx.bless(Audio,":Audio")
lx.bless(AudioWrite,":AudioWrite")

class MeshOperation(object):
    def mop_Evaluate(self,mesh,type,mode):
        lx.notimpl()
    def mop_Compare(self,other):
        return lx.symbol.iMESHOP_DIFFERENT
    def mop_Convert(self,other):
        lx.notimpl()
    def mop_ReEvaluate(self,mesh,type):
        lx.notimpl()
    def mop_SetTransform(self,matrix):
        lx.notimpl()
    def mop_Blend(self,other,blend):
        lx.notimpl()
    def mop_Clone(self,target,source):
        lx.notimpl()

class MeshMetaData(object):
    def meta_Validate(self,mesh,xtra,change):
        lx.notimpl()
    def meta_FreePointData(self,data):
        lx.notimpl()
    def meta_FreePolygonData(self,data):
        lx.notimpl()

class MeshListener(object):
    def ml_Destroy(self):
        lx.notimpl()
    def ml_Changes(self,event):
        lx.notimpl()

class MeshFilterBBox(object):
    def mfbbox_Evaluate(self):
        lx.notimpl()

class MeshFilter(object):
    def mfilt_Type(self):
        lx.notimpl()
    def mfilt_Evaluate(self,mesh,tracker):
        lx.notimpl()
    def mfilt_Generate(self):
        lx.notimpl()

lx.bless(MeshOperation,":MeshOperation")
lx.bless(MeshMetaData,":MeshMetaData")
lx.bless(MeshListener,":MeshListener")
lx.bless(MeshFilterBBox,":MeshFilterBBox")
lx.bless(MeshFilter,":MeshFilter")

class AutoSaveListener(object):
    def asl_AutoSaveNow(self):
        lx.notimpl()

lx.bless(AutoSaveListener,":AutoSaveListener")


class Notifier(object):
    def noti_Name(self):
        lx.notimpl()
    def noti_SetArgs(self,args):
        lx.notimpl()
    def noti_Args(self):
        lx.notimpl()
    def noti_AddClient(self,object):
        lx.notimpl()
    def noti_RemoveClient(self,object):
        lx.notimpl()

lx.bless(Notifier,":Notifier")

class SceneItemListener(object):
    def sil_SceneCreate(self,scene):
        lx.notimpl()
    def sil_SceneDestroy(self,scene):
        lx.notimpl()
    def sil_SceneFilename(self,scene,filename):
        lx.notimpl()
    def sil_SceneClear(self,scene):
        lx.notimpl()
    def sil_ItemPreChange(self,scene):
        lx.notimpl()
    def sil_ItemPostDelete(self,scene):
        lx.notimpl()
    def sil_ItemAdd(self,item):
        lx.notimpl()
    def sil_ItemRemove(self,item):
        lx.notimpl()
    def sil_ItemParent(self,item):
        lx.notimpl()
    def sil_ItemChild(self,item):
        lx.notimpl()
    def sil_ItemAddChannel(self,item):
        lx.notimpl()
    def sil_ItemLocal(self,item):
        lx.notimpl()
    def sil_ItemName(self,item):
        lx.notimpl()
    def sil_ItemSource(self,item):
        lx.notimpl()
    def sil_ItemPackage(self,item):
        lx.notimpl()
    def sil_ChannelValue(self,action,item,index):
        lx.notimpl()
    def sil_LinkAdd(self,graph,itemFrom,itemTo):
        lx.notimpl()
    def sil_LinkRemBefore(self,graph,itemFrom,itemTo):
        lx.notimpl()
    def sil_LinkRemAfter(self,graph,itemFrom,itemTo):
        lx.notimpl()
    def sil_LinkSet(self,graph,itemFrom,itemTo):
        lx.notimpl()
    def sil_ChanLinkAdd(self,graph,itemFrom,chanFrom,itemTo,chanTo):
        lx.notimpl()
    def sil_ChanLinkRemBefore(self,graph,itemFrom,chanFrom,itemTo,chanTo):
        lx.notimpl()
    def sil_ChanLinkRemAfter(self,graph,itemFrom,chanFrom,itemTo,chanTo):
        lx.notimpl()
    def sil_ChanLinkSet(self,graph,itemFrom,chanFrom,itemTo,chanTo):
        lx.notimpl()
    def sil_ItemTag(self,item):
        lx.notimpl()
    def sil_ItemRemoveChannel(self,item):
        lx.notimpl()
    def sil_ItemChannelName(self,item,index):
        lx.notimpl()
    def sil_ItemChannelDefault(self,item,index):
        lx.notimpl()
    def sil_ItemChannelMinMax(self,item,index):
        lx.notimpl()
    def sil_ItemChannelType(self,item,index):
        lx.notimpl()

class SceneEvalListener(object):
    def sel_ChannelValue(self,item,index):
        lx.notimpl()
    def sel_ChannelPreValue(self):
        lx.notimpl()
    def sel_ChannelPostValue(self):
        lx.notimpl()

class AssemblyAlias(object):
    def alias_Test(self,assembly,other):
        lx.notimpl()
    # Configure skipped
    def alias_SuperType(self):
        lx.notimpl()
    def alias_Flags(self):
        lx.notimpl()

class PackageInstance(object):
    def pins_Initialize(self,item,super):
        lx.notimpl()
    def pins_Cleanup(self):
        lx.notimpl()
    def pins_SynthName(self):
        lx.notimpl()
    def pins_DupType(self):
        return 0
    def pins_TestParent(self,item):
        return True
    def pins_Newborn(self,original,flags):
        lx.notimpl()
    def pins_Loading(self):
        lx.notimpl()
    def pins_AfterLoad(self):
        lx.notimpl()
    def pins_Doomed(self):
        lx.notimpl()
    def pins_Add(self):
        lx.notimpl()
    def pins_Remove(self):
        lx.notimpl()

class Package(object):
    def pkg_SetupChannels(self,addChan):
        lx.notimpl()
    def pkg_Attach(self):
        lx.notimpl()
    def pkg_TestInterface(self,guid):
        return False
    def pkg_PostLoad(self,scene):
        lx.notimpl()
    def pkg_CollectItems(self,collection,mode):
        lx.notimpl()

lx.bless(SceneItemListener,":SceneItemListener")
lx.bless(SceneEvalListener,":SceneEvalListener")
lx.bless(AssemblyAlias,":AssemblyAlias")
lx.bless(PackageInstance,":PackageInstance")
lx.bless(Package,":Package")

class ParticleFilter(object):
    def pfilt_Vertex(self,full):
        lx.notimpl()
    def pfilt_Flags(self):
        lx.notimpl()
    def pfilt_Initialize(self,vertex,frame,time):
        lx.notimpl()
    def pfilt_Step(self,other,dt):
        lx.notimpl()
    def pfilt_Cleanup(self):
        lx.notimpl()
    def pfilt_Frame(self,stage):
        lx.notimpl()
    # Run skipped
    def pfilt_Particle(self,stage,vertex):
        lx.notimpl()

class ParticleItem(object):
    def prti_Prepare(self,eval):
        lx.notimpl()
    def prti_Evaluate(self,attr,index):
        lx.notimpl()

class PointCacheItem(object):
    def pcache_Prepare(self,eval):
        lx.notimpl()
    def pcache_Initialize(self,vdesc,attr,index,time,sample):
        lx.notimpl()
    def pcache_SaveFrame(self,pobj,time):
        lx.notimpl()
    def pcache_Cleanup(self):
        lx.notimpl()

class ParticleCoOperator(object):
    def pcoi_Initialize(self,eval):
        lx.notimpl()
    def pcoi_Cleanup(self):
        lx.notimpl()
    def pcoi_Step(self,dT):
        lx.notimpl()
    def pcoi_Particle(self):
        lx.notimpl()

lx.bless(ParticleFilter,":ParticleFilter")
lx.bless(ParticleItem,":ParticleItem")
lx.bless(PointCacheItem,":PointCacheItem")
lx.bless(ParticleCoOperator,":ParticleCoOperator")


class PersistenceClient(object):
    def cc_Setup(self):
        lx.notimpl()
    def cc_SyncRead(self):
        lx.notimpl()
    def cc_SyncWrite(self):
        lx.notimpl()

lx.bless(PersistenceClient,":PersistenceClient")

class SelectionOperation(object):
    def selop_SetMesh(self,mesh):
        lx.notimpl()
    def selop_SetTransform(self):
        lx.notimpl()
    def selop_TestPoint(self,point):
        lx.notimpl()
    def selop_TestEdge(self,edge):
        lx.notimpl()
    def selop_TestPolygon(self,polygon):
        lx.notimpl()
    def selop_Evaluate(self,type,state):
        lx.notimpl()

class MeshElementGroup(object):
    def eltgrp_GroupCount(self):
        lx.notimpl()
    def eltgrp_GroupName(self,index):
        lx.notimpl()
    def eltgrp_GroupUserName(self,index):
        lx.notimpl()
    def eltgrp_TestPoint(self,index,point):
        lx.notimpl()
    def eltgrp_TestEdge(self,index,edge):
        lx.notimpl()
    def eltgrp_TestPolygon(self,index,polygon):
        lx.notimpl()

lx.bless(SelectionOperation,":SelectionOperation")
lx.bless(MeshElementGroup,":MeshElementGroup")

class Subdivision(object):
    def subdiv_Validate(self,mesh):
        lx.notimpl()
    def subdiv_Refine(self,mesh):
        lx.notimpl()
    def subdiv_InvalidateTopology(self):
        lx.notimpl()
    def subdiv_InvalidatePosition(self):
        lx.notimpl()
    def subdiv_Status(self):
        lx.notimpl()
    def subdiv_MaxLevel(self):
        lx.notimpl()
    def subdiv_SetMaxLevel(self,level):
        lx.notimpl()
    def subdiv_BoundaryRule(self):
        lx.notimpl()
    def subdiv_SetBoundaryRule(self,bound):
        lx.notimpl()
    def subdiv_UVBoundaryRule(self):
        lx.notimpl()
    def subdiv_SetUVBoundaryRule(self,bound):
        lx.notimpl()
    def subdiv_Scheme(self):
        lx.notimpl()
    def subdiv_SetScheme(self,scheme):
        lx.notimpl()
    def subdiv_Backend(self):
        lx.notimpl()
    def subdiv_SetBackend(self,backend):
        lx.notimpl()
    def subdiv_Adaptive(self):
        lx.notimpl()
    def subdiv_SetAdaptive(self,adaptive):
        lx.notimpl()
    def subdiv_NumFaces(self):
        lx.notimpl()
    def subdiv_FaceDepth(self,faceIndex):
        lx.notimpl()
    def subdiv_NumVerticesOfFace(self,faceIndex):
        lx.notimpl()
    def subdiv_VertexOfFace(self,faceIndex,vertofface):
        lx.notimpl()
    def subdiv_NumLevelFaces(self,level):
        lx.notimpl()
    def subdiv_FirstFaceOffset(self,level):
        lx.notimpl()
    def subdiv_ChildFace(self,faceIndex,vertOfFace):
        lx.notimpl()
    def subdiv_ParentFace(self,faceIndex):
        lx.notimpl()
    # PolygonID skipped
    # PolygonFace skipped
    def subdiv_NumVertices(self):
        lx.notimpl()
    def subdiv_NumLevelVertices(self,level):
        lx.notimpl()
    def subdiv_FirstVertexOffset(self,level):
        lx.notimpl()
    def subdiv_ParentVertex(self,vertIndex):
        lx.notimpl()
    def subdiv_VertexPosition(self,vertIndex):
        lx.notimpl()
    def subdiv_VertexNormal(self,vertIndex):
        lx.notimpl()
    def subdiv_AddUVMap(self,name):
        lx.notimpl()
    def subdiv_NumUVMap(self):
        lx.notimpl()
    def subdiv_UVMapName(self,mapIndex):
        lx.notimpl()
    def subdiv_LookupUVMap(self,name):
        lx.notimpl()
    def subdiv_GetUV(self,mapIndex,faceIndex,vertOfFace):
        lx.notimpl()

lx.bless(Subdivision,":Subdivision")

class ColorPreDest(object):
    def colpd_SetColor(self,rgb):
        lx.notimpl()
    def colpd_SetColorModel(self,name,vec):
        lx.notimpl()
    def colpd_Apply(self):
        lx.notimpl()

class Profile2DPreDest(object):
    def p2pd_MoveTo(self,x,y):
        lx.notimpl()
    def p2pd_LineTo(self,x,y):
        lx.notimpl()
    def p2pd_CurveTo(self,x0,y0,x1,y1,x2,y2):
        lx.notimpl()
    def p2pd_NewPath(self):
        lx.notimpl()
    def p2pd_Closed(self,closed):
        lx.notimpl()
    def p2pd_Box(self):
        lx.notimpl()
    def p2pd_Count(self):
        lx.notimpl()
    def p2pd_SelectByIndex(self,index):
        lx.notimpl()

class Profile1DPreDest(object):
    def p1pd_MoveTo(self,x,y):
        lx.notimpl()
    def p1pd_LineTo(self,x,y):
        lx.notimpl()
    def p1pd_CurveTo(self,x0,y0,x1,y1,x2,y2):
        lx.notimpl()
    def p1pd_Evaluate(self,t,flags,axis):
        lx.notimpl()
    def p1pd_PathSteps(self,tol,flags,x,y,nstep):
        lx.notimpl()
    def p1pd_Box(self):
        lx.notimpl()
    def p1pd_Count(self):
        lx.notimpl()
    def p1pd_SelectByIndex(self,index):
        lx.notimpl()
    def p1pd_SelectByParameter(self,t):
        lx.notimpl()
    # SelectByVertex skipped

class ShaderPreDest(object):
    def spd_Scene(self):
        lx.notimpl()
    def spd_Item(self):
        lx.notimpl()
    def spd_ContainerItem(self):
        lx.notimpl()
    def spd_HitItem(self):
        lx.notimpl()
    def spd_GetTag(self,type):
        lx.notimpl()
    def spd_Mode(self):
        lx.notimpl()

class SceneItemPreDest(object):
    def sipd_Scene(self):
        lx.notimpl()
    def sipd_Item(self):
        lx.notimpl()
    def sipd_ContainerItem(self):
        lx.notimpl()
    def sipd_Position(self):
        lx.notimpl()
    def sipd_Orientation(self):
        lx.notimpl()

class MeshLayerPreDest(object):
    def mlpd_Mesh(self):
        lx.notimpl()
    def mlpd_Transform(self):
        lx.notimpl()
    def mlpd_ShaderDest(self):
        lx.notimpl()

lx.bless(ColorPreDest,":ColorPreDest")
lx.bless(Profile2DPreDest,":Profile2DPreDest")
lx.bless(Profile1DPreDest,":Profile1DPreDest")
lx.bless(ShaderPreDest,":ShaderPreDest")
lx.bless(SceneItemPreDest,":SceneItemPreDest")
lx.bless(MeshLayerPreDest,":MeshLayerPreDest")

class PresetDo(object):
    def pdo_Test(self,path):
        lx.notimpl()
    def pdo_Do(self,path):
        lx.notimpl()

class PresetType(object):
    def ptyp_Recognize(self,path):
        lx.notimpl()
    def ptyp_Apply(self,path,destination):
        lx.notimpl()
    def ptyp_Do(self,path):
        lx.notimpl()
    def ptyp_DoCommandFlags(self,path):
        lx.notimpl()
    def ptyp_Metrics(self,path,flags,w,h,prevMetrics):
        lx.notimpl()
    def ptyp_GenericThumbnailResource(self,path):
        lx.notimpl()
    def ptyp_BaseAspect(self):
        lx.notimpl()
    def ptyp_StoreThumbnail(self,path,image):
        lx.notimpl()
    def ptyp_DefaultThumbnail(self,path):
        lx.notimpl()
    def ptyp_StoreMarkup(self,path,attr):
        lx.notimpl()

class PresetMetrics(object):
    def pmet_ThumbnailImage(self):
        lx.notimpl()
    def pmet_ThumbnailIdealSize(self):
        lx.notimpl()
    def pmet_ThumbnailResource(self):
        lx.notimpl()
    def pmet_Metadata(self):
        lx.notimpl()
    def pmet_Markup(self):
        lx.notimpl()
    def pmet_Flags(self):
        lx.notimpl()

lx.bless(PresetDo,":PresetDo")
lx.bless(PresetType,":PresetType")
lx.bless(PresetMetrics,":PresetMetrics")

class PreviewNotifier(object):
    # Notify skipped
    pass

lx.bless(PreviewNotifier,":PreviewNotifier")

class ProjDirOverride(object):
    def pdo_OverrideWith(self,originalPath):
        lx.notimpl()

lx.bless(ProjDirOverride,":ProjDirOverride")





class RenderCacheListener(object):
    def rli_RenderCacheDestroy(self):
        lx.notimpl()
    def rli_UpdateBegin(self):
        lx.notimpl()
    def rli_UpdateEnd(self):
        lx.notimpl()
    def rli_GeoCacheSurfaceAdd(self,geoSrf):
        lx.notimpl()
    def rli_GeoCacheSurfaceRemove(self,geoSrf):
        lx.notimpl()
    def rli_GeoCacheSurfaceGeoUpdate(self,geoSrf):
        lx.notimpl()
    def rli_GeoCacheSurfaceXformUpdate(self,geoSrf):
        lx.notimpl()
    def rli_GeoCacheSurfaceShaderUpdate(self,geoSrf):
        lx.notimpl()
    def rli_RenderCacheClear(self):
        lx.notimpl()

lx.bless(RenderCacheListener,":RenderCacheListener")


class FrameBuffer(object):
    # Allocate skipped
    def fbuf_IsStereo(self):
        lx.notimpl()
    def fbuf_GetStereoEyeDisplay(self):
        lx.notimpl()
    def fbuf_SetStereoEyeDisplay(self,eyeDisplay):
        lx.notimpl()
    def fbuf_GetStereoComposite(self):
        lx.notimpl()
    def fbuf_SetStereoComposite(self,composite):
        lx.notimpl()
    def fbuf_SetEyeSide(self,eyeSide):
        lx.notimpl()
    # GetLineBuffer skipped
    def fbuf_CreateFrameBufferTargetImage(self,type,w,h):
        lx.notimpl()
    def fbuf_GetRenderPassName(self,name):
        lx.notimpl()
    def fbuf_SetRenderPassName(self,name):
        lx.notimpl()
    def fbuf_BucketsOnDisk(self,index):
        lx.notimpl()
    def fbuf_Lookup(self,name,item):
        lx.notimpl()
    def fbuf_LookupByIdentity(self,identity):
        lx.notimpl()
    def fbuf_Count(self):
        lx.notimpl()
    def fbuf_ByIndex(self,index):
        lx.notimpl()
    def fbuf_Alpha(self,index):
        lx.notimpl()
    def fbuf_AlphaIndex(self,index):
        lx.notimpl()
    def fbuf_Size(self,index):
        lx.notimpl()
    def fbuf_AreaProcessingActive(self,bufferIndex):
        lx.notimpl()
    def fbuf_GetSaveProcessed(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetSaveProcessed(self,bufferIndex,enabled):
        lx.notimpl()
    def fbuf_GetBloomEnabled(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetBloomEnabled(self,bufferIndex,enabled):
        lx.notimpl()
    def fbuf_GetBloomThreshold(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetBloomThreshold(self,bufferIndex,threshold):
        lx.notimpl()
    def fbuf_GetBloomRadius(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetBloomRadius(self,bufferIndex,radius):
        lx.notimpl()
    def fbuf_GetVignetteAmount(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetVignetteAmount(self,bufferIndex,radius):
        lx.notimpl()
    def fbuf_GetInputBlackLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetInputBlackLevel(self,bufferIndex,blackLevel):
        lx.notimpl()
    def fbuf_GetInputGrayLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_GetInvInputGrayLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetInputGrayLevel(self,bufferIndex,gamma):
        lx.notimpl()
    def fbuf_GetInputWhiteLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetInputWhiteLevel(self,bufferIndex,whiteLevel):
        lx.notimpl()
    def fbuf_GetInputMinRedLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetInputMinRedLevel(self,bufferIndex,level):
        lx.notimpl()
    def fbuf_GetInputRedGrayLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_GetInvInputRedGrayLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetInputRedGrayLevel(self,bufferIndex,gamma):
        lx.notimpl()
    def fbuf_GetInputMaxRedLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetInputMaxRedLevel(self,bufferIndex,level):
        lx.notimpl()
    def fbuf_GetInputMinGreenLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetInputMinGreenLevel(self,bufferIndex,level):
        lx.notimpl()
    def fbuf_GetInputGreenGrayLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_GetInvInputGreenGrayLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetInputGreenGrayLevel(self,bufferIndex,gamma):
        lx.notimpl()
    def fbuf_GetInputMaxGreenLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetInputMaxGreenLevel(self,bufferIndex,level):
        lx.notimpl()
    def fbuf_GetInputMinBlueLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetInputMinBlueLevel(self,bufferIndex,level):
        lx.notimpl()
    def fbuf_GetInputBlueGrayLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_GetInvInputBlueGrayLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetInputBlueGrayLevel(self,bufferIndex,gamma):
        lx.notimpl()
    def fbuf_GetInputMaxBlueLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetInputMaxBlueLevel(self,bufferIndex,level):
        lx.notimpl()
    def fbuf_GetExpType(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetExpType(self,bufferIndex,expType):
        lx.notimpl()
    def fbuf_GetISO(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetISO(self,bufferIndex,iso):
        lx.notimpl()
    def fbuf_GetToneMap(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetToneMap(self,bufferIndex,toneMap):
        lx.notimpl()
    def fbuf_GetToneAmt(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetToneAmt(self,bufferIndex,toneAmt):
        lx.notimpl()
    def fbuf_GetHueOffset(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetHueOffset(self,bufferIndex,hueOffset):
        lx.notimpl()
    def fbuf_GetSaturation(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetSaturation(self,bufferIndex,saturation):
        lx.notimpl()
    def fbuf_GetColorization(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetColorization(self,bufferIndex,colorization):
        lx.notimpl()
    def fbuf_GetTargetColor(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetTargetColor(self,bufferIndex,color):
        lx.notimpl()
    def fbuf_GetOutputBlackLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetOutputBlackLevel(self,bufferIndex,blackLevel):
        lx.notimpl()
    def fbuf_GetOutputWhiteLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetOutputWhiteLevel(self,bufferIndex,whiteLevel):
        lx.notimpl()
    def fbuf_GetOutputMinRedLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetOutputMinRedLevel(self,bufferIndex,blackLevel):
        lx.notimpl()
    def fbuf_GetOutputMaxRedLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetOutputMaxRedLevel(self,bufferIndex,whiteLevel):
        lx.notimpl()
    def fbuf_GetOutputMinGreenLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetOutputMinGreenLevel(self,bufferIndex,blackLevel):
        lx.notimpl()
    def fbuf_GetOutputMaxGreenLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetOutputMaxGreenLevel(self,bufferIndex,whiteLevel):
        lx.notimpl()
    def fbuf_GetOutputMinBlueLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetOutputMinBlueLevel(self,bufferIndex,blackLevel):
        lx.notimpl()
    def fbuf_GetOutputMaxBlueLevel(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetOutputMaxBlueLevel(self,bufferIndex,whiteLevel):
        lx.notimpl()
    def fbuf_GetOutputGamma(self,bufferIndex):
        lx.notimpl()
    def fbuf_GetOutputInvGamma(self,bufferIndex):
        lx.notimpl()
    def fbuf_SetOutputGamma(self,bufferIndex,gamma):
        lx.notimpl()
    def fbuf_GetOutputColorspace(self):
        lx.notimpl()
    def fbuf_SetOutputColorspace(self,colorspace):
        lx.notimpl()
    # GetOutputColormapping skipped
    def fbuf_SetOutputColormapping(self,colormapping):
        lx.notimpl()
    def fbuf_AddAttribute(self,name,type):
        lx.notimpl()
    # RenderProcessAllocate skipped
    # RenderProcessDeallocate skipped

class RenderProgressListener(object):
    def rndprog_Begin(self):
        lx.notimpl()
    def rndprog_End(self,stats):
        lx.notimpl()

class RenderJob(object):
    def rjob_RenderItem(self):
        lx.notimpl()
    def rjob_ActionName(self):
        lx.notimpl()
    def rjob_GroupName(self):
        lx.notimpl()
    def rjob_RenderAs(self):
        lx.notimpl()
    def rjob_RenderAtTime(self):
        lx.notimpl()
    def rjob_RenderTurntableNumFrames(self):
        lx.notimpl()
    def rjob_RenderTurntableFPS(self):
        lx.notimpl()
    def rjob_RenderBakeVMap(self):
        lx.notimpl()
    def rjob_RenderBakeLookDistance(self):
        lx.notimpl()
    # RenderBakeItem skipped
    def rjob_RenderBakeEffect(self):
        lx.notimpl()
    def rjob_RenderBakeImage(self):
        lx.notimpl()
    def rjob_TestItem(self,item,eval):
        lx.notimpl()
    def rjob_FrameBufferSlot(self):
        lx.notimpl()
    def rjob_FrameBufferRegionBackgroundSlot(self):
        lx.notimpl()
    def rjob_OutputFormat(self):
        lx.notimpl()
    def rjob_OutputFilename(self):
        lx.notimpl()
    def rjob_Options(self):
        lx.notimpl()
    def rjob_ProgressAborted(self):
        lx.notimpl()
    def rjob_ProgressBegin(self,renderStats):
        lx.notimpl()
    def rjob_ProgressEnd(self,finalFrameBuffer,finalStats):
        lx.notimpl()
    def rjob_ProgressPercentDone(self,progressScene,progressFrame,progressRenderPass):
        lx.notimpl()
    def rjob_ProgressImageMetrics(self,resX,resH):
        lx.notimpl()
    def rjob_ProgressFrameBegin(self,frame,w,h):
        lx.notimpl()
    def rjob_ProgressFrameEnd(self,frame,stats):
        lx.notimpl()
    def rjob_ProgressRenderPassBegin(self,frameIndex,renderPassIndex,renderPassName,eye):
        lx.notimpl()
    def rjob_ProgressRenderPassEnd(self,frame,renderPassIndex,renderPassName,eye,frameBuffer,stats):
        lx.notimpl()
    def rjob_ProgressFramePassBegin(self,frame,renderPass,eye,pass_int):
        lx.notimpl()
    def rjob_ProgressFramePassEnd(self,frame,renderPass,eye,pass_int):
        lx.notimpl()
    def rjob_ProgressBucketBegin(self,row,col):
        lx.notimpl()
    def rjob_ProgressBucketEnd(self,row,col,code):
        lx.notimpl()
    def rjob_ProgressString(self,infoString,userString):
        lx.notimpl()
    def rjob_ProgressImage(self,img):
        lx.notimpl()
    def rjob_ProgressImageUpdated(self):
        lx.notimpl()
    def rjob_ProgressTickle(self):
        lx.notimpl()
    def rjob_RenderBakeCageVMap(self):
        lx.notimpl()
    # BakeItem skipped
    def rjob_UDIM(self):
        lx.notimpl()
    def rjob_RenderBakeToRGBA(self):
        lx.notimpl()
    def rjob_RenderBakeFromRGBA(self):
        lx.notimpl()

class ImageProcessingListener(object):
    def improl_Changed(self,identifier,eventCode):
        lx.notimpl()
    def improl_Reset(self,identifier):
        lx.notimpl()

class Buffer(object):
    def buff_SetFlags(self,flags):
        lx.notimpl()
    def buff_Flags(self):
        lx.notimpl()
    def buff_DataType(self):
        lx.notimpl()
    def buff_VectorType(self):
        lx.notimpl()
    def buff_SetSize(self,width,height,writeBucketsToDisk,isStereo):
        lx.notimpl()
    def buff_GetSize(self):
        lx.notimpl()
    def buff_SetEyeSide(self,eyeSide):
        lx.notimpl()
    def buff_Clear(self,x,y):
        lx.notimpl()
    # Convert skipped
    def buff_Pixel(self,x,y):
        lx.notimpl()
    def buff_Line(self,y):
        lx.notimpl()
    def buff_Name(self):
        lx.notimpl()
    def buff_SetUserName(self,name):
        lx.notimpl()
    def buff_UserName(self):
        lx.notimpl()
    def buff_CreateImageTileTree(self):
        lx.notimpl()
    def buff_DestroyImageTileTree(self):
        lx.notimpl()
    def buff_GetImageTileTree(self):
        lx.notimpl()
    # GetImageTileTreeSize skipped
    def buff_ResetImageTileTree(self):
        lx.notimpl()
    def buff_IncrementTileTreeSize(self):
        lx.notimpl()
    def buff_DecrementTileTreeSize(self):
        lx.notimpl()

lx.bless(FrameBuffer,":FrameBuffer")
lx.bless(RenderProgressListener,":RenderProgressListener")
lx.bless(RenderJob,":RenderJob")
lx.bless(ImageProcessingListener,":ImageProcessingListener")
lx.bless(Buffer,":Buffer")

class SchematicConnection(object):
    def schm_ItemFlags(self,item):
        lx.notimpl()
    def schm_AllowConnect(self,from_obj,to_obj):
        lx.notimpl()
    def schm_AllowConnectType(self,to_obj,type):
        lx.notimpl()
    def schm_GraphName(self):
        lx.notimpl()
    def schm_Count(self,item):
        lx.notimpl()
    def schm_ByIndex(self,item,index):
        lx.notimpl()
    def schm_Connect(self,from_obj,to_obj,toIndex):
        lx.notimpl()
    def schm_Disconnect(self,from_obj,to_obj):
        lx.notimpl()
    def schm_BaseFlags(self):
        return 0
    def schm_PerItemFlags(self,item):
        lx.notimpl()
    def schm_ItemFlagsValid(self):
        return 1
    def schm_ChannelAllowConnect(self,from_obj,fromIndex,to_obj,toIndex):
        lx.notimpl()
    def schm_ChannelIOType(self):
        lx.notimpl()
    def schm_ChannelCount(self,xItem,fromIndex):
        lx.notimpl()
    def schm_ChannelByIndex(self,xItem,fromIndex,index):
        lx.notimpl()
    def schm_ChannelConnect(self,from_obj,fromIndex,to_obj,toIndex):
        lx.notimpl()
    def schm_ChannelDisconnect(self,from_obj,fromIndex,to_obj,toIndex):
        lx.notimpl()

class SchemaDest(object):
    def schmd_ViewType(self):
        lx.notimpl()
    def schmd_Position(self):
        lx.notimpl()
    def schmd_Group(self):
        lx.notimpl()
    def schmd_Item(self):
        lx.notimpl()
    def schmd_Node(self):
        lx.notimpl()
    def schmd_Channel(self):
        lx.notimpl()
    def schmd_Graph(self):
        lx.notimpl()
    def schmd_Link(self):
        lx.notimpl()

lx.bless(SchematicConnection,":SchematicConnection")
lx.bless(SchemaDest,":SchemaDest")

class UserValueListener(object):
    def uvl_Added(self,userValue):
        lx.notimpl()
    def uvl_Deleted(self,name):
        lx.notimpl()
    def uvl_DefChanged(self,userValue):
        lx.notimpl()
    def uvl_ValueChanged(self,userValue):
        lx.notimpl()

class LineInterpreter(object):
    def lin_Flags(self):
        lx.notimpl()
    def lin_Prompt(self,type):
        lx.notimpl()
    def lin_Execute(self,line,execFlags,execution):
        lx.notimpl()

class ScriptManager(object):
    def scman_Name(self):
        lx.notimpl()
    def scman_Flags(self):
        lx.notimpl()
    def scman_Count(self):
        lx.notimpl()
    def scman_ByIndex(self,index,write):
        lx.notimpl()
    def scman_Lookup(self,hash,write,tryAsUserName):
        lx.notimpl()
    def scman_ReadWrite(self,hash,index):
        lx.notimpl()
    def scman_New(self,name):
        lx.notimpl()
    def scman_Remove(self,script):
        lx.notimpl()
    def scman_Validate(self,script,msg):
        lx.notimpl()
    def scman_Run(self,script,execFlags,args,msg):
        lx.notimpl()

class Script(object):
    def scr_Hash(self):
        lx.notimpl()
    def scr_UserName(self):
        lx.notimpl()
    def scr_SetUserName(self,userName):
        lx.notimpl()
    def scr_Desc(self):
        lx.notimpl()
    def scr_SetDesc(self,desc):
        lx.notimpl()
    def scr_Icon(self):
        lx.notimpl()
    def scr_HelpKey(self,args):
        lx.notimpl()
    def scr_Manager(self):
        lx.notimpl()
    def scr_GetBuffer(self):
        lx.notimpl()
    def scr_SetBuffer(self,buffer,bufferLength):
        lx.notimpl()

class TextScriptInterpreter(object):
    def tsi_ValidateFileType(self,script,firstLine):
        lx.notimpl()
    def tsi_Validate(self,script,msg):
        lx.notimpl()
    def tsi_Run(self,script,execFlags,args,msg):
        lx.notimpl()

class AppActiveListener(object):
    def activeevent_IsNowActive(self,isActive):
        lx.notimpl()

class LineExecution(object):
    def lin_CookedLine(self,text):
        lx.notimpl()
    def lin_Message(self,message):
        lx.notimpl()
    def lin_Results(self,valArray):
        lx.notimpl()
    def lin_ResultHints(self,hints):
        lx.notimpl()
    def lin_Info(self,text):
        lx.notimpl()

class SessionListener(object):
    def sesl_FirstWindowOpening(self):
        lx.notimpl()
    def sesl_BeforeStartupCommands(self):
        lx.notimpl()
    def sesl_SystemReady(self):
        lx.notimpl()
    def sesl_CheckQuitUI(self,quitWasAborted):
        lx.notimpl()
    def sesl_QuittingUI(self):
        lx.notimpl()
    def sesl_LastWindowClosed(self):
        lx.notimpl()
    def sesl_ShuttingDown(self):
        lx.notimpl()

class ScriptLineEvent(object):
    def slev_Index(self):
        lx.notimpl()
    def slev_Script(self):
        lx.notimpl()

lx.bless(UserValueListener,":UserValueListener")
lx.bless(LineInterpreter,":LineInterpreter")
lx.bless(ScriptManager,":ScriptManager")
lx.bless(Script,":Script")
lx.bless(TextScriptInterpreter,":TextScriptInterpreter")
lx.bless(AppActiveListener,":AppActiveListener")
lx.bless(LineExecution,":LineExecution")
lx.bless(SessionListener,":SessionListener")
lx.bless(ScriptLineEvent,":ScriptLineEvent")

class SelectionType(object):
    def seltyp_Size(self):
        lx.notimpl()
    def seltyp_Flags(self):
        lx.notimpl()
    def seltyp_MessageTable(self):
        lx.notimpl()
    def seltyp_Compare(self,pkey,pelt):
        lx.notimpl()
    def seltyp_SubType(self,pkt):
        return 0

class SelectionListener(object):
    def selevent_Current(self,type):
        lx.notimpl()
    def selevent_Add(self,type,subtType):
        lx.notimpl()
    def selevent_Remove(self,type,subtType):
        lx.notimpl()
    def selevent_Time(self,time):
        lx.notimpl()
    def selevent_TimeRange(self,type):
        lx.notimpl()

lx.bless(SelectionType,":SelectionType")
lx.bless(SelectionListener,":SelectionListener")

class VectorPathPacketTranslation(object):
    def pathtrans_Path(self,packet):
        lx.notimpl()
    def pathtrans_Shape(self,packet):
        lx.notimpl()
    def pathtrans_Canvas(self,packet):
        lx.notimpl()
    def pathtrans_Item(self,packet):
        lx.notimpl()
    def pathtrans_Packet(self,path):
        lx.notimpl()

class VectorShapePacketTranslation(object):
    def shapetrans_Shape(self,packet):
        lx.notimpl()
    def shapetrans_Canvas(self,packet):
        lx.notimpl()
    def shapetrans_Item(self,packet):
        lx.notimpl()
    def shapetrans_Packet(self,shape):
        lx.notimpl()

class VectorKnotPacketTranslation(object):
    # Knot skipped
    def knottrans_Path(self,packet):
        lx.notimpl()
    def knottrans_Shape(self,packet):
        lx.notimpl()
    def knottrans_Canvas(self,packet):
        lx.notimpl()
    def knottrans_Item(self,packet):
        lx.notimpl()
    # Packet skipped

lx.bless(VectorPathPacketTranslation,":VectorPathPacketTranslation")
lx.bless(VectorShapePacketTranslation,":VectorShapePacketTranslation")
lx.bless(VectorKnotPacketTranslation,":VectorKnotPacketTranslation")

class Module(object):
    def mod_Generate(self,name,iid):
        lx.notimpl()
    def mod_GetTags(self,name,iid):
        lx.notimpl()

class TagDescription(object):
    def tag_Count(self):
        lx.notimpl()
    # Describe skipped

class ServiceExtension(object):
    def ser_Dummy(self):
        lx.notimpl()

class Factory(object):
    def fac_Name(self):
        lx.notimpl()
    def fac_UserName(self):
        lx.notimpl()
    # ClassGUID skipped
    def fac_Module(self):
        lx.notimpl()
    def fac_InfoTag(self,type):
        lx.notimpl()
    def fac_TagCount(self):
        lx.notimpl()
    def fac_TagByIndex(self,index):
        lx.notimpl()
    def fac_Spawn(self):
        lx.notimpl()

class NeedContext(object):
    def need_SetContext(self,app):
        lx.notimpl()

lx.bless(Module,":Module")
lx.bless(TagDescription,":TagDescription")
lx.bless(ServiceExtension,":ServiceExtension")
lx.bless(Factory,":Factory")
lx.bless(NeedContext,":NeedContext")

class ValueTexture(object):
    def vtx_SetupChannels(self,addChan):
        lx.notimpl()
    def vtx_LinkChannels(self,eval,item):
        lx.notimpl()
    def vtx_LinkSampleChannels(self,nodalEtor,item):
        lx.notimpl()
    # ReadChannels skipped
    # Customize skipped
    def vtx_Setup(self,data):
        lx.notimpl()
    # Evaluate skipped
    def vtx_Cleanup(self,data):
        lx.notimpl()
    def vtx_IsSampleDriven(self):
        return (lx.symbol.e_FALSE,0)

class CompShader(object):
    def csh_SetupChannels(self,addChan):
        lx.notimpl()
    def csh_LinkChannels(self,eval,item):
        lx.notimpl()
    # ReadChannels skipped
    # Customize skipped
    # Evaluate skipped
    # SetShadeFlags skipped
    def csh_SetOpaque(self):
        lx.notimpl()
    def csh_CustomPacket(self):
        lx.notimpl()
    def csh_Cleanup(self,data):
        lx.notimpl()
    def csh_Flags(self):
        lx.notimpl()

class CustomMaterial(object):
    def cmt_SetupChannels(self,addChan):
        lx.notimpl()
    def cmt_LinkChannels(self,eval,item):
        lx.notimpl()
    def cmt_LinkSampleChannels(self,nodalEtor,item):
        lx.notimpl()
    def cmt_IsSampleDriven(self):
        return (lx.symbol.e_FALSE,0)
    # ReadChannels skipped
    # Customize skipped
    def cmt_MaterialEvaluate(self,etor,vector,data):
        lx.notimpl()
    # ShaderEvaluate skipped
    # SetShadeFlags skipped
    def cmt_SetBump(self):
        lx.notimpl()
    def cmt_SetDisplacement(self):
        lx.notimpl()
    def cmt_SetOpaque(self):
        lx.notimpl()
    def cmt_SetSmoothing(self):
        lx.notimpl()
    def cmt_CustomPacket(self):
        lx.notimpl()
    def cmt_Cleanup(self,data):
        lx.notimpl()
    def cmt_UpdatePreview(self,chanIdx):
        lx.notimpl()
    def cmt_Flags(self):
        lx.notimpl()

lx.bless(ValueTexture,":ValueTexture")
lx.bless(CompShader,":CompShader")
lx.bless(CustomMaterial,":CustomMaterial")


class FileDialogClient(object):
    def filedlg_Flags(self):
        return lx.symbol.fFILEDIALOG_LOAD
    def filedlg_Title(self,message):
        lx.notimpl()
    def filedlg_FileClass(self):
        return 0
    def filedlg_ContextString(self):
        lx.notimpl()
    def filedlg_FileFormat(self):
        lx.notimpl()
    def filedlg_StartPath(self):
        lx.notimpl()
    def filedlg_ResultPath(self,filepath):
        lx.notimpl()
    def filedlg_ResultFormat(self,format):
        lx.notimpl()

class ColorDialog(object):
    def colordlg_DoDialog(self,title,stops,gamma):
        lx.notimpl()

class AsyncMonitorInfo(object):
    def amonsys_System(self):
        lx.notimpl()
    def amonsys_Title(self):
        lx.notimpl()
    def amonsys_Progress(self):
        lx.notimpl()
    def amonsys_OverallProgress(self):
        lx.notimpl()
    def amonsys_Parent(self):
        lx.notimpl()
    def amonsys_Child(self):
        lx.notimpl()
    def amonsys_Identifier(self):
        lx.notimpl()
    def amonsys_CanAbort(self):
        lx.notimpl()
    def amonsys_Abort(self):
        lx.notimpl()
    def amonsys_IsAborted(self):
        lx.notimpl()

lx.bless(FileDialogClient,":FileDialogClient")
lx.bless(ColorDialog,":ColorDialog")
lx.bless(AsyncMonitorInfo,":AsyncMonitorInfo")

class SurfaceBin(object):
    def surfbin_GetBBox(self):
        lx.notimpl()
    def surfbin_FrontBBox(self,pos,dir):
        lx.notimpl()

class Curve(object):
    def curve_GetBBox(self):
        lx.notimpl()
    def curve_Length(self):
        lx.notimpl()
    def curve_SplineCount(self):
        lx.notimpl()
    def curve_SplineByIndex(self,index):
        lx.notimpl()
    def curve_SplineLengthByIndex(self,index):
        lx.notimpl()
    def curve_BendCount(self):
        lx.notimpl()
    def curve_Param(self):
        lx.notimpl()
    def curve_SetParam(self,param):
        lx.notimpl()
    def curve_LenFraction(self):
        lx.notimpl()
    def curve_SetLenFraction(self,frac):
        lx.notimpl()
    def curve_Position(self):
        lx.notimpl()
    def curve_Tangent(self):
        lx.notimpl()
    def curve_Curvature(self):
        lx.notimpl()
    def curve_Normal(self):
        lx.notimpl()
    def curve_MeshNormal(self,meshObj):
        lx.notimpl()
    def curve_GuideCurveNormal(self,other):
        lx.notimpl()
    def curve_Closest(self,probe):
        lx.notimpl()
    def curve_IsClosed(self):
        lx.notimpl()
    def curve_WalkByAngle(self,start,end,angle,visitor):
        lx.notimpl()

class GLShadingListener(object):
    def gls_ShadingUpdate(self,item):
        lx.notimpl()
    def gls_DisplacementUpdate(self,item):
        lx.notimpl()
    def gls_FurUpdate(self,item):
        lx.notimpl()

class Surface(object):
    def surf_GetBBox(self):
        lx.notimpl()
    def surf_FrontBBox(self,pos,dir):
        lx.notimpl()
    # RayCast skipped
    def surf_BinCount(self):
        lx.notimpl()
    def surf_BinByIndex(self,index):
        lx.notimpl()
    def surf_TagCount(self,type):
        lx.notimpl()
    def surf_TagByIndex(self,type,index):
        lx.notimpl()
    def surf_GLCount(self):
        lx.notimpl()

class CurveGroup(object):
    def cgrp_GetBBox(self):
        lx.notimpl()
    def cgrp_Count(self):
        lx.notimpl()
    def cgrp_ByIndex(self,index):
        lx.notimpl()

class SurfaceItem(object):
    def isurf_GetSurface(self,chanRead,morph):
        lx.notimpl()
    def isurf_Prepare(self,eval):
        lx.notimpl()
    def isurf_Evaluate(self,attr,index):
        lx.notimpl()

lx.bless(SurfaceBin,":SurfaceBin")
lx.bless(Curve,":Curve")
lx.bless(GLShadingListener,":GLShadingListener")
lx.bless(Surface,":Surface")
lx.bless(CurveGroup,":CurveGroup")
lx.bless(SurfaceItem,":SurfaceItem")

class TableauInstance(object):
    def tins_Properties(self,vecstack):
        lx.notimpl()
    def tins_GetTransform(self,endPoint):
        lx.notimpl()
    def tins_GetDissolve(self):
        lx.notimpl()
    def tins_ParticleDescription(self):
        lx.notimpl()
    def tins_ParticleArray(self):
        lx.notimpl()

class TableauListener(object):
    def tli_ChannelChange(self,tableau,item,channel):
        lx.notimpl()
    def tli_FlushElements(self,tableau):
        lx.notimpl()
    def tli_TableauDestroy(self,tableau):
        lx.notimpl()

class TriangleSoup(object):
    def soup_TestBox(self,bbox):
        return 1
    def soup_Segment(self,segID,type):
        return True
    def soup_Vertex(self,vertex):
        lx.notimpl()
    def soup_Polygon(self,v0,v1,v2):
        lx.notimpl()
    def soup_Connect(self,type):
        lx.notimpl()

class Instanceable(object):
    def instable_Compare(self,other):
        lx.notimpl()
    def instable_AddElements(self,tableau,instT0,instT1):
        lx.notimpl()
    def instable_GetSurface(self):
        lx.notimpl()

class TableauProxy(object):
    def tpro_Bound(self):
        lx.notimpl()
    def tpro_FeatureCount(self,type):
        return 0
    def tpro_FeatureByIndex(self,type,index):
        raise RuntimeError('bad result: OUTOFBOUNDS')
    def tpro_SetVertex(self,vdesc):
        lx.notimpl()
    def tpro_Sample(self,bbox,tableau):
        lx.notimpl()

class TableauLight(object):
    def tlgt_Bound(self):
        lx.notimpl()
    def tlgt_FeatureCount(self,type):
        return 0
    def tlgt_FeatureByIndex(self,type,index):
        raise RuntimeError('bad result: OUTOFBOUNDS')
    def tlgt_SetVertex(self,vdesc):
        lx.notimpl()
    def tlgt_Sample(self,u,v,dir,t):
        lx.notimpl()
    def tlgt_Geometry(self,gc):
        lx.notimpl()
    # Emit skipped
    def tlgt_ShadowMap(self):
        lx.notimpl()

class TableauSurface(object):
    def tsrf_Bound(self):
        lx.notimpl()
    def tsrf_FeatureCount(self,type):
        return 0
    def tsrf_FeatureByIndex(self,type,index):
        raise RuntimeError('bad result: OUTOFBOUNDS')
    def tsrf_SetVertex(self,vdesc):
        lx.notimpl()
    def tsrf_Sample(self,bbox,scale,trisoup):
        lx.notimpl()
    def tsrf_Padding(self):
        lx.notimpl()
    def tsrf_SegmentBox(self,segID):
        lx.notimpl()

class TableauSource(object):
    def tsrc_Elements(self,tableau):
        lx.notimpl()
    def tsrc_Preview(self,tableau):
        lx.notimpl()
    def tsrc_Instance(self,tableau,instance):
        lx.notimpl()
    def tsrc_SubShader(self,tableau):
        lx.notimpl()
    def tsrc_PreviewUpdate(self,chanIndex):
        lx.notimpl()
    def tsrc_GetCurves(self,tableau,tags):
        lx.notimpl()
    def tsrc_ElementType(self,type):
        lx.notimpl()

class TableauShader(object):
    def tsha_Select(self,teElt,tvDesc):
        lx.notimpl()
    def tsha_Slice(self,vtOutput,tvDesc):
        lx.notimpl()

class TableauVolume(object):
    def tvol_Bound(self):
        lx.notimpl()
    def tvol_FeatureCount(self,type):
        return 0
    def tvol_FeatureByIndex(self,type,index):
        raise RuntimeError('bad result: OUTOFBOUNDS')
    def tvol_SetVertex(self,vdesc):
        lx.notimpl()
    def tvol_Type(self):
        lx.notimpl()
    def tvol_RenderInit(self,sv):
        lx.notimpl()
    def tvol_RaySample(self,densitySlice,shadingSlice,sv,raycastObj,raymarchObj):
        lx.notimpl()
    def tvol_RayCast(self,densitySlice,sv,raycastObj):
        lx.notimpl()
    def tvol_Density(self,densitySlice,sv,raycastObj,pos,worldPos):
        lx.notimpl()

lx.bless(TableauInstance,":TableauInstance")
lx.bless(TableauListener,":TableauListener")
lx.bless(TriangleSoup,":TriangleSoup")
lx.bless(Instanceable,":Instanceable")
lx.bless(TableauProxy,":TableauProxy")
lx.bless(TableauLight,":TableauLight")
lx.bless(TableauSurface,":TableauSurface")
lx.bless(TableauSource,":TableauSource")
lx.bless(TableauShader,":TableauShader")
lx.bless(TableauVolume,":TableauVolume")

class WorkList(object):
    def work_IsEmpty(self):
        lx.notimpl()
    def work_Next(self):
        lx.notimpl()
    def work_Split(self,mode):
        lx.notimpl()
    def work_Clear(self):
        lx.notimpl()

class Waterfall(object):
    def wfall_Spawn(self):
        lx.notimpl()
    def wfall_State(self):
        lx.notimpl()
    def wfall_ProcessWork(self):
        lx.notimpl()
    def wfall_GetWork(self):
        lx.notimpl()
    def wfall_Advance(self):
        lx.notimpl()

class ThreadSlotClient(object):
    # Alloc skipped
    def tsc_Free(self,value):
        lx.notimpl()

class ThreadRangeWorker(object):
    def rngw_Execute(self,index,sharedData):
        lx.notimpl()

class ThreadJob(object):
    def job_Execute(self):
        lx.notimpl()

class SharedWork(object):
    def share_Evaluate(self):
        lx.notimpl()
    def share_Spawn(self):
        lx.notimpl()
    def share_Share(self,other,split):
        lx.notimpl()

lx.bless(WorkList,":WorkList")
lx.bless(Waterfall,":Waterfall")
lx.bless(ThreadSlotClient,":ThreadSlotClient")
lx.bless(ThreadRangeWorker,":ThreadRangeWorker")
lx.bless(ThreadJob,":ThreadJob")
lx.bless(SharedWork,":SharedWork")

class DTBBadgeOverride(object):
    def dtbbo_BadgesSupported(self,entry):
        lx.notimpl()
    def dtbbo_BadgeIsAlwaysVisible(self,entry,badge):
        lx.notimpl()
    def dtbbo_BadgeOverride(self,entry,badge):
        lx.notimpl()
    def dtbbo_BadgeTooltip(self,entry,badge):
        lx.notimpl()
    def dtbbo_BadgeStarRatingOverride(self,entry):
        lx.notimpl()
    def dtbbo_BadgeAction(self,entry,badge):
        lx.notimpl()
    def dtbbo_BadgeStarRatingAction(self,entry,rating):
        lx.notimpl()

class DTBGroupSortOverride(object):
    def gso_SetArguments(self,args):
        lx.notimpl()
    def gso_Sort(self,string1,string2):
        lx.notimpl()

lx.bless(DTBBadgeOverride,":DTBBadgeOverride")
lx.bless(DTBGroupSortOverride,":DTBGroupSortOverride")

class ToolOperation(object):
    def top_Evaluate(self,vts):
        lx.notimpl()
    def top_ReEvaluate(self,vts):
        lx.notimpl()
    def top_Blend(self,other,blend):
        lx.notimpl()

class ParticleGeneratorPacket(object):
    def partgen_Count(self,vts):
        return 0
    # Particle skipped
    # InitialParticleSet skipped
    # HintBoxSet skipped

class PathGeneratorPacket(object):
    def pathgen_Value(self,vts,t):
        lx.notimpl()
    def pathgen_Length(self,vts,t0,t1):
        return 0
    def pathgen_Tangent(self,vts,t):
        lx.notimpl()
    # Source skipped
    def pathgen_Count(self,vts):
        return 0
    # Knot skipped
    def pathgen_Current(self,vts):
        return 0
    def pathgen_KnotDataSet(self,gen):
        lx.notimpl()
    def pathgen_Walk(self,vts,pathStep,angle,ti,tf):
        return 0
    def pathgen_Bank(self,vts,t):
        return 0

class Tool(object):
    def tool_Reset(self):
        lx.notimpl()
    def tool_Evaluate(self,vts):
        lx.notimpl()
    def tool_VectorType(self):
        lx.notimpl()
    def tool_Order(self):
        lx.notimpl()
    def tool_Task(self):
        lx.notimpl()
    def tool_Sequence(self,seq):
        lx.notimpl()
    def tool_ShouldBeAttribute(self,task):
        return 0
    def tool_GetOp(self,flags):
        lx.notimpl()
    def tool_CompareOp(self,vts,toolop):
        return lx.symbol.iTOOLOP_DIFFERENT
    def tool_UpdateOp(self,toolop):
        lx.notimpl()

lx.bless(ToolOperation,":ToolOperation")
lx.bless(ParticleGeneratorPacket,":ParticleGeneratorPacket")
lx.bless(PathGeneratorPacket,":PathGeneratorPacket")
lx.bless(Tool,":Tool")

class ItemReplacement(object):
    def itemrep_ReplaceItems(self,current,replacement,targetType):
        lx.notimpl()
    def itemrep_Types(self,curType):
        lx.notimpl()
    def itemrep_NotifierCount(self,itemType,channelName):
        lx.notimpl()
    def itemrep_NotifierByIndex(self,itemType,channelName,index):
        lx.notimpl()

lx.bless(ItemReplacement,":ItemReplacement")

class TreeListener(object):
    def tlis_NewAttributes(self):
        lx.notimpl()
    def tlis_NewShape(self):
        lx.notimpl()
    def tlis_NewSpaceForThumbnails(self):
        lx.notimpl()
    def tlis_ClearCachedThumbnail(self,ident):
        lx.notimpl()
    def tlis_ClearAllCachedThumbnails(self):
        lx.notimpl()
    def tlis_NewShowDescriptionText(self):
        lx.notimpl()

class Tree(object):
    def tree_Spawn(self,mode):
        lx.notimpl()
    def tree_ToParent(self):
        lx.notimpl()
    def tree_ToChild(self):
        lx.notimpl()
    def tree_ToRoot(self):
        lx.notimpl()
    def tree_IsRoot(self):
        lx.notimpl()
    def tree_ChildIsLeaf(self):
        lx.notimpl()
    def tree_Count(self):
        lx.notimpl()
    def tree_Current(self):
        lx.notimpl()
    def tree_SetCurrent(self,index):
        lx.notimpl()
    def tree_ItemState(self,guid):
        lx.notimpl()
    def tree_SetItemState(self,guid,state):
        lx.notimpl()

lx.bless(TreeListener,":TreeListener")
lx.bless(Tree,":Tree")

class TreeView(object):
    def treeview_StoreState(self,uid):
        lx.notimpl()
    def treeview_RestoreState(self,uid):
        lx.notimpl()
    def treeview_StyleHints(self):
        lx.notimpl()
    def treeview_ColumnCount(self):
        lx.notimpl()
    def treeview_ColumnByIndex(self,columnIndex):
        lx.notimpl()
    def treeview_ColumnInternalName(self,columnIndex):
        lx.notimpl()
    def treeview_ColumnIconResource(self,columnIndex):
        lx.notimpl()
    def treeview_ColumnJustification(self,columnIndex):
        lx.notimpl()
    def treeview_PrimaryColumnPosition(self):
        lx.notimpl()
    def treeview_ToPrimary(self):
        lx.notimpl()
    def treeview_IsSelected(self):
        lx.notimpl()
    def treeview_Select(self,mode):
        lx.notimpl()
    def treeview_CellCommand(self,columnIndex):
        lx.notimpl()
    def treeview_BatchCommand(self,columnIndex):
        lx.notimpl()
    def treeview_ToolTip(self,columnIndex):
        lx.notimpl()
    def treeview_DescriptionText(self,columnIndex):
        lx.notimpl()
    def treeview_ShowDescriptionText(self):
        lx.notimpl()
    def treeview_ReservedSpaceForIcons(self):
        lx.notimpl()
    def treeview_IconResource(self,columnIndex,width,height):
        lx.notimpl()
    def treeview_ReservedSpaceForThumbnails(self):
        lx.notimpl()
    def treeview_Thumbnail(self,columnIndex,width,height):
        lx.notimpl()
    def treeview_BadgeType(self,columnIndex,badgeIndex):
        lx.notimpl()
    def treeview_BadgeType2(self,columnIndex,badgeIndex):
        lx.notimpl()
    def treeview_BadgeDetail(self,columnIndex,badgeIndex,badgeDetail):
        lx.notimpl()
    def treeview_IsInputRegion(self,columnIndex,regionID):
        lx.notimpl()
    def treeview_SupportedDragDropSourceTypes(self,columnIndex):
        lx.notimpl()
    def treeview_GetDragDropSourceObject(self,columnIndex,type):
        lx.notimpl()
    def treeview_GetDragDropDestinationObject(self,columnIndex,location):
        lx.notimpl()
    def treeview_IsDescendantSelected(self):
        lx.notimpl()
    def treeview_CanFilter(self):
        lx.notimpl()
    def treeview_Filter(self):
        lx.notimpl()

lx.bless(TreeView,":TreeView")



class Undo(object):
    def undo_Forward(self):
        lx.notimpl()
    def undo_Reverse(self):
        lx.notimpl()

lx.bless(Undo,":Undo")

class Message(object):
    def msg_Code(self):
        lx.notimpl()
    def msg_SetCode(self,code):
        lx.notimpl()
    def msg_SetMessage(self,table,name,id):
        lx.notimpl()
    def msg_SetArgumentInt(self,arg,value):
        lx.notimpl()
    def msg_SetArgumentFloat(self,arg,value):
        lx.notimpl()
    def msg_SetArgumentString(self,arg,string):
        lx.notimpl()
    def msg_SetArgumentObject(self,arg,object):
        lx.notimpl()
    def msg_Reset(self):
        lx.notimpl()
    def msg_Table(self):
        lx.notimpl()
    def msg_Name(self):
        lx.notimpl()
    def msg_SetMessageResult(self,id):
        lx.notimpl()

class ValueConversion(object):
    def conv_Test(self,fromType,toType):
        lx.notimpl()
    def conv_Convert(self,from_obj,fromType,to_obj,toType):
        lx.notimpl()

class Visitor(object):
    def vis_Evaluate(self):
        lx.notimpl()

class ScriptQuery(object):
    def sq_Select(self,attribute,which):
        lx.notimpl()
    def sq_Query(self,attribute,query):
        lx.notimpl()
    def sq_Type(self,attribute):
        lx.notimpl()
    def sq_TypeName(self,attribute):
        lx.notimpl()

class Attributes(object):
    def attr_Count(self):
        return 0
    def attr_Name(self,index):
        lx.notimpl()
    def attr_Lookup(self,name):
        lx.notimpl()
    def attr_Type(self,index):
        lx.notimpl()
    def attr_TypeName(self,index):
        lx.notimpl()
    def attr_Hints(self,index):
        return 0
    def attr_Value(self,index,writeOK):
        lx.notimpl()
    def attr_GetInt(self,index):
        lx.notimpl()
    def attr_SetInt(self,index,val):
        lx.notimpl()
    def attr_GetFlt(self,index):
        lx.notimpl()
    def attr_SetFlt(self,index,val):
        lx.notimpl()
    def attr_GetString(self,index):
        lx.notimpl()
    def attr_SetString(self,index,val):
        lx.notimpl()

class ValueArray(object):
    def va_Type(self):
        lx.notimpl()
    def va_TypeName(self):
        lx.notimpl()
    def va_Count(self):
        lx.notimpl()
    def va_AddEmptyValue(self):
        lx.notimpl()
    def va_AddValue(self,value):
        lx.notimpl()
    def va_AddInt(self,value):
        lx.notimpl()
    def va_AddFloat(self,value):
        lx.notimpl()
    def va_AddString(self,value):
        lx.notimpl()
    def va_GetValue(self,index):
        lx.notimpl()
    def va_GetInt(self,index):
        lx.notimpl()
    def va_GetFloat(self,index):
        lx.notimpl()
    def va_GetString(self,index):
        lx.notimpl()
    def va_FirstUnique(self):
        lx.notimpl()
    def va_Reset(self):
        lx.notimpl()
    def va_Remove(self,index):
        lx.notimpl()
    def va_SetValue(self,index,value):
        lx.notimpl()
    def va_SetInt(self,index,value):
        lx.notimpl()
    def va_SetFloat(self,index,value):
        lx.notimpl()
    def va_SetString(self,index,value):
        lx.notimpl()

class Value(object):
    def val_Clone(self):
        lx.notimpl()
    def val_Copy(self,from_obj):
        lx.notimpl()
    def val_Compare(self,other):
        lx.notimpl()
    def val_Type(self):
        lx.notimpl()
    def val_TypeName(self):
        lx.notimpl()
    def val_SubTypeName(self):
        lx.notimpl()
    def val_GetInt(self):
        lx.notimpl()
    def val_SetInt(self,val):
        lx.notimpl()
    def val_GetFlt(self):
        lx.notimpl()
    def val_SetFlt(self,val):
        lx.notimpl()
    def val_GetString(self):
        lx.notimpl()
    def val_SetString(self,val):
        lx.notimpl()
    def val_Intrinsic(self):
        return 0

class StringConversion(object):
    def str_Encode(self):
        lx.notimpl()
    def str_Decode(self,buf):
        lx.notimpl()

class StringTag(object):
    def stag_Get(self,type):
        lx.notimpl()
    def stag_Set(self,type,tag):
        lx.notimpl()
    def stag_Count(self):
        lx.notimpl()
    def stag_ByIndex(self,index):
        lx.notimpl()

class ValueMath(object):
    def math_Step(self,direction):
        lx.notimpl()
    def math_Detent(self):
        lx.notimpl()
    def math_Add(self,delta):
        lx.notimpl()
    def math_Multiply(self,factor):
        lx.notimpl()
    def math_Blend(self,other,blend):
        lx.notimpl()

class StringConversionNice(object):
    def nicestr_Encode(self):
        lx.notimpl()
    def nicestr_Decode(self,buf):
        lx.notimpl()

lx.bless(Message,":Message")
lx.bless(ValueConversion,":ValueConversion")
lx.bless(Visitor,":Visitor")
lx.bless(ScriptQuery,":ScriptQuery")
lx.bless(Attributes,":Attributes")
lx.bless(ValueArray,":ValueArray")
lx.bless(Value,":Value")
lx.bless(StringConversion,":StringConversion")
lx.bless(StringTag,":StringTag")
lx.bless(ValueMath,":ValueMath")
lx.bless(StringConversionNice,":StringConversionNice")

class Variation(object):
    def var_TestItem(self,item,chanRead):
        lx.notimpl()
    def var_Initialize(self,item,chanRead):
        lx.notimpl()
    def var_RangeX(self):
        lx.notimpl()
    def var_RangeY(self):
        lx.notimpl()
    def var_Thumb(self,x,y,size,chanRead):
        lx.notimpl()
    def var_Do(self,x,y):
        lx.notimpl()

lx.bless(Variation,":Variation")

class VectorPacket(object):
    def vpkt_Size(self):
        lx.notimpl()
    def vpkt_Interface(self):
        lx.notimpl()
    def vpkt_Initialize(self,packet):
        lx.notimpl()
    def vpkt_Reset(self,packet):
        lx.notimpl()
    def vpkt_Copy(self,packet,from_poi):
        lx.notimpl()
    def vpkt_Cleanup(self,packet):
        lx.notimpl()
    def vpkt_Blend(self,packet,p0,p1,t,mode):
        lx.notimpl()
    def vpkt_Invert(self,packet):
        lx.notimpl()
    def vpkt_NodeCount(self):
        return 0
    def vpkt_NodeName(self,index):
        lx.notimpl()
    # NodeType skipped
    # NodeGet skipped

class PacketEffect(object):
    def pfx_Packet(self):
        lx.notimpl()
    def pfx_Count(self):
        lx.notimpl()
    def pfx_ByIndex(self,index):
        lx.notimpl()
    def pfx_Get(self,index,packet,item):
        lx.notimpl()
    def pfx_Set(self,index,packet,val,item):
        lx.notimpl()

class TextureEffect(object):
    def tfx_Type(self):
        lx.notimpl()
    def tfx_TypeName(self):
        lx.notimpl()
    def tfx_Get(self,sv,item):
        lx.notimpl()
    def tfx_Set(self,sv,val,item):
        lx.notimpl()

lx.bless(VectorPacket,":VectorPacket")
lx.bless(PacketEffect,":PacketEffect")
lx.bless(TextureEffect,":TextureEffect")

class VectorShape(object):
    def shape_ShapeCount(self):
        lx.notimpl()
    def shape_ShapeByIndex(self,index):
        lx.notimpl()
    def shape_Parent(self):
        lx.notimpl()
    def shape_PathCount(self):
        lx.notimpl()
    def shape_PathByIndex(self,index):
        lx.notimpl()
    def shape_Transform(self,matrix):
        lx.notimpl()

class VectorCanvas(object):
    def canvas_GetItem(self):
        lx.notimpl()
    def canvas_BeginEditBatch(self):
        lx.notimpl()
    def canvas_EndEditBatch(self):
        lx.notimpl()

class VectorPath(object):
    def path_IsPathClosed(self):
        lx.notimpl()
    def path_SetPathClosed(self,closed):
        lx.notimpl()
    def path_KnotCount(self):
        lx.notimpl()
    def path_SelectKnotByIndex(self,index):
        lx.notimpl()
    def path_SelectKnot(self,knot):
        lx.notimpl()
    def path_KnotEnumerate(self,visitor):
        lx.notimpl()
    def path_ID(self):
        lx.notimpl()
    def path_Pos(self):
        lx.notimpl()

class VectorListener(object):
    def vtl_Destroy(self):
        lx.notimpl()
    def vtl_ShapeAdd(self,shape):
        lx.notimpl()
    def vtl_ShapeRemove(self,shape):
        lx.notimpl()
    def vtl_ShapeStyle(self,shape,name):
        lx.notimpl()
    def vtl_PathAdd(self,shape,path):
        lx.notimpl()
    def vtl_PathRemove(self,shape,path):
        lx.notimpl()
    def vtl_KnotPosition(self,shape,path):
        lx.notimpl()

lx.bless(VectorShape,":VectorShape")
lx.bless(VectorCanvas,":VectorCanvas")
lx.bless(VectorPath,":VectorPath")
lx.bless(VectorListener,":VectorListener")


class ViewObject(object):
    def viewobj_TestMode(self,type):
        lx.notimpl()
    def viewobj_Flags(self):
        return 0
    def viewobj_Generate(self,type):
        lx.notimpl()
    def viewobj_Count(self,type):
        return 0
    def viewobj_ByIndex(self,type,index):
        lx.notimpl()
    def viewobj_ByView(self,view):
        lx.notimpl()

lx.bless(ViewObject,":ViewObject")


class ViewItem3D(object):
    def vitm_Draw(self,chanRead,strokeDraw,selectionFlags,itemColor):
        lx.notimpl()
    def vitm_DrawBackground(self,chanRead,strokeDraw,itemColor):
        lx.notimpl()
    def vitm_WorldSpace(self):
        lx.notimpl()
    def vitm_HandleCount(self):
        lx.notimpl()
    def vitm_HandleMotion(self,handleIndex):
        lx.notimpl()
    def vitm_HandleChannel(self,handleIndex):
        lx.notimpl()
    def vitm_HandleValueToPosition(self,handleIndex,chanValue):
        lx.notimpl()
    def vitm_HandlePositionToValue(self,handleIndex,position):
        lx.notimpl()
    def vitm_Test(self,chanRead,strokeDraw,selectionFlags,itemColor):
        lx.notimpl()

class VirtualModel(object):
    def vmodel_Flags(self):
        return lx.symbol.fTMOD_DRAW_3D
    def vmodel_Draw(self,stroke):
        lx.notimpl()
    def vmodel_Test(self,stroke):
        lx.notimpl()
    def vmodel_Track(self,part):
        lx.notimpl()
    def vmodel_Down(self,vts):
        lx.notimpl()
    def vmodel_Move(self,vts):
        lx.notimpl()
    def vmodel_Up(self,vts):
        lx.notimpl()
    def vmodel_Tooltip(self,part):
        return NULL

class ToolModel(object):
    def tmod_Flags(self):
        return lx.symbol.fTMOD_DRAW_3D
    def tmod_Draw(self,vts,stroke,flags):
        lx.notimpl()
    def tmod_Test(self,vts,stroke,flags):
        lx.notimpl()
    def tmod_Filter(self,vts,adjust):
        lx.notimpl()
    def tmod_Initialize(self,vts,adjust,flags):
        lx.notimpl()
    def tmod_Down(self,vts,adjust):
        lx.notimpl()
    def tmod_Move(self,vts,adjust):
        lx.notimpl()
    def tmod_Up(self,vts,adjust):
        lx.notimpl()
    def tmod_Haul(self,index):
        return 0
    def tmod_AllowOverride(self,attrName,mouseInput,haulAxis):
        lx.notimpl()
    def tmod_Help(self,vts):
        return 0
    def tmod_Enable(self,msg):
        lx.notimpl()
    def tmod_Drop(self):
        lx.notimpl()
    def tmod_Track(self,vts,eventType):
        lx.notimpl()
    def tmod_TrackFlags(self):
        lx.notimpl()
    def tmod_Post(self,vts):
        lx.notimpl()
    def tmod_TestType(self,type):
        lx.notimpl()
    def tmod_Tooltip(self,vts,part):
        return 0

class NavigationListener(object):
    def nav_Down(self,view,item):
        lx.notimpl()
    def nav_Move(self,view,item,hot,pos,rot,zoom):
        lx.notimpl()
    def nav_Up(self,view,item):
        lx.notimpl()
    def nav_Delta(self,view,item,hot,pos,rot,zoom):
        lx.notimpl()
    def nav_Wheel(self,view,item):
        lx.notimpl()
    def nav_HotSyncPre(self,view,item):
        lx.notimpl()
    def nav_HotSyncPost(self,view,item):
        lx.notimpl()

lx.bless(ViewItem3D,":ViewItem3D")
lx.bless(VirtualModel,":VirtualModel")
lx.bless(ToolModel,":ToolModel")
lx.bless(NavigationListener,":NavigationListener")

class Raymarch(object):
    # AddVolume skipped
    # AddSurface skipped
    def rmrch_GetOpacity(self,vector,dist):
        lx.notimpl()
    def rmrch_ShaderEvaluate(self,vector,shader):
        lx.notimpl()
    def rmrch_Jitter1D(self,vector):
        lx.notimpl()

class Voxel(object):
    def voxel_FeatureCount(self):
        lx.notimpl()
    def voxel_FeatureByIndex(self,index):
        lx.notimpl()
    def voxel_BBox(self):
        lx.notimpl()
    def voxel_NextPos(self,currentPos,currentSegment,stride):
        lx.notimpl()
    def voxel_Sample(self,pos,index):
        lx.notimpl()
    def voxel_VDBData(self):
        lx.notimpl()
    # RayIntersect skipped
    # RayRelease skipped

lx.bless(Raymarch,":Raymarch")
lx.bless(Voxel,":Voxel")

class GLViewportClient(object):
    def glclient_Invalidate(self):
        lx.notimpl()
    def glclient_MousePosition(self):
        lx.notimpl()
    def glclient_MouseButton(self):
        lx.notimpl()
    def glclient_TabletPressure(self):
        lx.notimpl()
    def glclient_TabletTilt(self):
        lx.notimpl()
    def glclient_MouseCount(self):
        lx.notimpl()

lx.bless(GLViewportClient,":GLViewportClient")



