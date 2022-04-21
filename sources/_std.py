from OCC.Display.SimpleGui import init_display

from OCC.Core.GC import GC_MakeCircle
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Vec, gp_Ax1, gp_Trsf
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_TypeOfColor
from OCC.Core.Graphic3d import Graphic3d_NameOfMaterial, Graphic3d_MaterialAspect
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_Transform
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox, \
    BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeCone, BRepPrimAPI_MakeTorus

from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepTools import BRepTools_WireExplorer

import sys

MATERIAL_CONSTS = {
    'BRASS': Graphic3d_NameOfMaterial.Graphic3d_NOM_BRASS,
    'BRONZE': Graphic3d_NameOfMaterial.Graphic3d_NOM_BRONZE,
    'COPPER': Graphic3d_NameOfMaterial.Graphic3d_NOM_COPPER,
    'GOLD': Graphic3d_NameOfMaterial.Graphic3d_NOM_GOLD,
    'PEWTER': Graphic3d_NameOfMaterial.Graphic3d_NOM_PEWTER,
    'PLASTER': Graphic3d_NameOfMaterial.Graphic3d_NOM_PLASTER,
    'PLASTIC': Graphic3d_NameOfMaterial.Graphic3d_NOM_PLASTIC,
    'SILVER': Graphic3d_NameOfMaterial.Graphic3d_NOM_SILVER,
    'STEEL': Graphic3d_NameOfMaterial.Graphic3d_NOM_STEEL,
    'STONE': Graphic3d_NameOfMaterial.Graphic3d_NOM_STONE,
    'SHINY_PLASTIC': Graphic3d_NameOfMaterial.Graphic3d_NOM_SHINY_PLASTIC,
    'SATIN': Graphic3d_NameOfMaterial.Graphic3d_NOM_SATIN,
    'METALIZED': Graphic3d_NameOfMaterial.Graphic3d_NOM_METALIZED,
    'NEON_GNC': Graphic3d_NameOfMaterial.Graphic3d_NOM_NEON_GNC,
    'CHROME': Graphic3d_NameOfMaterial.Graphic3d_NOM_CHROME,
    'ALUMINIUM': Graphic3d_NameOfMaterial.Graphic3d_NOM_ALUMINIUM,
    'OBSIDIAN': Graphic3d_NameOfMaterial.Graphic3d_NOM_OBSIDIAN,
    'NEON_PHC': Graphic3d_NameOfMaterial.Graphic3d_NOM_NEON_PHC,
    'JADE': Graphic3d_NameOfMaterial.Graphic3d_NOM_JADE,
    'CHARCOAL': Graphic3d_NameOfMaterial.Graphic3d_NOM_CHARCOAL,
    'WATER': Graphic3d_NameOfMaterial.Graphic3d_NOM_WATER,
    'GLASS': Graphic3d_NameOfMaterial.Graphic3d_NOM_GLASS,
    'DIAMOND': Graphic3d_NameOfMaterial.Graphic3d_NOM_DIAMOND,
    'TRANSPARENT': Graphic3d_NameOfMaterial.Graphic3d_NOM_TRANSPARENT,
    'DEFAULT': Graphic3d_NameOfMaterial.Graphic3d_NOM_DEFAULT
}

DEFAULT_NORMED_COLOR = 0.5, 0.5, 0.5
DEFAULT_MATERIAL = 'CHROME'
DEFAULT_NORMED_TRANSPARENCY = 0.0
DEFAULT_LAYER_NAME = 'DefaultLayer'


def _checkObj(aObj, aClass):
    if not isinstance(aObj, aClass):
        raise Exception('EXPECTED ' + aClass.__name__ + '  - REAL ' + aObj.__class__.__name__)


def _getValue(aValue, aDefaultValue):
    if aValue is not None:
        return aValue
    return aDefaultValue


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


class Style:
    def __init__(self):
        self.aColor = None
        self.aMaterial = None
        self.aTransparency = None

    @staticmethod
    def mergeStyle(aItemStyle, aSuperStyle):
        ret = Style()
        ret.aColor = _getValue(aItemStyle.aColor, aSuperStyle.aColor)
        ret.aTransparency = _getValue(aItemStyle.aTransparency, aSuperStyle.aTransparency)
        ret.aMaterial = _getValue(aItemStyle.aMaterial, aSuperStyle.aMaterial)
        return ret

    def setColor(self, aColor_RGB_256):
        if aColor_RGB_256 is None:
            self.aColor = None
        else:
            r256, g256, b256 = aColor_RGB_256
            self.aColor = (r256 / 255, g256 / 255, b256 / 255)
        return self

    def setTransparency(self, aNormedTransparency):
        self.aTransparency = aNormedTransparency
        return self

    def setMaterial(self, aMaterialName):
        self.aMaterial = aMaterialName
        return self

    def getNormedColor(self):
        return self.aColor

    def getNormedTransparency(self):
        return self.aTransparency

    def getMaterial(self):
        return self.aMaterial


class Move:

    def __init__(self):
        self.aTrsf = gp_Trsf()
        self.aLayer = None

    @staticmethod
    def mergeMove(aItemMove, aSuperMove):
        ret = Move()
        ret.aTrsf = gp_Trsf()
        ret.aTrsf *= aItemMove.aTrsf
        ret.aTrsf *= aSuperMove.aTrsf
        ret.aLayer = _getValue(aItemMove.aLayer, aSuperMove.aLayer)
        return ret

    def _dumpTrsf(self):
        trsf = self.aTrsf
        for iRow in range(1, 4):
            prn = ''
            for iCol in range(1, 5):
                prn += '  ' + str(trsf.Value(iRow, iCol))
            print(prn)

    def setMove(self, dx, dy, dz):
        trsf = gp_Trsf()
        trsf.SetTranslation(gp_Vec(dx, dy, dz))
        self.aTrsf *= trsf
        return self

    # todo setScale K and XYZ

    def setRotate(self, pntAxFrom, pntAxTo, angle):

        trsf = gp_Trsf()
        ax1 = gp_Ax1(pntAxFrom, gp_Dir(gp_Vec(pntAxFrom, pntAxTo)))
        trsf.SetRotation(ax1, angle)
        self.aTrsf *= trsf

        return self

    def setDirect(self, pnt1, pnt2):

        dirVec = gp_Vec(pnt1, pnt2)
        targetDir = gp_Dir(dirVec)

        rotateAngle = gp_Dir(0, 0, 1).Angle(targetDir)
        if not gp_Dir(0, 0, 1).IsParallel(targetDir, 0.001):
            rotateDir = gp_Dir(0, 0, 1)
            rotateDir.Cross(targetDir)
        else:
            rotateDir = gp_Dir(0, 1, 0)

        trsf = gp_Trsf()
        trsf.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), rotateDir), rotateAngle)
        trsf.SetTranslationPart(gp_Vec(gp_Pnt(0, 0, 0), pnt1))
        self.aTrsf *= trsf

        return self

    def getTrsf(self):
        return self.aTrsf


class EnvParamLib:

    def __init__(self):
        self.envParams = {}
        for param in sys.argv:
            key, sep, val = param.partition('=')
            self.envParams[key] = val

    def get(self, paramName, defaultValue):
        if paramName in self.envParams:
            return self.envParams[paramName]
        else:
            return defaultValue


class RenderLib:

    def __init__(self):
        self.aStyle = Style()
        self.aMove = Move()

    def prepare(self, aMove, aStyle):
        self.aStyle = aStyle
        self.aMove = aMove


class ScreenRenderLib(RenderLib):

    def __init__(self):
        super().__init__()
        self.display = None
        self.start_display = None

    def init(self):
        self.display, self.start_display, add_menu, add_function_to_menu = init_display(
            None, (700, 500), True, [128, 128, 128], [128, 128, 128]
        )

    def show(self):
        self.display.FitAll()
        self.start_display()

    def _renderTextObj(self, aText, aHeightPx):
        pnt = gp_Pnt(0, 0, 0).Transformed(self.aMove.getTrsf())
        self.display.DisplayMessage(pnt, aText, aHeightPx, self.aStyle.getNormedColor(), False)

    def _renderShapeObj(self, aShape):
        shapeTr = BRepBuilderAPI_Transform(aShape, self.aMove.getTrsf()).Shape()
        ais = AIS_Shape(shapeTr)
        r, g, b = self.aStyle.getNormedColor()
        aisColor = Quantity_Color(r, g, b,
                                  Quantity_TypeOfColor(Quantity_TypeOfColor.Quantity_TOC_RGB))
        ais.SetColor(aisColor)
        ais.SetTransparency(self.aStyle.getNormedTransparency())
        aspect = Graphic3d_MaterialAspect(MATERIAL_CONSTS[self.aStyle.getMaterial()])
        ais.SetMaterial(aspect)
        self.display.Context.Display(ais, False)

    def _renderWireObj(self, aWire, aWireRadius):
        startPoint, tangentDir = _getWireStartPointAndTangentDir(aWire)
        profileCircle = GC_MakeCircle(startPoint, tangentDir, aWireRadius).Value()
        profileEdge = BRepBuilderAPI_MakeEdge(profileCircle).Edge()
        profileWire = BRepBuilderAPI_MakeWire(profileEdge).Wire()

        shape = BRepOffsetAPI_MakePipe(aWire, profileWire).Shape

        self._renderShapeObj(shape)

    def renderLabel(self, aText, aHeightPx):
        self._renderTextObj(aText, aHeightPx)

    def renderBox(self, aSizeX, aSizeY, aSizeZ):
        shape = BRepPrimAPI_MakeBox(aSizeX, aSizeY, aSizeZ).Shape()
        self._renderShapeObj(shape)

    def renderSphere(self, aRadius):
        shape = BRepPrimAPI_MakeSphere(aRadius).Shape()
        self._renderShapeObj(shape)

    def renderCone(self, aRadius1, aRadius2, aHeight):
        shape = BRepPrimAPI_MakeCone(aRadius1, aRadius2, aHeight).Shape()
        self._renderShapeObj(shape)

    def renderCylinder(self, aRadius, aHeight):
        shape = BRepPrimAPI_MakeCylinder(aRadius, aHeight).Shape()
        self._renderShapeObj(shape)

    def renderTorus(self, aRadius1, aRadius2):
        shape = BRepPrimAPI_MakeTorus(aRadius1, aRadius2).Shape()
        self._renderShapeObj(shape)

    def renderCircle(self, aPnt1, aPnt2, aPnt3, aLineWidth):
        geomCircle = GC_MakeCircle(aPnt1, aPnt2, aPnt3).Value()
        wire = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
        self._renderWireObj(wire, aLineWidth)

    def renderWire(self, aWire, aWireRadius):
        self._renderWireObj(aWire, aWireRadius)

    def renderSurface(self, aSurface):
        self._renderShapeObj(aSurface)

    def run(self, aDrawItem, aMove=Move(), aStyle=Style()):
        self.init()
        aDrawItem.render(self, aMove, aStyle)
        self.show()


# ************************************************************
class DrawObj:

    @staticmethod
    def makeStyle(aColor256=None, aMaterialName=None, aNormedTransparency=None):
        ret = Style()
        ret.setColor(aColor256)
        ret.setMaterial(aMaterialName)
        ret.setTransparency(aNormedTransparency)
        return ret

    @staticmethod
    def makeMove():
        return Move()


class DrawItem(DrawObj):

    def render(self, renderLib, aMove, aStyle):
        pass


class GroupDrawItem(DrawItem):

    def __init__(self):
        self.items = {}
        self.aNextItemName = 'Obj'
        self.aNextItemNum = 0
        self.aNextItemMove = Move()
        self.aNextItemStyle = Style()

    def _dump(self, prefix=''):
        print(prefix + self.__class__.__name__)
        for key in self.items:
            self.items[key].dump(prefix + '[' + key + ']')

    def makeItemName(self):
        if self.aNextItemNum is None:
            itemName = self.aNextItemName
        else:
            itemName = self.aNextItemName + '{0:3}'.format(self.aNextItemNum)
            self.aNextItemNum += 1
        return itemName

    def nm(self, aNextItemName, aNextItemNum=None):
        self.aNextItemName = aNextItemName
        self.aNextItemNum = aNextItemNum

    def mv(self, aMove=None):
        if aMove is not None:
            self.aNextItemMove = aMove
        return self.aNextItemMove

    def st(self, aStyle=None):
        if aStyle is not None:
            self.aNextItemStyle = aStyle
        return self.aNextItemStyle

    def add(self, aItem):
        _checkObj(aItem, DrawItem)
        self.items[self.makeItemName()] = (aItem, self.aNextItemMove, self.aNextItemStyle)
        self.aNextItemMove = self.makeMove()
        self.aNextItemStyle = self.makeStyle()

    def getItem(self, aPath):
        tokens = aPath.split('.')
        ret = self
        for token in tokens:
            ret = ret.children[token]
        return ret

    def render(self, renderLib, aSuperMove, aSuperStyle):
        for key in self.items:
            item, itemMove, itemStyle = self.items[key]
            mergedMove = Move.mergeMove(itemMove, aSuperMove)
            mergedStyle = Style.mergeStyle(itemStyle, aSuperStyle)
            item.render(renderLib, mergedMove, mergedStyle)


class CargoDrawItem(DrawItem):
    def __init__(self, aCargo):
        self.aCargo = aCargo


class HookDrawItem(DrawItem):
    def __init__(self, aHookPnt):
        self.aHookPnt = aHookPnt


class LabelDrawItem(DrawItem):
    def __init__(self, aText, aHeightPx):
        self.aText, self.aHeightPx = aText, aHeightPx

    def render(self, renderLib, aMove, aStyle):
        renderLib.prepare(aMove, aStyle)
        renderLib.renderLabel(self.aText, self.aHeightPx)


class BoxDrawItem(DrawItem):
    def __init__(self, aSizeX, aSizeY, aSizeZ):
        self.aSizeX, self.aSizeY, self.aSizeZ = aSizeX, aSizeY, aSizeZ

    def render(self, renderLib, aMove, aStyle):
        renderLib.prepare(aMove, aStyle)
        renderLib.renderCone(self.aSizeX, self.aSizeY, self.aSizeZ)


class SphereDrawItem(DrawItem):
    def __init__(self, aRadius):
        self.aRadius = aRadius

    def render(self, renderLib, aMove, aStyle):
        renderLib.prepare(aMove, aStyle)
        renderLib.renderSphere(self.aRadius)


class CylinderDrawItem(DrawItem):
    def __init__(self, aRadius, aHeight):
        self.aRadius, self.aHeight = aRadius, aHeight

    def render(self, renderLib, aMove, aStyle):
        renderLib.prepare(aMove, aStyle)
        renderLib.renderCylinder(self.aRadius, self.aHeight)


class ConeDrawItem(DrawItem):
    def __init__(self, aRadius1, aRadius2, aHeight):
        self.aRadius1, self.aRadius2, self.aHeight = aRadius1, aRadius2, aHeight

    def render(self, renderLib, aMove, aStyle):
        renderLib.prepare(aMove, aStyle)
        renderLib.renderCone(self.aRadius1, self.aRadius2, self.aHeight)


class TorusDrawItem(DrawItem):
    def __init__(self, aRadius1, aRadius2):
        self.aRadius1, self.aRadius2 = aRadius1, aRadius2

    def render(self, renderLib, aMove, aStyle):
        renderLib.prepare(aMove, aStyle)
        renderLib.renderTorus(self.aRadius1, self.aRadius2)


class CircleDrawItem(DrawItem):
    def __init__(self, aPnt1, aPnt2, aPnt3, aLineWidth):
        self.aPnt1, self.aPnt2, self.aPnt3, self.aLineWidth = aPnt1, aPnt2, aPnt3, aLineWidth

    def render(self, renderLib, aMove, aStyle):
        renderLib.prepare(aMove, aStyle)
        renderLib.renderCircle(self.aPnt1, self.aPnt2, self.aPnt3, self.aLineWidth)


class WireDrawItem(DrawItem):
    def __init__(self, aWire, aLineRadius):
        self.aWire, self.aLineRadius = aWire, aLineRadius

    def render(self, renderLib, aMove, aStyle):
        renderLib.prepare(aMove, aStyle)
        renderLib.renderWire(self.aWire, self.aLineRadius)


class SurfaceDrawItem(DrawItem):
    def __init__(self, aSurface):
        self.aSurface = aSurface

    def render(self, renderLib, aMove, aStyle):
        renderLib.prepare(aMove, aStyle)
        renderLib.renderSurface(self.aSurface)


class DrawLib(DrawObj):

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
            draw = self.cache[cacheKey]
        else:
            print('==> Compute', cacheKey)
            if param1 is None:
                draw = method()
            elif param2 is None:
                draw = method(param1)
            else:
                draw = method(param1, param2)
            self.cache[cacheKey] = draw
        return draw

    @staticmethod
    def getStdEmpty():
        return DrawItem()

    @staticmethod
    def getStdGroup():
        return GroupDrawItem()

    @staticmethod
    def getStdCargo(aCargo):
        return CargoDrawItem(aCargo)

    @staticmethod
    def getStdHook(aHookPnt):
        return HookDrawItem(aHookPnt)

    @staticmethod
    def getStdLabel(aText, aHeightPx):
        return LabelDrawItem(aText, aHeightPx)

    @staticmethod
    def getStdBox(aSizeX, aSizeY, aSizeZ):
        return BoxDrawItem(aSizeX, aSizeY, aSizeZ)

    @staticmethod
    def getStdSphere(aRadius):
        return SphereDrawItem(aRadius)

    @staticmethod
    def getStdCylinder(aRadius, aHeight):
        return CylinderDrawItem(aRadius, aHeight)

    @staticmethod
    def getStdCone(aRadius1, aRadius2, aHeight):
        return ConeDrawItem(aRadius1, aRadius2, aHeight)

    @staticmethod
    def getStdTorus(aRadius1, aRadius2):
        return TorusDrawItem(aRadius1, aRadius2)

    @staticmethod
    def getStdCircle(aPnt1, aPnt2, aPnt3, aLineWidth):
        return CircleDrawItem(aPnt1, aPnt2, aPnt3, aLineWidth)

    @staticmethod
    def getStdWire(aWire, aLineRadius):
        return WireDrawItem(aWire, aLineRadius)

    @staticmethod
    def getStdSurface(aSurface):
        return SurfaceDrawItem(aSurface)
