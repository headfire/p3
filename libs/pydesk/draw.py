from styles import Styles, SOLID_BRASH_STYLE
from position import Position

from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
# BRepPrimAPI_MakeBox, \
# BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeCone, BRepPrimAPI_MakeTorus


class Draw:
    def getStyledScene(self, styles: Styles): pass


class ShapeDraw(Draw):
    def __init__(self, shape):
        self.shape = shape


class LabelDraw(Draw):
    def __init__(self, pnt, text, hPx):
        self.pnt, self.text, self.hPx = pnt, text, hPx


class SphereDraw(Draw):
    def __init__(self, r):
        self.r = r

    def getStyledScene(self, styles: Styles):
        sphereShape = BRepPrimAPI_MakeSphere(gp_Pnt(0, 0, 0), self.r).Shape()
        return {
                 ('sphereShape', sphereShape, Position(), styles.getStyle(SOLID_BRASH_STYLE))
                }
