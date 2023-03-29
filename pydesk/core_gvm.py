from core_position import *
from core_style import *

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCone, \
    BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeTorus
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
from OCC.Core.BRepTools import BRepTools_WireExplorer
from OCC.Core.BRep import BRep_Tool
from OCC.Core.GC import GC_MakeCircle

from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire,
                                     BRepBuilderAPI_MakeFace)

class Gvm:
    def drawShape(self, nm): {
        self.getParam('shape')
    }


class Pnt(gp_Pnt):
    pass


class Draw:
    def __init__(self, nameWithCls: str = 'drawObj'):

        self.nm = None
        self.cls = []

        splitList = nameWithCls.split(':')
        self.nm = splitList[0]
        if len(splitList) > 1:
            self.addCls(splitList[1])

        self.position = Position()
        self.style = Style()

        self.items = []
        self.code = []

    def setName(self, nm):
        self.nm = nm

    def addCls(self, clsToAdd):
        self.cls.extend(clsToAdd.split('-'))

    def getNameWithCls(self):
        if len(self.cls) == 0:
            return self.nm
        return self.nm+':' + '-'.join(self.cls)

    def doNm(self, nm):
        self.nm = nm
        return self

    def doCls(self, nm):
        self.addCls(nm)
        return self

    def doPs(self, position: Position):
        self.position.do(position)
        return self

    def doSt(self, styleName, styleValue):
        self.style.set(styleName, styleValue)
        return self

    def doStl(self, style):
        self.style = style
        return self

    def addItem(self, draw):
        self.items.append(draw)

    def addCodeLine(self, line):
        self.code.append(line)

    def addStyledItems(self, style: Style): pass
    def addStyledCode(self, style: Style): pass


class FinalTextDraw(Draw):
    def __init__(self, pnt, text, textHeightPx):
        super().__init__('finalText:text')
        self.pnt = pnt
        self.text = text
        self.textHeightPx = textHeightPx


class FinalShapeDraw(Draw):
    def __init__(self, shape):
        super().__init__('finalShape:shape')
        self.shape = shape


# ************************************


class LabelDraw(Draw):
    def __init__(self, pnt, text):
        super().__init__('label')
        self.pnt = pnt
        self.text = text

    def addStyledItems(self, style: Style):
        delta = LABEL_DELTA * style.get(SCALE, 1)
        heightPx = LABEL_HEIGHT_PX * style.get(SCALE_PX, 1)
        draw = FinalTextDraw(self.pnt, self.text, heightPx)
        draw.position = Translate(delta, delta, delta)
        self.addItem(draw)


class SurfaceDraw(Draw):
    def __init__(self, shape):
        super().__init__('surfaceObj:surface')
        self.shape = shape

    def addStyledItems(self, style: Style):
        draw = FinalShapeDraw(self.shape)
        self.addItem(draw)


# *************************************


class SphereDraw(Draw):
    def __init__(self, pnt, r):
        super().__init__('sphereObj:sphere-solid')
        self.pnt = pnt
        self.r = r

    def addStyledItems(self, style: Style):
        shape = BRepPrimAPI_MakeSphere(self.pnt, self.r).Shape()
        draw = FinalShapeDraw(shape)
        self.addItem(draw)


class BoxDraw(Draw):
    def __init__(self, pnt, x, y, z):
        super().__init__('boxObj:box-solid')
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
        super().__init__('coneObj:cone-solid')
        self.r1 = r1
        self.r2 = r2
        self.h = h

    def addStyledItems(self, style: Style):
        shape = BRepPrimAPI_MakeCone(self.r1, self.r2, self.h).Shape()
        draw = FinalShapeDraw(shape)
        self.addItem(draw)


class CylinderDraw(Draw):
    def __init__(self, r, h):
        super().__init__('cylinderObj:cylinder-solid')
        self.r = r
        self.h = h

    def addStyledItems(self, style: Style):
        shape = BRepPrimAPI_MakeCylinder(self.r, self.h).Shape()
        draw = FinalShapeDraw(shape)
        self.addItem(draw)


class TorusDraw(Draw):
    def __init__(self, r1, r2):
        super().__init__('torusObj:torus-solid')
        self.r1 = r1
        self.r2 = r2

    def addStyledItems(self, style: Style):
        shape = BRepPrimAPI_MakeTorus(self.r1, self.r2).Shape()
        draw = FinalShapeDraw(shape)
        self.addItem(draw)


# ********************************************************************


class PointDraw(Draw):
    def __init__(self, pnt):
        super().__init__('pointObj:point')
        self.pnt = pnt

    def addStyledItems(self, style: Style):
        r = POINT_RADIUS * style.get(SCALE, 1) * style.get(SCALE_GEOM, 1)
        draw = SphereDraw(self.pnt, r)
        self.addItem(draw)


class LineDraw(Draw):
    def __init__(self, pnt1, pnt2):
        super().__init__('directObj:direct-line')
        self.pnt1 = pnt1
        self.pnt2 = pnt2

    def addStyledItems(self, style: Style):
        r = LINE_RADIUS * style.get(SCALE, 1) * style.get(SCALE_GEOM, 1)
        length = gp_Vec(self.pnt1, self.pnt2).Magnitude()
        draw = CylinderDraw(r, length)
        draw.position = Direct(self.pnt1, self.pnt2)
        self.addItem(draw)


class VectorDraw(Draw):
    def __init__(self, pnt1, pnt2):
        super().__init__('vectorObj:vector-line')
        self.pnt1 = pnt1
        self.pnt2 = pnt2

    def addStyledItems(self, style: Style):

        arrowR = LINE_ARROW_RADIUS * style.get(SCALE, 1) * style.get(SCALE_GEOM, 1)
        arrowL = LINE_ARROW_LENGTH * style.get(SCALE, 1) * style.get(SCALE_GEOM, 1) \
            * style.get(SCALE_ARROW, 1)

        v = gp_Vec(self.pnt1, self.pnt2)
        vLen = v.Magnitude()
        v *= (vLen - arrowL) / vLen
        pntM = self.pnt1.Translated(v)

        self.addItem(LineDraw(self.pnt1, pntM))
        self.addItem(ConeDraw(arrowR, 0, arrowL).doPs(Direct(pntM, self.pnt2)))


# ********************************************************************


def _getVectorTangentToCurveAtPoint(edge, uRatio):
    aCurve, aFP, aLP = BRep_Tool.Curve(edge)
    aP = aFP + (aLP - aFP) * uRatio
    v1 = gp_Vec()
    p1 = gp_Pnt()
    aCurve.D1(aP, p1, v1)

    return v1


def _getWireStartPointAndTangentDir(wire):
    ex = BRepTools_WireExplorer(wire)
    edge = ex.Current()
    vertex = ex.CurrentVertex()
    v = _getVectorTangentToCurveAtPoint(edge, 0)

    return BRep_Tool.Pnt(vertex), gp_Dir(v)


class WireDraw(Draw):
    def __init__(self, wire, r=None):
        super().__init__('wireObj:wire-line')
        self.wire = wire
        self.r = r

    def addStyledItems(self, style: Style()):
        if self.r is not None:
            aWireRadius = self.r
        else:
            aWireRadius = LINE_RADIUS * style.get(SCALE, 1) * style.get(SCALE_GEOM, 1)
        startPoint, tangentDir = _getWireStartPointAndTangentDir(self.wire)
        profileCircle = GC_MakeCircle(startPoint, tangentDir, aWireRadius).Value()
        profileEdge = BRepBuilderAPI_MakeEdge(profileCircle).Edge()
        profileWire = BRepBuilderAPI_MakeWire(profileEdge).Wire()
        shape = BRepOffsetAPI_MakePipe(self.wire, profileWire).Shape()
        draw = FinalShapeDraw(shape)
        self.addItem(draw)


def helperCircleWire(pnt1, pnt2, pnt3):
    geomCircle = GC_MakeCircle(pnt1, pnt2, pnt3).Value()
    edge = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
    return BRepBuilderAPI_MakeWire(edge).Wire()


class CircleDraw(Draw):
    def __init__(self, pnt1, pnt2, pnt3):
        super().__init__('circleObj:circle-line')
        self.pnt1 = pnt1
        self.pnt2 = pnt2
        self.pnt3 = pnt3

    def addStyledItems(self, style:  Style):
        aWireRadius = LINE_RADIUS * style.get(SCALE, 1) * style.get(SCALE_GEOM, 1)
        wire = helperCircleWire(self.pnt1, self.pnt2, self.pnt3)
        draw = WireDraw(wire, aWireRadius)
        self.addItem(draw)


def helperFaceFromPnts(pnts):
    bWire = BRepBuilderAPI_MakeWire()
    for i in range(len(pnts)):
        bEdge = BRepBuilderAPI_MakeEdge(pnts[i - 1], pnts[i])
        bWire.Add(bEdge.Edge())

    wire = bWire.Wire()
    return BRepBuilderAPI_MakeFace(wire).Face()


class FaceDraw(Draw):
    def __init__(self, pnts: [Pnt]):
        super().__init__('faceObj:face')
        self.pnts = pnts

    def addStyledItems(self, style:  Style):
        face = helperFaceFromPnts(self.pnts)
        self.addItem(FinalShapeDraw(face))


class DeskDraw(Draw):
    def __init__(self, labelText: str = None):
        super().__init__('deskObj:decor')
        self.labelText = labelText

    def _addPin(self, x, y, scale, nm):
        self.addItem(CylinderDraw(DESK_PIN_RADIUS * scale, DESK_PIN_HEIGHT * scale).doNm(nm)
                     .doPs(Translate(x * scale, y * scale, 0))
                     .doSt(MATERIAL, STEEL_MATERIAL))

    def addStyledItems(self, style:  Style):

        if self.labelText is None:
            labelText = style.get(SCALE_STR, 'A0 M1:1')
        else:
            labelText = self.labelText

        scale = style.get(SCALE, 1)

        paperSizeX, paperSizeY, paperSizeZ = DESK_PAPER_SIZE
        psx, psy, psz = paperSizeX * scale, paperSizeY * scale, paperSizeZ * scale
        bsx = (paperSizeX + DESK_BORDER_SIZE * 2) * scale
        bsy = (paperSizeY + DESK_BORDER_SIZE * 2) * scale
        bsz = DESK_HEIGHT * scale

        self.addItem(BoxDraw(Pnt(-psx / 2, -psy / 2, -psz), psx, psy, psz).doNm('paperObj'))
        self.addItem(BoxDraw(Pnt(-bsx / 2, -bsy / 2, -bsz-psz), bsx, bsy, bsz).doNm('boardObj'))
        self.addItem(LabelDraw(Pnt(-bsx / 2, -bsy / 2, 0), labelText).doNm('labelObj'))

        dx = (paperSizeX / 2 - DESK_PIN_OFFSET)
        dy = (paperSizeY / 2 - DESK_PIN_OFFSET)

        self._addPin(-dx, -dy, scale, 'pinObj01')
        self._addPin(dx, -dy, scale, 'pinObj02')
        self._addPin(dx, dy, scale, 'pinObj03')
        self._addPin(-dx, dy, scale, 'pinObj04')


class AxisDraw(Draw):
    def __init__(self, pnt1, pnt2, nMark):
        super().__init__('axisObj:decor')
        self.pnt1 = pnt1
        self.pnt2 = pnt2
        self.nMark = nMark

    def addStyledItems(self, style:  Style):
        self.addItem(VectorDraw(self.pnt1, self.pnt2))
        scale = style.get(SCALE, 1)
        markRadius = POINT_RADIUS * scale
        for i in range(1, self.nMark):
            k = i / self.nMark
            v = gp_Vec(self.pnt1, self.pnt2)
            v *= k
            pntMark = self.pnt1.Translated(v)
            self.addItem(CylinderDraw(markRadius, markRadius/2)
                         .doPs(Direct(pntMark, self.pnt2)))


class CoordDraw(Draw):
    def __init__(self, size=None):
        super().__init__('coordObj:decor')
        self.size = size

    def addStyledItems(self, style:  Style):
        if self.size is None:
            paperSizeX, paperSizeY, paperSizeZ = DESK_PAPER_SIZE
            scale = style.get(SCALE, 1)
            size = DESK_AXIS_SIZE * scale
        else:
            size = self.size

        n = DESK_COORD_MARK_DIV
        self.addItem(AxisDraw(Pnt(0, 0, 0), Pnt(size, 0, 0), n))
        self.addItem(AxisDraw(Pnt(0, 0, 0), Pnt(0, size, 0), n))
        self.addItem(AxisDraw(Pnt(0, 0, 0), Pnt(0, 0, size), n))
        self.addItem(PointDraw(Pnt(0, 0, 0)))



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
