#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.
#
import lx




class ActionListener(lx.object.ActionListener):

        '''
        Empty actionlistener Python user class.
        '''
        pass




class ChannelRead(lx.object.ChannelRead):

        '''
        The Python method is very much easier, just returning the right value type
        for any channel, given by index or name.
        '''
        def Value(self, item, index):
            """value = Value(item, channel)
            Channel can be given by index or name.
            """
            if isinstance(index, str):
                index = item.ChannelLookup(index)

            type = self.Type(item, index)

            if type == lx.symbol.i_TYPE_FLOAT:
                return self.Double(item, index)

            if type == lx.symbol.i_TYPE_INTEGER:
                try:
                    return self.EncodedInt(item, index)
                except:
                    return self.Integer(item, index)

            if type == lx.symbol.i_TYPE_STRING:
                return self.String(item, index)

            return self.ValueObj(item, index)




class ChannelWrite(lx.object.ChannelWrite):

        '''
        Python user method does all conversions this direction as well.
        '''
        def Set(self, item, index, value, key=False):
            """Set(item, channel, value, <key>)
            Channel can be given by index or name. Set key to True to make a keyframe.
            """
            if isinstance(index, str):
                index = item.ChannelLookup(index)

            type = self.Type(item, index)

            if type == lx.symbol.i_TYPE_FLOAT:
                if key:
                    self.DoubleKey(item, index, float(value), True)
                else:
                    self.Double(item, index, float(value))

            elif type == lx.symbol.i_TYPE_INTEGER:
                if isinstance(value, str):
                    try:
                        if key:
                            self.EncodedIntKey(item, index, value, True)
                        else:
                            self.EncodedInt(item, index, value)
        
                    except RuntimeError:
                        if key:
                            self.IntegerKey(item, index, int(value), True)
                        else:
                            self.Integer(item, index, int(value))        
                else:
                    if key:
                        self.IntegerKey(item, index, int(value), True)
                    else:
                        self.Integer(item, index, int(value))

            elif type == lx.symbol.i_TYPE_STRING:
                if key:
                   raise RuntimeError("Can't keyfame string channels.")

                self.String(item, index, str(value))

            else:
                raise RuntimeError("Can't set object channels.")




class EvalModifier(lx.object.EvalModifier):

        '''
        Empty EvalModifier Python user class.
        '''
        pass




class Modifier(lx.object.Modifier):

        '''
        Empty Modifier Python user class.
        '''
        pass




class SimulationModifier(lx.object.SimulationModifier):

        '''
        Empty SimulationModifier Python user class.
        '''
        pass




class Evaluation(lx.object.Evaluation):

        '''
        Empty Evaluation Python user class.
        '''
        pass





class ActionClip(lx.object.ActionClip):

        '''
        Empty actionclip Python user class.
        '''
        pass





class AnimListener(lx.object.AnimListener):
      pass








class ChannelUI(lx.object.ChannelUI):

        '''
        Empty ChannelUI Python user class.
        '''
        pass







class ColorModel(lx.object.ColorModel):

        '''
        Empty ColorModel Python user class.
        '''
        pass




class Color(lx.object.Color):

        '''
        Empty Color Python user class.
        '''
        pass





class ColorMapping(lx.object.ColorMapping):

        '''
        Empty ColorMapping Python user class.
        '''
        pass

        '''
        Empty ColorMapping Python user class.
        '''
        pass










class Command(lx.object.Command):

        '''
        Empty Command Python user class.
        '''
        pass




class CommandDBHelp(lx.object.CommandDBHelp):

        '''
        Empty CommandDBHelp Python user class.
        '''
        pass




class UIHints(lx.object.UIHints):

        '''
        It is not uncommon to want to use another command as the base for your own filter command's
        priority. For example, the item.withTypeIsSelected command is used in for the Item Properties
        forms.  In that case you could use ILxCommandService::SpawnFromString() to get an ILxCommand,
        then call ILxCommandService::AllocateUIHintsFromCommand() to get its hints.  You can then
        use the ILxUIHintsRead interface on the returned object to call FormFilterPriority(), using
        that as the baiss for the new priority in your hints.  You can also modify those hints and
        return them directly from your own command.
        Empty UIHints Python user class.
        '''
        pass




class UIHintsRead(lx.object.UIHintsRead):

        '''
        Empty UIHintsRead Python user class.
        '''
        pass




class UIValueHints(lx.object.UIValueHints):

        '''
        Empty UIValueHints Python user class.
        '''
        pass




class AttributesUI(lx.object.AttributesUI):

        '''
        Empty AttributesUI Python user class.
        '''
        pass




class CommandEvent(lx.object.CommandEvent):

        '''
        Empty CommandEvent Python user class.
        '''
        pass




class CmdSysListener(lx.object.CmdSysListener):

        '''
        Empty CmdSysListener Python user class.
        '''
        pass





class CustomPane(lx.object.CustomPane):

        '''
        Empty CustomPane Python user class.
        '''
        pass




class CustomView(lx.object.CustomView):

        '''
        Empty CustomView Python user class.
        '''
        pass





class Falloff(lx.object.Falloff):

        '''
        Empty Falloff Python user class.
        '''
        pass




class Deformation(lx.object.Deformation):

        '''
        Empty Deformation Python user class.
        '''
        pass




class Deformer(lx.object.Deformer):

        '''
        Empty Deformer Python user class.
        '''
        pass




class MeshInfluence(lx.object.MeshInfluence):

        '''
        Empty MeshInfluence Python user class.
        '''
        pass




class ItemInfluence(lx.object.ItemInfluence):

        '''
        Empty ItemInfluence Python user class.
        '''
        pass




class GroupDeformer(lx.object.GroupDeformer):

        '''
        Empty GroupDeformer Python user class.
        '''
        pass




class WeightMapDeformerItem(lx.object.WeightMapDeformerItem):

        '''
        Empty WeightMapDeformerItem Python user class.
        '''
        pass







class DirCacheEntry(lx.object.DirCacheEntry):
        pass




class DirEntryThumbAsync(lx.object.DirEntryThumbAsync):
        pass




class MergedDirCacheEntry(lx.object.MergedDirCacheEntry):
        pass




class DirCacheFileMetrics(lx.object.DirCacheFileMetrics):
        pass




class BasePathAddDest(lx.object.BasePathAddDest):
        pass




class DirCacheManualOrderDest(lx.object.DirCacheManualOrderDest):

        '''
        Empty DirCacheManualOrderDest Python user class.
        '''
        pass




class DirCacheGridPosDest(lx.object.DirCacheGridPosDest):

        '''
        Empty DirCacheGridPosDest Python user class.
        '''
        pass




class FileSysDest(lx.object.FileSysDest):

        '''
        Empty FileSysDest Python user class.
        '''
        pass




class MergedFileSysDest(lx.object.MergedFileSysDest):

        '''
        Empty MergedFileSysDest Python user class.
        '''
        pass




class DirBrowserBasePathEntryDest(lx.object.DirBrowserBasePathEntryDest):

        '''
        Empty DirBrowserBasePathEntryDest Python user class.
        '''
        pass





class DrawingOverride(lx.object.DrawingOverride):

        '''
        Empty DrawingOverride user classes.
        '''
        pass





class Drop(lx.object.Drop):
        pass




class AddDropAction(lx.object.AddDropAction):
        pass




class DropPreviewDefault(lx.object.DropPreviewDefault):
        pass







class Envelope(lx.object.Envelope):

        '''
        Empty Envelope Python user class.
        '''
        pass




class Keyframe(lx.object.Keyframe):

        '''
        Empty Keyframe Python user class.
        '''
        pass




class GradientFilter(lx.object.GradientFilter):

        '''
        Empty GradientFilter Python user class.
        '''
        pass





class ExternalRender(lx.object.ExternalRender):

        '''
        Empty External Render Python user class.
        '''
        pass




class ExternalRenderNotifier(lx.object.ExternalRenderNotifier):
        pass





class VirtualDevice(lx.object.VirtualDevice):

        '''
        Empty VirtualDevice Python user class.
        '''
        pass




class FileReference(lx.object.FileReference):
        pass




class FileRedirect(lx.object.FileRedirect):
        pass





class EvaluationStack(lx.object.EvaluationStack):

        '''
        Empty EvaluationStack Python user class.
        '''
        pass




class StackFilter(lx.object.StackFilter):

        '''
        Empty StackFilter Python user class.
        '''
        pass




class CacheData(lx.object.CacheData):

        '''
        Empty CacheData Python user class.
        '''
        pass







class Force(lx.object.Force):

        '''
        Empty Force Python user class.
        '''
        pass





class GroupItem(lx.object.GroupItem):

        '''
        Empty GroupItem Python user class.
        '''
        pass




class GroupEnumerator(lx.object.GroupEnumerator):

        '''
        Empty GroupEnumerator Python user class.
        '''
        pass





class GroupDest(lx.object.GroupDest):

        '''
        Empty GroupDest Python user class.
        '''
        pass




class GroupMemberItemDest(lx.object.GroupMemberItemDest):

        '''
        Empty GroupMemberItemDest Python user class.
        '''
        pass




class GroupMemberChanDest(lx.object.GroupMemberChanDest):

        '''
        Empty GroupMemberChanDest Python user class.
        '''
        pass





class ShapeDraw(lx.object.ShapeDraw):

        '''
        Empty ShapeDraw Python user class.
        '''
        pass




class HandleDraw(lx.object.HandleDraw):

        '''
        Empty HandleDraw Python user class.
        '''
        pass




class EventTranslatePacket(lx.object.EventTranslatePacket):

        '''
        Empty EventTranslatePacket Python user class.
        '''
        pass




class EventGuide(lx.object.EventGuide):

        '''
        Empty EventGuide Python user class.
        '''
        pass





class Image(lx.object.Image):
        def IsFloat(self):
            return (self.Format() & lx.symbol.fIMD_MASK) == lx.symbol.iIMD_FLOAT

        def Components(self):
            return self.Format() & lx.symbol.fIMV_MASK




class ImageSegment(lx.object.ImageSegment):

        '''
        Empty ImageSegment Python user class.
        '''
        pass




class ImageWrite(lx.object.ImageWrite):
        def IsFloat(self):
            return (self.Format() & lx.symbol.fIMD_MASK) == lx.symbol.iIMD_FLOAT

        def Components(self):
            return self.Format() & lx.symbol.fIMV_MASK




class IndexImage(lx.object.IndexImage):
        def IsFloat(self):
            return (self.Format() & lx.symbol.fIMD_MASK) == lx.symbol.iIMD_FLOAT

        def Components(self):
            return self.Format() & lx.symbol.fIMV_MASK




class IndexImageWrite(lx.object.IndexImageWrite):
        def IsFloat(self):
            return (self.Format() & lx.symbol.fIMD_MASK) == lx.symbol.iIMD_FLOAT

        def Components(self):
            return self.Format() & lx.symbol.fIMV_MASK




class LayeredImage(lx.object.LayeredImage):

        '''
        Empty LayeredImage Python user class.
        '''
        pass




class LayeredImageWrite(lx.object.LayeredImageWrite):

        '''
        Empty LayeredImageWrite Python user class.
        '''
        pass




class TileImage(lx.object.TileImage):

        '''
        Empty TileImage Python user class.
        '''
        pass




class ImageLoaderTarget(lx.object.ImageLoaderTarget):

        '''
        Empty ImageLoaderTarget Python user class.
        '''
        pass




class ImageLevelSample(lx.object.ImageLevelSample):

        '''
        Empty ImageLevelSample Python user class.
        '''
        pass




class ImageFilter(lx.object.ImageFilter):

        '''
        Empty ImageFilter Python user class.
        '''
        pass




class ImageFilterMetrics(lx.object.ImageFilterMetrics):

        '''
        Empty ImageFilterMetrics Python user class.
        '''
        pass





class ImageMonitor(lx.object.ImageMonitor):

        '''
        Empty ImageMonitor Python user class.
        '''
        pass







class InputDevices(lx.object.InputDevices):

        '''
        Empty InputDevices Python user class.
        '''
        pass




class InputDeviceInstance(lx.object.InputDeviceInstance):

        '''
        Empty InputDeviceInstance Python user class.
        '''
        pass





class Interviewer(lx.object.Interviewer):

        '''
        Empty Interviewer Python user class.
        '''
        pass





class IntRange(lx.object.IntRange):

        '''
        Empty IntRange Python user class.
        '''
        pass





class BlockRead(lx.object.BlockRead):

        '''
        Empty BlockRead Python user class.
        '''
        pass




class BlockWrite(lx.object.BlockWrite):

        '''
        Empty BlockWrite Python user class.
        '''
        pass




class LoaderInfo(lx.object.LoaderInfo):

        '''
        Empty LoaderInfo Python user class.
        '''
        pass




class Loader(lx.object.Loader):

        '''
        Empty Loader Python user class.
        '''
        pass




class Saver(lx.object.Saver):

        '''
        Empty Saver Python user class.
        '''
        pass




class Monitor(lx.object.Monitor):

        '''
        Similar methods for Python.
        '''
        def Init(self, count):
            if self.test(): self.Initialize(count)

        def Step(self):
            if self.test(): self.Increment(1)




class StreamIO(lx.object.StreamIO):

        '''
        Empty StreamIO Python user class.
        '''
        pass




class BlockStore(lx.object.BlockStore):
        pass





class SceneSubset(lx.object.SceneSubset):
    pass




class Scene(lx.object.Scene):

        '''
        Likewise in python.
        '''
        def from_item(self, item):
            """Set the scene wrapper from an item: scene.from_item(item)
            """
            self.set(item.Context())

        '''
        In python the list of all items of a given type can be read.
        '''
        def ItemList(self, type):
            """list of items = ItemList(type)
            """
            return [ self.ItemByIndex(type,i) for i in range(self.ItemCount(type)) ]




class Item(lx.object.Item):

        '''
        This python method returns true if an item matches or inherits from a given 
        type. The type can be passed as a type code or string.
        '''
        def IsA(self, type):
            if isinstance(type, str):
                type = lx.service.Scene().ItemTypeLookup(type)

            return self.TestType(type)

        '''
        This returns the list of all children of this item.
        '''
        def SubList(self):
            """list of sub-items = SubList()
            """
            return [ self.SubByIndex(i) for i in range(self.SubCount()) ]

        '''
        This returns a list of the names of all channels on the item.
        '''
        def ChannelList(self):
            """list of channel names = ChannelList()
            """
            return [ self.ChannelName(i) for i in range(self.ChannelCount()) ]

        '''
        Reading channel values can be done using the Python user wrapper class. It
        maintains a channel_read attribute that can be used for reading channels
        directly on the channel item.
        Reset the item so it has no read attribute.
        '''
        def ReadNone(self):
            if hasattr(self, 'channel_read'):
                del self.channel_read

        '''
        Set the item to read from a named action.
        '''
        def ReadAction(self, name=lx.symbol.s_ACTIONLAYER_EDIT, time=0.0):
            """Read channel values from named action: ReadAction(<name>, <time>)
            """
            self.ReadNone()
            self.channel_read = self.Context().Channels(name, time)

        '''
        Set the item to read from a setup mode.
        '''
        def ReadSetup(self):
            """Read evaluted channel values from setup: ReadSetup()
            """
            self.ReadNone()
            self.channel_read = self.Context().SetupChannels()

        '''
        Set the item to read evaluated channels.
        '''
        def ReadEvaluated(self, time=0.0):
            """Read evaluated channel values: ReadEvaluated(<time>)
            """
            self.ReadAction(None, time)

        '''
        Once set, channel values can be read using the user method Value() on the
        channel_read object.
        Read the channel value using bracket syntax.
        '''
        def __getitem__(self, index):
            """Read channel values: val = item[channel]
            """
            return self.ChannelValue(index)

        '''
        Read the channel value.
        '''
        def ChannelValue(self, index):
            """Read channel values: val = ChannelValue(channel)
            Channel can be given by name or index.
            """
            if not hasattr(self, 'channel_read'):
                raise RuntimeError('Item wrapper not set for reading')

            return self.channel_read.Value(self, index)

        '''
        Likewise writing sets the channel_write attribute which is then used for
        writing.
        Set the item to write to a named action.
        '''
        def WriteAction(self, name=lx.symbol.s_ACTIONLAYER_EDIT, time=0.0):
            """Write channel values to named action: WriteAction(<name>, <time>)
            """
            if hasattr(self, 'channel_write'):
                del self.channel_write

            self.channel_write = ChannelWrite(self.Context().Channels(name, time))

        '''
        Set the value of a channel using bracket syntax.
        '''
        def __setitem__(self, index, value):
            """Set channel values: item[channel] = val
            """
            return self.SetChannel(index, value)

        '''
        Set the value of a channel.
        '''
        def SetChannel(self, index, value, key=False):
            """Set channel values: SetChannel(channel, value, <key>)
            Channel can be given by name or index. Set key to true to make a keyframe.
            """
            if not hasattr(self, 'channel_write'):
                raise RuntimeError('Item wrapper not set for writing')

            return self.channel_write.Set(self, index, value, key)




class SceneGraph(lx.object.SceneGraph):

        '''
        Empty SceneGraph Python user class.
        '''
        pass




class ItemGraph(lx.object.ItemGraph):

        '''
        Empty ItemGraph Python user class.
        '''
        pass




class ChannelGraph(lx.object.ChannelGraph):

        '''
        Empty ChannelGraph Python user class.
        '''
        pass





class LocatorDest(lx.object.LocatorDest):
        pass




class MeshOpDest(lx.object.MeshOpDest):
        pass




class MeshDest(lx.object.MeshDest):
        pass




class ChannelDest(lx.object.ChannelDest):
        pass




class ChannelDropPreview(lx.object.ChannelDropPreview):
        pass




class ItemTypeDest(lx.object.ItemTypeDest):
        pass





class LayerScan(lx.object.LayerScan):

        '''
        Empty LayerScan Python user class.
        '''
        pass




class TransformScan(lx.object.TransformScan):

        '''
        Empty TransformScan Python user class.
        '''
        pass







class ItemListType(lx.object.ItemListType):
        pass





class ListenerPort(lx.object.ListenerPort):

        '''
        Empty ListenerPort Python user class.
        '''
        pass





class Locator(lx.object.Locator):

        '''
        Empty Locator Python user class.
        '''
        pass





class LogInfoBlock(lx.object.LogInfoBlock):

        '''
        Empty LogInfoBlock Python user class.
        '''
        pass




class Log(lx.object.Log):

        '''
        Empty Log Python user class.
        '''
        pass




class LogEntry(lx.object.LogEntry):

        '''
        Empty LogEntry Python user class.
        '''
        pass




class LogListener(lx.object.LogListener):

        '''
        Empty LogListener Python user class.
        '''
        pass





class VideoClipItem(lx.object.VideoClipItem):

        '''
        Empty VideoClipItem Python user class.
        '''
        pass





class View(lx.object.View):

        '''
        Empty View Python user class.
        '''
        pass




class StrokeDraw(lx.object.StrokeDraw):

        '''
        Empty StrokeDraw Python user class.
        '''
        pass




class GLMaterial(lx.object.GLMaterial):

        '''
        Empty GLMaterial Python user class.
        '''
        pass




class GLImage(lx.object.GLImage):

        '''
        Empty GLImage Python user class.
        '''
        pass





class Tree(lx.object.Tree):

        '''
        Empty Tree Python user class.
        '''
        pass




class TreeListener(lx.object.TreeListener):
        pass





class AudioLoaderTarget(lx.object.AudioLoaderTarget):

        '''
        Empty AudioLoaderTarget Python user class.
        '''
        pass




class Audio(lx.object.Audio):

        '''
        Empty Audio Python user class.
        '''
        pass




class AudioWrite(lx.object.AudioWrite):

        '''
        Empty AudioWrite Python user class.
        '''
        pass




class AudioDevice(lx.object.AudioDevice):

        '''
        Empty AudioDevice Python user class.
        '''
        pass




class AudioHandle(lx.object.AudioHandle):

        '''
        Empty AudioHandle Python user class.
        '''
        pass





class Mesh(lx.object.Mesh):

        '''
        Empty Mesh Python user class.
        '''
        pass




class Point(lx.object.Point):

        '''
        Empty Point Python user class.
        '''
        pass




class Polygon(lx.object.Polygon):

        '''
        Empty Polygon Python user class.
        '''
        pass




class Edge(lx.object.Edge):

        '''
        Empty Edge Python user class.
        '''
        pass




class MeshMap(lx.object.MeshMap):

        '''
        Empty MeshMap Python user class.
        '''
        pass




class MeshTracker(lx.object.MeshTracker):

        '''
        Empty MeshTracker Python user class.
        '''
        pass




class MeshOperation(lx.object.MeshOperation):

        '''
        Empty Mesh Operation Python user class.
        '''
        pass




class MeshFilter(lx.object.MeshFilter):

        '''
        Empty MeshFilter Python user class.
        '''
        pass




class MeshFilterBBox(lx.object.MeshFilterBBox):

        '''
        Empty MeshFilterBBox Python user class.
        '''
        pass




class MeshFilterIdent(lx.object.MeshFilterIdent):

        '''
        Empty MeshFilterIdent Python user class.
        '''
        pass




class MeshFilterBlend(lx.object.MeshFilterBlend):

        '''
        Empty MeshFilterBlend Python user class.
        '''
        pass




class MeshBlend(lx.object.MeshBlend):

        '''
        Empty MeshBlend Python user class.
        '''
        pass




class MeshXtraData(lx.object.MeshXtraData):

        '''
        Empty MeshXtraData Python user class.
        '''
        pass





class AutoSaveListener(lx.object.AutoSaveListener):

        '''
        Empty AutoSaveListener Python user class.
        '''
        pass








class Notifier(lx.object.Notifier):

        '''
        Empty Notifier Python user class.
        '''
        pass





class SceneEvalListener(lx.object.SceneEvalListener):

        '''
        Empty SceneEvalListener Python user class.
        '''
        pass




class SceneItemListener(lx.object.SceneItemListener):

        '''
        Empty SceneItemListener Python user class.
        '''
        pass




class SceneLoaderTarget(lx.object.SceneLoaderTarget):

        '''
        Empty SceneLoaderTarget Python user class.
        '''
        pass




class Package(lx.object.Package):

        '''
        Empty Package Python user class.
        '''
        pass




class AddChannel(lx.object.AddChannel):

        '''
        Empty AddChannel Python user class.
        '''
        pass




class ItemCollection(lx.object.ItemCollection):

        '''
        Python method gets list of items.
        '''
        def ItemList(self):
            """list of items = ItemList()
            """
            return [ self.ByIndex(lx.symbol.iTYPE_ANY,i) for i in range(self.Count(lx.symbol.iTYPE_ANY)) ]




class PackageInstance(lx.object.PackageInstance):
        pass





class ParticleItem(lx.object.ParticleItem):

        '''
        Empty ParticleItem Python user class.
        '''
        pass




class ReplicatorEnumerator(lx.object.ReplicatorEnumerator):

        '''
        Empty ReplicatorEnumerator Python user class.
        '''
        pass




class ParticleEvalFrame(lx.object.ParticleEvalFrame):
        pass




class ParticleFilter(lx.object.ParticleFilter):

        '''
        Empty ParticleFilter Python user class.
        '''
        pass




class ParticleCoOperator(lx.object.ParticleCoOperator):

        '''
        Empty ParticleCoOperator Python user class.
        '''
        pass




class PointCacheItem(lx.object.PointCacheItem):

        '''
        Empty PointCacheItem Python user class.
        '''
        pass







class Pattern(lx.object.Pattern):

        '''
        Empty Pattern Python user class.
        '''
        pass





class PersistenceClient(lx.object.PersistenceClient):

        '''
        Empty PersistenceClient Python user class.
        '''
        pass




class PersistentEntry(lx.object.PersistentEntry):

        '''
        Empty PersistentEntry Python user class.
        '''
        pass





class MeshElementGroup(lx.object.MeshElementGroup):

        '''
        Empty Mesh Element Group Python user class.
        '''
        pass




class SelectionOperation(lx.object.SelectionOperation):

        '''
        Empty Selection Operation Python user class.
        '''
        pass




class SelectionState(lx.object.SelectionState):

        '''
        Empty Selection State Python user class.
        '''
        pass





class ShaderPreDest(lx.object.ShaderPreDest):

        '''
        Empty ShaderPreDest Python user class.
        '''
        pass




class MeshLayerPreDest(lx.object.MeshLayerPreDest):

        '''
        Empty MeshLayerPreDest Python user class.
        '''
        pass




class SceneItemPreDest(lx.object.SceneItemPreDest):

        '''
        Empty SceneItemPreDest Python user class.
        '''
        pass




class Profile1DPreDest(lx.object.Profile1DPreDest):

        '''
        Empty Profile1DPreDest Python user class.
        '''
        pass




class Profile2DPreDest(lx.object.Profile2DPreDest):

        '''
        Empty Profile2DPreDest Python user class.
        '''
        pass




class ColorPreDest(lx.object.ColorPreDest):

        '''
        Empty ColorPreDest Python user class.
        '''
        pass







class PresetLoaderTarget(lx.object.PresetLoaderTarget):

        '''
        Empty PresetLoaderTarget Python user class.
        '''
        pass




class PresetType(lx.object.PresetType):

        '''
        Empty PresetType Python user class.
        '''
        pass




class PresetMetrics(lx.object.PresetMetrics):

        '''
        Empty PresetMetrics Python user class.
        '''
        pass




class PresetDo(lx.object.PresetDo):

        '''
        Empty PresetDo Python user class.
        '''
        pass




class PresetBrowserSource(lx.object.PresetBrowserSource):

        '''
        Empty PresetBrowserSource Python user class.
        '''
        pass







class Preview(lx.object.Preview):

        '''
        Empty Preview Python user class.
        '''
        pass




class PreviewNotifier(lx.object.PreviewNotifier):
        pass





class ProjDirOverride(lx.object.ProjDirOverride):

        '''
        Empty ProjDirOverride Python user class.
        '''
        pass





class SceneContents(lx.object.SceneContents):

        '''
        Empty SceneContents Python user class.
        '''
        pass




class ProxyOptions(lx.object.ProxyOptions):

        '''
        Empty ProxyOptions Python user class.
        '''
        pass





class PolygonSlice(lx.object.PolygonSlice):
        pass




class SolidDrill(lx.object.SolidDrill):
        pass





class Raycast(lx.object.Raycast):

        '''
        Empty Raycast Python user class.
        '''
        pass




class Lighting(lx.object.Lighting):

        '''
        Empty Lighting Python user class.
        '''
        pass





class RenderJob(lx.object.RenderJob):

        '''
        Empty RenderJob Python user class.
        '''
        pass




class RenderProgressListener(lx.object.RenderProgressListener):

        '''
        Empty RenderProgressListener Python user class.
        '''
        pass




class RenderStats(lx.object.RenderStats):

        '''
        Empty RenderStats Python user class.
        '''
        pass




class Buffer(lx.object.Buffer):

        '''
        Empty Buffer Python user class.
        '''
        pass




class ImageProcessing(lx.object.ImageProcessing):

        '''
        Empty ImageProcessing Python user class.
        '''
        pass




class ImageProcessingListener(lx.object.ImageProcessingListener):

        '''
        Empty ImageProcessingListener Python user class.
        '''
        pass




class ImageProcessingRead(lx.object.ImageProcessingRead):

        '''
        Empty ImageProcessingRead Python user class.
        '''
        pass







class SchematicConnection(lx.object.SchematicConnection):

        '''
        Empty SchematicConnection Python user class.
        '''
        pass




class SchemaDest(lx.object.SchemaDest):

        '''
        Empty SchemaDest Python user class.
        '''
        pass




class SchematicGroup(lx.object.SchematicGroup):

        '''
        Empty Schematic Group Python user class.
        '''
        pass




class SchematicNode(lx.object.SchematicNode):

        '''
        Empty Schematic Node Python user class.
        '''
        pass





class UserValue(lx.object.UserValue):

        '''
        Empty UserValue Python user class.
        '''
        pass




class Kit(lx.object.Kit):

        '''
        Empty Kit Python user class.
        '''
        pass




class SessionListener(lx.object.SessionListener):

        '''
        Empty SessionListener Python user class.
        '''
        pass




class UserValueListener(lx.object.UserValueListener):

        '''
        Empty UserValueListener Python user class.
        '''
        pass




class ScriptManager(lx.object.ScriptManager):
        pass




class TextScriptInterpreter(lx.object.TextScriptInterpreter):

        '''
        Empty TextScriptInterpreter Python user class.
        '''
        pass




class Script(lx.object.Script):

        '''
        Empty Script Python user class.
        '''
        pass




class AppActiveListener(lx.object.AppActiveListener):

        '''
        Empty AppActiveListener Python user class.
        '''
        pass




class LineInterpreter(lx.object.LineInterpreter):

        '''
        Empty LineInterpreter Python user class.
        '''
        pass




class LineExecution(lx.object.LineExecution):

        '''
        Empty LineExecution Python user class.
        '''
        pass




class ScriptLineEvent(lx.object.ScriptLineEvent):

        '''
        That's all there is to it.
        Empty ScriptLineEvent Python user class.
        '''
        pass





class SelectionType(lx.object.SelectionType):

        '''
        Empty SelectionType Python user class.
        '''
        pass




class SelectionListener(lx.object.SelectionListener):

        '''
        Empty SelectionListener Python user class.
        '''
        pass







class ScenePacketTranslation(lx.object.ScenePacketTranslation):

        '''
        Empty ScenePacketTranslation Python user class.
        '''
        pass




class ItemPacketTranslation(lx.object.ItemPacketTranslation):

        '''
        Empty ItemPacketTranslation Python user class.
        '''
        pass




class NodePacketTranslation(lx.object.NodePacketTranslation):

        '''
        Empty NodePacketTranslation Python user class.
        '''
        pass




class ChannelPacketTranslation(lx.object.ChannelPacketTranslation):

        '''
        Empty ChannelPacketTranslation Python user class.
        '''
        pass




class CenterPacketTranslation(lx.object.CenterPacketTranslation):

        '''
        Empty CenterPacketTranslation Python user class.
        '''
        pass




class PivotPacketTranslation(lx.object.PivotPacketTranslation):

        '''
        Empty PivotPacketTranslation Python user class.
        '''
        pass




class LinkPacketTranslation(lx.object.LinkPacketTranslation):

        '''
        Empty LinkPacketTranslation Python user class.
        '''
        pass




class ActionLayerPacketTranslation(lx.object.ActionLayerPacketTranslation):

        '''
        Empty ActionLayerPacketTranslation Python user class.
        '''
        pass




class VertexPacketTranslation(lx.object.VertexPacketTranslation):

        '''
        Empty VertexPacketTranslation Python user class.
        '''
        pass




class EdgePacketTranslation(lx.object.EdgePacketTranslation):

        '''
        Empty EdgePacketTranslation Python user class.
        '''
        pass




class PolygonPacketTranslation(lx.object.PolygonPacketTranslation):

        '''
        Empty PolygonPacketTranslation Python user class.
        '''
        pass




class VMapPacketTranslation(lx.object.VMapPacketTranslation):

        '''
        Empty VMapPacketTranslation Python user class.
        '''
        pass




class PresetPathPacketTranslation(lx.object.PresetPathPacketTranslation):

        '''
        Empty PresetPathPacketTranslation Python user class.
        '''
        pass




class ItemChannel(lx.object.ItemChannel):

        '''
        Empty ILxItemChannel Python user class.
        '''
        pass




class VectorShapePacketTranslation(lx.object.VectorShapePacketTranslation):

        '''
        Empty VectorShapePacketTranslation Python user class.
        '''
        pass




class VectorPathPacketTranslation(lx.object.VectorPathPacketTranslation):

        '''
        Empty VectorPathPacketTranslation Python user class.
        '''
        pass




class VectorKnotPacketTranslation(lx.object.VectorKnotPacketTranslation):

        '''
        Empty VectorKnotPacketTranslation Python user class.
        '''
        pass





class Factory(lx.object.Factory):

        '''
        Empty Factory Python user class.
        '''
        pass




class Module(lx.object.Module):

        '''
        Empty Module Python user class.
        '''
        pass




class TagDescription(lx.object.TagDescription):

        '''
        Empty TagDescription Python user class.
        '''
        pass




class NeedContext(lx.object.NeedContext):

        '''
        Empty NeedContext Python user class.
        '''
        pass





class ValueTexture(lx.object.ValueTexture):

        '''
        Empty ValueTexture Python user class.
        '''
        pass




class ValueTextureCustom(lx.object.ValueTextureCustom):

        '''
        Empty ValueTextureCustom Python user class.
        '''
        pass




class Texture(lx.object.Texture):

        '''
        Empty Texture Python user class.
        '''
        pass




class CompShader(lx.object.CompShader):

        '''
        Empty CompShader Python user class.
        '''
        pass




class CustomMaterial(lx.object.CustomMaterial):

        '''
        Empty CustomMaterial Python user class.
        '''
        pass





class Shader(lx.object.Shader):

        '''
        Empty Shader Python user class.
        '''
        pass





class AsyncMonitorInfo(lx.object.AsyncMonitorInfo):

        '''
        Empty AsyncMonitorInfo Python user class.
        '''
        pass




class AsyncMonitorSystem(lx.object.AsyncMonitorSystem):

        '''
        Empty AsyncMonitorSystem Python user class.
        '''
        pass




class ColorDialog(lx.object.ColorDialog):

        '''
        Empty ColorDialog Python user class.
        '''
        pass







class SurfaceItem(lx.object.SurfaceItem):

        '''
        Empty SurfaceItem Python user class.
        '''
        pass




class Surface(lx.object.Surface):

        '''
        Empty Surface Python user class.
        '''
        pass




class SurfaceBin(lx.object.SurfaceBin):

        '''
        Empty SurfaceBin Python user class.
        '''
        pass




class CurveGroup(lx.object.CurveGroup):

        '''
        Empty CurveGroup Python user class.
        '''
        pass




class Curve(lx.object.Curve):

        '''
        Empty Curve Python user class.
        '''
        pass





class Tableau(lx.object.Tableau):

        '''
        Empty Tableau Python user class.
        '''
        pass




class TableauElement(lx.object.TableauElement):

        '''
        Empty TableauElement Python user class.
        '''
        pass




class TableauSurface(lx.object.TableauSurface):

        '''
        Empty TableauSurface Python user class.
        '''
        pass




class TriangleSoup(lx.object.TriangleSoup):

        '''
        Empty TriangleSoup Python user class.
        '''
        pass




class TableauVolume(lx.object.TableauVolume):

        '''
        Empty TableauVolume Python user class.
        '''
        pass




class TableauLight(lx.object.TableauLight):

        '''
        Empty TableauLight Python user class.
        '''
        pass




class LightSample(lx.object.LightSample):

        '''
        Empty LightSample Python user class.
        '''
        pass




class TableauProxy(lx.object.TableauProxy):

        '''
        Empty TableauProxy Python user class.
        '''
        pass




class TableauInstance(lx.object.TableauInstance):

        '''
        Empty TableauInstance Python user class.
        '''
        pass




class TableauShader(lx.object.TableauShader):

        '''
        Empty TableauShader Python user class.
        '''
        pass




class ShaderSlice(lx.object.ShaderSlice):

        '''
        Empty ShaderSlice Python user class.
        '''
        pass




class TableauSource(lx.object.TableauSource):

        '''
        Empty TableauSource Python user class.
        '''
        pass







class DTBBadgeOverride(lx.object.DTBBadgeOverride):

        '''
        Empty Command Python user class.
        '''
        pass




class DTBGroupSortOverride(lx.object.DTBGroupSortOverride):

        '''
        Empty Command Python user class.
        '''
        pass





class Tool(lx.object.Tool):

        '''
        Empty Tool Python user class.
        '''
        pass




class AttrSequence(lx.object.AttrSequence):

        '''
        Empty AttrSequence Python user class.
        '''
        pass




class ToolOperation(lx.object.ToolOperation):

        '''
        Empty Tool Operation Python user class.
        '''
        pass




class FalloffPacket(lx.object.FalloffPacket):

        '''
        Empty FalloffPacket Python user class.
        '''
        pass




class SymmetryPacket(lx.object.SymmetryPacket):

        '''
        Empty SymmetryPacket Python user class.
        '''
        pass




class Subject2Packet(lx.object.Subject2Packet):

        '''
        Empty Subject2Packet Python user class.
        '''
        pass




class TexturePacket(lx.object.TexturePacket):

        '''
        Empty TexturePacket Python user class.
        '''
        pass




class ElementAxisPacket(lx.object.ElementAxisPacket):

        '''
        Empty ElementAxisPacket Python user class.
        '''
        pass




class ElementCenterPacket(lx.object.ElementCenterPacket):

        '''
        Empty ElementCenterPacket Python user class.
        '''
        pass




class BagGenerator(lx.object.BagGenerator):

        '''
        Empty BagGenerator Python user class.
        '''
        pass




class PathStep(lx.object.PathStep):

        '''
        Empty PathStep Python user class.
        '''
        pass




class PathGeneratorPacket(lx.object.PathGeneratorPacket):

        '''
        Empty PathGeneratorPacket Python user class.
        '''
        pass




class ParticleGeneratorPacket(lx.object.ParticleGeneratorPacket):

        '''
        Empty ParticleGeneratorPacket Python user class.
        '''
        pass





class RaycastPacket(lx.object.RaycastPacket):

        '''
        Empty RaycastPacket Python user class.
        '''
        pass




class PaintBrushPacket(lx.object.PaintBrushPacket):

        '''
        Empty PaintBrushPacket Python user class.
        '''
        pass




class PaintInkPacket(lx.object.PaintInkPacket):

        '''
        Empty PaintInkPacket Python user class.
        '''
        pass




class PaintNozzlePacket(lx.object.PaintNozzlePacket):

        '''
        Empty PaintNozzlePacket Python user class.
        '''
        pass





class TreeView(lx.object.TreeView):

        '''
        Empty TreeView Python user class.
        '''
        pass





class TriangleSurface(lx.object.TriangleSurface):

        '''
        Empty TriangleSurface Python user class.
        '''
        pass




class TriangleGroup(lx.object.TriangleGroup):

        '''
        Empty TriangleGroup Python user class.
        '''
        pass





class Undo(lx.object.Undo):

        '''
        Empty Undo Python user class.
        '''
        pass







class Value(lx.object.Value):

        '''
        The Python user class add Get() and Set() methods that try to hide type conversions.
        '''
        def Get(self):
            tp = self.Type()
            if tp == lx.symbol.i_TYPE_INTEGER:
                return self.GetInt()
            if tp == lx.symbol.i_TYPE_FLOAT:
                return self.GetFlt()
            if tp == lx.symbol.i_TYPE_STRING:
                return self.GetString()

            raise TypeError("can't get object values")

        def __str__(self):
            return str(self.Get())

        def Set(self, value):
            tp = self.Type()
            if tp == lx.symbol.i_TYPE_INTEGER:
                self.SetInt(int(value))
            elif tp == lx.symbol.i_TYPE_FLOAT:
                self.SetFlt(float(value))
            elif tp == lx.symbol.i_TYPE_STRING:
                self.SetString(str(value))
            else:
                raise TypeError("can't set object values");




class StringConversion(lx.object.StringConversion):

        '''
        Empty StringConversion Python user class.
        '''
        pass




class StringConversionNice(lx.object.StringConversionNice):

        '''
        Empty StringConversionNice Python user class.
        '''
        pass




class ValueMath(lx.object.ValueMath):

        '''
        Empty ValueMath Python user class.
        '''
        pass




class ValueReference(lx.object.ValueReference):

        '''
        Empty ValueReference Python user class.
        '''
        pass




class ValueConversion(lx.object.ValueConversion):

        '''
        Empty ValueConversion Python user class.
        '''
        pass




class Attributes(lx.object.Attributes):

        '''
        In Python we can get all the attribute names in a list.
        '''
        def NameList(self):
            return [ self.Name(i) for i in range(self.Count()) ]

        '''
        The Python user class adds Get() and Set() methods that infer the type of the
        attribute. The index can also be given as the name of the attribute.
        '''
        def Get(self, index):
            if isinstance(index, str):
                index = self.Lookup(index)

            tp = self.Type(index)
            if tp == lx.symbol.i_TYPE_INTEGER:
                return self.GetInt(index)
            if tp == lx.symbol.i_TYPE_FLOAT:
                return self.GetFlt(index)
            if tp == lx.symbol.i_TYPE_STRING:
                return self.GetString(index)

            return self.Value(index, 0)

        def Set(self, index, value):
            if isinstance(index, str):
                index = self.Lookup(index)

            tp = self.Type(index)
            if tp == lx.symbol.i_TYPE_INTEGER:
                self.SetInt(index, value)
            elif tp == lx.symbol.i_TYPE_FLOAT:
                self.SetFlt(index, value)
            elif tp == lx.symbol.i_TYPE_STRING:
                self.SetString(index, value)
            else:
                raise TypeError("can't set object type values")

        '''
        We also allow 'val = attr[index]' and 'attr[index] = val'.
        '''
        def __getitem__(self, index):
            return self.Get(index)

        def __setitem__(self, index, value):
            self.Set(index, value)




class Message(lx.object.Message):

        '''
        The Python SetArg() method passes every value as a string using repr(). We also
        allow 'msg[1] = "Hello"'.
        '''
        def SetArg(self, arg, value):
            self.SetArgumentString(arg, repr(value))

        def __setitem__(self, arg, value):
            self.SetArgumentString(arg, repr(value))




class ValueArray(lx.object.ValueArray):

        '''
        In Python we support 'x = array[i]', and 'array + x' for appending atomic value types.
        '''
        def __getitem__(self, index):
            tp = self.Type()
            if tp == lx.symbol.i_TYPE_INTEGER:
                return self.GetInt(index)
            if tp == lx.symbol.i_TYPE_FLOAT:
                return self.GetFloat(index)
            if tp == lx.symbol.i_TYPE_STRING:
                return self.GetString(index)
            else:
                return self.GetValue(index)

        def __add__(self, value):
            tp = self.Type()
            if tp == lx.symbol.i_TYPE_INTEGER:
                self.AddInt(value)
            elif tp == lx.symbol.i_TYPE_FLOAT:
                self.AddFloat(value)
            elif tp == lx.symbol.i_TYPE_STRING:
                self.AddString(value)
            else:
                self.AddValue(value)

        '''
        We also support iteration to allow the "for" syntax.
        '''
        def __iter__(self):
            for i in range(self.Count()):
                yield self[i]




class ScriptQuery(lx.object.ScriptQuery):

        '''
        Empty ScriptQuery Python user class.
        '''
        pass




class StringTag(lx.object.StringTag):

        '''
        Empty StringTag Python user class.
        '''
        pass




class Matrix(lx.object.Matrix):

        '''
        Empty Matrix Python user class.
        '''
        pass




class Quaternion(lx.object.Quaternion):

        '''
        Empty Quaternion Python user class.
        '''
        pass




class Visitor(lx.object.Visitor):

        '''
        Empty Visitor Python user class.
        '''
        pass




class TextEncoding(lx.object.TextEncoding):

        '''
        Empty TextEncoding Python user class.
        '''
        pass







class Variation(lx.object.Variation):

        '''
        Empty Variation Python user class.
        '''
        pass







class VectorType(lx.object.VectorType):

        '''
        Empty VectorType Python user class.
        '''
        pass




class VectorList(lx.object.VectorList):

        '''
        Empty VectorList Python user class.
        '''
        pass




class VectorStack(lx.object.VectorStack):

        '''
        Empty VectorStack Python user class.
        '''
        pass




class TextureEffect(lx.object.TextureEffect):

        '''
        Empty TextureEffect Python user class.
        '''
        pass




class PacketEffect(lx.object.PacketEffect):

        '''
        Empty PacketEffect Python user class.
        '''
        pass





class VectorCanvas(lx.object.VectorCanvas):

        '''
        Empty Vector Canvas Python user class.
        '''
        pass




class VectorShape(lx.object.VectorShape):

        '''
        Empty Vector Shape Python user class.
        '''
        pass




class VectorPath(lx.object.VectorPath):

        '''
        Empty Vector Path Python user class.
        '''
        pass




class VectorListener(lx.object.VectorListener):

        '''
        Empty Vector Listener Python user class.
        '''
        pass





class TableauVertex(lx.object.TableauVertex):

        '''
        Empty TableauVertex Python user class.
        '''
        pass







class ViewObject(lx.object.ViewObject):

        '''
        Empty View Object Python user class.
        '''
        pass





class ViewItem3D(lx.object.ViewItem3D):

        '''
        Empty ViewItem3D Python user class.
        '''
        pass




class VirtualModel(lx.object.VirtualModel):

        '''
        Empty VirtualModel Python user class.
        '''
        pass




class ToolModel(lx.object.ToolModel):

        '''
        Empty ToolModel Python user class.
        '''
        pass




class AdjustTool(lx.object.AdjustTool):

        '''
        Empty AdjustTool Python user class.
        '''
        pass




class NavigationListener(lx.object.NavigationListener):

        '''
        Empty NavigationListener Python user class.
        '''
        pass





class Raymarch(lx.object.Raymarch):

        '''
        Empty Raymarch Python user class.
        '''
        pass





class View3D(lx.object.View3D):

        '''
        Empty View3D Python user class.
        '''
        pass




class SimulationListener(lx.object.SimulationListener):
        pass




