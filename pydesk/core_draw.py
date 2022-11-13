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

    # def getOverride(self, styleName): pass  # todo

    def getValue(self, styleName: str):
        finalStyleValue = None  # self.findOverride(styleName)  # todo
        if finalStyleValue is None:
            finalStyleValue = DEF_STYLES[styleName]
        if styleName.endswith('_A_SCALED'):
            a = self.getValue('SCALE_A')
            finalStyleValue *= a
        elif styleName.endswith('_B_SCALED'):
            a = self.getValue('SCALE_A')
            b = self.getValue('SCALE_B')
            finalStyleValue *= a * b
        elif styleName.endswith('_C_SCALED'):
            a = self.getValue('SCALE_A')
            b = self.getValue('SCALE_B')
            c = self.getValue('SCALE_C')
            finalStyleValue *= a * b * c
        return finalStyleValue


SCALE_A = 'SCALE_A'
SCALE_B = 'SCALE_B'
SCALE_C = 'SCALE_C'

LABEL_BRASH = 'LABEL_BRASH'
LABEL_DELTA = 'LABEL_DELTA_A_SCALED'
LABEL_HEIGHT_PX = 'LABEL_HEIGHT_PX'

POINT_BRASH = 'POINT_BRASH_B_SCALED'
POINT_RADIUS = 'POINT_RADIUS'

LINE_BRASH = 'LINE_BRASH'
LINE_RADIUS = 'LINE_RADIUS_B_SCALED'
LINE_ARROW_RADIUS = 'ARROW_RADIUS_B_SCALED'
LINE_ARROW_LENGTH = 'ARROW_LENGTH_C_SCALED'

FACE_BRASH = 'FACE_BRASH'
FACE_WIDTH = 'FACE_WIDTH_B_SCALED'

SOLID_BRASH = 'SOLID_BRASH'

SURFACE_BRASH = 'SURFACE_BRASH'


DEF_STYLES = {

    SCALE_A: 1,
    SCALE_B: 1,
    SCALE_C: 1,

    LABEL_BRASH: Brash(SILVER_MATERIAL),
    LABEL_DELTA: 20,
    LABEL_HEIGHT_PX: 20,

    POINT_BRASH: Brash(CHROME_MATERIAL, NICE_YELLOW_COLOR),
    POINT_RADIUS: 5,

    LINE_BRASH: Brash(CHROME_MATERIAL, NICE_BLUE_COLOR),
    LINE_RADIUS: 2.5,
    LINE_ARROW_RADIUS: 5,
    LINE_ARROW_LENGTH: 20,

    FACE_BRASH: Brash(CHROME_MATERIAL, NICE_BLUE_COLOR),
    FACE_WIDTH: 1,

    SOLID_BRASH: Brash(GOLD_MATERIAL),

    SURFACE_BRASH: Brash(PLASTIC_MATERIAL, NICE_GRAY_COLOR)
}


class Draw:
    def __init__(self):
        self.position = Position()
        self.brash = Brash()
        self.items = {}
        self.code = []

    def addItem(self, nm, draw, position, brash):
        self.items[nm] = draw, position, brash

    def addCodeLine(self, line):
        self.code.append(line)

    def addStyledItems(self, styler): pass
    def addStyledCodeLines(self, styler): pass


class FinalTextDraw(Draw):
    def __init__(self, pnt, text, textHeightPx):
        super().__init__()
        self.pnt = pnt
        self.text = text
        self.textHeightPx = textHeightPx


class FinalShapeDraw(Draw):
    def __init__(self, shape):
        super().__init__()
        self.shape = shape


# ************************************


class LabelDraw(Draw):
    def __init__(self, pnt, text):
        super().__init__()
        self.pnt = pnt
        self.text = text

    def addStyledItems(self, styler):
        delta = styler.getValue(LABEL_DELTA)
        heightPx = styler.getValue(LABEL_HEIGHT_PX)
        finalBrash = styler.getValue(LABEL_BRASH)
        finalPosition = Translate(delta, delta, delta)
        finalDraw = FinalTextDraw(self.pnt, self.text, heightPx)
        self.addItem('draw', finalDraw, finalPosition, finalBrash)


class SurfaceDraw(Draw):
    def __init__(self, shape):
        super().__init__()
        self.shape = shape

    def addStyledItems(self, styler):
        brash = styler.getValue(SURFACE_BRASH)
        draw = FinalShapeDraw(self.shape)
        self.addItem('draw', draw, Position(), brash)


# *************************************


class SphereDraw(Draw):
    def __init__(self, pnt, r):
        super().__init__()
        self.pnt = pnt
        self.r = r

    def addStyledItems(self, styler):
        brash = styler.getValue(SOLID_BRASH)
        shape = BRepPrimAPI_MakeSphere(self.pnt, self.r).Shape()
        draw = FinalShapeDraw(shape)
        self.addItem('draw', draw, Position(), brash)


class BoxDraw(Draw):
    def __init__(self, pnt, x, y, z):
        super().__init__()
        self.pnt = pnt
        self.x = x
        self.y = y
        self.z = z

    def addStyledItems(self, styler):
        brash = styler.getValue(SOLID_BRASH)
        shape = BRepPrimAPI_MakeBox(self.pnt, self.x, self.y, self.z).Shape()
        draw = FinalShapeDraw(shape)
        self.addItem('draw', draw, Position(), brash)


'''
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
