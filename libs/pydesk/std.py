import sys







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
    def __init__(self, aText):
        super().__init__()
        self.aText = aText

    def drawTo(self, renderLib, aMove=Move(), aStyle=Style()):
        renderLib.setMoveAndStyle(aMove, aStyle)
        renderLib.renderLabel(self.aText)


class PointDraw(Draw):
    def __init__(self, aPnt):
        super().__init__()
        self.aPnt = aPnt

    def drawTo(self, renderLib, aMove=Move(), aStyle=Style()):
        renderLib.setMoveAndStyle(aMove, aStyle)
        renderLib.renderPoint(self.aPnt)


class LineDraw(Draw):
    def __init__(self, aPnt1, aPnt2):
        super().__init__()
        self.aPnt1, self.aPnt2 = aPnt1, aPnt2

    def drawTo(self, renderLib, aMove=Move(), aStyle=Style()):
        renderLib.setMoveAndStyle(aMove, aStyle)
        renderLib.renderLine(self.aPnt1, self.aPnt2)


class VectorDraw(Draw):
    def __init__(self, aPnt1, aPnt2):
        super().__init__()
        self.aPnt1, self.aPnt2 = aPnt1, aPnt2

    def drawTo(self, renderLib, aMove=Move(), aStyle=Style()):
        renderLib.setMoveAndStyle(aMove, aStyle)
        renderLib.renderVector(self.aPnt1, self.aPnt2)


class CircleDraw(Draw):
    def __init__(self, aPnt1, aPnt2, aPnt3):
        super().__init__()
        self.aPnt1, self.aPnt2, self.aPnt3 = aPnt1, aPnt2, aPnt3

    def drawTo(self, renderLib, aMove=Move(), aStyle=Style()):
        super().__init__()
        renderLib.setMoveAndStyle(aMove, aStyle)
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
