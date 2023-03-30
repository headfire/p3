# from core_position import *
from core_style import *

# from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox
# , BRepPrimAPI_MakeCone, \
# BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeTorus
#  from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
# from OCC.Core.BRepTools import BRepTools_WireExplorer
# from OCC.Core.BRep import BRep_Tool
# from OCC.Core.GC import GC_MakeCircle
from OCC.Core.Geom import Geom_CartesianPoint

# from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire,
#                                      BRepBuilderAPI_MakeFace)

from OCC.Core.AIS import AIS_Shape, AIS_Point
from OCC.Core.Quantity import Quantity_Color, Quantity_TypeOfColor
# from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.Graphic3d import Graphic3d_MaterialAspect

from OCC.Display.SimpleGui import init_display


BRASS_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_BRASS
BRONZE_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_BRONZE
COPPER_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_COPPER
GOLD_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_GOLD
PEWTER_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_PEWTER
PLASTER_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_PLASTER
PLASTIC_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_PLASTIC
SILVER_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_SILVER
STEEL_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_STEEL
STONE_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_STONE
SHINY_PLASTIC_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_SHINY_PLASTIC
SATIN_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_SATIN
METALIZED_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_METALIZED
NEON_GNC_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_NEON_GNC
CHROME_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_CHROME
ALUMINIUM_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_ALUMINIUM
OBSIDIAN_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_OBSIDIAN
NEON_PHC_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_NEON_PHC
JADE_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_JADE
CHARCOAL_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_CHARCOAL
WATER_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_WATER
GLASS_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_GLASS
DIAMOND_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_DIAMOND
TRANSPARENT_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_TRANSPARENT
DEFAULT_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_DEFAULT

WOOD_COLOR = 208/255, 117/255, 28/255
PAPER_COLOR = 230/255, 230/255, 230/255
STEEL_COLOR = 100/255, 100/255, 100/255

NICE_WHITE_COLOR = 240/255, 240/255, 240/255
NICE_GRAY_COLOR = 100/255, 100/255, 100/255
NICE_RED_COLOR = 200/255, 30/255, 30/255
NICE_BLUE_COLOR = 100/255, 100/255, 255/255
NICE_YELLOW_COLOR = 255/255, 255/255, 100/255
NICE_ORIGINAL_COLOR = 241/255, 79/255, 160/255

P_RADIUS = 'P_RADIUS'
DEF_RADIUS = 100

P_SHAPE = 'P_SHAPE'
DEF_SHAPE = BRepPrimAPI_MakeSphere(DEF_RADIUS).Shape()

P_MATERIAL = 'P_MATERIAL'
DEF_MATERIAL = PLASTIC_MATERIAL

P_COLOR = 'P_COLOR'
DEF_COLOR = NICE_GRAY_COLOR

P_TRANSPARENCY = 'P_TRANSPARENCY'
DEF_TRANSPARENCY = 0

P_SCALE = 'P_SCALE'
P_SCALE_GEOM = 'P_SCALE_GEOM'
P_SCALE_ARROW = 'P_SCALE_ARROW'
P_SCALE_PX = 'P_SCALE_PX'
P_SCALE_STR = 'P_SCALE_STR'

LABEL_HEIGHT_PX = 20  # not scaled
LABEL_DELTA = 5
POINT_RADIUS = 4
LINE_RADIUS = 2
LINE_ARROW_RADIUS = 4
LINE_ARROW_LENGTH = 15
FACE_WIDTH = 1

AO_SIZE_XYZ = 1189, 841, 1

M_1_1_SCALE = (1, 1)
M_5_1_SCALE = (5, 1)

DESK_HEIGHT = 20
DESK_BORDER_SIZE = 60
DESK_PAPER_SIZE = 1189, 841, 1
DESK_AXIS_SIZE = 300
DESK_COORD_MARK_DIV = 6
DESK_PIN_OFFSET = 30
DESK_PIN_RADIUS = 10
DESK_PIN_HEIGHT = 2
DESK_DEFAULT_DRAW_AREA_SIZE = 400


class Computer:

    def __init__(self):
        self.cache = {}

    def compute(self, methodName, arg1=None, arg2=None):

        args = ''
        if arg1 is not None:
            args += str(arg1)
        if arg2 is not None:
            args += ',' + str(arg2)

        cacheKey = methodName + '(' + args + ')'

        method = self.__getattribute__(methodName)
        if cacheKey in self.cache:
            print('==> Get from cache', cacheKey)
            obj = self.cache[cacheKey]
        else:
            print('==> Compute', cacheKey)
            if arg1 is None:
                obj = method()
            elif arg2 is None:
                obj = method(arg1)
            else:
                obj = method(arg1, arg2)
            self.cache[cacheKey] = obj
        return obj


class DeskComputer(Computer):

    @staticmethod
    def computeSphere(r):
        return BRepPrimAPI_MakeSphere(r).Shape()


AIS_GROUP_MARKER = 'AIS_GROUP_MARKER'


class Desk:

    def __init__(self):
        self.params = {}
        self.curPath = ['root']
        self.aisStack = []
        self.log = []
        self.computer = DeskComputer()

    def log(self, line):
        self.log.append(line)

    def render(self, screenX: int = 800, screenY: int = 600):
        display, display_start, add_menu, add_function_to_menu = init_display(
            None, (screenX, screenY), True, [128, 128, 128], [128, 128, 128])

        for ais in self.aisStack:
            display.Context.Display(ais, False)

        display.FitAll()
        display_start()

    def objBegin(self, objName):
        self.curPath.append(objName)
        self.aisStack.append(AIS_GROUP_MARKER)

    def objEnd(self):
        self.curPath.pop()
        # parent = AIS_Point(Geom_CartesianPoint(0, 0, 0))
        parent = AIS_Shape(BRepPrimAPI_MakeBox(20,20,20).Shape())
        aspect = Graphic3d_MaterialAspect(DEF_MATERIAL)
        parent.SetMaterial(aspect)

        r, g, b = NICE_GRAY_COLOR
        qColor = Quantity_Color(r, g, b, Quantity_TypeOfColor(Quantity_TypeOfColor.Quantity_TOC_RGB))
        parent.SetColor(qColor)

        item = self.aisStack.pop()
        while item != AIS_GROUP_MARKER:
            parent.AddChild(item)
            item = self.aisStack.pop()
        self.aisStack.append(parent)

    def drawShape(self, shape, material, transparency, color):
        print(self.curPath, shape, material, transparency, color)

        ais = AIS_Shape(shape)

        aspect = Graphic3d_MaterialAspect(material)
        ais.SetMaterial(aspect)

        ais.SetTransparency(transparency)

        r, g, b = color
        qColor = Quantity_Color(r, g, b, Quantity_TypeOfColor(Quantity_TypeOfColor.Quantity_TOC_RGB))
        ais.SetColor(qColor)

        self.aisStack.append(ais)

    def setParam(self, paramName, paramValue, paramPath=None):
        path = ''
        for objName in self.curPath:
            path += '.' + objName
        if paramPath is not None:
            path += '.' + paramPath
        self.params[path + paramPath + '-' + paramName] = paramValue

    def getParam(self, paramName, preValue, postValue):

        if preValue is not None:
            return preValue

        value = None
        path = ''
        for objName in self.curPath:
            path += '.' + objName
            if path + '-' + paramName in self.params:
                value = self.params[path + '-' + paramName]

        if value is None:
            return postValue

        return value


desk = Desk()
comp = DeskComputer()


def Render():
    desk.render()


def Set(paramName, paramValue, paramPath):
    desk.setParam(paramName, paramValue, paramPath)


def Get(paramName, preValue, postValue):
    return desk.getParam(paramName, preValue, postValue)


def Begin(objName):
    desk.objBegin(objName)


def End():
    desk.objEnd()


def Shape(objName, argShape):

    Begin(objName)

    shape = Get(P_SHAPE, argShape, DEF_SHAPE)
    material = Get(P_MATERIAL, None, DEF_MATERIAL)
    transparency = Get(P_TRANSPARENCY, None, DEF_TRANSPARENCY)
    color = Get(P_COLOR, None, DEF_COLOR)

    desk.drawShape(shape, material, transparency, color)

    End()


def Sphere(objName, argRadius):
    Begin(objName)
    radius = Get(P_RADIUS, argRadius, DEF_RADIUS)
    shape = comp.compute('computeSphere', radius)
    Shape('Shape', shape)
    End()


if __name__ == "__main__":
    Sphere('Sphere001', 5)
    Sphere('Sphere002', 15)
    Render()
