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


def _coord(pnt):
    return pnt.X(), pnt.Y(), pnt.Z()


def _pnt(coord):
    x, y, z = coord
    return gp_Pnt(x, y, z)


def _vec(coord1):
    x, y, z = coord1
    return gp_Vec(x, y, z)


def Decart(x, y, z):
    return x, y, z


def UnDecart(coord):
    return coord


def Rgb(r, g, b):
    return r, g, b


def Style(material, color, transparency, texture):
    return material, color, transparency, texture


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
NICE_GREEN_COLOR = 100 / 255, 255 / 255, 100 / 255
NICE_BLUE_COLOR = 100 / 255, 100 / 255, 255 / 255
NICE_YELLOW_COLOR = 255 / 255, 255 / 255, 100 / 255
NICE_ORIGINAL_COLOR = 241 / 255, 79 / 255, 160 / 255

FULL_VISIBLE_TRANSPARENCY = 0
SEMI_VISIBLE_TRANSPARENCY = 0.5
NO_VISIBLE_TRANSPARENCY = 1

A0_M_1_1_DESK = ('A0 M1:1', 1, 1)
A0_M_5_1_DESK = ('A0 M5:1', 5, 1)

# *************************************************
# *************************************************
# *************************************************

ARG_COUNT = 'ARG_COUNT'
ARG_DELTA = 'ARG_DELTA'
ARG_RADIUS = 'ARG_RADIUS'
ARG_RADIUS_1 = 'ARG_RADIUS_1'
ARG_RADIUS_2 = 'ARG_RADIUS_2'
ARG_HEIGHT = 'ARG_HEIGHT'
ARG_X = 'ARG_X'
ARG_Y = 'ARG_Y'
ARG_Z = 'ARG_Z'
ARG_COORD = 'ARG_PNT'
ARG_COORD_1 = 'ARG_COORD_1'
ARG_COORD_2 = 'ARG_COORD_2'
ARG_COORD_3 = 'ARG_COORD_3'
ARG_TEXT = 'ARG_TEXT'
ARG_SHAPE = 'ARG_SHAPE'
ARG_WIRE = 'ARG_WIRE'
ARG_FRAME_VERTEXES = 'ARG_FRAME_VERTEXES'
ARG_FRAME_EDGES = 'ARG_FRAME_EDGES'

VAR_MATERIAL = 'VAR_MATERIAL'
VAR_COLOR = 'VAR_COLOR'
VAR_TRANSPARENCY = 'VAR_TRANSPARENCY'
VAR_TEXTURE = 'VAR_TEXTURE'

VAR_MAIN_SCALE = 'VAR_MAIN_SCALE'
VAR_GEOM_SCALE = 'VAR_GEOM_SCALE'
VAR_LABEL_SCALE = 'VAR_LABEL_SCALE'

VAR_LABEL_HEIGHT_PX = 'VAR_LABEL_HEIGHT_PX'
VAR_LABEL_DELTA = 'VAR_LABEL_DELTA'

VAR_POINT_RADIUS = 'VAR_POINT_RADIUS'
VAR_LINE_RADIUS = 'VAR_LINE_RADIUS'
VAR_ARROW_RADIUS = 'VAR_ARROW_RADIUS'
VAR_ARROW_LENGTH = 'VAR_ARROW_LENGTH'
VAR_FACE_WIDTH = 'VAR_FACE_WIDTH'

VAR_DESK_TEXT_STR = 'VAR_DESK_TEXT_STR'
VAR_DESK_TEXT_STYLE = 'VAR_DESK_TEXT_STYLE'
VAR_DESK_PAPER_XYZ = 'VAR_DESK_PAPER_XYZ'
VAR_DESK_HEIGHT = 'VAR_DESK_HEIGHT'
VAR_DESK_BORDER_SIZE = 'VAR_DESK_BORDER_SIZE'
VAR_DESK_AXIS_SIZE = 'VAR_DESK_AXIS_SIZE'
VAR_DESK_COORD_MARK_DIV = 'VAR_DESK_COORD_MARK_DIV'
VAR_DESK_PIN_OFFSET = 'VAR_DESK_PIN_OFFSET'
VAR_DESK_PIN_RADIUS = 'VAR_DESK_PIN_RADIUS'
VAR_DESK_PIN_HEIGHT = 'VAR_DESK_PIN_HEIGHT'
VAR_DESK_DRAW_AREA_SIZE = 'VAR_DESK_DRAW_AREA_SIZE'
VAR_DESK_BOARD_STYLE = 'VAR_DESK_BOARD_STYLE'
VAR_DESK_PAPER_STYLE = 'VAR_DESK_PAPER_STYLE'
VAR_DESK_PIN_STYLE = 'VAR_DESK_PIN_STYLE'

VAR_COORD_X_COLOR = 'VAR_COORD_X_COLOR'
VAR_COORD_Y_COLOR = 'VAR_COORD_Y_COLOR'
VAR_COORD_Z_COLOR = 'VAR_COORD_Z_COLOR'
VAR_COORD_C_COLOR = 'VAR_COORD_C_COLOR'
VAR_COORD_LABEL_COLOR = 'VAR_COORD_LABEL_COLOR'
VAR_COORD_DELTA = 'VAR_COORD_DELTA'

VAR_FRAME_POINT_COLOR = 'VAR_FRAME_POINT_COLOR'
VAR_FRAME_LINE_COLOR = 'VAR_FRAME_LINE_COLOR'
VAR_FRAME_MATERIAL = 'VAR_FRAME_MATERIAL'

VAR_DEFAULTS = {

    VAR_MATERIAL: None,
    VAR_COLOR: None,
    VAR_TRANSPARENCY: None,
    VAR_TEXTURE: None,

    VAR_MAIN_SCALE: 1,
    VAR_GEOM_SCALE: 1,
    VAR_LABEL_SCALE: 1,

    VAR_LABEL_HEIGHT_PX: 20,  # not scaled

    VAR_LABEL_DELTA: 5,

    VAR_POINT_RADIUS: 8,
    VAR_LINE_RADIUS: 4,
    VAR_ARROW_RADIUS: 8,
    VAR_ARROW_LENGTH: 30,
    VAR_FACE_WIDTH: 2,

    VAR_DESK_TEXT_STR: 'A0 M1:1',
    VAR_DESK_HEIGHT: 20,
    VAR_DESK_BORDER_SIZE: 60,
    VAR_DESK_PAPER_XYZ: (1189, 841, 1),  # A0
    VAR_DESK_AXIS_SIZE: 300,
    VAR_DESK_COORD_MARK_DIV: 6,
    VAR_DESK_PIN_OFFSET: 30,
    VAR_DESK_PIN_RADIUS: 10,
    VAR_DESK_PIN_HEIGHT: 2,
    VAR_DESK_DRAW_AREA_SIZE: 400,
    VAR_DESK_BOARD_STYLE: (PLASTIC_MATERIAL, WOOD_COLOR, FULL_VISIBLE_TRANSPARENCY, None),
    VAR_DESK_PAPER_STYLE: (PLASTIC_MATERIAL, PAPER_COLOR, FULL_VISIBLE_TRANSPARENCY, None),
    VAR_DESK_PIN_STYLE: (STEEL_MATERIAL, None, FULL_VISIBLE_TRANSPARENCY, None),
    VAR_DESK_TEXT_STYLE: (None, NICE_WHITE_COLOR, FULL_VISIBLE_TRANSPARENCY, None),

    VAR_COORD_X_COLOR: NICE_RED_COLOR,
    VAR_COORD_Y_COLOR: NICE_GREEN_COLOR,
    VAR_COORD_Z_COLOR: NICE_BLUE_COLOR,
    VAR_COORD_C_COLOR: NICE_WHITE_COLOR,
    VAR_COORD_LABEL_COLOR: NICE_YELLOW_COLOR,
    VAR_COORD_DELTA: 50,

    VAR_FRAME_POINT_COLOR: NICE_YELLOW_COLOR,
    VAR_FRAME_LINE_COLOR: NICE_BLUE_COLOR,
    VAR_FRAME_MATERIAL: CHROME_MATERIAL,
}


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
    def __init__(self, defaults):
        self.defaults = defaults
        self.vars = {}
        self.levels = ['root']

    def _dump(self):
        print('******* Registry dump **********')
        for var in self.vars:
            print(var, ' = ', self.vars[var])

        path = ''
        for levelName in self.levels:
            path += '.' + levelName
        print('CURRENT: ', path)

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

        if varName in self.defaults:
            return self.defaults[varName]

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

    def render(self, screenX: int = 1200, screenY: int = 980):
        display, display_start, add_menu, add_function_to_menu = init_display(
            None, (screenX, screenY), True, [128, 128, 128], [128, 128, 128])

        for ais in self.rootsAis:
            display.Context.Display(ais, False)

        # display.DisplayMessage(labelPnt, text, heightPx, color, False)

        display.FitAll()
        display_start()

    def childrenBegin(self):
        self.parentAis = self.currentAis
        self.currentAis = None

    def childrenEnd(self):
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


def Render():
    scene.render()


def LevelBegin(nm):
    reg.levelBegin(nm)


def LevelEnd():
    reg.levelEnd()


def ChildrenBegin():
    scene.childrenBegin()


def ChildrenEnd():
    scene.childrenEnd()


def SetVar(varName, varValue, varPath=None):
    reg.setVar(varName, varValue, varPath)


def GetVar(varName, defaultValue=None):
    return reg.getVar(varName, defaultValue)


def SetColor(color):
    SetVar(VAR_COLOR, color)


def SetTransparency(transparency):
    SetVar(VAR_TRANSPARENCY, transparency)


def SetMaterial(material):
    SetVar(VAR_MATERIAL, material)


def SetTexture(texture):
    SetVar(VAR_TEXTURE, texture)


def SetStyle(style):
    material, color, transparency, texture = style
    SetMaterial(material)
    SetColor(color)
    SetTransparency(transparency)
    SetTexture(texture)


def DoHide():
    scene.doHide()


def DoMove(moveCoord):
    trsf = gp_Trsf()
    trsf.SetTranslation(_vec(moveCoord))
    scene.doTrsf(trsf)


def DoRotate(axFromCoord, axToCoord, angle):
    trsf = gp_Trsf()
    ax1 = gp_Ax1(_pnt(axFromCoord), gp_Dir(gp_Vec(_pnt(axFromCoord), axToCoord)))
    trsf.SetRotation(ax1, angle / 180 * math.pi)
    scene.doTrsf(trsf)


def DoRotateX(angle):
    DoRotate(Decart(0, 0, 0), Decart(1, 0, 0), angle)


def DoRotateY(angle):
    DoRotate(Decart(0, 0, 0), Decart(0, 1, 0), angle)


def DoRotateZ(angle):
    DoRotate(Decart(0, 0, 0), Decart(0, 0, 1), angle)


def DoDirect(fromCoord, toCoord):
    trsf = gp_Trsf()

    dirVec = gp_Vec(_pnt(fromCoord), _pnt(toCoord))
    targetDir = gp_Dir(dirVec)

    rotateAngle = gp_Dir(0, 0, 1).Angle(targetDir)
    if not gp_Dir(0, 0, 1).IsParallel(targetDir, 0.001):
        rotateDir = gp_Dir(0, 0, 1)
        rotateDir.Cross(targetDir)
    else:
        rotateDir = gp_Dir(0, 1, 0)

    trsf.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), rotateDir), rotateAngle)
    trsf.SetTranslationPart(_vec(fromCoord))
    scene.doTrsf(trsf)


def DrawShape(argShape):
    shape = GetVar(ARG_SHAPE, argShape)

    material = GetVar(VAR_MATERIAL)
    transparency = GetVar(VAR_TRANSPARENCY)
    color = GetVar(VAR_COLOR)

    scene.drawShape(shape, material, transparency, color)


def DrawLabel(argCoord, argText):
    coord = GetVar(ARG_COORD, argCoord)
    text = GetVar(ARG_TEXT, argText)

    pnt = _pnt(coord)

    transparency = GetVar(VAR_TRANSPARENCY)
    color = GetVar(VAR_COLOR)
    mainScale = GetVar(VAR_MAIN_SCALE)
    labelScale = GetVar(VAR_LABEL_SCALE)
    labelHeightPx = GetVar(VAR_LABEL_HEIGHT_PX)
    labelDelta = GetVar(VAR_LABEL_DELTA)

    delta = labelDelta * mainScale
    heightPx = labelHeightPx * labelScale
    targetPnt = pnt.Translated(gp_Vec(delta, delta, delta))
    scene.drawLabel(targetPnt, text, heightPx, color, transparency)


def DrawSphere(argRadius):
    radius = GetVar(ARG_RADIUS, argRadius)

    shape = comp.compute('computeSphere', radius)
    LevelBegin('Shape')
    DrawShape(shape)
    LevelEnd()


def DrawDummy():
    DrawSphere(1)
    DoHide()


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


def DrawPoint(argCoord):
    coord = GetVar(ARG_COORD, argCoord)

    mainScale = GetVar(VAR_MAIN_SCALE)
    geomScale = GetVar(VAR_GEOM_SCALE)
    pointRadius = GetVar(VAR_POINT_RADIUS)

    r = pointRadius * geomScale * mainScale

    LevelBegin('Sphere')
    DrawSphere(r)
    DoMove(coord)
    LevelEnd()


def DrawLine(argCoord1, argCoord2):
    coord1 = GetVar(ARG_COORD_1, argCoord1)
    coord2 = GetVar(ARG_COORD_2, argCoord2)

    pnt1 = _pnt(coord1)
    pnt2 = _pnt(coord2)

    mainScale = GetVar(VAR_MAIN_SCALE)
    geomScale = GetVar(VAR_GEOM_SCALE)
    lineRadius = GetVar(VAR_LINE_RADIUS)

    r = lineRadius * mainScale * geomScale
    length = gp_Vec(pnt1, pnt2).Magnitude()

    LevelBegin('Cylinder')
    DrawCylinder(r, length)
    DoDirect(_coord(pnt1), _coord(pnt2))
    LevelEnd()


def DrawArrow(argCoord1, argCoord2):
    coord1 = GetVar(ARG_COORD_1, argCoord1)
    coord2 = GetVar(ARG_COORD_2, argCoord2)

    pnt1 = _pnt(coord1)
    pnt2 = _pnt(coord2)

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

    LevelBegin('VectorLine')
    DrawLine(_coord(pnt1), _coord(pntM))
    LevelEnd()

    LevelBegin('VectorFinishCone')
    DrawCone(scaledArrowRadius, 0, scaledArrowLength)
    DoDirect(_coord(pntM), _coord(pnt2))
    LevelEnd()


def DrawArrow2(argCoord1, argCoord2):
    coord1 = GetVar(ARG_COORD_1, argCoord1)
    coord2 = GetVar(ARG_COORD_2, argCoord2)

    pnt1 = _pnt(coord1)
    pnt2 = _pnt(coord2)

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

    LevelBegin('ArrowLine')
    DrawLine(pntM1, pntM2)
    LevelEnd()
    LevelBegin('ArrowStartCone')
    DrawCone(scaledArrowRadius, 0, scaledArrowLength)
    LevelEnd()
    DoDirect(pntM1, pnt1)
    LevelBegin('ArrowFinishCone')
    DrawCone(scaledArrowRadius, 0, scaledArrowLength)
    LevelEnd()
    DoDirect(pntM2, pnt2)


def helperCircleWire(pnt1, pnt2, pnt3):
    geomCircle = GC_MakeCircle(pnt1, pnt2, pnt3).Value()
    edge = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
    return BRepBuilderAPI_MakeWire(edge).Wire()


def DrawWire(argWire):
    wire = GetVar(ARG_WIRE, argWire)

    wireRadius = GetVar(VAR_LINE_RADIUS)
    mainScale = GetVar(VAR_MAIN_SCALE)
    geomScale = GetVar(VAR_GEOM_SCALE)

    scaledWireRadius = wireRadius * mainScale * geomScale

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

    profileCircle = GC_MakeCircle(startPoint, tangentDir, scaledWireRadius).Value()
    profileEdge = BRepBuilderAPI_MakeEdge(profileCircle).Edge()
    profileWire = BRepBuilderAPI_MakeWire(profileEdge).Wire()

    shape = BRepOffsetAPI_MakePipe(wire, profileWire).Shape()
    LevelBegin('WireShape')
    DrawShape(shape)
    LevelEnd()


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



def DrawBoxFrame(argCoord1, argCoord2):
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


def DrawLimits(argCoord1, argCoord2):

    SetVar(VAR_FRAME_POINT_COLOR, NICE_GRAY_COLOR, 'BoxFrame')
    SetVar(VAR_FRAME_LINE_COLOR, NICE_GRAY_COLOR, 'BoxFrame')
    DrawBoxFrame(argCoord1, argCoord2)


def DrawDecor(isDesk=True, isCoord=True, isLimits=True):

    if isDesk:
        DrawDummy()
        ChildrenBegin()
        DrawDesk()
        ChildrenEnd()
        DoMove(Decart(0, 0, -100))
    if isCoord:
        DrawCoord(Decart(0, 0, 0), Decart(500, 400, 500))
    if isLimits:
        DrawLimits(Decart(-400, -300, 0), Decart(400, 300, 400))


'''
        n = DESK_COORD_MARK_DIV
        self.addItem(AxisDraw(argCoord1, Pnt(size, 0, 0), n))
        self.addItem(AxisDraw(Pnt(0, 0, 0), Pnt(0, size, 0), n))
        Set
        DrawAxis(Pnt(0, 0, 0), Pnt(0, 0, size), n))
        DrawPoint(argCoord1)
'''
