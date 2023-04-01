import math
from typing import Optional
# from core_position import *
from core_style import *

from OCC.Core.gp import gp_Trsf, gp_Vec, gp_Dir, gp_Ax1, gp_Pnt

# from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox

# , BRepPrimAPI_MakeCone, \
# BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeTorus
#  from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
# from OCC.Core.BRepTools import BRepTools_WireExplorer
# from OCC.Core.BRep import BRep_Tool
# from OCC.Core.GC import GC_MakeCircle
# from OCC.Core.Geom import Geom_CartesianPoint

# from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire,
#                                      BRepBuilderAPI_MakeFace)

from OCC.Core.AIS import AIS_Shape

#    , AIS_Point
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

WOOD_COLOR = 208 / 255, 117 / 255, 28 / 255
PAPER_COLOR = 230 / 255, 230 / 255, 230 / 255
STEEL_COLOR = 100 / 255, 100 / 255, 100 / 255

NICE_WHITE_COLOR = 240 / 255, 240 / 255, 240 / 255
NICE_GRAY_COLOR = 100 / 255, 100 / 255, 100 / 255
NICE_RED_COLOR = 200 / 255, 30 / 255, 30 / 255
NICE_BLUE_COLOR = 100 / 255, 100 / 255, 255 / 255
NICE_YELLOW_COLOR = 255 / 255, 255 / 255, 100 / 255
NICE_ORIGINAL_COLOR = 241 / 255, 79 / 255, 160 / 255

PARENT_DUMMY_SHAPE = BRepPrimAPI_MakeSphere(1).Shape()

INVISIBLE_TRANSPARENCY = 1
SEMI_TRANSPARENCY = 0.5

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

P_DX = 'P_DX'
DEF_DX = 10
P_DY = 'P_DY'
DEF_DY = 10
P_DZ = 'P_DZ'
DEF_DZ = 10

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

    def compute(self, methodName, arg1=None, arg2=None, arg3=None):

        args = ''
        if arg1 is not None:
            args += str(arg1)
        if arg2 is not None:
            args += ',' + str(arg2)
        if arg3 is not None:
            args += ',' + str(arg3)

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
            elif arg3 is None:
                obj = method(arg1, arg2)
            else:
                obj = method(arg1, arg2, arg3)
            self.cache[cacheKey] = obj
        return obj


class DeskComputer(Computer):

    @staticmethod
    def computeSphere(argR):
        return BRepPrimAPI_MakeSphere(argR).Shape()

    @staticmethod
    def computeBox(argDx, argDy, argDz):
        return BRepPrimAPI_MakeBox(argDx, argDy, argDz).Shape()


class Scripting:
    def __init__(self):
        self.script = []

    def addLine(self, line):
        self.script.append(line)

    def addShape(self, shape):
        pass


class Registry:
    def __init__(self):
        self.params = {}
        self.curPath = ['root']

    def setParam(self, paramName, paramValue, paramPath=None):
        path = ''
        for objName in self.curPath:
            path += '.' + objName
        if paramPath is not None:
            path += '.' + paramPath
        self.params[path + '-' + paramName] = paramValue

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

    def nameBegin(self, nm):
        self.curPath.append(nm)

    def nameEnd(self):
        self.curPath.pop()


AIS_CHILD_MARKER = 'AIS_CHILD_MARKER'


class Scene:

    def __init__(self):
        self.rootsAis: [Optional[AIS_Shape]] = []
        self.parentAis: Optional[AIS_Shape] = None
        self.currentAis: Optional[AIS_Shape] = None

    def render(self, screenX: int = 800, screenY: int = 600):
        display, display_start, add_menu, add_function_to_menu = init_display(
            None, (screenX, screenY), True, [128, 128, 128], [128, 128, 128])

        for ais in self.rootsAis:
            display.Context.Display(ais, False)

        display.FitAll()
        display_start()

    def childBegin(self):
        self.parentAis = self.currentAis = None

    def childEnd(self):
        self.currentAis = self.parentAis
        self.parentAis = self.parentAis.Parent()

    def draw(self, ais: AIS_Shape):
        if self.parentAis is None:
            self.rootsAis.append(ais)
        else:
            self.parentAis.AddChild(ais)
        self.currentAis = ais

    def doTrsf(self, trsf):
        trsf *= self.currentAis.LocalTransformation()
        self.currentAis.SetLocalTransformation(trsf)

    def drawShape(self, shape, material, transparency, color):
        # print(self.curPath, shape, material, transparency, color)

        ais = AIS_Shape(shape)

        aspect = Graphic3d_MaterialAspect(material)
        ais.SetMaterial(aspect)

        ais.SetTransparency(transparency)

        r, g, b = color
        qColor = Quantity_Color(r, g, b, Quantity_TypeOfColor(Quantity_TypeOfColor.Quantity_TOC_RGB))
        ais.SetColor(qColor)

        self.draw(ais)

    def drawDummy(self):

        ais = AIS_Shape(PARENT_DUMMY_SHAPE)
        ais.SetTransparency(INVISIBLE_TRANSPARENCY)
        self.draw(ais)


scene = Scene()
comp = DeskComputer()
reg = Registry()


def _Render():
    scene.render()


def _NameBegin(nm):
    reg.nameBegin(nm)


def _NameEnd():
    reg.nameEnd()


def _SetParam(paramName, paramValue, paramPath):
    reg.setParam(paramName, paramValue, paramPath)


def _GetParam(paramName, preValue, postValue):
    return reg.getParam(paramName, preValue, postValue)


def _SetColor(color):
    reg.setParam(P_COLOR, color)


def _SetTransparency(argTransparency):
    reg.setParam(P_TRANSPARENCY, argTransparency)


def _SetMaterial(argMaterial):
    reg.setParam(P_MATERIAL, argMaterial)


def _DoMove(dx, dy, dz):
    trsf = gp_Trsf()
    trsf.SetTranslation(gp_Vec(dx, dy, dz))
    scene.doTrsf(trsf)


def _DoRotate(pntAxFrom, pntAxTo, angle):
    trsf = gp_Trsf()
    ax1 = gp_Ax1(pntAxFrom, gp_Dir(gp_Vec(pntAxFrom, pntAxTo)))
    trsf.SetRotation(ax1, angle / 180 * math.pi)
    scene.doTrsf(trsf)


def _DoRotateX(angle):
    _DoRotate(gp_Pnt(0, 0, 0), gp_Pnt(1, 0, 0), angle)


def _DoRotateY(angle):
    _DoRotate(gp_Pnt(0, 0, 0), gp_Pnt(0, 1, 0), angle)


def _DoRotateZ(angle):
    _DoRotate(gp_Pnt(0, 0, 0), gp_Pnt(0, 0, 1), angle)


def _DoDirect(pntFrom, pntTo):

    trsf = gp_Trsf()

    dirVec = gp_Vec(pntFrom, pntTo)
    targetDir = gp_Dir(dirVec)

    rotateAngle = gp_Dir(0, 0, 1).Angle(targetDir)
    if not gp_Dir(0, 0, 1).IsParallel(targetDir, 0.001):
        rotateDir = gp_Dir(0, 0, 1)
        rotateDir.Cross(targetDir)
    else:
        rotateDir = gp_Dir(0, 1, 0)

    trsf.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), rotateDir), rotateAngle)
    trsf.SetTranslationPart(gp_Vec(gp_Pnt(0, 0, 0), pntFrom))
    scene.doTrsf(trsf)


def _DrawDummy():
    scene.drawDummy()


def _DrawShape(argShape):
    shape = _GetParam(P_SHAPE, argShape, DEF_SHAPE)
    material = _GetParam(P_MATERIAL, None, DEF_MATERIAL)
    transparency = _GetParam(P_TRANSPARENCY, None, DEF_TRANSPARENCY)
    color = _GetParam(P_COLOR, None, DEF_COLOR)
    scene.drawShape(shape, material, transparency, color)


def _DrawSphere(argRadius):
    radius = _GetParam(P_RADIUS, argRadius, DEF_RADIUS)
    shape = comp.compute('computeSphere', radius)
    _NameBegin('Shape')
    _DrawShape(shape)
    _NameEnd()


def _DrawBox(argDx, argDy, argDz):
    dx = _GetParam(P_DX, argDx, DEF_DX)
    dy = _GetParam(P_DY, argDy, DEF_DY)
    dz = _GetParam(P_DZ, argDz, DEF_DZ)
    shape = comp.compute('computeBox', dx, dy, dz)
    _NameBegin('Shape')
    _DrawShape(shape)
    _NameEnd()


# ***************************************************
# ***************************************************
# ***************************************************

def Point(argX, argY, argZ):
    return gp_Pnt(argX, argY, argZ)


def Render():
    _Render()


def SetColor(argColor):
    _SetColor(argColor)


def SetTransparency(argTransparency):
    _SetTransparency(argTransparency)


def SetMaterial(argMaterial):
    _SetMaterial(argMaterial)


def DoMove(dx, dy, dz):
    _DoMove(dx, dy, dz)


def DoRotate(pntAxFrom, pntAxTo, angle):
    _DoRotate(pntAxFrom, pntAxTo, angle)


def DoRotateX(angle):
    _DoRotateX(angle)


def DoRotateY(angle):
    _DoRotateY(angle)


def DoRotateZ(angle):
    _DoRotateZ(angle)


def DoDirect(pntFrom, pntTo):
    _DoDirect(pntFrom, pntTo)


def DrawSphere(argRadius):
    _DrawSphere(argRadius)


def DrawBox(argDx, argDy, argDz):
    _DrawBox(argDx, argDy, argDz)
