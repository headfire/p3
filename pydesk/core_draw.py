from core_consts import *
from core_styles import Styles
from core_position import Position, Direct

from OCC.Core.gp import gp_Pnt, gp_Vec
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCone,\
    BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeTorus


class Pnt(gp_Pnt):
    pass


class Draw:
    def getStyledScene(self, styles: Styles): pass


class LabelDraw(Draw):
    def __init__(self, pnt, text, hPx):
        self.pnt, self.text, self.hPx = pnt, text, hPx


class ShapeDraw(Draw):
    def __init__(self, shape):
        self.shape = shape


def _solidScene(shape, styles):
    return {'solidShape': (ShapeDraw(shape), Position(), styles.getStyle(SOLID_BRASH_STYLE))}

def _getScaled(styles, normalSize, factorStyleName):
    scale = styles.getScale()
    generalFactor = styles.getStyle(GENERAL_FACTOR_STYLE)
    localFactor = styles.getStyle(factorStyleName)
    return normalSize *

def _getArrowSizes(styles):

    scale = styles.getScale()
    generalFactor = styles.getStyle(GENERAL_FACTOR_STYLE)
    arrowRadiusFactor = styles.getStyle(ARROW_RADIUS_FACTOR_STYLE)
    arrowLengthFactor = styles.getStyle(ARROW_LENGTH_FACTOR_STYLE)
    arrowRadius = NORMAL_ARROW_RADIUS * scale * generalFactor * arrowRadiusFactor
    arrowLength = NORMAL_ARROW_LENGTH * scale * generalFactor * arrowLengthFactor
    return (arrowRadius, arrowLength)


class SphereDraw(Draw):
    def __init__(self, r):
        self.r = r

    def getStyledScene(self, styles: Styles):
        shape = BRepPrimAPI_MakeSphere(gp_Pnt(0, 0, 0), self.r).Shape()
        return _solidScene(shape, styles)


class BoxDraw(Draw):
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def getStyledScene(self, styles: Styles):
        shape = BRepPrimAPI_MakeBox(self.x, self.y, self.z).Shape()
        return _solidScene(shape, styles)


class ConeDraw(Draw):
    def __init__(self, r1, r2, h):
        self.r1, self.r2, self.h = r1, r2, h

    def getStyledScene(self, styles: Styles):
        shape = BRepPrimAPI_MakeCone(self.r1, self.r2, self.h).Shape()
        return _solidScene(shape, styles)


class CylinderDraw(Draw):
    def __init__(self, r, h):
        self.r, self.h = r, h

    def getStyledScene(self, styles: Styles):
        shape = BRepPrimAPI_MakeCylinder(self.r, self.h).Shape()
        return _solidScene(shape, styles)


class TorusDraw(Draw):
    def __init__(self, r1, r2):
        self.r1, self.r2 = r1, r2

    def getStyledScene(self, styles: Styles):
        shape = BRepPrimAPI_MakeTorus(self.r1, self.r2).Shape()
        return _solidScene(shape, styles)


class LineDraw(Draw):
    def __init__(self, pnt1, pnt2):
        self.pnt1, self.pnt2 = pnt1, pnt2

    def getStyledScene(self, styles: Styles):
        # size
        scale = styles.getScale()
        generalFactor = styles.getStyle(GENERAL_FACTOR_STYLE)
        lineRadiusFactor = styles.getStyle(LINE_RADIUS_FACTOR_STYLE)
        radius = NORMAL_LINE_RADIUS * generalFactor * lineRadiusFactor * scale
        position = Direct(self.pnt1, self.pnt2)
        length = gp_Vec(self.pnt1, self.pnt2).Magnitude()
        # brash
        brash = styles.getStyle(LINE_BRASH_STYLE)
        return {'cylinder': (CylinderDraw(radius, length), position, brash)}


class ArrowDraw(Draw):
    def __init__(self, pnt1, pnt2):
        self.pnt1, self.pnt2 = pnt1, pnt2

    def getStyledScene(self, styles: Styles):

        scale = styles.getScale()
        generalFactor = styles.getStyle(GENERAL_FACTOR_STYLE)
        arrowRadiusFactor = styles.getStyle(ARROW_RADIUS_FACTOR_STYLE)
        arrowLengthFactor = styles.getStyle(ARROW_LENGTH_FACTOR_STYLE)

        arrowRadius = NORMAL_ARROW_RADIUS * scale * generalFactor * arrowRadiusFactor
        arrowLength = NORMAL_ARROW_LENGTH * scale * generalFactor * arrowLengthFactor

        brash = styles.getStyle(LINE_BRASH_STYLE)

        return {'cone': (ConeDraw(arrowRadius, 0, arrowLength), Direct(self.pnt1, self.pnt2), brash)}


class VectorDraw(Draw):
    def __init__(self, pnt1, pnt2):
        self.pnt1, self.pnt2 = pnt1, pnt2

    def getStyledScene(self, styles: Styles):

        v = gp_Vec(self.pnt1, self.pnt2)
        vLen = v.Magnitude()
        v *= (vLen - arrowLength) / vLen
        pntM = pnt1.Translated(v)
        return {'line': (LineDraw(pnt1, pntM), None, None)
        return  'arrow': (ArrowDraw(pntM, pnt2), None, None)
        }

'''
'''