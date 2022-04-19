from OCC.Display.SimpleGui import init_display

from OCC.Core.GC import GC_MakeCircle
from OCC.Core.gp import gp_XYZ, gp_Pnt, gp_Dir, gp_Vec, gp_Ax1, gp_Trsf, gp_GTrsf
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_TypeOfColor
from OCC.Core.Graphic3d import Graphic3d_NameOfMaterial, Graphic3d_MaterialAspect
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_Transform
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox, \
    BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeCone

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

DEFAULT_COLOR = (100, 100, 100)
DEFAULT_TRANSPARENCY = 0.0
DEFAULT_MATERIAL = 'PLASTIC'


class SmartObject:

    def __init__(self):
        self.theIsDebug = False

    def debug(self, aVar):
        if self.theIsDebug:
            print('DEBUG:', aVar)

    def makeMethodNonStatic(self):
        self.debug('Make this method non static')

    def checkObj(self, aObj, aClass):
        self.makeMethodNonStatic()
        if not isinstance(aObj, aClass):
            raise Exception('EXPECTED ' + aClass.__name__ + '  - REAL ' + aObj.__class__.__name__)


class EnvParamLib(SmartObject):

    def __init__(self):

        super().__init__()

        self.envParams = {}
        for param in sys.argv:
            key, sep, val = param.partition('=')
            self.envParams[key] = val

    def get(self, paramName, defaultValue):
        if paramName in self.envParams:
            return self.envParams[paramName]
        else:
            return defaultValue


class ScreenRenderLib(SmartObject):

    def __init__(self):

        super().__init__()

        self.display = None

        self.aGeom = None
        self.aMaterial = None
        self.aColor = None
        self.aTransparency = None
        self.aTransform = None

    def _getVectorTangentToCurveAtPoint(self, edge, uRatio):
        self.makeMethodNonStatic()
        aCurve, aFP, aLP = BRep_Tool.Curve(edge)
        aP = aFP + (aLP - aFP) * uRatio
        v1 = gp_Vec()
        p1 = gp_Pnt()
        aCurve.D1(aP, p1, v1)
        return v1

    def _getWireStartPointAndTangentDir(self, wire):
        ex = BRepTools_WireExplorer(wire)
        edge = ex.Current()
        vertex = ex.CurrentVertex()
        v = self._getVectorTangentToCurveAtPoint(edge, 0)
        return BRep_Tool.Pnt(vertex), gp_Dir(v)

    def _renderTextObj(self, aText, aHeightPx):
        pnt = gp_Pnt(0, 0, 0).Transformed(self.aTransform)
        r, g, b = self.aColor
        self.display.DisplayMessage(pnt, aText, aHeightPx, (r/255, g/255, b/255), False)

    def _renderShapeObj(self, shape):
        shape = BRepBuilderAPI_Transform(shape, self.aTransform).Shape()
        ais = AIS_Shape(shape)
        r, g, b = self.aColor
        aisColor = Quantity_Color(r/255, g/255, b/255,
                                  Quantity_TypeOfColor(Quantity_TypeOfColor.Quantity_TOC_RGB))
        ais.SetColor(aisColor)
        ais.SetTransparency(self.aTransparency)
        aspect = Graphic3d_MaterialAspect(MATERIAL_CONSTS[self.aMaterial])
        ais.SetMaterial(aspect)
        self.display.Context.Display(ais, False)

    def _renderWireObj(self, aWire, aWireRadius):

        startPoint, tangentDir = self._getWireStartPointAndTangentDir(aWire)
        profileCircle = GC_MakeCircle(startPoint, tangentDir, aWireRadius).Value()
        profileEdge = BRepBuilderAPI_MakeEdge(profileCircle).Edge()
        profileWire = BRepBuilderAPI_MakeWire(profileEdge).Wire()

        shape = BRepOffsetAPI_MakePipe(aWire, profileWire).Shape

        self._renderShapeObj(shape)

    def _renderAsEmpty(self):
        pass

    def _renderAsLabel(self):
        aText, aHeightPx = self.aGeom
        self._renderTextObj(aText, aHeightPx)

    def _renderAsBox(self):
        aSizeX, aSizeY, aSizeZ = self.aGeom
        shape = BRepPrimAPI_MakeBox(aSizeX, aSizeY, aSizeZ).Shape()
        self._renderShapeObj(shape)

    def _renderAsSphere(self):
        aRadius = self.aGeom
        shape = BRepPrimAPI_MakeSphere(aRadius).Shape()
        self._renderShapeObj(shape)

    def _renderAsCone(self):
        aRadius1, aRadius2, aHeight = self.aGeom
        shape = BRepPrimAPI_MakeCone(aRadius1, aRadius2, aHeight).Shape()
        self._renderShapeObj(shape)

    def _renderAsCylinder(self):
        aRadius, aHeight = self.aGeom
        shape = BRepPrimAPI_MakeCylinder(aRadius, aHeight).Shape()
        self._renderShapeObj(shape)

    # todo _renderAsTorus

    def _renderAsCircle(self):
        aPnt1, aPnt2, aPnt3, aLineWidth = self.aGeom
        geomCircle = GC_MakeCircle(aPnt1, aPnt2, aPnt3).Value()
        wire = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
        self._renderWireObj(wire, aLineWidth)

    def _renderAsWire(self):
        aWire, aWireRadius = self.aGeom
        self._renderWireObj(aWire, aWireRadius)

    def _renderAsSurface(self):
        aSurface = self.aGeom
        self._renderShapeObj(aSurface)

    def _renderDrawItem(self, aDrawItem):

        renderMethod = self.__getattribute__('_renderAs' + aDrawItem.getGeomType())
        renderMethod(aDrawItem)

        self.aGeom = aDrawItem.getGeomImmutable()
        self.aMaterial = aDrawItem.getMaterial()
        self.aColor = aDrawItem.getColor()
        self.aTransparency = aDrawItem.getTransparency()
        self.aTransform = aDrawItem.getTransform()

        for key in aDrawItem.children:
            self._renderDrawItem(aDrawItem.children[key])

    def render(self, aDrawItem):
        self.display, start_display, add_menu, add_function_to_menu = init_display(
            None, (700, 500), True, [128, 128, 128], [128, 128, 128]
        )

        self._renderDrawItem(aDrawItem)

        self.display.FitAll()
        start_display()


# ************************************************************

class DrawItem(SmartObject):

    def __init__(self):

        super().__init__()

        self.parent = None
        self.children = {}
        self.childrenCount = 0

        self.aGeomType = 'Empty'
        self.aGeomImmutable = None
        self.aGeomTransform = gp_Trsf()

        self.aMaterial = None
        self.aTransparency = None
        self.aColor = None
        self.aLayer = None

    def copy(self):
        ret = DrawItem()
        ret.aColor = self.aColor
        ret.aMaterial = self.aMaterial
        ret.aTransparency = self.aTransparency
        ret.aLayer = self.aLayer
        ret.aGeomType = self.aGeomType
        ret.aGeomImmutable = self.aGeomImmutable
        ret.aGeomTransform = gp_GTrsf(ret.aGeomTransform)
        for key in self.children:
            ret.children[key] = self.children[key].copy()

    def getHierarchyAttr(self, aAttrName, aDefaultValue):
        value = self.__getattribute__(aAttrName)
        if value is not None:
            return value
        if self.parent is not None:
            return self.parent.getHierarchyAttr(self, aAttrName, aDefaultValue)
        return aDefaultValue

    def _dump(self, prefix=''):
        print(prefix + self.__class__.__name__, self.aGeomType)
        for key in self.children:
            self.children[key].dump(prefix + '[' + key + ']')

    def _applyGeomTransform(self, aAppliedTransform):
        self.aGeomTransform *= aAppliedTransform

    def add(self, aDrawItem, aItemName=None):
        self.checkObj(aDrawItem, DrawItem)
        aDrawItem.parent = self
        if aItemName is None:
            aItemName = 'Child' + str(self.childrenCount)
        self.children[aItemName] = aDrawItem
        self.childrenCount += 1
        return aDrawItem

    def setAsEmpty(self):
        self.aGeomType = 'Empty'
        self.aGeomImmutable = None
        return self

    def setAsLabel(self, aText, aHeightPx):
        self.aGeomType = 'Label'
        self.aGeomImmutable = aText, aHeightPx
        return self

    def setAsBox(self, aSizeX, aSizeY, aSizeZ):
        self.aGeomType = 'Box'
        self.aGeomImmutable = aSizeX, aSizeY, aSizeZ

        return self

    def setAsSphere(self, aRadius):
        self.aGeomType = 'Sphere'
        self.aGeomImmutable = aRadius
        return self

    def setAsCylinder(self, aRadius, aHeight):
        self.aGeomType = 'Cylinder'
        self.aGeomImmutable = aRadius, aHeight
        return self

    def setAsCone(self, aRadius1, aRadius2, aHeight):
        self.aGeomType = 'Cone'
        self.aGeomImmutable = aRadius1, aRadius2, aHeight
        return self

    # todo def setAsTorus(self, aRadius1, aRadius2):

    def setAsCircle(self, aPnt1, aPnt2, aPnt3, aLineWidth):
        self.aGeomType = 'Circle'
        self.aGeomImmutable = aPnt1, aPnt2, aPnt3, aLineWidth
        return self

    def setAsWire(self, aWire, aLineRadius):
        self.aGeomType = 'Wire'
        self.aGeomImmutable = aWire, aLineRadius
        return self

    def setAsSurface(self, aSurface):
        self.aGeomType = 'Surface'
        self.aGeomImmutable = aSurface
        return self

    def setColor(self, aColor_RGB_256):
        self.aColor = aColor_RGB_256

    def setTransparency(self, aFloat_0_1):
        self.aTransparency = aFloat_0_1

    def setMaterial(self, aMaterialName):
        self.aMaterial = aMaterialName
        return self

    def setLayer(self, aLayerName):
        self.aLayer = aLayerName
        return self

    def setTranslate(self, dx, dy, dz):
        tObj = gp_GTrsf()
        tObj.SetTranslationPart(gp_XYZ(dx, dy, dz))
        self._applyGeomTransform(tObj)
        return self

    def setScale(self, kx, ky, kz):
        self.checkObj(kx, int)
        self.checkObj(ky, int)
        self.checkObj(kz, int)
        tObj = gp_GTrsf()
        # todo SetAffinity tObj.SetScale(kx, ky, kz)
        self._applyGeomTransform(tObj)
        return self

    def setRotate(self, pntAxFrom, pntAxTo, angle):

        tObj = gp_Trsf()
        ax1 = gp_Ax1(pntAxFrom, gp_Dir(gp_Vec(pntAxFrom, pntAxTo)))
        tObj.SetRotation(ax1, angle)
        self._applyGeomTransform(tObj)
        return self

    def setDirection(self, pnt1, pnt2):

        dirVec = gp_Vec(pnt1, pnt2)
        targetDir = gp_Dir(dirVec)

        rotateAngle = gp_Dir(0, 0, 1).Angle(targetDir)
        if not gp_Dir(0, 0, 1).IsParallel(targetDir, 0.001):
            rotateDir = gp_Dir(0, 0, 1)
            rotateDir.Cross(targetDir)
        else:
            rotateDir = gp_Dir(0, 1, 0)

        tObj = gp_Trsf()
        tObj.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), rotateDir), rotateAngle)
        tObj.SetTranslationPart(gp_Vec(gp_Pnt(0, 0, 0), pnt1))
        self._applyGeomTransform(tObj)

        return self

    def getGeomType(self):
        return self.aGeomType

    def getGeomImmutable(self):
        return self.aGeomImmutable

    def getTransform(self):
        if self.parent is not None:
            ret = gp_Trsf()
            ret *= self.parent.getTransform()
            return ret
        else:
            return self.aGeomTransform

    def getLayer(self):
        if self.aLayer is not None:
            return self.aLayer
        if self.parent is not None:
            return self.parent.getLayer()
        return None

    def getColor(self):
        if self.aColor is not None:
            return self.aColor
        if self.parent is not None:
            return self.parent.getColor()
        return DEFAULT_COLOR

    def getTransparency(self):
        if self.aTransparency is not None:
            return self.aTransparency
        if self.parent is not None:
            return self.parent.getTransparentcy()
        return DEFAULT_TRANSPARENCY

    def getMaterial(self):
        if self.aMaterial is not None:
            return self.aMaterial
        if self.parent is not None:
            return self.parent.getMaterial()
        return DEFAULT_MATERIAL

    def getChild(self, fullName):
        names = fullName.split('.')
        ret = self
        for childName in names:
            ret = ret.children[childName]
        return ret

    def getPosition(self):
        return gp_Pnt(0, 0, 0).Transformed(self.getTransform())


class DrawLib(SmartObject):

    def __init__(self):
        super().__init__()
        self.drawCache = {}
        self.aDrawItemClass = DrawItem

    def drawCached(self, methodName, param1=None, param2=None):
        params = ''
        if param1 is not None:
            params += str(param1)
        if param2 is not None:
            params += ',' + str(param2)

        cacheKey = methodName + '(' + params + ')'

        method = self.__getattribute__(methodName)
        if cacheKey in self.drawCache:
            print('==> Get from cache', cacheKey)
            draw = self.drawCache[cacheKey].copy()
        else:
            print('==> Compute', cacheKey)
            if param1 is None:
                draw = method()
            elif param2 is None:
                draw = method(param1)
            else:
                draw = method(param1, param2)
            self.drawCache[cacheKey] = draw
            self.checkObj(draw, DrawItem)
        return draw

    def drawGroup(self):
        return self.aDrawItemClass()

    def drawPrimitive(self):
        return self.aDrawItemClass()
