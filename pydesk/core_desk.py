import math
from typing import Optional
# from core_position import *
from core_style import *

from OCC.Core.TCollection import TCollection_ExtendedString

from OCC.Core.gp import gp_Trsf, gp_Vec, gp_Dir, gp_Ax1, gp_Pnt

# from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCone, \
    BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeTorus

#  from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
# from OCC.Core.BRepTools import BRepTools_WireExplorer
# from OCC.Core.BRep import BRep_Tool
# from OCC.Core.GC import GC_MakeCircle
# from OCC.Core.Geom import Geom_CartesianPoint

# from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire,
#                                      BRepBuilderAPI_MakeFace)

from OCC.Core.AIS import AIS_InteractiveObject, AIS_Shape, AIS_TextLabel

#    , AIS_Point
from OCC.Core.Quantity import Quantity_Color, Quantity_TypeOfColor
# from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.Graphic3d import Graphic3d_MaterialAspect

from OCC.Display.SimpleGui import init_display

ARG_RADIUS = 'ARG_RADIUS'
ARG_RADIUS_1 = 'ARG_RADIUS_1'
ARG_RADIUS_2 = 'ARG_RADIUS_2'
ARG_HEIGHT = 'ARG_HEIGHT'
ARG_X = 'ARG_X'
ARG_Y = 'ARG_Y'
ARG_Z = 'ARG_Z'
ARG_PNT = 'ARG_PNT'
ARG_PNT_1 = 'ARG_PNT_1'
ARG_PNT_2 = 'ARG_PNT_2'
ARG_TEXT = 'ARG_TEXT'
ARG_SHAPE = 'ARG_SHAPE'

VAR_MATERIAL = 'VAR_MATERIAL'
VAR_COLOR = 'VAR_COLOR'
VAR_TRANSPARENCY = 'VAR_TRANSPARENCY'

VAR_MAIN_SCALE = 'VAR_MAIN_SCALE'
VAR_GEOM_SCALE = 'VAR_GEOM_SCALE'
VAR_LABEL_SCALE = 'VAR_LABEL_SCALE'

VAR_LABEL_HEIGHT_PX = 'VAR_LABEL_HEIGHT_PX'
VAR_LABEL_DELTA = 'VAR_LABEL_DELTA'
VAR_LABEL_COLOR = 'VAR_LABEL_COLOR'

VAR_POINT_RADIUS = 'VAR_POINT_RADIUS'
VAR_LINE_RADIUS = 'VAR_LINE_RADIUS'
VAR_ARROW_RADIUS = 'VAR_ARROW_RADIUS'
VAR_ARROW_LENGTH  = 'VAR_ARROW_LENGTH'
VAR_FACE_WIDTH = 'VAR_FACE_WIDTH'

VAR_DEFAULTS = {
    VAR_MATERIAL: None,
    VAR_COLOR: None,
    VAR_TRANSPARENCY: None,
    VAR_MAIN_SCALE: 1,
    VAR_GEOM_SCALE: 1,
    VAR_LABEL_SCALE: 1,

    VAR_LABEL_HEIGHT_PX: 20, # not scaled

    VAR_LABEL_DELTA: 5,
    VAR_LABEL_COLOR: None,

    VAR_POINT_RADIUS: 4,
    VAR_LINE_RADIUS: 2,
    VAR_ARROW_RADIUS: 4,
    VAR_ARROW_LENGTH: 15,
    VAR_FACE_WIDTH: 1
}


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

FULL_VISIBLE_TRANSPARENCY = 0
SEMI_VISIBLE_TRANSPARENCY = 0.5
NO_VISIBLE_TRANSPARENCY = 1


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
    def computeSphere(argRadius):
        return BRepPrimAPI_MakeSphere(argRadius).Shape()

    @staticmethod
    def computeBox(argDx, argDy, argDz):
        return BRepPrimAPI_MakeBox(argDx, argDy, argDz).Shape()

    @staticmethod
    def computeCone(argRadius1, argRadius2, argHeight):
        return BRepPrimAPI_MakeCone(argRadius1, argRadius2, argHeight).Shape()

    @staticmethod
    def computeCylinder(argRadius, argHeight):
        return BRepPrimAPI_MakeCylinder(argRadius, argHeight).Shape()

    @staticmethod
    def computeTorus(argRadius1, argRadius2):
        return BRepPrimAPI_MakeTorus(argRadius1, argRadius2).Shape()


class Scripting:
    def __init__(self):
        self.script = []

    def addLine(self, line):
        self.script.append(line)

    def addShape(self, shape):
        pass


class Registry:
    def __init__(self, defs):
        self.defs =  defs
        self.vars = {}
        self.levels = ['root']

    def setVar(self, varName, varValue, varSubPath):
        path = ''
        for levelName in self.levels:
            path += '.' + levelName
        if varSubPath is not None:
            path += '.' + varSubPath
        self.vars[path + '-' + varName] = varValue

    def getVar(self, varName, defaultValue):

        path = ''
        paths = []
        for levelName in self.levels:
            path += '.' + levelName
            paths.append(path + '-' + varName)

        fullPath = paths.pop()
        if fullPath in self.vars:
            return self.vars[fullPath]

        if defaultValue is not None:
            return defaultValue

        while len(paths) > 0:
            notFullPath = paths.pop()
            if notFullPath in self.vars:
                return self.vars[notFullPath]

        if varName in self.defs:
            return self.defs[varName]

        return None

    def levelBegin(self, levelName):
        self.levels.append(levelName)

    def levelEnd(self):
        self.levels.pop()


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

        # display.DisplayMessage(labelPnt, text, heightPx, color, False)

        display.FitAll()
        display_start()

    def childBegin(self):
        self.parentAis = self.currentAis = None

    def childEnd(self):
        self.currentAis = self.parentAis
        self.parentAis = self.parentAis.Parent()

    def drawAis(self, ais: AIS_InteractiveObject):
        if self.parentAis is None:
            self.rootsAis.append(ais)
        else:
            self.parentAis.AddChild(ais)
        self.currentAis = ais

    def doTrsf(self, trsf):
        trsf *= self.currentAis.LocalTransformation()
        self.currentAis.SetLocalTransformation(trsf)

    def doHide(self):
        self.currentAis.SetTransparency(NO_VISIBLE_TRANSPARENCY)

    def drawShape(self, shape, material, transparency, color):
        # print(self.curPath, shape, material, transparency, color)

        ais = AIS_Shape(shape)

        # material set anyway
        if material is None:
            material = GOLD_MATERIAL
        aspect = Graphic3d_MaterialAspect(material)
        ais.SetMaterial(aspect)

        if transparency is not None:
            ais.SetTransparency(transparency)

        if color is not None:
            r, g, b = color
            qColor = Quantity_Color(r, g, b, Quantity_TypeOfColor(Quantity_TypeOfColor.Quantity_TOC_RGB))
            ais.SetColor(qColor)

        self.drawAis(ais)

    def drawLabel(self, pnt, text, height, color, transparency):
        # labelPnt = pnt.Transformed(position.trsf)
        # self.display.DisplayMessage(labelPnt, text, heightPx, color, False)
        ais = AIS_TextLabel()

        ais.SetText(TCollection_ExtendedString(text, True))
        ais.SetPosition(pnt)
        ais.SetHeight(height)

        if transparency is not None:
            ais.SetTransparency(transparency)

        if color is not None:
            r, g, b = color
            qColor = Quantity_Color(r, g, b, Quantity_TypeOfColor(Quantity_TypeOfColor.Quantity_TOC_RGB))
            ais.SetColor(qColor)

        self.drawAis(ais)


scene = Scene()
comp = DeskComputer()
reg = Registry(VAR_DEFAULTS)


def Clear():
    global scene, comp, reg
    scene = Scene()
    comp = DeskComputer()
    reg = Registry(VAR_DEFAULTS)


def Pnt(x, y, z):
    return gp_Pnt(x, y, z)


def Rgb(r, g, b):
    return [r, g, b]


def Render():
    scene.render()


def LevelBegin(nm):
    reg.levelBegin(nm)


def LevelEnd():
    reg.levelEnd()


def SetVar(varName, varValue, varPath=None):
    reg.setVar(varName, varValue, varPath)


def GetVar(varName, defaultValue = None):
    return reg.getVar(varName, defaultValue)


def SetLabelColor(color):
    SetVar(VAR_LABEL_COLOR, color)


def SetColor(color):
    SetVar(VAR_COLOR, color)


def SetTransparency(transparency):
    SetVar(VAR_TRANSPARENCY, transparency)


def SetMaterial(material):
    SetVar(VAR_MATERIAL, material)


def DoHide():
    scene.doHide()


def DoMove(pnt):
    trsf = gp_Trsf()
    trsf.SetTranslation(gp_Vec(pnt.X(), pnt.Y(), pnt.Z()))
    scene.doTrsf(trsf)


def DoRotate(pntAxFrom, pntAxTo, angle):
    trsf = gp_Trsf()
    ax1 = gp_Ax1(pntAxFrom, gp_Dir(gp_Vec(pntAxFrom, pntAxTo)))
    trsf.SetRotation(ax1, angle / 180 * math.pi)
    scene.doTrsf(trsf)


def DoRotateX(angle):
    DoRotate(gp_Pnt(0, 0, 0), gp_Pnt(1, 0, 0), angle)


def DoRotateY(angle):
    DoRotate(gp_Pnt(0, 0, 0), gp_Pnt(0, 1, 0), angle)


def DoRotateZ(angle):
    DoRotate(gp_Pnt(0, 0, 0), gp_Pnt(0, 0, 1), angle)


def DoDirect(pntFrom, pntTo):
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


def DrawDummy():
    DrawSphere(1)
    DoHide()


def DrawShape(shape):
    material = GetVar(VAR_MATERIAL)
    transparency = GetVar(VAR_TRANSPARENCY)
    color = GetVar(VAR_COLOR)
    scene.drawShape(shape, material, transparency, color)


def DrawSphere(argRadius):
    radius = GetVar(ARG_RADIUS, argRadius)
    shape = comp.compute('computeSphere', radius)
    LevelBegin('Shape')
    DrawShape(shape)
    LevelEnd()


def DrawBox(argX, argY, argZ):
    x = GetVar(ARG_X, argX)
    y = GetVar(ARG_Y, argY)
    z = GetVar(ARG_Z, argZ)
    shape = comp.compute('computeBox', x, y, z)
    LevelBegin('Shape')
    DrawShape(shape)
    LevelEnd()


def DrawCone(argRadius1, argRadius2, argHeight):
    radius1 = GetVar(ARG_RADIUS_1, argRadius1)
    radius2 = GetVar(ARG_RADIUS_2, argRadius2)
    height = GetVar(ARG_HEIGHT, argHeight)
    shape = comp.compute('computeCone', radius1, radius2, height)
    LevelBegin('Shape')
    DrawShape(shape)
    LevelEnd()


def DrawCylinder(argRadius, argHeight):
    radius = GetVar(ARG_RADIUS, argRadius)
    height = GetVar(ARG_HEIGHT, argHeight)
    shape = comp.compute('computeCylinder', radius, height)
    LevelBegin('Shape')
    DrawShape(shape)
    LevelEnd()


def DrawTorus(argRadius1, argRadius2):
    radius1 = GetVar(ARG_RADIUS_1, argRadius1)
    radius2 = GetVar(ARG_RADIUS_2, argRadius2)
    shape = comp.compute('computeTorus', radius1, radius2)
    LevelBegin('Shape')
    DrawShape(shape)
    LevelEnd()


def DrawLabel(argPnt, argText):

    pnt = GetVar(ARG_PNT, argPnt)
    text = GetVar(ARG_TEXT, argText)

    transparency = GetVar(VAR_TRANSPARENCY)
    color = GetVar(VAR_LABEL_COLOR)
    mainScale = GetVar(VAR_MAIN_SCALE)
    labelScale = GetVar(VAR_LABEL_SCALE)
    labelHeightPx = GetVar(LABEL_HEIGHT_PX)
    labelDelta = GetVar(LABEL_DELTA)

    delta = labelDelta * mainScale
    heightPx = labelHeightPx * labelScale
    targetPnt = pnt.Translated(gp_Vec(delta, delta, delta))
    scene.drawLabel(targetPnt, argText, heightPx, color, transparency)


def DrawPoint(argPnt):

    pnt = GetVar(ARG_PNT, argPnt)

    mainScale = GetVar(VAR_MAIN_SCALE)
    geomScale = GetVar(VAR_GEOM_SCALE)
    pointRadius = GetVar(VAR_POINT_RADIUS)

    r = pointRadius * geomScale * mainScale
    LevelBegin('Sphere')
    DrawSphere(r)
    LevelEnd()
    DoMove(pnt)


def DrawLine(argPnt1, argPnt2):

    pnt1 = GetVar(ARG_PNT_1, argPnt1)
    pnt2 = GetVar(ARG_PNT_2, argPnt2)

    mainScale = GetVar(VAR_MAIN_SCALE)
    geomScale = GetVar(VAR_GEOM_SCALE)
    lineRadius = GetVar(VAR_LINE_RADIUS)

    r = lineRadius * mainScale * geomScale
    length = gp_Vec(pnt1, pnt2).Magnitude()
    LevelBegin('Cylinder')
    DrawCylinder(r, length)
    LevelEnd()
    DoDirect(pnt1, pnt2)


def DrawVector(argPnt1, argPnt2):

    pnt1 = GetVar(ARG_PNT_1, argPnt1)
    pnt2 = GetVar(ARG_PNT_2, argPnt2)

    mainScale = GetVar(VAR_MAIN_SCALE)
    geomScale = GetVar(VAR_GEOM_SCALE)
    arrowRadius = GetVar(VAR_ARROW_RADIUS)
    arrowLength = GetVar(VAR_ARROW_LENGTH)

    scaledArrowRadius = arrowRadius * geomScale * mainScale
    scaledArrowLength = arrowLength * geomScale * mainScale

    v = gp_Vec(pnt1, pnt2)
    vLen = v.Magnitude()
    v *= -scaledArrowLength / vLen
    pntM = pnt2.Translated(v)
    LevelBegin('Line')
    DrawLine(pnt1, pntM)
    LevelEnd()
    LevelBegin('Cone')
    DrawCone(scaledArrowRadius, 0, scaledArrowLength)
    LevelEnd()
    DoDirect(pntM, pnt2)


def DrawArrow(argPnt1, argPnt2):

    pnt1 = GetVar(ARG_PNT_1, argPnt1)
    pnt2 = GetVar(ARG_PNT_2, argPnt2)

    mainScale = GetVar(VAR_MAIN_SCALE)
    geomScale = GetVar(VAR_GEOM_SCALE)
    arrowRadius = GetVar(VAR_ARROW_RADIUS)
    arrowLength = GetVar(VAR_ARROW_LENGTH)

    scaledArrowRadius = arrowRadius * geomScale * mainScale
    scaledArrowLength = arrowLength * geomScale * mainScale

    v = gp_Vec(pnt1, pnt2)
    vLen = v.Magnitude()
    v *= scaledArrowLength / vLen
    pntM1 = pnt1.Translated(v)
    v *= -1
    pntM2 = pnt2.Translated(v)

    LevelBegin('Line')
    DrawLine(pntM1, pntM2)
    LevelEnd()
    LevelBegin('Cone1')
    DrawCone(scaledArrowRadius, 0, scaledArrowLength)
    LevelEnd()
    DoDirect(pntM1, pnt1)
    LevelBegin('Cone2')
    DrawCone(scaledArrowRadius, 0, scaledArrowLength)
    LevelEnd()
    DoDirect(pntM2, pnt2)

'''

class VectorDraw(Draw):
    def __init__(self, pnt1, pnt2):
        super().__init__('vectorObj:vector-line')
        self.pnt1 = pnt1
        self.pnt2 = pnt2

    def addStyledItems(self, style: Style):

        arrowR = LINE_ARROW_RADIUS * style.GetVar(SCALE, 1) * style.GetVar(SCALE_GEOM, 1)
        arrowL = LINE_ARROW_LENGTH * style.GetVar(SCALE, 1) * style.GetVar(SCALE_GEOM, 1) \
            * style.GetVar(SCALE_ARROW, 1)

        v = gp_Vec(self.pnt1, self.pnt2)
        vLen = v.Magnitude()
        v *= (vLen - arrowL) / vLen
        pntM = self.pnt1.Translated(v)

        self.addItem(LineDraw(self.pnt1, pntM))
        self.addItem(ConeDraw(arrowR, 0, arrowL).doPs(Direct(pntM, self.pnt2)))
'''
