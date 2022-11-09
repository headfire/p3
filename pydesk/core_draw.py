from core_consts import *
from core_styles import Styles
from core_position import Position

from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox
# todo BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeCone, BRepPrimAPI_MakeTorus


class Draw:
    def getStyledScene(self, styles: Styles): pass


class LabelDraw(Draw):
    def __init__(self, pnt, text, hPx):
        self.pnt, self.text, self.hPx = pnt, text, hPx


class ShapeDraw(Draw):
    def __init__(self, shape):
        self.shape = shape


def _solidScene(nm, shape, styles):
    return { nm: (ShapeDraw(shape), Position(), styles.getStyle(SOLID_BRASH_STYLE)) }


class SphereDraw(Draw):
    def __init__(self, r):
        self.r = r

    def getStyledScene(self, styles: Styles):
        shape = BRepPrimAPI_MakeSphere(gp_Pnt(0, 0, 0), self.r).Shape()
        return _solidScene('sphereShape', shape, styles)


class BoxDraw(Draw):
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def getStyledScene(self, styles: Styles):
        shape = BRepPrimAPI_MakeBox(self.x, self.y, self.z).Shape()
        return _solidScene('boxShape', shape, styles)
