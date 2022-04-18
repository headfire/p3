from OCC.Display.SimpleGui import init_display

from OCC.Core.GC import GC_MakeCircle
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Vec, gp_Ax1, gp_Trsf, gp_GTrsf
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


class EnvParamLib:

    def __init__(self):
        self.envParams = {}
        for param in sys.argv:
            key, sep, val = param.partition('=')
            if val != '':
                try:
                    self.envParams[key] = int(val)
                except ValueError:
                    print('Non int param')

    def get(self, paramName, defaultValue):
        if paramName in self.envParams:
            return self.envParams[paramName]
        else:
            return defaultValue


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


def todoUse(varToUse):
    print('TODO use', varToUse)


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


class ScreenRenderLib:

    def __init__(self):
        self.display = None
        self.curMaterial = None
        self.curLayer = None
        self.curTransObj = None

    def _renderText(self, pnt, text, size):
        color, transparency, materialTypeName = self.curMaterial
        r, g, b = color
        if self.curTransObj is not None:
            pnt = pnt.Transformed(self.curTransObj)
        self.display.DisplayMessage(pnt, text, size, (r / 256, g / 256, b / 256), False)

    def setMaterial(self, material):
        self.curMaterial = material

    def setLayer(self, layer):
        self.curLayer = layer

    def setTransObj(self, transObj):
        self.curTransObj = transObj

    def _renderShapeObj(self, shape):
        color, transparency, materialName = self.curMaterial
        if self.curTransObj is not None:
            shape = BRepBuilderAPI_Transform(shape, self.curTransObj).Shape()
        ais = AIS_Shape(shape)
        r, g, b = color
        aisColor = Quantity_Color(r / 256, g / 256, b / 256,
                                  Quantity_TypeOfColor(Quantity_TypeOfColor.Quantity_TOC_RGB))
        ais.SetColor(aisColor)
        ais.SetTransparency(transparency / 100)
        aspect = Graphic3d_MaterialAspect(MATERIAL_CONSTS[materialName])
        ais.SetMaterial(aspect)
        self.display.Context.Display(ais, False)

    def render(self, drawable):
        self.display, start_display, add_menu, add_function_to_menu = init_display(
            None, (700, 500), True, [128, 128, 128], [128, 128, 128]
        )

        drawable.render(self)

        self.display.FitAll()
        start_display()

    def renderLabel(self, geometry):
        pnt, text, size = geometry
        self._renderText(pnt, text, size)

    def renderBox(self, geometry):
        xSize, ySize, zSize = geometry
        shape = BRepPrimAPI_MakeBox(xSize, ySize, zSize).Shape()
        self._renderShapeObj(shape)

    def renderSphere(self, geometry):
        pnt, r = geometry
        shape = BRepPrimAPI_MakeSphere(pnt, r).Shape()
        self._renderShapeObj(shape)

    def renderCone(self, geometry):
        r1, r2, h = geometry
        shape = BRepPrimAPI_MakeCone(r1, r2, h).Shape()
        self._renderShapeObj(shape)

    def renderCylinder(self, geometry):
        r, h = geometry
        shape = BRepPrimAPI_MakeCylinder(r, h).Shape()
        self._renderShapeObj(shape)

    def renderTube(self, geometry):
        wire, radius = geometry
        startPoint, tangentDir = _getWireStartPointAndTangentDir(wire)
        profileCircle = GC_MakeCircle(startPoint, tangentDir, radius).Value()
        profileEdge = BRepBuilderAPI_MakeEdge(profileCircle).Edge()
        profileWire = BRepBuilderAPI_MakeWire(profileEdge).Wire()

        pipeShell = BRepOffsetAPI_MakePipe(wire, profileWire)
        pipeShape = pipeShell.Shape()

        self._renderShapeObj(pipeShape)

    def renderSurface(self, geometry):
        surfaceShape = geometry
        self._renderShapeObj(surfaceShape)


# ************************************************************

class Transform:
    def __init__(self, geometry):
        self.geometry = geometry

    def getTrans(self):
        pass


class Rotate(Transform):

    def getTransObj(self):
        pntAxFrom, pntAxTo, angle = self.geometry
        tObj = gp_Trsf()
        ax1 = gp_Ax1(pntAxFrom, gp_Dir(gp_Vec(pntAxFrom, pntAxTo)))
        tObj.SetRotation(ax1, angle)
        return tObj


class Translate(Transform):

    def getTransObj(self):
        dx, dy, dz = self.geometry
        tObj = gp_Trsf()
        tObj.SetTranslation(gp_Vec(dx, dy, dz))
        return tObj


class Scale(Transform):

    def getTransObj(self):
        kx, ky, kz = self.geometry
        todoUse((kx, ky, kz))
        tObj = gp_GTrsf()
        # todo SetAffinity tObj.SetScale(kx, ky, kz)
        return tObj


class FromPointToPoint(Transform):

    def getTransObj(self):
        pnt1, pnt2 = self.geometry
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

        return tObj


# ************************************************************

class Drawable:
    def __init__(self, geometry):

        self.parent = None

        self.geometry = geometry

        self.layer = None
        self.material = None
        self.trans = None

        self.children = {}
        self.childrenCount = 0

    def setMaterial(self, material):
        self.material = material

    def setLayer(self, layer):
        self.layer = layer

    def addTransform(self, transform):
        trans = transform.getTransObj()
        if self.trans is None:
            self.trans = trans
        else:
            self.trans *= trans

    def add(self, drawable, name=None):
        drawable.parent = self
        if name is None:
            name = 'Child' + str(self.childrenCount)
        self.children[name] = drawable
        self.childrenCount += 1

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

    def dump(self, prefix=''):
        print(prefix + self.__class__.__name__, self.material, self.getFinalMaterial())
        for key in self.children:
            self.children[key].dump(prefix + '[' + key + ']')

    def copy(self):
        copied = self.__class__(self.geometry)
        copied.layer = self.layer
        copied.material = self.material
        for key in self.children:
            copied.children[key] = self.children[key].copy()
        return copied

    def translate(self, dx, dy, dz):
        self.addTransform(Translate((dx, dy, dz)))

    def scale(self, kx, ky, kz):
        self.addTransform(Scale((kx, ky, kz)))

    def rotate(self, pntAxFrom, pntAxTo, angle):
        self.addTransform(Rotate((pntAxFrom, pntAxTo, angle)))

    def fromPointToPoint(self, pnt1, pnt2):
        self.addTransform(FromPointToPoint((pnt1, pnt2)))

    def render(self, renderer):
        renderer.setMaterial(self.getFinalMaterial())
        renderer.setLayer(self.getFinalLayer())
        renderer.setTransObj(self.getFinalTrans())
        self.renderSelf(renderer)
        for key in self.children:
            self.children[key].render(renderer)

    def renderSelf(self, renderer):
        pass


class Hook(Drawable):
    # pnt = self.geometry
    pass


class Label(Drawable):
    def renderSelf(self, renderer):
        renderer.renderLabel(self.geometry)


class Box(Drawable):
    def renderSelf(self, renderer):
        renderer.renderBox(self.geometry)


class Sphere(Drawable):
    def renderSelf(self, renderer):
        renderer.renderSphere(self.geometry)


class Cone(Drawable):
    def renderSelf(self, renderer):
        renderer.renderCone(self.geometry)


class Cylinder(Drawable):
    def renderSelf(self, renderer):
        renderer.renderCylinder(self.geometry)


class Tube(Drawable):
    def renderSelf(self, renderer):
        renderer.renderTube(self.geometry)


class Tor(Drawable):
    def renderSelf(self, renderer):
        pnt1, pnt2, pnt3, r = self.geometry
        geomCircle = GC_MakeCircle(pnt1, pnt2, pnt3).Value()
        wire = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
        renderer.renderTube((wire, r))


class Surface(Drawable):
    def renderSelf(self, renderer):
        renderer.renderSurface(self.geometry)


# ************************************************************


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
            return self.cache[cacheKey].copy()
        print('==> Compute', cacheKey)
        if param1 is None:
            return method()
        if param2 is None:
            return method(param1)
        method(param1, param2)


class StdDrawLib(DrawLib):

    @staticmethod
    def drawGroup():
        return Drawable(None)

    @staticmethod
    def drawFoo():
        return Drawable(None)

    @staticmethod
    def drawContainer(customData):
        return Drawable(customData)

    @staticmethod
    def drawHook(pnt):
        return Drawable(pnt)

    @staticmethod
    def drawLabel(pnt, text, size):
        return Label((pnt, text, size))

    @staticmethod
    def drawBox(xSize, ySize, zSize):
        return Box((xSize, ySize, zSize))

    @staticmethod
    def drawSphere(pnt, r):
        return Sphere((pnt, r))

    @staticmethod
    def drawCone(r1, r2, h):
        return Cone((r1, r2, h))

    @staticmethod
    def drawCylinder(r, h):
        return Cylinder((r, h))

    @staticmethod
    def drawTube(wire, radius):
        return Tube((wire, radius))

    @staticmethod
    def drawSurface(surface):
        return Surface(surface)
