from draw import DrawLib
from OCC.Core.gp import gp_Pnt, gp_Vec



class Draw:
    def drawTo(self, aRenderLib, fullObjectName, aMove): pass


class DeskDrawLib(DrawLib):

    def __init__(self, aScaleK=1 / 1, aScaleText='A0 M1:1'):
        super().__init__()


    # ***********************************************************************

    def getDeskLabel(self, aPnt, aText, aDeskStyleName):
        delta = self.getLabelDelta(aDeskStyleName)

        dr = self.makeDraw()

        dr.nm('labelText')
        dr.mv().setMove(aPnt.X() + delta, aPnt.Y() + delta, aPnt.Z() + delta)
        dr.st(self.getDeskStyle(aDeskStyleName, 'LabelGeom'))
        dr.add(self.getLabel(aText, self.getLabelHeightPx(aDeskStyleName)))

        return dr

    def getDeskPoint(self, aPnt, aDeskStyleName):
        dr = self.makeDraw()

        pointR = self.getBaseRadius(aDeskStyleName) * self.aPointRFactor

        dr.nm('pointSphere')
        dr.mv().setMove(aPnt.X(), aPnt.Y(), aPnt.Z())
        dr.st(self.getDeskStyle(aDeskStyleName, 'PointGeom'))
        dr.add(self.getSphere(pointR))

        return dr

    def getDeskLine(self, pnt1, pnt2, aDeskStyleName):
        dr = self.makeDraw()

        lineR = self.getBaseRadius(aDeskStyleName)
        vec = gp_Vec(pnt1, pnt2)

        dr.nm('lineCylinder')
        dr.mv().setDirect(pnt1, pnt2)
        dr.st(self.getDeskStyle(aDeskStyleName, 'LineGeom'))
        dr.add(self.getCylinder(lineR, vec.Magnitude()))

        return dr

    def getDeskCircle(self, aPnt1, aPnt2, aPnt3, aDeskStyleName):
        dr = self.makeDraw()

        lineR = self.getBaseRadius(aDeskStyleName)

        dr.nm('circleObj')
        dr.st(self.getDeskStyle(aDeskStyleName, 'LineGeom'))
        dr.add(self.getCircle(aPnt1, aPnt2, aPnt3, lineR))

        return dr

    def getDeskVector(self, aPnt1, aPnt2, aDeskStyleName):
        rArrow = self.getBaseRadius(aDeskStyleName) * self.aArrowRFactor
        hArrow = self.getBaseRadius(aDeskStyleName) * self.aArrowHFactor
        v = gp_Vec(aPnt1, aPnt2)
        vLen = v.Magnitude()
        v *= (vLen - hArrow) / vLen
        pntM = aPnt1.Translated(v)

        dr = self.makeDraw()

        dr.nm('vectorLine')
        dr.add(self.getDeskLine(aPnt1, pntM, aDeskStyleName))

        dr.nm('vectorArrow')
        dr.mv().setDirect(pntM, aPnt2)
        dr.st(self.getDeskStyle(aDeskStyleName, 'LineGeom'))
        dr.add(self.getCone(rArrow, 0, hArrow))

        return dr

    def getDeskWire(self, aWire, aDeskStyleName):
        dr = self.makeDraw()

        dr.nm('aWire')
        dr.st(self.getDeskStyle(aDeskStyleName, 'LineGeom'))
        dr.add(self.getWire(aWire))

        return dr

    def getDeskSurface(self, aSurface, aDeskStyleName):
        dr = self.makeDraw()

        dr.nm('aSurface')
        dr.st(self.getDeskStyle(aDeskStyleName, 'FaceGeom'))
        dr.add(self.getSurface(aSurface))

        return dr

    # **************************************

    def getDeskPin(self, x, y):
        dr = self.makeDraw()

        dr.nm('pinCylinder')
        dr.st(self.aPinStyle)
        dr.mv().setMove(x, y, 0)
        dr.add(self.getCylinder(self.aPinR / self.aScale, self.aPinH / self.aScale))

        return dr

    def getDeskDrawBoard(self):
        dr = self.makeDraw()

        paperSizeX, paperSizeY, paperSizeZ = self.aPaperSizes
        psx, psy, psz = paperSizeX / self.aScale, paperSizeY / self.aScale, paperSizeZ / self.aScale

        dr.nm('boardPaper')
        dr.mv().setMove(-psx / 2, -psy / 2, -psz)
        dr.st(self.aPaperStyle)
        dr.add(self.getBox(psx, psy, psz))

        bsx = (paperSizeX + self.aBoardBorderSize * 2) / self.aScale
        bsy = (paperSizeY + self.aBoardBorderSize * 2) / self.aScale
        bsz = self.aBoardH / self.aScale

        dr.nm('boardWood')
        dr.mv().setMove(-bsx / 2, -bsy / 2, -psz - bsz)
        dr.st(self.aBoardWoodStyle)
        dr.add(self.getBox(bsx, bsy, bsz))

        dr.nm('scaleLabel')
        dr.add(self.getDeskLabel(gp_Pnt(-bsx / 2, -bsy / 2, -psz), self.aScaleText, 'InfoStyle'))

        dx = (paperSizeX / 2 - self.aPinOffset) / self.aScale
        dy = (paperSizeY / 2 - self.aPinOffset) / self.aScale

        dr.nm('pin', 1)
        dr.add(self.getDeskPin(-dx, -dy))
        dr.add(self.getDeskPin(dx, -dy))
        dr.add(self.getDeskPin(dx, dy))
        dr.add(self.getDeskPin(-dx, dy))

        return dr

    def getDeskBounds(self, pnt1, pnt2):
        dr = self.makeDraw()

        x1, y1, z1 = pnt1.X(), pnt1.Y(), pnt1.Z()
        x2, y2, z2 = pnt2.X(), pnt2.Y(), pnt2.Z()

        dr.nm('boundsLine', 1)

        dr.add(self.getDeskLine(gp_Pnt(x1, y1, z1), gp_Pnt(x1, y2, z1), 'InfoStyle'))
        dr.add(self.getDeskLine(gp_Pnt(x1, y2, z1), gp_Pnt(x2, y2, z1), 'InfoStyle'))
        dr.add(self.getDeskLine(gp_Pnt(x2, y2, z1), gp_Pnt(x2, y1, z1), 'InfoStyle'))
        dr.add(self.getDeskLine(gp_Pnt(x2, y1, z1), gp_Pnt(x1, y1, z1), 'InfoStyle'))

        dr.add(self.getDeskLine(gp_Pnt(x1, y1, z1), gp_Pnt(x1, y1, z2), 'InfoStyle'))
        dr.add(self.getDeskLine(gp_Pnt(x1, y2, z1), gp_Pnt(x1, y2, z2), 'InfoStyle'))
        dr.add(self.getDeskLine(gp_Pnt(x2, y1, z1), gp_Pnt(x2, y1, z2), 'InfoStyle'))
        dr.add(self.getDeskLine(gp_Pnt(x2, y2, z1), gp_Pnt(x2, y2, z2), 'InfoStyle'))

        dr.add(self.getDeskLine(gp_Pnt(x1, y1, z2), gp_Pnt(x1, y2, z2), 'InfoStyle'))
        dr.add(self.getDeskLine(gp_Pnt(x1, y2, z2), gp_Pnt(x2, y2, z2), 'InfoStyle'))
        dr.add(self.getDeskLine(gp_Pnt(x2, y2, z2), gp_Pnt(x2, y1, z2), 'InfoStyle'))
        dr.add(self.getDeskLine(gp_Pnt(x2, y1, z2), gp_Pnt(x1, y1, z2), 'InfoStyle'))

        return dr

    def drawAxis(self, size, step):
        dr = self.makeDraw()

        dr.nm('axisVector', 1)
        dr.add(self.getDeskVector(gp_Pnt(0, 0, 0), gp_Pnt(size, 0, 0), 'InfoStyle'))
        dr.add(self.getDeskVector(gp_Pnt(0, 0, 0), gp_Pnt(0, size, 0), 'InfoStyle'))
        dr.add(self.getDeskVector(gp_Pnt(0, 0, 0), gp_Pnt(0, 0, size), 'InfoStyle'))

        dr.nm('axisLabel', 1)
        dr.add(self.getDeskLabel(gp_Pnt(size, 0, 0), 'X', 'InfoStyle'))
        dr.add(self.getDeskLabel(gp_Pnt(0, size, 0), 'Y', 'InfoStyle'))
        dr.add(self.getDeskLabel(gp_Pnt(0, 0, size), 'Z', 'InfoStyle'))

        dr.nm('axisPoint', 1)
        dr.add(self.getDeskPoint(gp_Pnt(0, 0, 0), 'InfoStyle'))
        cnt = size // step
        for i in range(1, cnt - 1):
            d = i * step
            dr.add(self.getDeskPoint(gp_Pnt(d, 0, 0), 'InfoStyle'))
            dr.add(self.getDeskPoint(gp_Pnt(0, d, 0), 'InfoStyle'))
            dr.add(self.getDeskPoint(gp_Pnt(0, 0, d), 'InfoStyle'))

        return dr

    # **************************************

    def getDeskDemo(self):
        dr = self.makeDraw()

        dr.nm('desk')
        dr.mv().setMove(0, 0, -60)
        dr.add(self.getDeskDrawBoard())

        dr.nm('bounds')
        dr.add(self.getDeskBounds(gp_Pnt(-50, -50, -50), gp_Pnt(50, 50, 20)))

        dr.nm('axis')
        dr.add(self.drawAxis(50, 10))

        dr.nm('demoThree')
        dr.mv().setMove(0, 0, -50)
        dr.st(self.makeStyle((50, 200, 50), 'CHROME', 0.7))
        dr.add(self.getCone(30, 0, 100))

        return dr


if __name__ == '__main__':
    from render import ScreenRender
    desk = DeskDrawLib(5 / 1, 'A0 M5:1')
    screen = ScreenRender()
    desk.getDeskDemo().drawTo(screen)
    screen.show()