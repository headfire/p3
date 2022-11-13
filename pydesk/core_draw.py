from core_consts import *
from core_style import Style
from core_position import Position, Direct  # , Translate

from OCC.Core.gp import gp_Pnt, gp_Vec
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCone, \
    BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeTorus


class Pnt(gp_Pnt):
    pass


NORMAL_POINT_RADIUS = 5
NORMAL_LINE_RADIUS = NORMAL_POINT_RADIUS * 0.5
NORMAL_SURFACE_HALF_WIDTH = NORMAL_POINT_RADIUS * 0.2
NORMAL_ARROW_RADIUS = NORMAL_POINT_RADIUS
NORMAL_ARROW_LENGTH = NORMAL_ARROW_RADIUS * 3
NORMAL_LABEL_HEIGHT_PX = 20

DEF_POINT_STYLE = Style(CHROME_MATERIAL, NICE_YELLOW_COLOR)
DEF_LINE_STYLE = Style(CHROME_MATERIAL, NICE_BLUE_COLOR)
DEF_SOLID_STYLE = Style(GOLD_MATERIAL)
DEF_SHAPE_STYLE = Style(PLASTIC_MATERIAL)
DEF_LABEL_STYLE = Style(SILVER_MATERIAL)
LABEL_DELTA = 20


class Draw:
    def __init__(self, style):
        self.style = style
        self.position = Position()
        self.items = {}
        self.exportCommand = 'Draw()'


class LabelDraw(Draw):
    def __init__(self, pnt, text):
        super().__init__(DEF_LABEL_STYLE)
        self.pnt, self.text = pnt, text
        self.delta = LABEL_DELTA


class ShapeDraw(Draw):
    def __init__(self, shape):
        super().__init__(DEF_SHAPE_STYLE)
        self.shape = shape
        self.style = DEF_SHAPE_STYLE


class SolidDraw(ShapeDraw):
    def __init__(self, shape):
        super().__init__(shape)
        self.style = DEF_SOLID_STYLE


class SphereDraw(SolidDraw):
    def __init__(self, centerPnt, radius):
        shape = BRepPrimAPI_MakeSphere(centerPnt, radius).Shape()
        super().__init__(shape)


class BoxDraw(SolidDraw):
    def __init__(self, centerPnt, xSize, ySize, zSize):
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
        radius = NORMAL_POINT_RADIUS * self.style.sizeFactor
        sphereDraw = SphereDraw(pnt, radius)
        self.items = {'Sphere': sphereDraw}


class LineDraw(Draw):
    def __init__(self, pnt1, pnt2):
        super().__init__(DEF_LINE_STYLE)
        radius = NORMAL_LINE_RADIUS * self.style.sizeFactor
        length = gp_Vec(pnt1, pnt2).Magnitude()
        cylDraw = CylinderDraw(radius, length)
        cylDraw.position = Direct(pnt1, pnt2)
        self.items = {'Cylinder': cylDraw}


'''
class ArrowDraw(Draw):
    def __init__(self, pnt1, pnt2):
        self.pnt1, self.pnt2 = pnt1, pnt2

    def getStyledScene(self, styles: Styles):
        arrowRadius = styles.getScaledSize(NORMAL_ARROW_RADIUS, ARROW_RADIUS_FACTOR_STYLE)
        arrowLength = styles.getScaledSize(NORMAL_ARROW_LENGTH, ARROW_LENGTH_FACTOR_STYLE)
        brash = styles.getBrash(LINE_BRASH_STYLE)
        return {'cone': (ConeDraw(arrowRadius, 0, arrowLength), Direct(self.pnt1, self.pnt2), brash)}


class VectorDraw(Draw):
    def __init__(self, pnt1, pnt2):
        self.pnt1, self.pnt2 = pnt1, pnt2

    def getStyledScene(self, styles: Styles):
        arrowLength = styles.getScaledSize(NORMAL_ARROW_LENGTH, ARROW_LENGTH_FACTOR_STYLE)
        v = gp_Vec(self.pnt1, self.pnt2)
        vLen = v.Magnitude()
        v *= (vLen - arrowLength) / vLen
        pntM = self.pnt1.Translated(v)
        return { 'line': (LineDraw(self.pnt1, pntM), Position()),
                 'arrow': (ArrowDraw(pntM, self.pnt2), Position())
                }
'''
