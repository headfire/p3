from _std import DrawLib, ScreenRenderLib
from OCC.Core.gp import gp_Pnt, gp_Vec

WOOD_COLOR = 208, 117, 28
PAPER_COLOR = 230, 230, 230
STEEL_COLOR = 100, 100, 100

NICE_WHITE_COLOR = 240, 240, 240
NICE_GRAY_COLOR = 100, 100, 100
NICE_RED_COLOR = 200, 30, 30
NICE_BLUE_COLOR = 100, 100, 255
NICE_YELLOW_COLOR = 255, 255, 100
NICE_ORIGINAL_COLOR = 241, 79, 160

AO_SIZE_XYZ = 1189, 841, 1

MATE = 'PLASTIC'
CHROME = 'CHROME'


class DeskDrawLib(DrawLib):

    def __init__(self):
        super().__init__()

        self.theScale = 1 / 1
        self.theScaleText = 'A0 M1:1'

        self.theStyleSizeValues = {
            # [BaseLineR, TextHeightPx, TextDelta]

            'MainStyle': [5, 20, 5],
            'InfoStyle': [3, 20, 5],
            'FocusStyle': [3, 20, 5]
        }

        self.thePointRFactor = 3
        self.theArrowRFactor = 3
        self.theArrowHFactor = 15

        self.theStyleValues = {
            # [color, material, transparency]
            'MainStylePointGeom': self.makeStyle(NICE_YELLOW_COLOR, CHROME, 0.0),
            'MainStyleLineGeom': self.makeStyle(NICE_BLUE_COLOR, CHROME, 0.0),
            'MainStyleFaceGeom': self.makeStyle(NICE_ORIGINAL_COLOR, CHROME, 0.0),
            'MainStyleLabelGeom': self.makeStyle(NICE_WHITE_COLOR, MATE, 0.0),

            'InfoStylePointGeom': self.makeStyle(NICE_GRAY_COLOR, MATE, 0.5),
            'InfoStyleLineGeom': self.makeStyle(NICE_GRAY_COLOR, MATE, 0.5),
            'InfoStyleFaceGeom': self.makeStyle(NICE_GRAY_COLOR, MATE, 0.5),
            'InfoStyleLabelGeom': self.makeStyle(NICE_GRAY_COLOR, MATE, 0.0),

            'FocusStylePointGeom': self.makeStyle(NICE_RED_COLOR, MATE, 0.0),
            'FocusStyleLineGeom': self.makeStyle(NICE_RED_COLOR, MATE, 0.0),
            'FocusStyleFaceGeom': self.makeStyle(NICE_RED_COLOR, MATE, 0.5),
            'FocusStyleLabelGeom': self.makeStyle(NICE_RED_COLOR, MATE, 0.0),
        }

        self.theBoardH = 20
        self.theBoardBorderSize = 60
        self.theBoardWoodStyle = self.makeStyle(WOOD_COLOR, MATE, 0)

        self.thePaperSizes = AO_SIZE_XYZ
        self.thePaperStyle = self.makeStyle(PAPER_COLOR, MATE, 0)

        self.thePinOffset = 30
        self.thePinR = 10
        self.thePinH = 2
        self.thePinStyle = self.makeStyle(STEEL_COLOR, CHROME, 0)

    def setScale(self, scaleK, scaleText):
        self.theScale = scaleK
        self.theScaleText = scaleText

    def getBaseRadius(self, aDeskStyleName):
        return self.theStyleSizeValues[aDeskStyleName][0] / self.theScale

    def getLabelHeightPx(self, aDeskStyleName):
        return self.theStyleSizeValues[aDeskStyleName][1]  # not scaled

    def getLabelDelta(self, aDeskStyleName):
        return self.theStyleSizeValues[aDeskStyleName][2] / self.theScale

    def getDeskStyle(self, aDeskStyleName, aDeskGeomType):
        return self.theStyleValues[aDeskStyleName + aDeskGeomType]

    # ***********************************************************************

    def getDeskLabel(self, aPnt, aText, aDeskStyleName):
        delta = self.getLabelDelta(aDeskStyleName)

        gr = self.getStdGroup()

        gr.nm('labelText')
        item = self.getStdLabel(aText, self.getLabelHeightPx(aDeskStyleName))
        move = self.makeMove()
        move.setTranslate(aPnt.X() + delta, aPnt.Y() + delta, aPnt.Z() + delta)
        style = self.getDeskStyle(aDeskStyleName, 'LabelGeom')
        gr.add(item, move, style)

        return gr

    def getDeskPoint(self, aPnt, aDeskStyleName):

        gr = self.getStdGroup()

        pointR = self.getBaseRadius(aDeskStyleName) * self.thePointRFactor

        gr.nm('pointSphere')
        gr.mv().setTranslate(aPnt.X(), aPnt.Y(), aPnt.Z())
        gr.st(self.getDeskStyle(aDeskStyleName, 'PointGeom'))
        gr.add(self.getStdSphere(pointR))

        return gr

    def getDeskLine(self, pnt1, pnt2, aDeskStyleName):

        gr = self.getStdGroup()

        lineR = self.getBaseRadius(aDeskStyleName)
        vec = gp_Vec(pnt1, pnt2)

        gr.nm('lineCylinder')
        gr.mv().setDirection(pnt1, pnt2)
        gr.st(self.getDeskStyle(aDeskStyleName, 'LineGeom'))
        gr.add(self.getStdCylinder(lineR, vec.Magnitude()))

        return gr

    def getDeskCircle(self, aPnt1, aPnt2, aPnt3, aDeskStyleName):

        gr = self.getStdGroup()

        lineR = self.getBaseRadius(aDeskStyleName)

        gr.nm('circleObj')
        gr.st(self.getDeskStyle(aDeskStyleName, 'LineGeom'))
        gr.add(self.getStdCircle(aPnt1, aPnt2, aPnt3, lineR))

        return gr

    def getDeskVector(self, aPnt1, aPnt2, aDeskStyleName):

        rArrow = self.getBaseRadius(aDeskStyleName) * self.theArrowRFactor
        hArrow = self.getBaseRadius(aDeskStyleName) * self.theArrowHFactor
        v = gp_Vec(aPnt1, aPnt2)
        vLen = v.Magnitude()
        v *= (vLen - hArrow) / vLen
        pntM = aPnt1.Translated(v)

        gr = self.getStdGroup()

        gr.nm('vectorLine')
        gr.add(self.getDeskLine(aPnt1, pntM, aDeskStyleName))

        gr.nm('vectorArrow')
        gr.mv().setDirection(pntM, aPnt2)
        gr.st(self.getDeskStyle(aDeskStyleName, 'LineGeom'))
        gr.add(self.getStdCone(rArrow, 0, hArrow))

        return gr

    def getDeskWire(self, aWire, aDeskStyleName):

        gr = self.getStdGroup()

        gr.nm('aWire')
        gr.st(self.getDeskStyle(aDeskStyleName, 'LineGeom'))
        gr.add(self.getStdWire(aWire, self.getBaseRadius(aDeskStyleName)))

        return gr

    # **************************************

    def getDeskPin(self, x, y):

        gr = self.getStdGroup()

        gr.nm('pinCylinder')
        gr.st(self.thePinStyle)
        gr.mv().setTranslate(x, y, 0)
        gr.add(self.getStdCylinder(self.thePinR / self.theScale, self.thePinH / self.theScale))

        return gr

    def getDeskDrawBoard(self):

        gr = self.getStdGroup()

        paperSizeX, paperSizeY, paperSizeZ = self.thePaperSizes
        psx, psy, psz = paperSizeX / self.theScale, paperSizeY / self.theScale, paperSizeZ / self.theScale

        gr.nm('boardPaper')
        gr.mv().setTranslate(-psx / 2, -psy / 2, -psz)
        gr.st(self.thePaperStyle)
        gr.add(self.getStdBox(psx, psy, psz))

        bsx = (paperSizeX + self.theBoardBorderSize * 2) / self.theScale
        bsy = (paperSizeY + self.theBoardBorderSize * 2) / self.theScale
        bsz = self.theBoardH / self.theScale

        gr.nm('boardWood')
        gr.mv().setTranslate(-bsx / 2, -bsy / 2, -psz - bsz)
        gr.st(self.theBoardWoodStyle)
        gr.add(self.getStdBox(bsx, bsy, bsz))

        gr.nm('scaleLabel')
        gr.add(self.getDeskLabel(gp_Pnt(-bsx / 2, -bsy / 2, -psz), self.theScaleText, 'InfoStyle'))

        dx = (paperSizeX / 2 - self.thePinOffset) / self.theScale
        dy = (paperSizeY / 2 - self.thePinOffset) / self.theScale

        gr.nm('pin', 1)
        gr.add(self.getDeskPin(-dx, -dy))
        gr.add(self.getDeskPin(dx, -dy))
        gr.add(self.getDeskPin(dx, dy))
        gr.add(self.getDeskPin(-dx, dy))

        return gr

    def getDeskBounds(self, pnt1, pnt2):

        gr = self.getStdGroup()

        x1, y1, z1 = pnt1.X(), pnt1.Y(), pnt1.Z()
        x2, y2, z2 = pnt2.X(), pnt2.Y(), pnt2.Z()

        gr.nm('boundsLine', 1)

        gr.add(self.getDeskLine(gp_Pnt(x1, y1, z1), gp_Pnt(x1, y2, z1), 'InfoStyle'))
        gr.add(self.getDeskLine(gp_Pnt(x1, y2, z1), gp_Pnt(x2, y2, z1), 'InfoStyle'))
        gr.add(self.getDeskLine(gp_Pnt(x2, y2, z1), gp_Pnt(x2, y1, z1), 'InfoStyle'))
        gr.add(self.getDeskLine(gp_Pnt(x2, y1, z1), gp_Pnt(x1, y1, z1), 'InfoStyle'))

        gr.add(self.getDeskLine(gp_Pnt(x1, y1, z1), gp_Pnt(x1, y1, z2), 'InfoStyle'))
        gr.add(self.getDeskLine(gp_Pnt(x1, y2, z1), gp_Pnt(x1, y2, z2), 'InfoStyle'))
        gr.add(self.getDeskLine(gp_Pnt(x2, y1, z1), gp_Pnt(x2, y1, z2), 'InfoStyle'))
        gr.add(self.getDeskLine(gp_Pnt(x2, y2, z1), gp_Pnt(x2, y2, z2), 'InfoStyle'))

        gr.add(self.getDeskLine(gp_Pnt(x1, y1, z2), gp_Pnt(x1, y2, z2), 'InfoStyle'))
        gr.add(self.getDeskLine(gp_Pnt(x1, y2, z2), gp_Pnt(x2, y2, z2), 'InfoStyle'))
        gr.add(self.getDeskLine(gp_Pnt(x2, y2, z2), gp_Pnt(x2, y1, z2), 'InfoStyle'))
        gr.add(self.getDeskLine(gp_Pnt(x2, y1, z2), gp_Pnt(x1, y1, z2), 'InfoStyle'))

        return gr

    def drawAxis(self, size, step):

        gr = self.getStdGroup()

        gr.nm('axisVector', 1)
        gr.add(self.getDeskVector(gp_Pnt(0, 0, 0), gp_Pnt(size, 0, 0), 'InfoStyle'))
        gr.add(self.getDeskVector(gp_Pnt(0, 0, 0), gp_Pnt(0, size, 0), 'InfoStyle'))
        gr.add(self.getDeskVector(gp_Pnt(0, 0, 0), gp_Pnt(0, 0, size), 'InfoStyle'))

        gr.nm('axisLabel', 1)
        gr.add(self.getDeskLabel(gp_Pnt(size, 0, 0), 'X', 'InfoStyle'))
        gr.add(self.getDeskLabel(gp_Pnt(0, size, 0), 'Y', 'InfoStyle'))
        gr.add(self.getDeskLabel(gp_Pnt(0, 0, size), 'Z', 'InfoStyle'))

        gr.nm('axisPoint', 1)
        gr.add(self.getDeskPoint(gp_Pnt(0, 0, 0), 'InfoStyle'))
        cnt = size // step
        for i in range(1, cnt - 1):
            d = i * step
            gr.add(self.getDeskPoint(gp_Pnt(d, 0, 0), 'InfoStyle'))
            gr.add(self.getDeskPoint(gp_Pnt(0, d, 0), 'InfoStyle'))
            gr.add(self.getDeskPoint(gp_Pnt(0, 0, d), 'InfoStyle'))

        return gr

    # **************************************

    def getDeskDemo(self):

        gr = self.getStdGroup()

        gr.nm('desk')
        gr.mv().setTranslate(0, 0, -60)
        gr.add(self.getDeskDrawBoard())

        gr.nm('bounds')
        gr.add(self.getDeskBounds(gp_Pnt(-50, -50, -50), gp_Pnt(50, 50, 20)))

        gr.nm('axis')
        gr.add(self.drawAxis(50, 10))

        gr.nm('demoThree')
        gr.mv().setTranslate(0, 0, -50)
        gr.st(self.makeStyle((50, 200, 50), 'CHROME', 0.7))
        gr.add(self.getStdCone(30, 0, 100))

        return gr


if __name__ == '__main__':
    deskLib = DeskDrawLib()
    deskLib.setScale(5 / 1, 'A0 M5:1')
    ScreenRenderLib().render(deskLib.getDeskDemo())
