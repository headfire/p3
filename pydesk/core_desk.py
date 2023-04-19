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

from math import pi


# ***************************************************
# Base convert functions
# ***************************************************


def PlasticBrash(color=None, transparency=None):
    return color, transparency, Graphic3d_NameOfMaterial.Graphic3d_NOM_PLASTIC


def ChromeBrash(color=None, transparency=None):
    return color, transparency, Graphic3d_NameOfMaterial.Graphic3d_NOM_CHROME


def GoldBrash(color=None, transparency=None):
    return color, transparency, Graphic3d_NameOfMaterial.Graphic3d_NOM_GOLD


def TextBrash(color=None, transparency=None):
    return color, transparency, None


def InvisibleBrash():
    return None, 1, None


def DecartPnt(x, y, z):
    return gp_Pnt(x, y, z)


def IsEqualPnt(pnt1, pnt2):
    return pnt1.IsEqual(pnt2, EQUAL_POINTS_PRECISION)


def Rgb(r, g, b):
    return r, g, b


# ***************************************************
# Base constants
# ***************************************************

EQUAL_POINTS_PRECISION = 0.001
PI = pi

WHITE_COLOR = Rgb(0.9, 0.9, 0.9)
GRAY_COLOR = Rgb(0.6, 0.6, 0.6)
DARK_GRAY_COLOR = Rgb(0.3, 0.3, 0.3)

RED_COLOR = Rgb(0.9, 0.3, 0.3)
GREEN_COLOR = Rgb(0.3, 0.9, 0.3)
BLUE_COLOR = Rgb(0.3, 0.3, 0.9)

YELLOW_COLOR = Rgb(0.9, 0.9, 0.3)
CYAN_COLOR = Rgb(0.3, 0.9, 0.9)
MAGENTA_COLOR = Rgb(0.9, 0.3, 0.9)

DARK_RED_COLOR = Rgb(0.6, 0.3, 0.3)
DARK_GREEN_COLOR = Rgb(0.3, 0.6, 0.3)
DARK_BLUE_COLOR = Rgb(0.3, 0.3, 0.6)

DARK_YELLOW_COLOR = Rgb(0.6, 0.6, 0.3)
DARK_CYAN_COLOR = Rgb(0.3, 0.6, 0.6)
DARK_MAGENTA_COLOR = Rgb(0.6, 0.3, 0.6)

WOOD_COLOR = Rgb(0.82, 0.46, 0.11)
PAPER_COLOR = Rgb(0.90, 0.90, 0.90)
STEEL_COLOR = Rgb(0.39, 0.39, 0.39)
GOLD_COLOR = Rgb(0.99, 0.78, 0.12)

# ***************************************************
# Compute caching system
# ***************************************************


computeCache = {}


def Compute(func, arg1=None, arg2=None, arg3=None):
    args = ''
    if arg1 is not None:
        args += str(arg1)
    if arg2 is not None:
        args += ',' + str(arg2)
    if arg3 is not None:
        args += ',' + str(arg3)

    cacheKey = func.__module__ + '.' + func.__name__ + '(' + args + ')'

    if cacheKey in computeCache:
        print('==> Get from cache', cacheKey)
        obj = computeCache[cacheKey]
    else:
        print('==> Compute', cacheKey)
        if arg1 is None:
            obj = func()
        elif arg2 is None:
            obj = func(arg1)
        elif arg3 is None:
            obj = func(arg1, arg2)
        else:
            obj = func(arg1, arg2, arg3)
        computeCache[cacheKey] = obj
    return obj


def ComputeSphere(argRadius):
    return BRepPrimAPI_MakeSphere(argRadius).Shape()


def ComputeBox(argDx, argDy, argDz):
    return BRepPrimAPI_MakeBox(argDx, argDy, argDz).Shape()


def ComputeCone(argRadius1, argRadius2, argHeight):
    return BRepPrimAPI_MakeCone(argRadius1, argRadius2, argHeight).Shape()


def ComputeCylinder(argRadius, argHeight):
    return BRepPrimAPI_MakeCylinder(argRadius, argHeight).Shape()


def ComputeTorus(argRadius1, argRadius2):
    return BRepPrimAPI_MakeTorus(argRadius1, argRadius2).Shape()


# **************************************************************
# Virtual graphic machine
# **************************************************************

class Exporter:
    def __init__(self):
        self.lines = []
        self.dir = None

    @staticmethod
    def getArgStr(arg):
        return str(arg)

    def setDir(self, dirName):
        self.dir = dirName

    def log(self, funcName, arg1=None, arg2=None, arg3=None, arg4=None):

        if self.dir is None:
            return

        if arg4 is not None:
            args = self.getArgStr(arg1) + ', ' + self.getArgStr(arg2) + ', ' + self.getArgStr(
                arg3) + ', ' + self.getArgStr(arg4)
        elif arg3 is not None:
            args = self.getArgStr(arg1) + ', ' + self.getArgStr(arg2) + ', ' + self.getArgStr(arg3)
        elif arg2 is not None:
            args = self.getArgStr(arg1) + ', ' + self.getArgStr(arg2)
        elif arg1 is not None:
            args = self.getArgStr(arg1)
        else:
            args = ''

        self.lines.append(funcName + '(' + args + ')')

    def save(self):
        with open('scene.js', 'a') as f:
            for line in self.lines:
                f.write(line + '\n')


class Scene:

    def __init__(self):
        self.rootsAis: [Optional[AIS_Shape]] = []
        self.parentAis: Optional[AIS_Shape] = None
        self.currentAis: Optional[AIS_Shape] = None
        self.dummyShape = BRepPrimAPI_MakeSphere(0.0001).Shape()
        self.dummyBrash = InvisibleBrash()
        self.ex = Exporter()

    def _drawAis(self, ais: AIS_InteractiveObject, brash):

        color, transparency, material = brash

        if material is not None:
            aspect = Graphic3d_MaterialAspect(material)
            ais.SetMaterial(aspect)

        if transparency is not None:
            ais.SetTransparency(transparency)

        if color is not None:
            r, g, b = color
            qColor = Quantity_Color(r, g, b, Quantity_TypeOfColor(Quantity_TypeOfColor.Quantity_TOC_RGB))
            ais.SetColor(qColor)

        if self.parentAis is None:
            self.rootsAis.append(ais)
        else:
            self.parentAis.AddChild(ais)
        self.currentAis = ais

    def _doTrsf(self, trsf):
        trsf *= self.currentAis.LocalTransformation()
        self.currentAis.SetLocalTransformation(trsf)

    def _doMove(self, pnt):
        trsf = gp_Trsf()
        trsf.SetTranslation(gp_Vec(DecartPnt(0, 0, 0), pnt))
        self._doTrsf(trsf)

    def _doRotate(self, axFromPnt, axToPnt, angle):
        trsf = gp_Trsf()
        ax1 = gp_Ax1(axFromPnt, gp_Dir(gp_Vec(axFromPnt, axToPnt)))
        trsf.SetRotation(ax1, angle / 180 * math.pi)
        self._doTrsf(trsf)

    def _doDirect(self, fromPnt, toPnt):
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
        self._doTrsf(trsf)

    def _render(self, screenX: int = 1200, screenY: int = 980):
        display, display_start, add_menu, add_function_to_menu = init_display(
            None, (screenX, screenY), True, [128, 128, 128], [128, 128, 128])

        for ais in self.rootsAis:
            display.Context.Display(ais, False)

        display.FitAll()
        display_start()

    def _groupBegin(self):
        self._drawShape(self.dummyShape, self.dummyBrash)
        self.parentAis = self.currentAis
        self.currentAis = None

    def _groupEnd(self):
        self.currentAis = self.parentAis
        self.parentAis = self.parentAis.Parent()

    def _drawLabel(self, pnt, text, height, brash):

        ais = AIS_TextLabel()

        ais.SetText(TCollection_ExtendedString(text, True))
        ais.SetPosition(pnt)
        ais.SetHeight(height)

        self._drawAis(ais, brash)

    def _drawShape(self, shape, brash):
        ais = AIS_Shape(shape)
        self._drawAis(ais, brash)

    def _drawWire(self, wire, wireRadius, brash):

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
        self._drawShape(shape, brash)

    def doMove(self, pnt):
        self.ex.log('DoMove', pnt)
        self._doMove(pnt)

    def doRotate(self, axFromPnt, axToPnt, angle):
        self.ex.log('DoRotate', axFromPnt, axToPnt, angle)
        self._doRotate(axFromPnt, axToPnt, angle)

    def doRotateX(self, angle):
        self.ex.log('DoRotateX', angle)
        self._doRotate(gp_Pnt(0, 0, 0), gp_Pnt(1, 0, 0), angle)

    def doRotateY(self, angle):
        self.ex.log('DoRotateY', angle)
        self._doRotate(gp_Pnt(0, 0, 0), DecartPnt(0, 1, 0), angle)

    def doRotateZ(self, angle):
        self.ex.log('DoRotateZ', angle)
        self._doRotate(gp_Pnt(0, 0, 0), DecartPnt(0, 0, 1), angle)

    def doDirect(self, fromPnt, toPnt):
        self.ex.log('DoDirect', fromPnt, toPnt)
        self._doDirect(fromPnt, toPnt)

    def drawLabel(self, pnt, text, height, brash):
        self.ex.log('DrawLabel', pnt, text, height, brash)
        self._drawLabel(pnt, text, height, brash)

    def drawShape(self, shape, brash):
        self.ex.log('DrawShape', shape, brash)
        self._drawShape(shape, brash)

    def drawWire(self, wire, wireRadius, brash):
        self.ex.log('DrawWire', wire, wireRadius, brash)
        self._drawWire(wire, wireRadius, brash)

    def drawSphere(self, r, brash):
        self.ex.log('DrawSphere', r, brash)
        shape = Compute(ComputeSphere, r)
        self._drawShape(shape, brash)

    def drawBox(self, x, y, z, brash):
        self.ex.log('DrawBox', x, y, z, brash)
        shape = Compute(ComputeBox, x, y, z)
        self._drawShape(shape, brash)

    def drawCone(self, r1, r2, h, brash):
        self.ex.log('DrawCone', r1, r2, h, brash)
        shape = Compute(ComputeCone, r1, r2, h)
        self._drawShape(shape, brash)

    def drawCylinder(self, r, h, brash):
        self.ex.log('DrawCylinder', r, h, brash)
        shape = Compute(ComputeCylinder, r, h)
        self._drawShape(shape, brash)

    def drawTorus(self, r1, r2, brash):
        self.ex.log('DrawTorus', r1, r2, brash)
        shape = Compute(ComputeTorus, r1, r2)
        self._drawShape(shape, brash)

    def groupBegin(self):
        self.ex.log('GroupBegin')
        self._groupBegin()

    def groupEnd(self):
        self.ex.log('GroupEnd')
        self._groupEnd()

    def show(self):
        self.ex.log('Show')
        self._render()


scene = Scene()

# *************************************************
# Desk style vars
# *************************************************

DESK_LABEL_BRASH = 'DESK_LABEL_BRASH'
DESK_POINT_BRASH = 'DESK_POINT_BRASH'
DESK_LINE_BRASH = 'DESK_LINE_BRASH'
DESK_SOLID_BRASH = 'DESK_SOLID_BRASH'
DESK_SURFACE_BRASH = 'DESK_SURFACE_BRASH'

# *************************************************
# Desk geom vars
# *************************************************

DESK_SCALE_TEXT = 'DESK_SCALE_TEXT'
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

DESK_AXES_X_BRASH = 'DESK_AXES_X_BRASH'
DESK_AXES_Y_BRASH = 'DESK_AXES_Y_BRASH'
DESK_AXES_Z_BRASH = 'DESK_AXES_Z_BRASH'
DESK_AXES_C_BRASH = 'DESK_AXES_C_BRASH'
DESK_AXES_LABEL_BRASH = 'DESK_AXES_LABEL_BRASH'
DESK_AXES_STEP = 'DESK_AXES_STEP'

DESK_BOARD_HEIGHT = 'DESK_BOARD_HEIGHT'
DESK_BOARD_BORDER_SIZE = 'DESK_BOARD_BORDER_SIZE'
DESK_PAPER_SIZES = 'DESK_PAPER_XYZ'
DESK_PIN_OFFSET = 'DESK_PIN_OFFSET'
DESK_PIN_RADIUS = 'DESK_PIN_RADIUS'
DESK_PIN_HEIGHT = 'DESK_PIN_HEIGHT'

DESK_LIMITS_SIZES = 'DESK_LIMITS_SIZES'
DESK_BOARD_DOWN = 'DESK_BOARD_DOWN'

DESK_BOARD_BRASH = 'DESK_BOARD_BRASH'
DESK_PAPER_BRASH = 'DESK_PAPER_BRASH'
DESK_PIN_BRASH = 'DESK_PIN_BRASH'

# ***************************************************
# Style definitions
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

    DESK_AXES_X_BRASH: PlasticBrash(RED_COLOR),
    DESK_AXES_Y_BRASH: PlasticBrash(GREEN_COLOR),
    DESK_AXES_Z_BRASH: PlasticBrash(BLUE_COLOR),
    DESK_AXES_C_BRASH: PlasticBrash(WHITE_COLOR),
    DESK_AXES_LABEL_BRASH: PlasticBrash(YELLOW_COLOR),
    DESK_AXES_STEP: 50,

    DESK_BOARD_HEIGHT: 20,
    DESK_BOARD_BORDER_SIZE: 60,
    DESK_PAPER_SIZES: DecartPnt(1189, 841, 1),  # A0
    DESK_PIN_OFFSET: 30,
    DESK_PIN_RADIUS: 10,
    DESK_PIN_HEIGHT: 2,

    DESK_LIMITS_SIZES: DecartPnt(400, 300, 300),
    DESK_BOARD_DOWN: 100,

    DESK_BOARD_BRASH: PlasticBrash(WOOD_COLOR),
    DESK_PAPER_BRASH: PlasticBrash(PAPER_COLOR),
    DESK_PIN_BRASH: ChromeBrash(STEEL_COLOR),

}

DESK_MAIN_STYLE = {
    DESK_POINT_BRASH: GoldBrash(),
    DESK_LINE_BRASH: ChromeBrash(BLUE_COLOR),
    DESK_SOLID_BRASH: GoldBrash(),
    DESK_SURFACE_BRASH: ChromeBrash(GRAY_COLOR, 0.6),
    DESK_LABEL_BRASH: PlasticBrash(YELLOW_COLOR),
    DESK_GEOM_SCALE: 1
}

DESK_FOCUS_STYLE = {
    DESK_POINT_BRASH: ChromeBrash(RED_COLOR),
    DESK_LINE_BRASH: ChromeBrash(RED_COLOR),
    DESK_SOLID_BRASH: ChromeBrash(RED_COLOR),
    DESK_SURFACE_BRASH: ChromeBrash(RED_COLOR, 0.6),
    DESK_LABEL_BRASH: PlasticBrash(RED_COLOR),
    DESK_GEOM_SCALE: 0.7
}

DESK_INFO_STYLE = {
    DESK_POINT_BRASH: ChromeBrash(GRAY_COLOR),
    DESK_LINE_BRASH: ChromeBrash(GRAY_COLOR),
    DESK_SOLID_BRASH: ChromeBrash(GRAY_COLOR),
    DESK_SURFACE_BRASH: ChromeBrash(GRAY_COLOR, 0.6),
    DESK_LABEL_BRASH: PlasticBrash(GRAY_COLOR),
    DESK_GEOM_SCALE: 0.5
}

styles = {}


def SetVar(varName, varValue):
    global styles
    styles[varName] = varValue


def GetVar(varName):
    global styles
    return styles[varName]


def BackupVars():
    global styles
    return styles.copy()


def RestoreVars(backup):
    global styles
    styles = backup


def SetStyle(style):
    global styles
    for var in style:
        styles[var] = style[var]


def SetLabelBrash(brash):
    SetVar(DESK_LABEL_BRASH, brash)


def SetPointBrash(brash):
    SetVar(DESK_POINT_BRASH, brash)


def SetLineBrash(brash):
    SetVar(DESK_LINE_BRASH, brash)


def SetSurfaceBrash(brash):
    SetVar(DESK_SURFACE_BRASH, brash)


def SetSolidBrash(brash):
    SetVar(DESK_SOLID_BRASH, brash)


def SetScale(zoom, div):
    SetVar(DESK_SCALE_TEXT, 'M' + str(zoom) + ':' + str(div))
    SetVar(DESK_MAIN_SCALE, div / zoom)


def SetScaleGeom(scaleValue):
    SetVar(DESK_GEOM_SCALE, scaleValue)


def ScaleMain(value):
    mainScale = GetVar(DESK_MAIN_SCALE)
    return value * mainScale


def ScaleGeom(value):
    mainScale = GetVar(DESK_MAIN_SCALE)
    geomScale = GetVar(DESK_GEOM_SCALE)
    return value * mainScale * geomScale


# *************************************************
# Render control
# *************************************************


def Show():
    scene.show()


# *************************************************
# Hierarchy
# *************************************************


def GroupBegin():
    scene.groupBegin()


def GroupEnd():
    scene.groupEnd()


# *************************************************
# Object transformation
# *************************************************


def DoMove(pnt):
    scene.doMove(pnt)


def DoRotate(axFromPnt, axToPnt, angle):
    scene.doRotate(axFromPnt, axToPnt, angle)


def DoRotateX(angle):
    scene.doRotateX(angle)


def DoRotateY(angle):
    scene.doRotateY(angle)


def DoRotateZ(angle):
    scene.doRotateZ(angle)


def DoDirect(fromPnt, toPnt):
    scene.doDirect(fromPnt, toPnt)


# *************************************************
# Base primitives
# *************************************************

def DrawLabel(pnt, text):
    brash = GetVar(DESK_LABEL_BRASH)
    heightPx = GetVar(DESK_LABEL_HEIGHT_PX)
    step = ScaleMain(GetVar(DESK_LABEL_STEP))
    targetPnt = pnt.Translated(gp_Vec(step, step, step))
    scene.drawLabel(targetPnt, text, heightPx, brash)


def DrawSolid(shape):
    brash = GetVar(DESK_SOLID_BRASH)
    scene.drawShape(shape, brash)


def DrawSurface(shape):
    brash = GetVar(DESK_SURFACE_BRASH)
    scene.drawShape(shape, brash)


# *************************************************
# Construct primitives
# *************************************************


def DrawSphere(r):
    brash = GetVar(DESK_SOLID_BRASH)
    scene.drawSphere(r, brash)


def DrawBox(x, y, z):
    brash = GetVar(DESK_SOLID_BRASH)
    scene.drawBox(x, y, z, brash)


def DrawCone(r1, r2, h):
    brash = GetVar(DESK_SOLID_BRASH)
    scene.drawCone(r1, r2, h, brash)


def DrawCylinder(r, h):
    brash = GetVar(DESK_SOLID_BRASH)
    scene.drawCylinder(r, h, brash)


def DrawTorus(r1, r2):
    brash = GetVar(DESK_SOLID_BRASH)
    scene.drawTorus(r1, r2, brash)


# *************************************************
# Geom primitives
# *************************************************

def DrawPoint(pnt):
    brash = GetVar(DESK_POINT_BRASH)
    r = ScaleGeom(GetVar(DESK_POINT_RADIUS))
    scene.drawSphere(r, brash)
    scene.doMove(pnt)


def DrawLine(pnt1, pnt2):
    brash = GetVar(DESK_LINE_BRASH)
    r = ScaleGeom(GetVar(DESK_LINE_RADIUS))
    length = gp_Vec(pnt1, pnt2).Magnitude()
    scene.drawCylinder(r, length, brash)
    scene.doDirect(pnt1, pnt2)


def DrawArrowEnd(pnt1, pnt2):
    brash = GetVar(DESK_LINE_BRASH)
    r = ScaleGeom(GetVar(DESK_ARROW_RADIUS))
    h = ScaleGeom(GetVar(DESK_ARROW_LENGTH))
    scene.drawCone(r, 0, h, brash)
    scene.doDirect(pnt1, pnt2)


def DrawMark(pntMark, pntDirect):
    brash = GetVar(DESK_LINE_BRASH)
    markRadius = ScaleGeom(GetVar(DESK_MARK_RADIUS))
    markLength = ScaleGeom(GetVar(DESK_MARK_LENGTH))

    scene.drawCylinder(markRadius, markLength, brash)
    scene.doMove(DecartPnt(0, 0, -markLength / 2))
    scene.doDirect(pntMark, pntDirect)


def DrawWire(wire):
    brash = GetVar(DESK_LINE_BRASH)
    wireRadius = ScaleGeom(GetVar(DESK_LINE_RADIUS))
    scene.drawWire(wire, wireRadius, brash)


# *************************************************************
# Complex objects
# *************************************************************

def DrawArrow(pnt1, pnt2):
    arrowLength = ScaleGeom(GetVar(DESK_ARROW_LENGTH))

    v = gp_Vec(pnt1, pnt2)
    vLen = v.Magnitude()
    v *= -arrowLength / vLen
    pntM2 = pnt2.Translated(v)

    GroupBegin()
    DrawLine(pnt1, pntM2)
    DrawArrowEnd(pntM2, pnt2)
    GroupEnd()


def DrawArrow2(pnt1, pnt2):
    arrowLength = ScaleGeom(GetVar(DESK_ARROW_LENGTH))

    v = gp_Vec(pnt1, pnt2)
    vLen = v.Magnitude()
    v *= arrowLength / vLen
    pntM1 = pnt1.Translated(v)
    v *= -1
    pntM2 = pnt2.Translated(v)

    GroupBegin()
    DrawLine(pntM1, pntM2)
    DrawArrowEnd(pntM1, pnt1)
    DrawArrowEnd(pntM2, pnt2)
    GroupEnd()


def DrawCircle(pnt1, pnt2, pnt3):
    geomCircle = GC_MakeCircle(pnt1, pnt2, pnt3).Value()
    edge = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
    wire = BRepBuilderAPI_MakeWire(edge).Wire()

    DrawWire(wire)


def DrawBoard():
    backup = BackupVars()
    GroupBegin()

    borderSize = ScaleMain(GetVar(DESK_BOARD_BORDER_SIZE))
    deskHeight = ScaleMain(GetVar(DESK_BOARD_HEIGHT))

    textStr = 'A0 ' + GetVar(DESK_SCALE_TEXT)

    pinOffset = ScaleMain(GetVar(DESK_PIN_OFFSET))
    pinRadius = ScaleMain(GetVar(DESK_PIN_RADIUS))
    pinHeight = ScaleMain(GetVar(DESK_PIN_HEIGHT))

    decart = GetVar(DESK_PAPER_SIZES)
    x, y, z = decart.X(), decart.Y(), decart.Z()
    psx = ScaleMain(x)
    psy = ScaleMain(y)
    psz = ScaleMain(z)
    bsx = psx + borderSize * 2
    bsy = psy + borderSize * 2
    bsz = deskHeight

    SetSolidBrash(GetVar(DESK_BOARD_BRASH))
    DrawBox(bsx, bsy, bsz)
    DoMove(DecartPnt(-bsx / 2, -bsy / 2, -bsz - psz))

    SetSolidBrash(GetVar(DESK_PAPER_BRASH))
    DrawBox(psx, psy, psz)
    DoMove(DecartPnt(-psx / 2, -psy / 2, -psz))

    SetLabelBrash(GetVar(DESK_LABEL_BRASH))
    DrawLabel(DecartPnt(-bsx / 2, -bsy / 2, bsz * 3), textStr)

    dx = (psx / 2 - pinOffset)
    dy = (psy / 2 - pinOffset)

    pins = [
        (-dx, -dy),
        (dx, -dy),
        (dx, dy),
        (-dx, dy),
    ]

    SetSolidBrash(GetVar(DESK_PIN_BRASH))
    for x, y in pins:
        DrawCylinder(pinRadius, pinHeight)
        DoMove(DecartPnt(x, y, 0))

    GroupEnd()
    RestoreVars(backup)


def DrawAxis(pnt1, pnt2, step):
    DrawArrow(pnt1, pnt2)

    v = gp_Vec(pnt1, pnt2)
    totalLen = v.Magnitude()
    cnt = int(totalLen / step - 1)

    for i in range(cnt):
        targetLen = (1 + i) * step
        v = gp_Vec(pnt1, pnt2)
        v *= targetLen / totalLen
        pntMark = pnt1.Translated(v)
        DrawMark(pntMark, pnt2)


def DrawAxisSystem(pnt1, pnt2, step):
    xBrash = GetVar(DESK_AXES_X_BRASH)
    yBrash = GetVar(DESK_AXES_Y_BRASH)
    zBrash = GetVar(DESK_AXES_Z_BRASH)
    cBrash = GetVar(DESK_AXES_C_BRASH)
    labelBrash = GetVar(DESK_AXES_LABEL_BRASH)

    xPnt = DecartPnt(pnt2.X(), pnt1.Y(), pnt1.Z())
    yPnt = DecartPnt(pnt1.X(), pnt2.Y(), pnt1.Z())
    zPnt = DecartPnt(pnt1.X(), pnt1.Y(), pnt2.Z())

    SetLineBrash(xBrash)
    DrawAxis(pnt1, xPnt, step)

    SetLineBrash(yBrash)
    DrawAxis(pnt1, yPnt, step)

    SetLineBrash(zBrash)
    DrawAxis(pnt1, zPnt, step)

    SetPointBrash(cBrash)
    DrawPoint(pnt1)

    SetLabelBrash(labelBrash)
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
        DecartPnt(x1, y1, z1),
        DecartPnt(x1, y2, z1),
        DecartPnt(x2, y2, z1),
        DecartPnt(x2, y1, z1),

        DecartPnt(x1, y1, z2),
        DecartPnt(x1, y2, z2),
        DecartPnt(x2, y2, z2),
        DecartPnt(x2, y1, z2),
    ]

    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),
    ]

    DrawFrame(vertexes, edges, isLabeled)


def DrawLimits(pnt1, pnt2, isLabeled=False):
    SetStyle(DESK_INFO_STYLE)
    DrawBoxFrame(pnt1, pnt2, isLabeled)


def DrawDesk(down=0, isAxisSystem=False, isLimits=False, isLabeled=False):
    DrawBoard()
    DoMove(DecartPnt(0, 0, down))

    pnt = GetVar(DESK_LIMITS_SIZES)
    ax, ay, az = ScaleMain(pnt.X()), ScaleMain(pnt.Y()), ScaleMain(pnt.Z())

    if isLimits:
        DrawLimits(DecartPnt(-ax, -ay, 0), DecartPnt(ax, ay, az), isLabeled)

    if isAxisSystem:
        step = ScaleMain(GetVar(DESK_AXES_STEP))
        DrawAxisSystem(DecartPnt(0, 0, 0), DecartPnt(ax * 1.2, ay * 1.2, az * 1.2), step)


# ************************************
# ************************************
# ************************************

SetScale(1, 1)
SetStyle(DESK_DEFAULT_STYLE)
SetStyle(DESK_MAIN_STYLE)
