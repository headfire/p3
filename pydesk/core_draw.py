from core_consts import *
from core_styles import Styles
from core_position import Position

from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCone, BRepPrimAPI_MakeCylinder
# todo BRepPrimAPI_MakeTorus


class Draw:
    def getStyledScene(self, styles: Styles): pass


class LabelDraw(Draw):
    def __init__(self, pnt, text, hPx):
        self.pnt, self.text, self.hPx = pnt, text, hPx


class ShapeDraw(Draw):
    def __init__(self, shape):
        self.shape = shape


def _solidScene(shape, styles):
    return { 'solidShape': (ShapeDraw(shape), Position(), styles.getStyle(SOLID_BRASH_STYLE)) }


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


'''

class CylinderSolid(Solid):

    def getShape(self):
        return BRepPrimAPI_MakeCylinder(self.r, self.h).Shape()

class TorusSolid(Solid):
    def __init__(self, r1, r2):
        self.r1, self.r2 = r1, r2

    def getShape(self):
        return BRepPrimAPI_MakeTorus(self.r1, self.r2).Shape()
'''