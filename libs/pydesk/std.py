import sys

limit = (DESK_DEFAULT_DRAW_AREA_SIZE / 2) * self.scale
self.decorLimitMinX = -limit
self.decorLimitMaxX = limit
self.decorLimitMinY = -limit
self.decorLimitMaxY = limit
self.decorLimitMinZ = -limit
self.decorLimitMaxZ = limit
self.decorDeskDX = 0
self.decorDeskDY = 0
self.decorDeskDZ = -limit * 1.2
self.decorIsDesk = True
self.decorIsAxis = True
self.decorIsLimits = True


class Prim:

    def getShape(self): pass

class BoxPrim(Prim):

    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def getShape(self):
        return BRepPrimAPI_MakeBox(self.x, self.y, self.z).Shape()

class SpherePrim(Prim):

    def __init__(self, r):
        self.r = r

    def getShape(self):
        return BRepPrimAPI_MakeSphere(gp_Pnt(0, 0, 0), self.r).Shape()

class ConePrim(Prim):

    def __init__(self, r1, r2, h):
        self.r1, self.r2, self.h = r1, r2, h

    def getShape(self):
        return BRepPrimAPI_MakeCone(self.r1, self.r2, self.h).Shape()

class CylinderPrim(Prim):

    def __init__(self, r, h):
        self.r, self.h = r, h

    def getShape(self):
        return BRepPrimAPI_MakeCylinder(self.r, self.h).Shape()

class TorusPrim(Prim):

    def __init__(self, r1, r2):
        self.r1, self.r2 = r1, r2

    def getShape(self):
        return BRepPrimAPI_MakeTorus(self.r1, self.r2).Shape()


def initDeskPosition(self, deskDX, deskDY, deskDZ):
    self.decorDeskDX = deskDX
    self.decorDeskDY = deskDY
    self.decorDeskDZ = deskDZ


def initDrawLimits(self, limitMinX, limitMaxX, limitMinY, limitMaxY, limitMinZ, limitMaxZ):
    self.decorLimitMinX = limitMinX
    self.decorLimitMaxX = limitMaxX
    self.decorLimitMinY = limitMinY
    self.decorLimitMaxY = limitMaxY
    self.decorLimitMinZ = limitMinZ
    self.decorLimitMaxZ = limitMaxZ


def initDecor(self, isDesk, isAxis, isLimits):
    self.styleIsDesk = isDesk
    self.styleIsAxis = isAxis
    self.styleIsLimits = isLimits


class Draw(Draw):

    def __init__(self):
        super().__init__()
        self.items = {}

    def _dump(self, prefix=''):
        print(prefix + self.__class__.__name__)
        for key in self.items:
            self.items[key].dump(prefix + '[' + key + ']')

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

    def render(self, renderLib): pass

    def draw(self, renderLib, renderName, position=Position()):
        renderLib.renderSetName(renderName)
        renderLib.renderSetPosition(position)
        self.render(renderLib)
        for itemName in self.items:
            item, itemMove, itemStyle = self.items[key]
            mergedMove = Move.mergeMove(itemMove, aMove)
            item.draw(renderLib, renderName + '.' + itemName, mergedMove)


class PointDraw(Draw):

    def __init__(self, pnt, isVisible=True, labelText=None):
        super().__init__()
        self.pnt = pnt

    def render(self, renderLib, aMove=Move(), aStyle=Style()):
        if self.isVisible:
            renderLib.renderPoint(self.apnt)
        if self.labelText is not None:
            renderLib.renderPoint(self.pnt, self.labelText)


class LineDraw(Draw):
    def __init__(self, aPnt1, aPnt2):
        super().__init__()
        self.aPnt1, self.aPnt2 = aPnt1, aPnt2

    def render(self, renderLib):
        renderLib.renderLine(self.aPnt1, self.aPnt2)


class VectorDraw(Draw):
    def __init__(self, aPnt1, aPnt2):
        super().__init__()
        self.aPnt1, self.aPnt2 = aPnt1, aPnt2

    def drawTo(self, renderLib, aMove=Move(), aStyle=Style()):
        renderLib.renderArrow(self.aPnt1, self.aPnt2)


class CircleDraw(Draw):
    def __init__(self, aPnt1, aPnt2, aPnt3):
        super().__init__()
        self.aPnt1, self.aPnt2, self.aPnt3 = aPnt1, aPnt2, aPnt3

    def render(self, renderLib, aMove=Move(), aStyle=Style()):
        super().__init__()
        renderLib.renderCircle(self.aPnt1, self.aPnt2, self.aPnt3)


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


class WireDraw(Draw):
    def __init__(self, aWire):
        super().__init__()
        self.aWire = aWire

    def drawTo(self, renderLib, aMove=Move(), aStyle=Style()):
        renderLib.setMoveAndStyle(aMove, aStyle)
        renderLib.renderWire(self.aWire)


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
    def getLabel(aText):
        return LabelDraw(aText)

    @staticmethod
    def getPoint(aPnt):
        return PointDraw(aPnt)

    @staticmethod
    def getVector(aPnt1, aPnt2):
        return LineDraw(aPnt1, aPnt2)

    @staticmethod
    def getLine(aPnt1, aPnt2):
        return LineDraw(aPnt1, aPnt2)

    @staticmethod
    def getCircle(aPnt1, aPnt2, aPnt3):
        return CircleDraw(aPnt1, aPnt2, aPnt3)

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
    def getWire(aWire):
        return WireDraw(aWire)

    @staticmethod
    def getSurface(aSurface):
        return SurfaceDraw(aSurface)
