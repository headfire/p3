from OCC.Display.SimpleGui import init_display

from OCC.Core.GC import GC_MakeCircle
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Vec, gp_Ax1, gp_Trsf, gp_GTrsf
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_TypeOfColor
from OCC.Core.Graphic3d import Graphic3d_NameOfMaterial, Graphic3d_MaterialAspect
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_Transform
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
from OCC.Core.TopoDS import TopoDS_Shape

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox, \
    BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeCone

from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepTools import BRepTools_WireExplorer

import sys

DEFAULT_MATERIAL = (50, 50, 50), 0, 'CHROME'

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


def check(aObj, aClass):
    if not isinstance(aObj, aClass):
        raise Exception('EXPECTED ' + aClass.__name__ + '  - REAL ' + aObj.__class__.__name__)


def checkGeom(aGeom):
    if not isinstance(aGeom, dict):
        raise Exception('geom MUST BE dict() - REAL ' + aGeom.__class__.__name__)
    for key in aGeom:
        if not isinstance(key, str):
            raise Exception('geom KEY MUST BE str - REAL ' + key.__class__.__name__)
        if not isinstance(aGeom[key], (int, float, str, gp_Pnt, TopoDS_Shape)):
            raise Exception('geom[' + key + '] INCORRECT geom item type - REAL ' + aGeom.__class__.__name__)


def getVectorTangentToCurveAtPoint(edge, uRatio):
    aCurve, aFP, aLP = BRep_Tool.Curve(edge)
    aP = aFP + (aLP - aFP) * uRatio
    v1 = gp_Vec()
    p1 = gp_Pnt()
    aCurve.D1(aP, p1, v1)
    return v1


def getWireStartPointAndTangentDir(wire):
    ex = BRepTools_WireExplorer(wire)
    edge = ex.Current()
    vertex = ex.CurrentVertex()
    v = getVectorTangentToCurveAtPoint(edge, 0)
    return BRep_Tool.Pnt(vertex), gp_Dir(v)


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


class ScreenRenderLib:

    def __init__(self):

        self.display = None

        self.curGeom = None
        self.curTrans = None
        self.curMaterial = None
        self.curLayer = None

    def renderTextObj(self, aText, aHeightPx):
        pnt = gp_Pnt(0, 0, 0)
        if self.curTrans is not None:
            pnt = gp_Pnt(0, 0, 0).Transformed(self.curTrans)
        rgb = (self.curMaterial['r'] / 256, self.curMaterial['g'] / 256, self.curMaterial['b'] / 256)
        self.display.DisplayMessage(pnt, aText, aHeightPx, rgb, False)

    def renderShapeObj(self, shape):
        if self.curTrans is not None:
            shape = BRepBuilderAPI_Transform(shape, self.curTrans).Shape()
        ais = AIS_Shape(shape)
        aisColor = Quantity_Color(self.curMaterial['r'] / 256, self.curMaterial['g'] / 256, self.curMaterial['b'] / 256,
                                  Quantity_TypeOfColor(Quantity_TypeOfColor.Quantity_TOC_RGB))
        ais.SetColor(aisColor)
        ais.SetTransparency(1 - self.curMaterial['a'] / 256)
        aspect = Graphic3d_MaterialAspect(MATERIAL_CONSTS[self.curMaterial['materialName']])
        ais.SetMaterial(aspect)
        self.display.Context.Display(ais, False)

    def renderWireObj(self, aWire, aWireRadius):

        startPoint, tangentDir = getWireStartPointAndTangentDir(aWire)
        profileCircle = GC_MakeCircle(startPoint, tangentDir, aWireRadius).Value()
        profileEdge = BRepBuilderAPI_MakeEdge(profileCircle).Edge()
        profileWire = BRepBuilderAPI_MakeWire(profileEdge).Wire()

        shape = BRepOffsetAPI_MakePipe(aWire, profileWire).Shape

        self.renderShapeObj(shape)

    def renderNone(self):
        pass

    def renderLabel(self):
        self.renderTextObj(self.curGeom['aText'], self.curGeom['aHeightPx'])

    def renderBox(self):
        shape = BRepPrimAPI_MakeBox(self.curGeom['aSizeX'], self.curGeom['aSizeY'], self.curGeom['aSizeZ']).Shape()
        self.renderShapeObj(shape)

    def renderSphere(self):
        shape = BRepPrimAPI_MakeSphere(self.curGeom['aRadius']).Shape()
        self.renderShapeObj(shape)

    def renderCone(self):
        shape = BRepPrimAPI_MakeCone(self.curGeom['aRadius1'], self.curGeom['aRadius2'],
                                     self.curGeom['aHeight']).Shape()
        self.renderShapeObj(shape)

    def renderCylinder(self):
        shape = BRepPrimAPI_MakeCylinder(self.curGeom['aRadius'], self.curGeom['aHeight']).Shape()
        self.renderShapeObj(shape)

    def renderTor(self):
        geomCircle = GC_MakeCircle(self.curGeom['aPnt1'], self.curGeom['aPnt12'], self.curGeom['aPnt1']).Value()
        wire = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
        self.renderWireObj(wire, self.curGeom['aTorRadius'])

    def renderWire(self):
        self.renderWireObj(self.curGeom['aWire'], self.curGeom['aWireRadius'])

    def renderSurface(self):
        self.renderShapeObj(self.curGeom['aSurface'])

    def renderDrawItem(self, aDrawItem):

        self.curMaterial = aDrawItem.getFinalMaterial()
        self.curLayer = aDrawItem.getFinalLayer()
        self.curTrans = aDrawItem.getFinalTrans()
        self.curGeom = aDrawItem.getFinalTrans()

        renderMethod = self.__getattribute__('render' + self.curGeom['renderAs'])
        renderMethod()

        for key in aDrawItem.children:
            self.renderDrawItem(aDrawItem.children[key])

    def renderScene(self, aSceneDrawItem):
        self.display, start_display, add_menu, add_function_to_menu = init_display(
            None, (700, 500), True, [128, 128, 128], [128, 128, 128]
        )

        self.renderDrawItem(aSceneDrawItem)

        self.display.FitAll()
        start_display()


# ************************************************************


class StdDrawItem:

    def __init__(self, aGeom):

        self.parent = None

        self.geom = aGeom

        self.layer = None
        self.material = None
        self.trans = None

        self.children = {}
        self.childrenCount = 0

    def addTrans(self, aNewTrans):
        if self.trans is None:
            self.trans = aNewTrans
        else:
            self.trans *= aNewTrans

    def dump(self, prefix=''):
        print(prefix + self.__class__.__name__, self.material, self.getFinalMaterial())
        for key in self.children:
            self.children[key].dump(prefix + '[' + key + ']')

    def add(self, aDrawItem, aItemName=None):
        check(aDrawItem, StdDrawItem)
        aDrawItem.parent = self
        if aItemName is None:
            aItemName = 'Child' + str(self.childrenCount)
        self.children[aItemName] = aDrawItem
        self.childrenCount += 1
        return aDrawItem

    def setMaterial(self, material):
        self.material = material
        return self

    def setLayer(self, layer):
        self.layer = layer
        return self

    def translate(self, dx, dy, dz):
        tObj = gp_Trsf()
        tObj.SetTranslation(gp_Vec(dx, dy, dz))
        self.addTrans(tObj)
        return self

    def scale(self, kx, ky, kz):
        check(kx, int)
        check(ky, int)
        check(kz, int)
        tObj = gp_GTrsf()
        # todo SetAffinity tObj.SetScale(kx, ky, kz)
        self.addTrans(tObj)
        return self

    def rotate(self, pntAxFrom, pntAxTo, angle):

        tObj = gp_Trsf()
        ax1 = gp_Ax1(pntAxFrom, gp_Dir(gp_Vec(pntAxFrom, pntAxTo)))
        tObj.SetRotation(ax1, angle)
        self.addTrans(tObj)
        return self

    def fromPointToPoint(self, pnt1, pnt2):

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
        self.addTrans(tObj)
        return self

    def getFinalTrans(self):
        if self.parent is not None:
            parentTrans = self.parent.getFinalTrans()
        else:
            parentTrans = None
        if parentTrans is not None:
            if self.trans is not None:
                return self.trans * parentTrans
            else:
                return parentTrans
        else:
            if self.trans is not None:
                return self.trans
            else:
                return None

    def getFinalLayer(self):
        if self.layer is not None:
            return self.layer
        if self.parent is not None:
            return self.parent.getFinalLayer()
        return None

    def getFinalMaterial(self):
        if self.material is not None:
            return self.material
        if self.parent is not None:
            return self.parent.getFinalMaterial()
        return None


class DrawLib:

    def __init__(self):

        self.cache = {}

        self.theDebug = False

    def createDrawItem(self, aGeom):
        if self.theDebug:
            print('Create Draw Item from', aGeom)
        return StdDrawItem(aGeom)

    def geom(self, methodName, param1=None, param2=None):

        params = ''
        if param1 is not None:
            params += str(param1)
        if param2 is not None:
            params += ',' + str(param2)

        cacheKey = methodName + '(' + params + ')'

        method = self.__getattribute__(methodName)
        if cacheKey in self.cache:
            print('==> Get from cache', cacheKey)
            geom = self.cache[cacheKey]
            return geom
        else:
            if param1 is None:
                geom = method()
            elif param2 is None:
                geom = method(param1)
            else:
                geom = method(param1, param2)
            checkGeom(geom)
            print('==> Compute', cacheKey)
            self.cache[cacheKey] = geom
        return geom


class StdDrawLib(DrawLib):

    def drawGroup(self):
        return self.createDrawItem({'renderAs': 'None'})

    def drawHook(self):
        return self.createDrawItem({'renderAs': 'None'})

    def drawLabel(self, aText, aHeightPx):
        return self.createDrawItem({'aText': aText, 'aHeightPx': aHeightPx, 'renderAs': 'Label'})

    def drawBox(self, aSizeX, aSizeY, aSizeZ):
        return self.createDrawItem({'aSizeX': aSizeX, 'aSizeY': aSizeY, 'aSizeZ': aSizeZ, 'renderAs': 'Box'})

    def drawSphere(self, r):
        return self.createDrawItem({r})

    def drawCylinder(self, aRadius, aHeight):
        return self.createDrawItem({'aRadius': aRadius, 'aHeight': aHeight, 'renderAs': 'Cylinder'})

    def drawCone(self, aRadius1, aRadius2, aHeight):
        return self.createDrawItem({'aRadius1': aRadius1, 'aRadius2': aRadius2, 'aHeight': aHeight, 'renderAs': 'Cone'})

    def drawTor(self, aPnt1, aPnt2, aPnt3, aTorRadius):
        return self.createDrawItem({'aPnt1': aPnt1, 'aPnt2': aPnt2, 'aPnt3': aPnt3,
                                    'aTorRadius': aTorRadius, 'renderAs': 'Tor'})

    def drawWire(self, aWire, aWireRadius):
        return self.createDrawItem({'aWire': aWire, 'aWireRadius': aWireRadius, 'renderAs': 'Tube'})

    def drawSurface(self, aSurface):
        return self.createDrawItem({'aSurface': aSurface, 'renderAs': 'Surface'})
