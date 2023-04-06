import math
from typing import Optional

from OCC.Core.Graphic3d import Graphic3d_NameOfMaterial
from OCC.Core.TCollection import TCollection_ExtendedString

from OCC.Core.gp import gp_Trsf, gp_Vec, gp_Dir, gp_Ax1, gp_Pnt

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCone, \
    BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeTorus

from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
from OCC.Core.BRepTools import BRepTools_WireExplorer
from OCC.Core.BRep import BRep_Tool
from OCC.Core.GC import GC_MakeCircle

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
#                                      BRepBuilderAPI_MakeFace

from OCC.Core.AIS import AIS_InteractiveObject, AIS_Shape, AIS_TextLabel

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

WHITE_COLOR = 240 / 255, 240 / 255, 240 / 255
GRAY_COLOR = 100 / 255, 100 / 255, 100 / 255

RED_COLOR = 200 / 255, 30 / 255, 30 / 255
GREEN_COLOR = 100 / 255, 255 / 255, 100 / 255
BLUE_COLOR = 100 / 255, 100 / 255, 255 / 255

YELLOW_COLOR = 255 / 255, 255 / 255, 100 / 255
ORIGINAL_COLOR = 241 / 255, 79 / 255, 160 / 255
GOLD_COLOR = 180 / 255, 180 / 255, 90 / 255


FULL_VISIBLE_TRANSPARENCY = 0
SEMI_VISIBLE_TRANSPARENCY = 0.5
NO_VISIBLE_TRANSPARENCY = 1

A0_M_1_1_DESK = ('A0 M1:1', 1, 1)
A0_M_5_1_DESK = ('A0 M5:1', 5, 1)


# *************************************************
# Style vars
# *************************************************

VAR_LABEL_PREFIX = 'VAR_LABEL_'
VAR_POINT_PREFIX = 'VAR_POINT_'
VAR_LINE_PREFIX = 'VAR_LINE_'
VAR_SOLID_PREFIX = 'VAR_SOLID_'
VAR_SURFACE_PREFIX = 'VAR_SURFACE_'

VAR_MATERIAL = 'MATERIAL'
VAR_COLOR = 'COLOR'
VAR_TRANSPARENCY = 'TRANSPARENCY'

# **************************************************

VAR_MAIN_SCALE = 'VAR_MAIN_SCALE'
VAR_GEOM_SCALE = 'VAR_GEOM_SCALE'
VAR_LABEL_SCALE = 'VAR_LABEL_SCALE'

VAR_POINT_RADIUS = 'VAR_POINT_RADIUS'
VAR_LINE_RADIUS = 'VAR_LINE_RADIUS'
VAR_LINE_ARROW_RADIUS = 'VAR_LINE_ARROW_RADIUS'
VAR_LINE_ARROW_LENGTH = 'VAR_LINE_ARROW_LENGTH'
VAR_SURFACE_WIDTH = 'VAR_SURFACE_WIDTH'

VAR_LABEL_DELTA = 'DELTA'
VAR_LABEL_HEIGHT_PX = 'TEXT_HEIGHT_PX'

# ***************************************************

DEFAULT_VARS = {

    VAR_MAIN_SCALE: 1,
    VAR_GEOM_SCALE: 1,

    VAR_LABEL_HEIGHT_PX: 20,  # not scaled
    VAR_LABEL_DELTA: 5,

    VAR_POINT_RADIUS: 8,
    VAR_LINE_RADIUS: 4,
    VAR_LINE_ARROW_RADIUS: 8,
    VAR_LINE_ARROW_LENGTH: 30,
    VAR_SURFACE_WIDTH: 2,
}


MAIN_STYLE = {

    VAR_POINT_PREFIX + VAR_MATERIAL: CHROME_MATERIAL,
    VAR_POINT_PREFIX + VAR_COLOR: GOLD_COLOR,
    VAR_POINT_PREFIX + VAR_TRANSPARENCY: 0,

    VAR_LINE_PREFIX + VAR_MATERIAL: CHROME_MATERIAL,
    VAR_LINE_PREFIX + VAR_COLOR: BLUE_COLOR,
    VAR_LINE_PREFIX + VAR_TRANSPARENCY: 0,

    VAR_SOLID_PREFIX + VAR_MATERIAL: CHROME_MATERIAL,
    VAR_SOLID_PREFIX + VAR_COLOR: WHITE_COLOR,
    VAR_SOLID_PREFIX + VAR_TRANSPARENCY: 0,

    VAR_SURFACE_PREFIX + VAR_MATERIAL: CHROME_MATERIAL,
    VAR_SURFACE_PREFIX + VAR_COLOR: GRAY_COLOR,
    VAR_SURFACE_PREFIX + VAR_TRANSPARENCY: 0,

    VAR_LABEL_PREFIX + VAR_COLOR: GRAY_COLOR,
    VAR_LABEL_PREFIX + VAR_TRANSPARENCY: 0,

    VAR_GEOM_SCALE: 1

}

FOCUS_STYLE = {

    VAR_POINT_PREFIX + VAR_MATERIAL: CHROME_MATERIAL,
    VAR_POINT_PREFIX + VAR_COLOR: GOLD_COLOR,
    VAR_POINT_PREFIX + VAR_TRANSPARENCY: 0,

    VAR_LINE_PREFIX + VAR_MATERIAL: CHROME_MATERIAL,
    VAR_LINE_PREFIX + VAR_COLOR: BLUE_COLOR,
    VAR_LINE_PREFIX + VAR_TRANSPARENCY: 0,

    VAR_SOLID_PREFIX + VAR_MATERIAL: CHROME_MATERIAL,
    VAR_SOLID_PREFIX + VAR_COLOR: WHITE_COLOR,
    VAR_SOLID_PREFIX + VAR_TRANSPARENCY: 0,

    VAR_SURFACE_PREFIX + VAR_MATERIAL: CHROME_MATERIAL,
    VAR_SURFACE_PREFIX + VAR_COLOR: GRAY_COLOR,
    VAR_SURFACE_PREFIX + VAR_TRANSPARENCY: 0,

    VAR_LABEL_PREFIX + VAR_COLOR: GRAY_COLOR,
    VAR_LABEL_PREFIX + VAR_TRANSPARENCY: 0,

    VAR_GEOM_SCALE: 1

}

INFO_STYLE = {

    VAR_POINT_PREFIX + VAR_MATERIAL: CHROME_MATERIAL,
    VAR_POINT_PREFIX + VAR_COLOR: GOLD_COLOR,
    VAR_POINT_PREFIX + VAR_TRANSPARENCY: 0,

    VAR_LINE_PREFIX + VAR_MATERIAL: CHROME_MATERIAL,
    VAR_LINE_PREFIX + VAR_COLOR: BLUE_COLOR,
    VAR_LINE_PREFIX + VAR_TRANSPARENCY: 0,

    VAR_SOLID_PREFIX + VAR_MATERIAL: CHROME_MATERIAL,
    VAR_SOLID_PREFIX + VAR_COLOR: WHITE_COLOR,
    VAR_SOLID_PREFIX + VAR_TRANSPARENCY: 0,

    VAR_SURFACE_PREFIX + VAR_MATERIAL: CHROME_MATERIAL,
    VAR_SURFACE_PREFIX + VAR_COLOR: GRAY_COLOR,
    VAR_SURFACE_PREFIX + VAR_TRANSPARENCY: 0,

    VAR_LABEL_PREFIX + VAR_COLOR: GRAY_COLOR,
    VAR_LABEL_PREFIX + VAR_TRANSPARENCY: 0,

    VAR_GEOM_SCALE: 1

}

DESK_TEXT_STR = 'A0 M1:1'
DESK_HEIGHT = 20
DESK_BORDER_SIZE = 60
DESK_PAPER_XYZ = (1189, 841, 1)  # A0
DESK_AXIS_SIZE = 300
DESK_COORD_MARK_DIV = 6
DESK_PIN_OFFSET = 30
DESK_PIN_RADIUS = 10
DESK_PIN_HEIGHT = 2
DESK_DRAW_AREA_SIZE = 400

DESK_BOARD_STYLE = {
    VAR_SOLID_PREFIX + VAR_MATERIAL: PLASTIC_MATERIAL,
    VAR_SOLID_PREFIX + VAR_COLOR: WOOD_COLOR
    }

DESK_PAPER_STYLE = {
    VAR_SOLID_PREFIX + VAR_MATERIAL: PLASTIC_MATERIAL,
    VAR_SOLID_PREFIX + VAR_COLOR: PAPER_COLOR
    }

DESK_PIN_STYLE = {
    VAR_SOLID_PREFIX + VAR_MATERIAL: STEEL_MATERIAL,
    VAR_SOLID_PREFIX + VAR_COLOR: None
    }

COORD_X_COLOR = RED_COLOR
COORD_Y_COLOR = GREEN_COLOR
COORD_Z_COLOR = BLUE_COLOR
COORD_C_COLOR = WHITE_COLOR
COORD_DELTA = 50

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


class Scene:

    def __init__(self):
        self.rootsAis: [Optional[AIS_Shape]] = []
        self.parentAis: Optional[AIS_Shape] = None
        self.currentAis: Optional[AIS_Shape] = None
        self.dummyShape = BRepPrimAPI_MakeSphere(1)


    def render(self, screenX: int = 1200, screenY: int = 980):
        display, display_start, add_menu, add_function_to_menu = init_display(
            None, (screenX, screenY), True, [128, 128, 128], [128, 128, 128])

        for ais in self.rootsAis:
            display.Context.Display(ais, False)

        # display.DisplayMessage(labelPnt, text, heightPx, color, False)

        display.FitAll()
        display_start()

    def groupBegin(self):
        self.drawShape(self.dummyShape, None, 1, None)
        self.parentAis = self.currentAis
        self.currentAis = None

    def groupEnd(self):
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

    def drawShape(self, shape, color, transparency, material):
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

    def drawAsPoint(self):
        material = GetVar(VAR_POINT_MATERIAL)


VAR_POINT_MATERIAL = 'VAR_POINT_MATERIAL'
VAR_POINT_COLOR = 'VAR_POINT_COLOR'
VAR_POINT_TRANSPARENCY = 'VAR_POINT_TRANSPARENCY'

VAR_LINE_MATERIAL = 'VAR_LINE_MATERIAL'
VAR_LINE_COLOR = 'VAR_LINE_COLOR'
VAR_LINE_TRANSPARENCY = 'VAR_LINE_TRANSPARENCY'

VAR_SOLID_MATERIAL = 'VAR_SOLID_MATERIAL'
VAR_SOLID_COLOR = 'VAR_SOLID_COLOR'
VAR_SOLID_TRANSPARENCY = 'VAR_SOLID_TRANSPARENCY'

VAR_SURFACE_MATERIAL = 'VAR_SHAPE_MATERIAL'
VAR_SURFACE_COLOR = 'VAR_SHAPE_COLOR'
VAR_SURFACE_TRANSPARENCY = 'VAR_SHAPE_TRANSPARENCY'

scene = Scene()
comp = DeskComputer()
registry = {}


def SetVar(varName, varValue):
    registry[varName] = varValue


def GetVar(varName, style=None):
    if style is not None:
        if varName in style:
            return style[varName]
    if varName in registry:
        return registry[varName]
    return None


def SetVars(vars):
    for var in vars:
        registry[var] = vars[var]


def GetVars():
    return registry.copy()


def GetScaledVar(varName, varValue):
    varValue = GetVar(varName)
    mainScale = GetVar(VAR_MAIN_SCALE)
    return varValue * mainScale


def GetGeomVar(varName, varValue):
    scaledValue = GetScaledVar(varName)
    geomScale = GetVar(VAR_GEOM_SCALE)
    return scaledValue * geomScale


# *************************************************************
# VM level
# *************************************************************


def DecartPnt(x, y, z):
    return gp_Pnt(x, y, z)


def GroupBegin():
    scene.groupBegin()


def GroupEnd():
    scene.groupEnd()


def DoMove(pnt):
    trsf = gp_Trsf()
    trsf.SetTranslation(gp_Vec(DecartPnt(0,0,0), pnt))
    scene.doTrsf(trsf)


def DoRotate(axFromPnt, axToPnt, angle):
    trsf = gp_Trsf()
    ax1 = gp_Ax1(axFromPnt, gp_Dir(gp_Vec(axFromPnt, axToPnt)))
    trsf.SetRotation(ax1, angle / 180 * math.pi)
    scene.doTrsf(trsf)


def DoRotateX(angle):
    DoRotate(DecartPnt(0, 0, 0), DecartPnt(1, 0, 0), angle)


def DoRotateY(angle):
    DoRotate(DecartPnt(0, 0, 0), DecartPnt(0, 1, 0), angle)


def DoRotateZ(angle):
    DoRotate(DecartPnt(0, 0, 0), DecartPnt(0, 0, 1), angle)


def DoDirect(fromPnt, toPnt):
    trsf = gp_Trsf()

    dirVec = gp_Vec(fromPnt, toPnt)
    targetDir = gp_Dir(dirVec)

    rotateAngle = gp_Dir(0, 0, 1).Angle(targetDir)
    if not gp_Dir(0, 0, 1).IsParallel(targetDir, 0.001):
        rotateDir = gp_Dir(0, 0, 1)
        rotateDir.Cross(targetDir)
    else:
        rotateDir = gp_Dir(0, 1, 0)

    trsf.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), rotateDir), rotateAngle)
    trsf.SetTranslationPart(gp_Vec(DecartPnt(0, 0, 0), fromPnt))
    scene.doTrsf(trsf)


def DrawLabel(pnt, text):

    transparency = GetVar(VAR_LABEL_TRANSPARENCY)
    color = GetVar(VAR_LABEL_COLOR)
    heightPx = GetVar(VAR_LABEL_HEIGHT_PX)
    delta = GetScaledVar(VAR_LABEL_DELTA)

    targetPnt = pnt.Translated(gp_Vec(delta, delta, delta))
    scene.drawLabel(targetPnt, text, heightPx, color, transparency)


def DrawShape(shape, varPrefix):
    material = GetVar(varPrefix + '_MATERIAL')
    color = GetVar(varPrefix + '_COLOR')
    transparency = GetVar(varPrefix + '_TRANSPARENCY')
    scene.drawShape(shape, color, transparency, material)


def DrawSolid(shape):
    DrawShape(shape, 'VAR_SOLID')


def DrawSurface(shape):
    DrawShape(shape, 'VAR_SURFACE')


def DrawSphere(r):
    shape = comp.compute('computeSphere', r)
    DrawSolid(shape)


def DrawBox(x, y, z):
    shape = comp.compute('computeBox', x, y, z)
    DrawSolid(shape)


def DrawCone(r1, r2, h):
    shape = comp.compute('computeCone', r1, r2, h)
    DrawSolid(shape)


def DrawCylinder(r, h):
    shape = comp.compute('computeCylinder', r, h)
    DrawSolid(shape)


def DrawTorus(r1, r2):
    shape = comp.compute('computeTorus', r1, r2)
    DrawShape(shape)


def DrawPoint(pnt):
    r = GetGeomVar(VAR_POINT_RADIUS)
    DrawShape(r, 'VAR_POINT')


def DrawLine(pnt1, pnt2):
    r = GetGeomVar(VAR_LINE_RADIUS)
    length = gp_Vec(pnt1, pnt2).Magnitude()

    shape = comp.compute('computeCylinder', r, length)
    DrawShape(shape, 'VAR_LINE')
    DoDirect(pnt1, pnt2)


def DrawArrow(pnt1, pnt2):
    r = GetGeomVar(VAR_ARROW_RADIUS)
    h = GetGeomVar(VAR_ARROW_LENGTH)

    shape = comp.compute('computeCone', r, 0, h)
    DrawShape(shape, 'VAR_LINE')
    DoDirect(pnt1, pnt2)


def DrawLineArrow(pnt1, pnt2):

    arrowLength = GetGeomVar(VAR_ARROW_LENGTH)

    v = gp_Vec(pnt1, pnt2)
    vLen = v.Magnitude()
    v *= -arrowLength / vLen
    pntM2 = pnt2.Translated(v)

    GroupBegin()
    DrawLine(pnt1, pntM2)
    DrawArrow(pntM2, pnt2)
    GroupEnd()


def DrawLineArrow2(pnt1, pnt2):

    arrowLength = GetGeomVar(VAR_ARROW_LENGTH)

    v = gp_Vec(pnt1, pnt2)
    vLen = v.Magnitude()
    v *= arrowLength / vLen
    pntM1 = pnt1.Translated(v)
    v *= -1
    pntM2 = pnt2.Translated(v)

    GroupBegin()
    DrawLine(pntM1, pntM2)
    DrawArrow(pntM1, pnt1)
    DrawArrow(pntM2, pnt2)
    GroupEnd()


def DrawWire(wire):

    wireRadius = GetGeomVar(VAR_LINE_RADIUS)

    # getWireStartPointAndTangentDir:
    ex = BRepTools_WireExplorer(wire)
    edge = ex.Current()
    vertex = ex.CurrentVertex()
    aCurve, aFP, aLP = BRep_Tool.Curve(edge)
    aP = aFP
    tangentVec = gp_Vec()
    tempPnt = gp_Pnt()
    aCurve.D1(aP, tempPnt, tangentVec)
    tangentDir = gp_Dir(tangentVec)
    startPoint = BRep_Tool.Pnt(vertex)

    profileCircle = GC_MakeCircle(startPoint, tangentDir, wireRadius).Value()
    profileEdge = BRepBuilderAPI_MakeEdge(profileCircle).Edge()
    profileWire = BRepBuilderAPI_MakeWire(profileEdge).Wire()

    shape = BRepOffsetAPI_MakePipe(wire, profileWire).Shape()
    DrawShape(shape, 'VAR_LINE')


def SetSolidColor(color):
    SetVarPrefix(SOLID_VAR_PREFIX)
    SetVarWithPrefix('_COLOR', color)


def SetSurfaceColor(color):
    SetVarPrefix(SURFACE_VAR_PREFIX)
    SetVarWithPrefix('COLOR', color)


def SetPointColor(color):
    SetVarPrefix(POINT_VAR_PREFIX)
    SetVarWithPrefix('COLOR', color)


def SetLineColor(color):
    SetVarPrefix(LINE_VAR_PREFIX)
    SetVarWithPrefix('COLOR', color)


def SetLabelColor(color):
    SetVarPrefix(LABEL_VAR_PREFIX)
    SetVarWithPrefix('COLOR', color)


def SetTransparency(transparency):
    SetVarWithPrefix('TRANSPARENCY', transparency)


def SetMaterial(material):
    SetVarWithPrefix('MATERIAL', material)


def SetStyle(style)
    SetVars(style)


def SetScale(scaleStyle)
    SetVars(scaleStyle)

# *************************************************************
# Use level
# *************************************************************

def helperCircleWire(pnt1, pnt2, pnt3):
    geomCircle = GC_MakeCircle(pnt1, pnt2, pnt3).Value()
    edge = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
    return BRepBuilderAPI_MakeWire(edge).Wire()




def SetTransparency(transparency):
    SetVar(VAR_POINT_TRANSPARENCY, transparency)
    SetVar(VAR_LINE_TRANSPARENCY, transparency)
    SetVar(VAR_SOLID_TRANSPARENCY, transparency)
    SetVar(VAR_SHAPE_TRANSPARENCY, transparency)
    SetVar(VAR_LABEL_TRANSPARENCY, transparency)


def SetMaterial(material):
    SetVar(VAR_POINT_MATERIAL, material)
    SetVar(VAR_LINE_MATERIAL, material)
    SetVar(VAR_SOLID_MATERIAL, material)
    SetVar(VAR_SHAPE_MATERIAL, material)


def SetStyle(style):
    for var in style:
        SetVar(var, style[var])


def DrawCircle(argCoord1, argCoord2, argCoord3):
    coord1 = GetVar(ARG_COORD_1, argCoord1)
    coord2 = GetVar(ARG_COORD_2, argCoord2)
    coord3 = GetVar(ARG_COORD_3, argCoord3)

    pnt1 = _pnt(coord1)
    pnt2 = _pnt(coord2)
    pnt3 = _pnt(coord3)

    geomCircle = GC_MakeCircle(pnt1, pnt2, pnt3).Value()
    edge = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
    wire = BRepBuilderAPI_MakeWire(edge).Wire()

    LevelBegin('CircleWire')
    DrawWire(wire)
    LevelEnd()


def DrawDesk():
    mainScale = GetVar(VAR_MAIN_SCALE)
    borderSize = GetVar(VAR_DESK_BORDER_SIZE)
    height = GetVar(VAR_DESK_HEIGHT)
    paperStyle = GetVar(VAR_DESK_PAPER_STYLE)
    boardStyle = GetVar(VAR_DESK_BOARD_STYLE)

    textStr = GetVar(VAR_DESK_TEXT_STR)
    textStyle = GetVar(VAR_DESK_TEXT_STYLE)

    pinOffset = GetVar(VAR_DESK_PIN_OFFSET)
    pinRadius = GetVar(VAR_DESK_PIN_RADIUS)
    pinHeight = GetVar(VAR_DESK_PIN_HEIGHT)
    pinStyle = GetVar(VAR_DESK_PIN_STYLE)

    paperSizeX, paperSizeY, paperSizeZ = GetVar(VAR_DESK_PAPER_XYZ)
    psx, psy, psz = paperSizeX * mainScale, paperSizeY * mainScale, paperSizeZ * mainScale
    bsx = (paperSizeX + borderSize * 2) * mainScale
    bsy = (paperSizeY + borderSize * 2) * mainScale
    bsz = height * mainScale

    LevelBegin('BoardBox')
    SetStyle(boardStyle)
    DrawBox(bsx, bsy, bsz)
    DoMove(Decart(-bsx / 2, -bsy / 2, -bsz - psz))
    LevelEnd()

    LevelBegin('PaperBox')
    SetStyle(paperStyle)
    DrawBox(psx, psy, psz)
    DoMove(Decart(-psx / 2, -psy / 2, -psz))
    LevelEnd()

    LevelBegin('DeskLabel')
    SetStyle(textStyle)
    DrawLabel(Decart(-bsx / 2, -bsy / 2, bsz * 3), textStr)
    LevelEnd()

    dx = (paperSizeX / 2 - pinOffset * mainScale)
    dy = (paperSizeY / 2 - pinOffset * mainScale)

    pins = [
        ('DeskPin01Cylinder', -dx, -dy),
        ('DeskPin02Cylinder', dx, -dy),
        ('DeskPin03Cylinder', dx, dy),
        ('DeskPin04Cylinder', -dx, dy),
    ]

    SetStyle(pinStyle)
    for pinName, x, y in pins:
        LevelBegin(pinName)
        DrawCylinder(pinRadius * mainScale, pinHeight * mainScale)
        DoMove(Decart(x, y, 0))
        LevelEnd()


def DrawAxis(argCoord1, argCoord2, argDelta):
    coord1 = GetVar(ARG_COORD_1, argCoord1)
    coord2 = GetVar(ARG_COORD_2, argCoord2)
    delta = GetVar(ARG_DELTA, argDelta)

    mainScale = GetVar(VAR_MAIN_SCALE)
    geomScale = GetVar(VAR_GEOM_SCALE)
    pointRadius = GetVar(VAR_POINT_RADIUS)

    pnt1 = _pnt(coord1)
    pnt2 = _pnt(coord2)

    markRadius = pointRadius * mainScale * geomScale

    LevelBegin('AxisArrow')
    DrawArrow(coord1, coord2)
    LevelEnd()

    v = gp_Vec(pnt1, pnt2)
    totalLen = v.Magnitude()
    cnt = int(totalLen / delta - 1)

    for i in range(cnt):
        targetLen = (1 + i) * delta
        v = gp_Vec(pnt1, pnt2)
        v *= targetLen / totalLen
        pntMark = pnt1.Translated(v)

        LevelBegin('Mark' + str(i))
        DrawCylinder(markRadius, markRadius / 2)
        DoDirect(_coord(pntMark), _coord(pnt2))
        LevelEnd()


def DrawCoord(argCoord1, argCoord2):
    coord1 = GetVar(ARG_COORD_1, argCoord1)
    coord2 = GetVar(ARG_COORD_2, argCoord2)

    xColor = GetVar(VAR_COORD_X_COLOR)
    yColor = GetVar(VAR_COORD_Y_COLOR)
    zColor = GetVar(VAR_COORD_Z_COLOR)
    cColor = GetVar(VAR_COORD_C_COLOR)
    labelColor = GetVar(VAR_COORD_LABEL_COLOR)

    normDelta = GetVar(VAR_COORD_DELTA)
    mainScale = GetVar(VAR_MAIN_SCALE)
    delta = normDelta * mainScale

    x1, y1, z1 = UnDecart(coord1)
    x2, y2, z2 = UnDecart(coord2)

    cCoord = Decart(x1, y1, z1)
    xCoord = Decart(x2, y1, z1)
    yCoord = Decart(x1, y2, z1)
    zCoord = Decart(x1, y1, z2)

    SetColor(xColor)
    DrawAxis(cCoord, xCoord, delta)

    SetColor(yColor)
    DrawAxis(cCoord, yCoord, delta)

    SetColor(zColor)
    DrawAxis(cCoord, zCoord, delta)

    SetColor(cColor)
    DrawPoint(cCoord)

    SetColor(labelColor)
    DrawLabel(xCoord, 'X')
    DrawLabel(yCoord, 'Y')
    DrawLabel(zCoord, 'Z')


def DrawFrame(argVertexes, argEdges):
    vertexes = GetVar(ARG_FRAME_VERTEXES, argVertexes)
    edges = GetVar(ARG_FRAME_EDGES, argEdges)

    pointColor = GetVar(VAR_FRAME_POINT_COLOR)
    lineColor = GetVar(VAR_FRAME_LINE_COLOR)
    material = GetVar(VAR_FRAME_MATERIAL)

    SetMaterial(material)
    SetColor(pointColor)
    for coord in vertexes:
        DrawPoint(coord)

    SetColor(lineColor)
    for i1, i2 in edges:
        DrawLine(vertexes[i1], vertexes[i2])

    SetColor(NICE_YELLOW_COLOR)
    for coord in vertexes:
        x, y, z = UnDecart(coord)
        DrawLabel(coord, '(' + str(x) + ',' + str(y) + ',' + str(z) + ')')


def DrawBoxFrame(argCoord1, argCoord2, isLabeled):
    coord1 = GetVar(ARG_COORD_1, argCoord1)
    coord2 = GetVar(ARG_COORD_2, argCoord2)

    x1, y1, z1 = UnDecart(coord1)
    x2, y2, z2 = UnDecart(coord2)

    vertexes = [
        Decart(x1, y1, z1),
        Decart(x1, y2, z1),
        Decart(x2, y2, z1),
        Decart(x2, y1, z1),

        Decart(x1, y1, z2),
        Decart(x1, y2, z2),
        Decart(x2, y2, z2),
        Decart(x2, y1, z2),
    ]

    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),
    ]

    LevelBegin('BoxFrame')
    DrawFrame(vertexes, edges)
    LevelEnd()


def SetScale(scale):
    SetVar()


def SceneShow(isDesk=True, isCoord=True, isLimits=True, screenX=1200, screenY=900):


    if isDesk:
        DrawDummy()
        ChildrenBegin()
        DrawDesk()
        ChildrenEnd()
        DoMove(Decart(0, 0, -100))
    if isCoord:
        DrawCoord(Decart(0, 0, 0), Decart(500, 400, 500))
    if isLimits:
        SetVar(VAR_FRAME_POINT_COLOR, NICE_GRAY_COLOR, 'BoxFrame')
        SetVar(VAR_FRAME_LINE_COLOR, NICE_GRAY_COLOR, 'BoxFrame')
        DrawBoxFrame(Decart(-400, -300, 0), Decart(400, 300, 400), True)

    scene.render()

    global scene, reg
    scene = Scene(screenX, screenY)
    reg = Registry(VAR_DEFAULTS)

SetStyle(DEFAULT_VARS)
SetStyle(MAIN_STYLE)

