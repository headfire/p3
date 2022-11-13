from core_consts import *
from core_style import Style
from core_position import Position, Direct, Translate

from OCC.Core.gp import gp_Pnt, gp_Vec
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCone, \
    BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeTorus
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform


class Pnt(gp_Pnt):
    pass


NORMAL_POINT_RADIUS = 5
NORMAL_LINE_RADIUS = NORMAL_POINT_RADIUS * 0.5
NORMAL_SURFACE_HALF_WIDTH = NORMAL_POINT_RADIUS * 0.2
NORMAL_ARROW_RADIUS = NORMAL_POINT_RADIUS
NORMAL_ARROW_LENGTH = NORMAL_ARROW_RADIUS * 4
NORMAL_LABEL_HEIGHT_PX = 20

DEF_POINT_STYLE = Style(CHROME_MATERIAL, NICE_YELLOW_COLOR)
DEF_LINE_STYLE = Style(CHROME_MATERIAL, NICE_BLUE_COLOR)
DEF_SOLID_STYLE = Style(GOLD_MATERIAL)
DEF_SHAPE_STYLE = Style(PLASTIC_MATERIAL)
DEF_LABEL_STYLE = Style(SILVER_MATERIAL)
DEF_LABEL_DELTA = 20


class Draw:
    def __init__(self):
        self.position = Position()
        self.exportCommand = 'Draw()'

    def getStyledScene(self, styler, position): pass


class LabelFinalDraw(Draw):
    def __init__(self, pnt, text, style, delta, textHeightPx):
        super().__init__()
        self.pnt = pnt
        self.text = text
        self.style = style
        self.delta = delta
        self.delta = delta
        self.textHeightPx = textHeightPx


class ShapeFinalDraw(Draw):
    def __init__(self, shape, style):
        super().__init__()
        self.shape = shape
        self.style = style


class LabelDraw(Draw):
    def __init__(self, pnt, text):
        super().__init__()
        self.pnt = pnt
        self.text = text
        self.style = DEF_LABEL_STYLE
        self.delta = DEF_LABEL_DELTA

    def getStyledScene(self, styler, position):
        labelStyle = styler.getValue('LABEL_STYLE', self.style)
        delta = styler.getValue('LABEL_DELTA', self.delta)
        labelPosition = Position().next(Translate(delta, delta, delta)).next(position)
        labelPoint = labelPosition.movePnt(self.pnt)
        return {'finalDraw': LabelFinalDraw(labelPoint, self.text, labelStyle)}


class ShapeDraw(Draw):
    def __init__(self, shape):
        super().__init__()
        self.shape = shape
        self.style = DEF_LABEL_STYLE

    def getStyledScene(self, styler, position):
        finalStyle = styler.getValue('LABEL_STYLE', self.style)
        delta = styler.getValue('LABEL_DELTA', self.delta)
        finalShape = BRepBuilderAPI_Transform(self.shape, position.trsf).Shape()
        return {'finalDraw': ShapeFinalDraw(finalShape, finalStyle)}


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
