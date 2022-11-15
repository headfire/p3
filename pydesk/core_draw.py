# from core_brash import *
from core_position import Position, Direct, Translate

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCone, \
    BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeTorus
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
from OCC.Core.BRepTools import BRepTools_WireExplorer
from OCC.Core.BRep import BRep_Tool
from OCC.Core.GC import GC_MakeCircle


# *****************************************************************************

LABEL_HEIGHT_PX = 20  # not scaled
LABEL_DELTA = 15
POINT_RADIUS = 4
LINE_RADIUS = 2
LINE_ARROW_RADIUS = 4
LINE_ARROW_LENGTH = 10
FACE_WIDTH = 1

AO_SIZE_XYZ = 1189, 841, 1

M_1_1_SCALE = (1, 1)
M_5_1_SCALE = (5, 1)

DESK_HEIGHT = 20
DESK_BORDER_SIZE = 60
DESK_PAPER_SIZE = 1189, 841, 1
DESK_PIN_OFFSET = 30
DESK_PIN_RADIUS = 10
DESK_PIN_HEIGHT = 2
DESK_DEFAULT_DRAW_AREA_SIZE = 400

# *****************************************************

MATERIAL_STYLE = 'MATERIAL_STYLE'
COLOR_STYLE = 'COLOR_STYLE'
TRANSPARENCY_STYLE = 'TRANSPARENCY_STYLE'
SCALE_STYLE = 'SCALE_STYLE'
SCALE_A_STYLE = 'SCALE_A_STYLE'
SCALE_B_STYLE = 'SCALE_B_STYLE'
SCALE_C_STYLE = 'SCALE_C_STYLE'
SCALE_PX_STYLE = 'SCALE_PX_STYLE'


class Style:
    def __init__(self, material=None, color=None, transparency=None):
        self.values = {}
        self.set(MATERIAL_STYLE, material)
        self.set(COLOR_STYLE, color)
        self.set(TRANSPARENCY_STYLE, transparency)

    def get(self, styleName, defValue=None):
        value = self.values.get(styleName)
        if value is not None:
            return value
        return defValue

    def set(self, styleName, styleValue):
        if styleValue is not None:
            self.values[styleName] = styleValue

    def merge(self, styleName, mergedStyleValue):
        if self.get(styleName) is None:
            self.set(styleName, mergedStyleValue)

    def mergeAll(self, mergedStyle):
        for styleName, styleValue in mergedStyle.values.items():
            self.merge(styleName, styleValue)
        return self

    def getMaterial(self):
        return self.get(MATERIAL_STYLE)

    def getTransparency(self):
        return self.get(TRANSPARENCY_STYLE)

    def getColor(self):
        return self.get(COLOR_STYLE)

    def getScaled(self, value):
        s = self.get(SCALE_STYLE, 1)
        return value * s

    def getScaledA(self, value):
        s = self.get(SCALE_STYLE, 1)
        a = self.get(SCALE_A_STYLE, 1)
        return value * s * a

    def getScaledAB(self, value):
        s = self.get(SCALE_STYLE, 1)
        a = self.get(SCALE_A_STYLE, 1)
        b = self.get(SCALE_B_STYLE, 1)
        return value * s * a * b

    def getScaledAC(self, value):
        s = self.get(SCALE_STYLE, 1)
        a = self.get(SCALE_A_STYLE, 1)
        c = self.get(SCALE_B_STYLE, 1)
        return value * s * a * c

    def getScaledPx(self, value):
        spx = self.get(SCALE_PX_STYLE, 1)
        return value * spx


class Pnt(gp_Pnt):
    pass


# ********************************************************************************

class Draw:
    def __init__(self, cls: str):

        self.nm = 'drawObj'
        self.cls = cls.split('-')

        self.position = Position()
        self.style = Style()

        self.items = []
        self.code = []

    def getClsSuffix(self):
        if len(self.cls) == 0:
            return ''
        return ':' + '-'.join(self.cls)

    def addItem(self, draw, position=Position(), nm='obj'):
        splitList = nm.split(':')
        itemName = splitList[0]
        if len(splitList) > 1:
            clsToAdd = splitList[1].split('-')
            self.cls.extend(clsToAdd)
        self.items[itemName] = draw, position

    def addCodeLine(self, line):
        self.code.append(line)

    def addStyledItems(self, style: Style): pass
    def addStyledCode(self, style: Style): pass


class FinalTextDraw(Draw):
    def __init__(self, pnt, text, textHeightPx):
        super().__init__('final')
        self.pnt = pnt
        self.text = text
        self.textHeightPx = textHeightPx


class FinalShapeDraw(Draw):
    def __init__(self, shape):
        super().__init__('final')
        self.shape = shape


# ************************************


class LabelDraw(Draw):
    def __init__(self, pnt, text):
        super().__init__('label')
        self.pnt = pnt
        self.text = text

    def addStyledItems(self, style: Style):
        delta = style.getScaled(LABEL_DELTA)
        heightPx = style.getScaledPx(LABEL_HEIGHT_PX)
        finalPosition = Translate(delta, delta, delta)
        finalDraw = FinalTextDraw(self.pnt, self.text, heightPx)
        self.addItem(finalDraw, finalPosition)


class SurfaceDraw(Draw):
    def __init__(self, shape):
        super().__init__('surface')
        self.shape = shape

    def addStyledItems(self, style: Style):
        draw = FinalShapeDraw(self.shape)
        self.addItem(draw)


# *************************************


class SphereDraw(Draw):
    def __init__(self, pnt, r):
        super().__init__('sphere-solid')
        self.pnt = pnt
        self.r = r

    def addStyledItems(self, style: Style):
        shape = BRepPrimAPI_MakeSphere(self.pnt, self.r).Shape()
        draw = FinalShapeDraw(shape)
        self.addItem(draw)


class BoxDraw(Draw):
    def __init__(self, pnt, x, y, z):
        super().__init__('box-solid')
        self.pnt = pnt
        self.x = x
        self.y = y
        self.z = z

    def addStyledItems(self, style: Style):
        shape = BRepPrimAPI_MakeBox(self.pnt, self.x, self.y, self.z).Shape()
        draw = FinalShapeDraw(shape)
        self.addItem(draw)


class ConeDraw(Draw):
    def __init__(self, r1, r2, h):
        super().__init__('cone-solid')
        self.r1 = r1
        self.r2 = r2
        self.h = h

    def addStyledItems(self, style: Style):
        shape = BRepPrimAPI_MakeCone(self.r1, self.r2, self.h).Shape()
        draw = FinalShapeDraw(shape)
        self.addItem(draw)


class CylinderDraw(Draw):
    def __init__(self, r, h):
        super().__init__('cylinder-solid')
        self.r = r
        self.h = h

    def addStyledItems(self, style: Style):
        shape = BRepPrimAPI_MakeCylinder(self.r, self.h).Shape()
        draw = FinalShapeDraw(shape)
        self.addItem(draw)


class TorusDraw(Draw):
    def __init__(self, r1, r2):
        super().__init__('torus-solid')
        self.r1 = r1
        self.r2 = r2

    def addStyledItems(self, style: Style):
        shape = BRepPrimAPI_MakeTorus(self.r1, self.r2).Shape()
        draw = FinalShapeDraw(shape)
        self.addItem(draw)


# ********************************************************************


class PointDraw(Draw):
    def __init__(self, pnt):
        super().__init__('point')
        self.pnt = pnt

    def addStyledItems(self, style: Style):
        r = style.getScaled(POINT_RADIUS)
        draw = SphereDraw(self.pnt, r)
        self.addItem(draw)


class LineDraw(Draw):
    def __init__(self, pnt1, pnt2):
        super().__init__('direct-line')
        self.pnt1 = pnt1
        self.pnt2 = pnt2

    def addStyledItems(self, style: Style):
        r = style.getScaled(LINE_RADIUS)
        length = gp_Vec(self.pnt1, self.pnt2).Magnitude()
        draw = CylinderDraw(r, length)
        position = Direct(self.pnt1, self.pnt2)
        self.addItem(draw, position)


class ArrowDraw(Draw):
    def __init__(self, pnt1, pnt2):
        super().__init__('arrow-line')
        self.pnt1 = pnt1
        self.pnt2 = pnt2

    def addStyledItems(self, style: Style):
        r = style.getScaledA(LINE_ARROW_RADIUS)
        length = style.getScaledAB(LINE_ARROW_LENGTH)
        draw = ConeDraw(r, 0, length)
        position = Direct(self.pnt1, self.pnt2)
        self.addItem(draw, position)


class VectorDraw(Draw):
    def __init__(self, pnt1, pnt2):
        super().__init__('vector-line')
        self.pnt1 = pnt1
        self.pnt2 = pnt2

    def addStyledItems(self, style: Style):
        arrowLength = style.getScaledAB(LINE_ARROW_LENGTH)
        v = gp_Vec(self.pnt1, self.pnt2)
        vLen = v.Magnitude()
        v *= (vLen - arrowLength) / vLen
        pntM = self.pnt1.Translated(v)
        self.addItem(LineDraw(self.pnt1, pntM), nm='line')
        self.addItem(ArrowDraw(pntM, self.pnt2), nm='arrow')


# ********************************************************************


def _getVectorTangentToCurveAtPoint(edge, uRatio):
    aCurve, aFP, aLP = BRep_Tool.Curve(edge)
    aP = aFP + (aLP - aFP) * uRatio
    v1 = gp_Vec()
    p1 = gp_Pnt()
    aCurve.D1(aP, p1, v1)

    return v1


def _getWireStartPointAndTangentDir(wire):
    print(wire)
    ex = BRepTools_WireExplorer(wire)
    edge = ex.Current()
    vertex = ex.CurrentVertex()
    v = _getVectorTangentToCurveAtPoint(edge, 0)

    return BRep_Tool.Pnt(vertex), gp_Dir(v)


class WireDraw(Draw):
    def __init__(self, wire, r=None):
        super().__init__('wire-line')
        self.wire = wire
        self.r = r

    def addStyledItems(self, styler):
        if self.r is not None:
            aWireRadius = self.r
        else:
            aWireRadius = styler.getValue(LINE_RADIUS)
        startPoint, tangentDir = _getWireStartPointAndTangentDir(self.wire)
        profileCircle = GC_MakeCircle(startPoint, tangentDir, aWireRadius).Value()
        profileEdge = BRepBuilderAPI_MakeEdge(profileCircle).Edge()
        profileWire = BRepBuilderAPI_MakeWire(profileEdge).Wire()
        shape = BRepOffsetAPI_MakePipe(self.wire, profileWire).Shape()
        draw = FinalShapeDraw(shape)
        self.addItem(draw)


class Circle3Draw(Draw):
    def __init__(self, pnt1, pnt2, pnt3):
        super().__init__('circle-line')
        self.pnt1 = pnt1
        self.pnt2 = pnt2
        self.pnt3 = pnt3

    def addStyledItems(self, style:  Style):
        aWireRadius = style.getScaled(LINE_RADIUS)
        geomCircle = GC_MakeCircle(self.pnt1, self.pnt2, self.pnt3).Value()
        edge = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
        wire = BRepBuilderAPI_MakeWire(edge).Wire()
        draw = WireDraw(wire, aWireRadius)
        self.addItem(draw)


# ****************************************************************************


class DrawLib:

    def __init__(self):
        self.cache = {}

    def getCached(self, methodName, param1=None, param2=None):

        params = ''
        if param1 is not None:
            params += str(param1)
        if param2 is not None:
            params += ',' + str(param2)

        cacheKey = methodName + '(' + params + ')'

        method = self.__getattribute__(methodName)
        if cacheKey in self.cache:
            print('==> Get from cache', cacheKey)
            obj = self.cache[cacheKey]
        else:
            print('==> Compute', cacheKey)
            if param1 is None:
                obj = method()
            elif param2 is None:
                obj = method(param1)
            else:
                obj = method(param1, param2)
            self.cache[cacheKey] = obj
        return obj
