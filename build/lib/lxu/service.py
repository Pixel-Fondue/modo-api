#   Copyright (c) 2001-2021, The Foundry Group LLC
#   All Rights Reserved. Patents granted and pending.
#
import lx





class AudioAnim(lx.service.AudioAnim):

        '''
        Empty AudioAnim service Python user class.
        '''
        pass



class ChannelUI(lx.service.ChannelUI):

        '''
        Empty ChannelUI service Python user class.
        '''
        pass




class ColorMapping(lx.service.ColorMapping):
        pass



class GUID(lx.service.GUID):

        '''
        Empty GUID service Python user class.
        '''
        pass



class Command(lx.service.Command):

        '''
        Empty Command service Python user class.
        '''
        pass






class Deformer(lx.service.Deformer):

        '''
        Empty Deformer service Python user class.
        '''
        pass



class DirCache(lx.service.DirCache):
        pass






class Drop(lx.service.Drop):
        pass





class File(lx.service.File):

        '''
        Empty File service Python user class.
        '''
        pass





class Cache(lx.service.Cache):

        '''
        Empty CacheData Python user class.
        '''
        pass







class Image(lx.service.Image):

        '''
        Empty Image service Python user class.
        '''
        pass





class ImageMonitor(lx.service.ImageMonitor):

        '''
        Empty ImageMonitor service Python user class.
        '''
        pass



class InputMap(lx.service.InputMap):

        '''
        Empty Command service Python user class.
        '''
        pass







class IO(lx.service.IO):

        '''
        Empty IO service Python user class.
        '''
        pass





class Scene(lx.service.Scene):

        '''
        In python the entire list can be read at once.
        '''
        def ItemTypeList(self):
            """list of types = ItemTypeList()
            """
            return [ self.ItemTypeByIndex(i) for i in range(self.ItemTypeCount()) ]

        '''
        In python all the subtype names can be read as a list.
        '''
        def ItemSubTypeList(self, type):
            """list of sub-types = ItemSubTypeList(type)
            """
            return [ self.ItemSubTypeByIndex(type, i) for i in range(self.ItemSubTypeCount(type)) ]






class Layer(lx.service.Layer):

        '''
        Empty layer service Python user class.
        '''
        pass




class Listener(lx.service.Listener):

        '''
        Empty listener service Python user class.
        '''
        pass






class Log(lx.service.Log):

        '''
        Empty log service Python user class.
        '''
        pass









class Mesh(lx.service.Mesh):

        '''
        Empty mesh service Python user class.
        '''
        pass





class Message(lx.service.Message):

        '''
        Empty message service Python user class.
        '''
        pass





class Network(lx.service.Network):
        pass



class NotifySys(lx.service.NotifySys):

        '''
        Empty notifysys service Python user class.
        '''
        pass






class Particle(lx.service.Particle):

        '''
        Empty particle service Python user class.
        '''
        pass




class Persistence(lx.service.Persistence):

        '''
        Empty persistence service Python user class.
        '''
        pass






class PresetDestination(lx.service.PresetDestination):

        '''
        Empty Python user class
        '''
        pass



class PresetBrowser(lx.service.PresetBrowser):

        '''
        Empty PresetBrowser service Python user class.
        '''
        pass



class Preview(lx.service.Preview):

        '''
        Empty preview service Python user class.
        '''
        pass









class Render(lx.service.Render):

        '''
        Empty render service Python user class.
        '''
        pass




class ImageProcessing(lx.service.ImageProcessing):

        '''
        Empty ImageProcessing service Python user class.
        '''
        pass




class ScriptSys(lx.service.ScriptSys):

        '''
        Empty scriptsys service Python user class.
        '''
        pass




class Platform(lx.service.Platform):

        '''
        Empty platform service Python user class.
        '''
        pass





class Selection(lx.service.Selection):

        '''
        Empty selection service Python user class.
        '''
        pass




class Host(lx.service.Host):

        '''
        Empty Host service Python user class.
        '''
        pass






class Shader(lx.service.Shader):

        '''
        Empty shader service Python user class.
        '''
        pass





class StdDialog(lx.service.StdDialog):

        '''
        Empty StdDialog service Python user class.
        '''
        pass




class Tableau(lx.service.Tableau):

        '''
        Empty tableau service Python user class.
        '''
        pass




class Nodal(lx.service.Nodal):

        '''
        Empty nodal service Python user class.
        '''
        pass








class Undo(lx.service.Undo):

        '''
        Empty undo service Python user class.
        '''
        pass



class Value(lx.service.Value):

        '''
        Empty value service Python user class.
        '''
        pass




class TextEncoding(lx.service.TextEncoding):

        '''
        Empty textencoding service Python user class.
        '''
        pass



class Variation(lx.service.Variation):

        '''
        Empty Variation Service Python user class.
        '''
        pass



class Packet(lx.service.Packet):

        '''
        Empty packet service Python user class.
        '''
        pass






class VertexFeature(lx.service.VertexFeature):

        '''
        Empty vertes service Python user class.
        '''
        pass






class View3Dport(lx.service.View3Dport):
        pass






