from core_consts import *
from core_style import Brash
from core_position import Position, Direct, Translate

from OCC.Core.gp import gp_Pnt, gp_Vec
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCone, \
    BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeTorus
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform


class Pnt(gp_Pnt):
    pass


class Styler:
    def __init__(self):
        self.renderName = 'root'

    def setRenderName(self, renderName):
        self.renderName = renderName

    def getValue(self, styleName, normalValue):
        # todo
        if styleName is not None and self.renderName is not None:
            return normalValue


NORMAL_POINT_RADIUS = 5
NORMAL_LINE_RADIUS = NORMAL_POINT_RADIUS * 0.5
NORMAL_SURFACE_HALF_WIDTH = NORMAL_POINT_RADIUS * 0.2
NORMAL_ARROW_RADIUS = NORMAL_POINT_RADIUS
NORMAL_ARROW_LENGTH = NORMAL_ARROW_RADIUS * 4
NORMAL_LABEL_HEIGHT_PX = 20

DEF_POINT_BRASH = Brash(CHROME_MATERIAL, NICE_YELLOW_COLOR)
DEF_LINE_BRASH = Brash(CHROME_MATERIAL, NICE_BLUE_COLOR)
DEF_SOLID_BRASH = Brash(GOLD_MATERIAL)
DEF_SHAPE_BRASH = Brash(PLASTIC_MATERIAL)
DEF_LABEL_BRASH = Brash(SILVER_MATERIAL)
DEF_LABEL_DELTA = 20


class Draw:
    def __init__(self):
        self.position = Position()
        self.brash = Brash()
        self.items = {}
        self.code = []

    def makeStyledItems(self, styler): pass
    def makeCode(self, styler): pass

    def add(self, nm, draw, position, brash):
        self.items[nm] = draw, position, brash

    def makeCode(self, line):
        self.code.append(line)


class FinalLabelDraw(Draw):
    def __init__(self, pnt, text, textHeightPx):
        super().__init__()
        self.pnt = pnt
        self.text = text
        self.textHeightPx = textHeightPx


class FinalShapeDraw(Draw):
    def __init__(self, shape):
        super().__init__()
        self.shape = shape


class LabelDraw(Draw):
    def __init__(self, pnt, text):
        super().__init__()
        self.pnt = pnt
        self.text = text

    def makeStyledScene(self, styler):
        delta = styler.getValue('LABEL_DELTA', DEF_LABEL_DELTA)
        finalBrash = styler.getValue('LABEL_BRASH', DEF_LABEL_BRASH)
        finalPosition = Translate(delta, delta, delta)
        finalDraw = FinalLabelDraw(self.pnt, self.text)
        self.add('finalDraw', finalDraw, finalPosition, finalBrash)


class ShapeDraw(Draw):
    def __init__(self, shape):
        super().__init__()
        self.shape = shape

    def makeStyledScene(self, styler):
        brash = styler.getValue('SHAPE_BRASH', DEF_SHAPE_BRASH)
        position = Position()
        draw = FinalShapeDraw(self.shape)
        self.add('draw', draw, position, brash)


class SphereDraw(SolidDraw):
    def __init__(self, pnt, r):
        super().__init__(shape)
        self.pnt = pnt
        self.r = r

    def makeStyledScene(self, styler):
        brash = styler.getValue('SOLID_BRASH', DEF_SOLID_BRASH)
        shape = BRepPrimAPI_MakeSphere(self.pnt, self.r).Shape()
        draw = FinalShapeDraw(shape)
        self.add('draw', draw, Position(), brash)

'''
class BoxDraw(SolidDraw):
    def __init__(self, pnt, xSize, ySize, zSize):
        shape = BRepPrimAPI_MakeBox(centerPnt, xSize, ySize, zSize).Shape()
        super().__init__(shape)


class ConeDraw(SolidDraw):
    def __init__(self, r1, r2, h):
        shape = BRepPrimAPI_MakeCone(r1, r2, h).Shape()
        super().__init__(shape)


class CylinderDraw(SolidDraw):
    def __init__(self, r, h):
        shape = BRepPrimAPI_MakeCylinder(r, h).Shape()
        super().__init__(shape)


class TorusDraw(SolidDraw):
    def __init__(self, r1, r2):
        shape = BRepPrimAPI_MakeTorus(r1, r2).Shape()
        super().__init__(shape)


class PointDraw(Draw):
    def __init__(self, pnt):
        super().__init__(DEF_POINT_STYLE)
        radius = self.style.getSize(NORMAL_POINT_RADIUS)
        sphere = SphereDraw(pnt, radius)
        self.items['Sphere'] = sphere


class LineDraw(Draw):
    def __init__(self, pnt1, pnt2):
        super().__init__(DEF_LINE_STYLE)
        radius = self.style.getSize(NORMAL_LINE_RADIUS)
        length = gp_Vec(pnt1, pnt2).Magnitude()
        cyl = CylinderDraw(radius, length)
        cyl.position = Direct(pnt1, pnt2)
        self.items['Cylinder'] = cyl


class ArrowDraw(Draw):
    def __init__(self, pnt1, pnt2):
        super().__init__(DEF_LINE_STYLE)
        arrowRadius = self.style.getSize(NORMAL_ARROW_RADIUS)
        arrowLength = self.style.getSubSize(NORMAL_ARROW_LENGTH)
        cone = ConeDraw(arrowRadius, 0, arrowLength)
        cone.position = Direct(pnt1, pnt2)
        self.items['Cone'] = cone


class VectorDraw(Draw):
    def __init__(self, pnt1, pnt2):
        super().__init__(DEF_LINE_STYLE)
        arrowLength = self.style.getSubSize(NORMAL_ARROW_LENGTH)
        v = gp_Vec(pnt1, pnt2)
        vLen = v.Magnitude()
        v *= (vLen - arrowLength) / vLen
        pntM = pnt1.Translated(v)
        self.items['Line'] = LineDraw(pnt1, pntM)
        self.items['Arrow'] = ArrowDraw(pntM, pnt2)
'''