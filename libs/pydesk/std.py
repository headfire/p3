from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Vec, gp_Ax1, gp_Trsf


import sys


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


class Draw:
    pass


class GroupDraw(Draw):

    def __init__(self):
        super().__init__()
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
            self.aNextItemNum = 1
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
        _checkObj(aItem, Draw)
        self.items[self.makeItemName()] = (aItem, self.aNextItemMove, self.aNextItemStyle)
        self.aNextItemMove = Move()
        self.aNextItemStyle = Style()

    def getItem(self, aPath):
        tokens = aPath.split('.')
        ret = self
        for token in tokens:
            ret = ret.children[token]
        return ret

    def drawTo(self, renderLib, aMove=Move(), aStyle=Style()):
        for key in self.items:
            item, itemMove, itemStyle = self.items[key]
            mergedMove = Move.mergeMove(itemMove, aMove)
            mergedStyle = Style.mergeStyle(itemStyle, aStyle)
            item.drawTo(renderLib, mergedMove, mergedStyle)


class HookDraw(Draw):
    def __init__(self, aHookPnt, aHookObj):
        super().__init__()
        self.aHookPnt = aHookPnt
        self.aHookObj = aHookObj

    def drawTo(self, renderLib, aMove=Move(), aStyle=Style()):
        pass


class LabelDraw(Draw):
    def __init__(self, aText, aHeightPx):
        super().__init__()
        self.aText, self.aHeightPx = aText, aHeightPx

    def drawTo(self, renderLib, aMove=Move(), aStyle=Style()):
        renderLib.setMoveAndStyle(aMove, aStyle)
        renderLib.renderLabel(self.aText, self.aHeightPx)


class BoxDraw(Draw):
    def __init__(self, aSizeX, aSizeY, aSizeZ):
        super().__init__()
        self.aSizeX, self.aSizeY, self.aSizeZ = aSizeX, aSizeY, aSizeZ

    def drawTo(self, renderLib, aMove=Move(), aStyle=Style()):
        renderLib.setMoveAndStyle(aMove, aStyle)
        renderLib.renderBox(self.aSizeX, self.aSizeY, self.aSizeZ)


class SphereDraw(Draw):
    def __init__(self, aRadius):
        super().__init__()
        self.aRadius = aRadius

    def drawTo(self, renderLib, aMove=Move(), aStyle=Style()):
        renderLib.setMoveAndStyle(aMove, aStyle)
        renderLib.renderSphere(self.aRadius)


class CylinderDraw(Draw):
    def __init__(self, aRadius, aHeight):
        super().__init__()
        self.aRadius, self.aHeight = aRadius, aHeight

    def drawTo(self, renderLib, aMove=Move(), aStyle=Style()):
        renderLib.setMoveAndStyle(aMove, aStyle)
        renderLib.renderCylinder(self.aRadius, self.aHeight)


class ConeDraw(Draw):
    def __init__(self, aRadius1, aRadius2, aHeight):
        super().__init__()
        self.aRadius1, self.aRadius2, self.aHeight = aRadius1, aRadius2, aHeight

    def drawTo(self, renderLib, aMove=Move(), aStyle=Style()):
        renderLib.setMoveAndStyle(aMove, aStyle)
        renderLib.renderCone(self.aRadius1, self.aRadius2, self.aHeight)


class TorusDraw(Draw):
    def __init__(self, aRadius1, aRadius2):
        super().__init__()
        self.aRadius1, self.aRadius2 = aRadius1, aRadius2

    def drawTo(self, renderLib, aMove=Move(), aStyle=Style()):
        super().__init__()
        renderLib.setMoveAndStyle(aMove, aStyle)
        renderLib.renderTorus(self.aRadius1, self.aRadius2)


class CircleDraw(Draw):
    def __init__(self, aPnt1, aPnt2, aPnt3, aLineWidth):
        super().__init__()
        self.aPnt1, self.aPnt2, self.aPnt3, self.aLineWidth = aPnt1, aPnt2, aPnt3, aLineWidth

    def drawTo(self, renderLib, aMove=Move(), aStyle=Style()):
        super().__init__()
        renderLib.setMoveAndStyle(aMove, aStyle)
        renderLib.renderCircle(self.aPnt1, self.aPnt2, self.aPnt3, self.aLineWidth)


class WireDraw(Draw):
    def __init__(self, aWire, aLineRadius):
        super().__init__()
        self.aWire, self.aLineRadius = aWire, aLineRadius

    def drawTo(self, renderLib, aMove=Move(), aStyle=Style()):
        renderLib.setMoveAndStyle(aMove, aStyle)
        renderLib.renderWire(self.aWire, self.aLineRadius)


class SurfaceDraw(Draw):
    def __init__(self, aSurface):
        super().__init__()
        self.aSurface = aSurface

    def drawTo(self, renderLib, aMove=Move(), aStyle=Style()):
        renderLib.setMoveAndStyle(aMove, aStyle)
        renderLib.renderSurface(self.aSurface)


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

    @staticmethod
    def makeDraw():
        return GroupDraw()

    @staticmethod
    def getHook(aHookPnt, aHookObj=None):
        return HookDraw(aHookPnt, aHookObj)

    @staticmethod
    def getLabel(aText, aHeightPx):
        return LabelDraw(aText, aHeightPx)

    @staticmethod
    def getBox(aSizeX, aSizeY, aSizeZ):
        return BoxDraw(aSizeX, aSizeY, aSizeZ)

    @staticmethod
    def getSphere(aRadius):
        return SphereDraw(aRadius)

    @staticmethod
    def getCylinder(aRadius, aHeight):
        return CylinderDraw(aRadius, aHeight)

    @staticmethod
    def getCone(aRadius1, aRadius2, aHeight):
        return ConeDraw(aRadius1, aRadius2, aHeight)

    @staticmethod
    def getTorus(aRadius1, aRadius2):
        return TorusDraw(aRadius1, aRadius2)

    @staticmethod
    def getCircle(aPnt1, aPnt2, aPnt3, aLineWidth):
        return CircleDraw(aPnt1, aPnt2, aPnt3, aLineWidth)

    @staticmethod
    def getWire(aWire, aLineRadius):
        return WireDraw(aWire, aLineRadius)

    @staticmethod
    def getSurface(aSurface):
        return SurfaceDraw(aSurface)
