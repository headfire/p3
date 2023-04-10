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

WHITE_COLOR = 0xF0F0F0
GRAY_COLOR = 0x646464

RED_COLOR = 0xC81E1E
GREEN_COLOR = 0x1EC81E
BLUE_COLOR =  0x1E1EC8

YELLOW_COLOR = 0xC8C81E
CYAN_COLOR = 0x1EC8C8
MAGENTA_COLOR = 0xC81EC8

DARK_WHITE_COLOR = 0x787878
DARK_GRAY_COLOR = 0x323232

DARK_RED_COLOR = 0x640F0F
DARK_GREEN_COLOR = 0x0F640F
DARK_BLUE_COLOR =  0x0F0F64

DARK_YELLOW_COLOR = 0x64640F
DARK_CYAN_COLOR = 0x0F6464
DARK_MAGENTA_COLOR = 0x640F64


WOOD_COLOR = 0xD0751C
PAPER_COLOR = 0xE6E6E6
STEEL_COLOR = 0x646464
GOLD_COLOR = 0xFFB92D


FULL_VISIBLE_TRANSPARENCY = 0
SEMI_VISIBLE_TRANSPARENCY = 0.5
NO_VISIBLE_TRANSPARENCY = 1

LABEL = 'DESK_LABEL_'
SOLID = 'DESK_SOLID_'
SURFACE = 'DESK_SURFACE_'
POINT = 'DESK_POINT_'
LINE = 'DESK_LINE_'

COLOR = 'COLOR'
MATERIAL = 'MATERIAL'
TRANSPARENCY = 'TRANSPARENCY'

# *************************************************
# Style vars
# *************************************************

DESK_LABEL_MATERIAL = 'DESK_LABEL_MATERIAL'
DESK_LABEL_COLOR = 'DESK_LABEL_COLOR'
DESK_LABEL_TRANSPARENCY = 'DESK_LABEL_TRANSPARENCY'

DESK_POINT_MATERIAL = 'DESK_POINT_MATERIAL'
DESK_POINT_COLOR = 'DESK_POINT_COLOR'
DESK_POINT_TRANSPARENCY = 'DESK_POINT_TRANSPARENCY'

DESK_LINE_MATERIAL = 'DESK_LINE_MATERIAL'
DESK_LINE_COLOR = 'DESK_LINE_COLOR'
DESK_LINE_TRANSPARENCY = 'DESK_LINE_TRANSPARENCY'

DESK_SOLID_MATERIAL = 'DESK_SOLID_MATERIAL'
DESK_SOLID_COLOR = 'DESK_SOLID_COLOR'
DESK_SOLID_TRANSPARENCY = 'DESK_SOLID_TRANSPARENCY'

DESK_SURFACE_MATERIAL = 'DESK_SURFACE_MATERIAL'
DESK_SURFACE_COLOR = 'DESK_SURFACE_COLOR'
DESK_SURFACE_TRANSPARENCY = 'DESK_SURFACE_TRANSPARENCY'


# *************************************************
# Geom vars
# *************************************************

DESK_MAIN_SCALE_TEXT = 'DESK_MAIN_SCALE_TEXT'
DESK_MAIN_SCALE = 'DESK_MAIN_SCALE'
DESK_GEOM_SCALE = 'DESK_GEOM_SCALE'
DESK_LABEL_SCALE = 'DESK_LABEL_SCALE'

DESK_POINT_RADIUS = 'DESK_POINT_RADIUS'
DESK_LINE_RADIUS = 'DESK_LINE_RADIUS'
DESK_MARK_RADIUS = 'DESK_MARK_RADIUS'
DESK_MARK_LENGTH = 'DESK_MARK_LENGTH'
DESK_ARROW_RADIUS = 'DESK_ARROW_RADIUS'
DESK_ARROW_LENGTH = 'DESK_ARROW_LENGTH'
DESK_SURFACE_WIDTH = 'DESK_SURFACE_WIDTH'

DESK_LABEL_STEP = 'DESK_LABEL_STEP'
DESK_LABEL_HEIGHT_PX = 'TEXT_HEIGHT_PX'

DESK_AXES_X_COLOR = 'DESK_AXES_X_COLOR'
DESK_AXES_Y_COLOR = 'DESK_AXES_Y_COLOR'
DESK_AXES_Z_COLOR = 'DESK_AXES_Z_COLOR'
DESK_AXES_C_COLOR = 'DESK_AXES_C_COLOR'
DESK_AXES_LABEL_COLOR = 'DESK_AXES_LABEL_COLOR'

# ***************************************************
# ***************************************************
# ***************************************************

DESK_DEFAULT_STYLE = {

    DESK_LABEL_HEIGHT_PX: 20,  # not scaled
    DESK_LABEL_STEP: 5,

    DESK_POINT_RADIUS: 8,
    DESK_LINE_RADIUS: 4,
    DESK_MARK_RADIUS: 8,
    DESK_MARK_LENGTH: 4,
    DESK_ARROW_RADIUS: 8,
    DESK_ARROW_LENGTH: 30,
    DESK_SURFACE_WIDTH: 2,

    DESK_AXES_X_COLOR: RED_COLOR,
    DESK_AXES_Y_COLOR: GREEN_COLOR,
    DESK_AXES_Z_COLOR: BLUE_COLOR,
    DESK_AXES_C_COLOR: WHITE_COLOR,
    DESK_AXES_LABEL_COLOR: YELLOW_COLOR,

}


DESK_MAIN_STYLE = {

    DESK_POINT_MATERIAL: CHROME_MATERIAL,
    DESK_POINT_COLOR: GOLD_COLOR,
    DESK_POINT_TRANSPARENCY: 0,

    DESK_LINE_MATERIAL: CHROME_MATERIAL,
    DESK_LINE_COLOR: BLUE_COLOR,
    DESK_LINE_TRANSPARENCY: 0,

    DESK_SOLID_MATERIAL: CHROME_MATERIAL,
    DESK_SOLID_COLOR: WHITE_COLOR,
    DESK_SOLID_TRANSPARENCY: 0,

    DESK_SURFACE_MATERIAL: CHROME_MATERIAL,
    DESK_SURFACE_COLOR: GRAY_COLOR,
    DESK_SURFACE_TRANSPARENCY: 0.6,

    DESK_LABEL_COLOR: YELLOW_COLOR,
    DESK_LABEL_TRANSPARENCY: 0,

    DESK_GEOM_SCALE: 1

}

FOCUS_STYLE = {

    DESK_POINT_MATERIAL: CHROME_MATERIAL,
    DESK_POINT_COLOR: GOLD_COLOR,
    DESK_POINT_TRANSPARENCY: 0,

    DESK_LINE_MATERIAL: CHROME_MATERIAL,
    DESK_LINE_COLOR: BLUE_COLOR,
    DESK_LINE_TRANSPARENCY: 0,

    DESK_SOLID_MATERIAL: CHROME_MATERIAL,
    DESK_SOLID_COLOR: WHITE_COLOR,
    DESK_SOLID_TRANSPARENCY: 0,

    DESK_SURFACE_MATERIAL: CHROME_MATERIAL,
    DESK_SURFACE_COLOR: GRAY_COLOR,
    DESK_SURFACE_TRANSPARENCY: 0.6,

    DESK_LABEL_COLOR: GRAY_COLOR,
    DESK_LABEL_TRANSPARENCY: 0,

    DESK_GEOM_SCALE: 0.7

}

INFO_STYLE = {

    DESK_POINT_MATERIAL: CHROME_MATERIAL,
    DESK_POINT_COLOR: GOLD_COLOR,
    DESK_POINT_TRANSPARENCY: 0,

    DESK_LINE_MATERIAL: CHROME_MATERIAL,
    DESK_LINE_COLOR: BLUE_COLOR,
    DESK_LINE_TRANSPARENCY: 0,

    DESK_SOLID_MATERIAL: CHROME_MATERIAL,
    DESK_SOLID_COLOR: WHITE_COLOR,
    DESK_SOLID_TRANSPARENCY: 0,

    DESK_SURFACE_MATERIAL: CHROME_MATERIAL,
    DESK_SURFACE_COLOR: GRAY_COLOR,
    DESK_SURFACE_TRANSPARENCY: 0.6,

    DESK_LABEL_COLOR: GRAY_COLOR,
    DESK_LABEL_TRANSPARENCY: 0,

    DESK_GEOM_SCALE: 0.7


}


DESK_M_1_1_STYLE = {
    DESK_MAIN_SCALE_TEXT: 'A0 M1:1',
    DESK_MAIN_SCALE: 1
}

DESK_M_5_1_STYLE = {
    DESK_MAIN_SCALE_TEXT: 'A0 M5:1',
    DESK_MAIN_SCALE: 1/5
}


DESK_BOARD_STYLE = {
    DESK_SOLID_MATERIAL: PLASTIC_MATERIAL,
    DESK_SOLID_COLOR: WOOD_COLOR
    }

DESK_PAPER_STYLE = {
    DESK_SOLID_MATERIAL: PLASTIC_MATERIAL,
    DESK_SOLID_COLOR: PAPER_COLOR
    }

DESK_PIN_STYLE = {
    DESK_SOLID_MATERIAL: STEEL_MATERIAL,
    DESK_SOLID_COLOR: None
    }

DESK_LABEL_STYLE = {
    DESK_LABEL_COLOR: WHITE_COLOR
    }

DESK_HEIGHT = 20
DESK_BORDER_SIZE = 60
DESK_PAPER_X: 1189  # A0
DESK_PAPER_Y: 841  # A0
DESK_PAPER_Z: 1  # A0
DESK_PIN_OFFSET: 30
DESK_PIN_RADIUS: 10
DESK_PIN_HEIGHT: 2

DESK_DRAW_AREA_X1: -400
DESK_DRAW_AREA_Y1: -300
DESK_DRAW_AREA_Z1: 0

DESK_DRAW_AREA_X2: 400
DESK_DRAW_AREA_Y2: 300
DESK_DRAW_AREA_Z2: 400

DESK_AXES_STEP: 50

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
        self.registry = {}
        self.setStyle(DESK_DEFAULT_STYLE)
        self.setStyle(DESK_MAIN_STYLE)
        self.setStyle(DESK_M_1_1_STYLE)

    def setVar(self, varName, varValue):
        self.registry[varName] = varValue

    def getVar(self, varName):
        return self.registry[varName]

    def backupVars(self):
        return self.registry.copy()

    def restoreVars(self, backup):
        self.registry = backup

    def setStyle(self, style):
        for var in style:
            self.registry[var] = style[var]

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


scene = Scene()
comp = DeskComputer()


def SetVar(varName, varValue):
    scene.setVar(varName, varValue)


def GetVar(varName):
    return scene.getVar(varName)


def BackupVars():
    return scene.backupVars()


def RestoreVars(backup):
    scene.restoreVars(backup)


def SetStyle(style):
    scene.setStyle(style)


def SetStyleVar(drawType, styleVar, varValue):
    if drawType is not None:
        drawTypes = [drawType]
    else:
        drawTypes = [POINT, LINE, SURFACE, SOLID, LABEL]
    for styleDrawType in drawTypes:
        SetVar(styleDrawType + styleVar, varValue)


def SetColor(color, drawType=None):
    SetStyleVar(COLOR, drawType, color)


def SetTransparency(transparency, drawType=None):
    SetStyleVar(TRANSPARENCY, drawType, transparency)


def SetMaterial(material, drawType=None):
    SetStyleVar(MATERIAL, drawType, material)


def ScaleMain(value):
    mainScale = GetVar(DESK_MAIN_SCALE)
    return value * mainScale


def ScaleGeom(value):
    mainScale = GetVar(DESK_MAIN_SCALE)
    geomScale = GetVar(DESK_GEOM_SCALE)
    return value * mainScale * geomScale


# *************************************************************
# VM level
# *************************************************************


def Decart(x, y, z):
    return gp_Pnt(x, y, z)


def GroupBegin():
    scene.groupBegin()


def GroupEnd():
    scene.groupEnd()


def DoMove(pnt):
    trsf = gp_Trsf()
    trsf.SetTranslation(gp_Vec(Decart(0,0,0), pnt))
    scene.doTrsf(trsf)


def DoRotate(axFromPnt, axToPnt, angle):
    trsf = gp_Trsf()
    ax1 = gp_Ax1(axFromPnt, gp_Dir(gp_Vec(axFromPnt, axToPnt)))
    trsf.SetRotation(ax1, angle / 180 * math.pi)
    scene.doTrsf(trsf)


def DoRotateX(angle):
    DoRotate(Decart(0, 0, 0), Decart(1, 0, 0), angle)


def DoRotateY(angle):
    DoRotate(Decart(0, 0, 0), Decart(0, 1, 0), angle)


def DoRotateZ(angle):
    DoRotate(Decart(0, 0, 0), Decart(0, 0, 1), angle)


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
    trsf.SetTranslationPart(gp_Vec(Decart(0, 0, 0), fromPnt))
    scene.doTrsf(trsf)


def DrawLabel(pnt, text):

    transparency = GetVar(DESK_LABEL_TRANSPARENCY)
    color = GetVar(DESK_LABEL_COLOR)
    heightPx = GetVar(DESK_LABEL_HEIGHT_PX)
    step = ScaleMain(GetVar(DESK_LABEL_STEP))

    targetPnt = pnt.Translated(gp_Vec(step, step, step))
    scene.drawLabel(targetPnt, text, heightPx, color, transparency)


def DrawShape(shape, stylePrefix):
    material = GetVar(stylePrefix + '_MATERIAL')
    color = GetVar(stylePrefix + '_COLOR')
    transparency = GetVar(stylePrefix + '_TRANSPARENCY')
    scene.drawShape(shape, color, transparency, material)


def DrawSolid(shape):
    DrawShape(shape, 'DESK_SOLID')


def DrawSurface(shape):
    DrawShape(shape, 'DESK_SURFACE')


def DrawPipe(wire, wireRadius):

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
    DrawShape(shape, LINE)


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
    DrawSolid(shape)


def DrawPoint(pnt):
    r = ScaleGeom(GetVar(DESK_POINT_RADIUS))
    DrawShape(r, 'DESK_POINT')


def DrawLine(pnt1, pnt2):
    r = ScaleGeom(GetVar(DESK_LINE_RADIUS))
    length = gp_Vec(pnt1, pnt2).Magnitude()

    shape = comp.compute('computeCylinder', r, length)
    DrawShape(shape, 'DESK_LINE')
    DoDirect(pnt1, pnt2)


def DrawArrow(pnt1, pnt2):
    r = ScaleGeom(GetVar(DESK_ARROW_RADIUS))
    h = ScaleGeom(GetVar(DESK_ARROW_LENGTH))

    shape = comp.compute('computeCone', r, 0, h)
    DrawShape(shape, 'DESK_LINE')
    DoDirect(pnt1, pnt2)


def DrawLineArrow(pnt1, pnt2):

    arrowLength = ScaleGeom(GetVar(DESK_ARROW_LENGTH))

    v = gp_Vec(pnt1, pnt2)
    vLen = v.Magnitude()
    v *= -arrowLength / vLen
    pntM2 = pnt2.Translated(v)

    GroupBegin()
    DrawLine(pnt1, pntM2)
    DrawArrow(pntM2, pnt2)
    GroupEnd()


def DrawLineArrow2(pnt1, pnt2):

    arrowLength = ScaleGeom(GetVar(DESK_ARROW_LENGTH))

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

    wireRadius = ScaleGeom(GetVar(DESK_LINE_RADIUS))

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
    DrawShape(shape, LINE)



# *************************************************************
# Use level
# *************************************************************

def DrawCircle(pnt1, pnt2, pnt3):

    geomCircle = GC_MakeCircle(pnt1, pnt2, pnt3).Value()
    edge = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
    wire = BRepBuilderAPI_MakeWire(edge).Wire()

    DrawWire(wire)


def DrawDesk():

    borderSize = ScaleMain(GetVar(DESK_BORDER_SIZE))
    deskHeight = ScaleMain(GetVar(DESK_HEIGHT))

    textStr = GetVar(DESK_MAIN_SCALE_TEXT)

    pinOffset = ScaleMain(GetVar(DESK_PIN_OFFSET))
    pinRadius = ScaleMain(GetVar(DESK_PIN_RADIUS))
    pinHeight = ScaleMain(GetVar(DESK_PIN_HEIGHT))

    psx = ScaleMain(GetVar(DESK_PAPER_X))
    psy = ScaleMain(GetVar(DESK_PAPER_Y))
    psz = ScaleMain(GetVar(DESK_PAPER_Z))
    bsx = psx + borderSize * 2
    bsy = psy + borderSize * 2
    bsz = deskHeight

    backup = BackupVars()

    SetStyle(DESK_BOARD_STYLE)
    DrawBox(bsx, bsy, bsz)
    DoMove(Decart(-bsx / 2, -bsy / 2, -bsz - psz))

    SetStyle(DESK_PAPER_STYLE)
    DrawBox(psx, psy, psz)
    DoMove(Decart(-psx / 2, -psy / 2, -psz))

    SetStyle(DESK_LABEL_STYLE)
    DrawLabel(Decart(-bsx / 2, -bsy / 2, bsz * 3), textStr)

    dx = (psx / 2 - pinOffset)
    dy = (psy / 2 - pinOffset)

    pins = [
        (-dx, -dy),
        (dx, -dy),
        (dx, dy),
        (-dx, dy),
    ]

    SetStyle(DESK_PIN_STYLE)
    for x, y in pins:
        DrawCylinder(pinRadius, pinHeight)
        DoMove(Decart(x, y, 0))

    RestoreVars(backup)


def DrawAxis(pnt1, pnt2, step):

    markRadius = ScaleGeom(GetVar(DESK_MARK_RADIUS))
    markLength = ScaleGeom(GetVar(DESK_MARK_LENGTH))

    DrawArrow(pnt1, pnt2)

    v = gp_Vec(pnt1, pnt2)
    totalLen = v.Magnitude()
    cnt = int(totalLen / step - 1)

    for i in range(cnt):
        targetLen = (1 + i) * step
        v = gp_Vec(pnt1, pnt2)
        v *= targetLen / totalLen
        pntMark = pnt1.Translated(v)

        DrawCylinder(markRadius, markLength)
        DoMove(Decart(0, 0, -markLength/2))
        DoDirect(pntMark, pnt2)


def DrawAxes(pnt1, pnt2, step):

    xColor = GetVar(DESK_AXES_X_COLOR)
    yColor = GetVar(DESK_AXES_Y_COLOR)
    zColor = GetVar(DESK_AXES_Z_COLOR)
    cColor = GetVar(DESK_AXES_C_COLOR)
    labelColor = GetVar(DESK_AXES_LABEL_COLOR)

    xPnt = Decart(pnt2.X(), pnt1.Y(), pnt1.Z())
    yPnt = Decart(pnt1.X(), pnt2.Y(), pnt1.Z())
    zPnt = Decart(pnt1.X(), pnt1.Y(), pnt2.Z())

    SetColor(xColor)
    DrawAxis(pnt1, xPnt, step)

    SetColor(yColor)
    DrawAxis(pnt1, yPnt, step)

    SetColor(zColor)
    DrawAxis(pnt1, yPnt, step)

    SetColor(cColor)
    DrawPoint(pnt1)

    SetColor(labelColor)
    DrawLabel(xPnt, 'X')
    DrawLabel(yPnt, 'Y')
    DrawLabel(zPnt, 'Z')


def DrawFrame(points, lines, isLabeled):

    for pnt in points:
        DrawPoint(pnt)

    for i1, i2 in lines:
        DrawLine(points[i1], points[i2])

    if isLabeled:
        for pnt in points:
            DrawLabel(pnt, '(' + str(pnt.X()) + ',' + str(pnt.Y()) + ',' + str(pnt.Z()) + ')')


def DrawBoxFrame(pnt1, pnt2, isLabeled):

    x1, y1, z1 = pnt1.X(), pnt1.Y(), pnt1.Z()
    x2, y2, z2 = pnt2.X(), pnt2.Y(), pnt2.Z()

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

    DrawFrame(vertexes, edges, isLabeled)


def Show():
    scene.render()


