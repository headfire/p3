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
            'MainStylePointGeom': self.getStdStyle(NICE_YELLOW_COLOR, CHROME, 0.0),
            'MainStyleLineGeom': self.getStdStyle(NICE_BLUE_COLOR, CHROME, 0.0),
            'MainStyleFaceGeom': self.getStdStyle(NICE_ORIGINAL_COLOR, CHROME, 0.0),
            'MainStyleLabelGeom': self.getStdStyle(NICE_WHITE_COLOR, MATE, 0.0),

            'InfoStylePointGeom': self.getStdStyle(NICE_GRAY_COLOR, MATE, 0.5),
            'InfoStyleLineGeom': self.getStdStyle(NICE_GRAY_COLOR, MATE, 0.5),
            'InfoStyleFaceGeom': self.getStdStyle(NICE_GRAY_COLOR, MATE, 0.5),
            'InfoStyleLabelGeom': self.getStdStyle(NICE_GRAY_COLOR, MATE, 0.0),

            'FocusStylePointGeom': self.getStdStyle(NICE_RED_COLOR, MATE, 0.0),
            'FocusStyleLineGeom': self.getStdStyle(NICE_RED_COLOR, MATE, 0.0),
            'FocusStyleFaceGeom': self.getStdStyle(NICE_RED_COLOR, MATE, 0.5),
            'FocusStyleLabelGeom': self.getStdStyle(NICE_RED_COLOR, MATE, 0.0),
        }

        self.theBoardH = 20
        self.theBoardBorderSize = 60
        self.theBoardWoodStyle = self.getStdStyle(WOOD_COLOR, MATE, 0)

        self.thePaperSizes = AO_SIZE_XYZ
        self.thePaperStyle = self.getStdStyle(PAPER_COLOR, MATE, 0)

        self.thePinOffset = 30
        self.thePinR = 10
        self.thePinH = 2
        self.thePinStyle = self.getStdStyle(STEEL_COLOR, CHROME, 0)

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

        group = self.getStdGroup()

        group.nameHint('labelText')
        item = self.getStdLabel(aText, self.getLabelHeightPx(aDeskStyleName))
        move = self.getStdMove()
        move.setTranslate(aPnt.X() + delta, aPnt.Y() + delta, aPnt.Z() + delta)
        style = self.getDeskStyle(aDeskStyleName, 'LabelGeom')
        group.addItem(item, move, style)

        return group

    def getDeskPoint(self, aPnt, aDeskStyleName):

        group = self.getStdGroup()

        pointR = self.getBaseRadius(aDeskStyleName) * self.thePointRFactor
        item = self.getStdSphere(pointR)
        move = self.getStdMove()
        move.setTranslate(aPnt.X(), aPnt.Y(), aPnt.Z())
        style = self.getDeskStyle(aDeskStyleName, 'PointGeom')
        group.nameHint('pointSphere')
        group.addItem(item, move, style)

        return group

    def getDeskLine(self, pnt1, pnt2, aDeskStyleName):

        group = self.getStdGroup()

        lineR = self.getBaseRadius(aDeskStyleName)
        vec = gp_Vec(pnt1, pnt2)

        group.nameHint('lineCylinder')
        item = self.getStdCylinder(lineR, vec.Magnitude())
        move = self.getStdMove()
        move.setDirection(pnt1, pnt2)
        style = self.getDeskStyle(aDeskStyleName, 'LineGeom')
        group.addItem(item, move, style)

        return group

    def getDeskCircle(self, aPnt1, aPnt2, aPnt3, aDeskStyleName):

        group = self.getStdGroup()

        group.nameHint('circleObj')
        item = self.getStdCircle(aPnt1, aPnt2, aPnt3, self.getBaseRadius(aDeskStyleName))
        move = self.getStdMove()
        style = self.getDeskStyle(aDeskStyleName, 'LineGeom')
        group.addItem(item, move, style)

        return group

    def getDeskVector(self, aPnt1, aPnt2, aDeskStyleName):

        rArrow = self.getBaseRadius(aDeskStyleName) * self.theArrowRFactor
        hArrow = self.getBaseRadius(aDeskStyleName) * self.theArrowHFactor
        v = gp_Vec(aPnt1, aPnt2)
        vLen = v.Magnitude()
        v *= (vLen - hArrow) / vLen
        pntM = aPnt1.Translated(v)

        group = self.getStdGroup()

        group.nameHint('vectorLine')
        item = self.getDeskLine(aPnt1, pntM, aDeskStyleName)
        group.addItem(item)

        group.nameHint('vectorArrow')
        item = self.getStdCone(rArrow, 0, hArrow)
        move = self.getStdMove()
        move.setDirection(pntM, aPnt2)
        style = self.getDeskStyle(aDeskStyleName, 'LineGeom')
        group.addItem(item, move, style)

        return group

    def getDeskWire(self, aWire, aDeskStyleName):

        group = self.getStdGroup()

        group.nameHint('aWire')
        item = self.getStdWire(aWire, self.getBaseRadius(aDeskStyleName))
        style = self.getDeskStyle(aDeskStyleName, 'LineGeom')
        group.addItem(item, None, style)

        return group

    # **************************************

    def getDeskPin(self, x, y):

        group = self.getStdGroup()

        group.nameHint('pinCylinder')
        item = self.getStdCylinder(self.thePinR / self.theScale, self.thePinH / self.theScale)
        move = self.getStdMove()
        move.setTranslate(x, y, 0)
        group.addItem(item, move, self.thePinStyle)

        return group

    def getDeskDrawBoard(self):

        group = self.getStdGroup()

        paperSizeX, paperSizeY, paperSizeZ = self.thePaperSizes
        psx, psy, psz = paperSizeX / self.theScale, paperSizeY / self.theScale, paperSizeZ / self.theScale

        group.nameHint('boardPaper')
        item = self.getStdBox(psx, psy, psz)
        move = self.getStdMove()
        move.setTranslate(-psx / 2, -psy / 2, -psz)
        group.addItem(item, move, self.thePaperStyle)

        bsx = (paperSizeX + self.theBoardBorderSize * 2) / self.theScale
        bsy = (paperSizeY + self.theBoardBorderSize * 2) / self.theScale
        bsz = self.theBoardH / self.theScale

        group.nameHint('boardWood')
        item = self.getStdBox(bsx, bsy, bsz)
        move = self.getStdMove()
        move.setTranslate(-bsx / 2, -bsy / 2, -psz - bsz)
        group.addItem(item, move, self.theBoardWoodStyle)

        group.nameHint('scaleLabel')
        item = self.getDeskLabel(gp_Pnt(-bsx / 2, -bsy / 2, -psz), self.theScaleText, 'InfoStyle')
        group.addItem(item)

        dx = (paperSizeX / 2 - self.thePinOffset) / self.theScale
        dy = (paperSizeY / 2 - self.thePinOffset) / self.theScale

        group.nameHint('pinN')
        group.addItem(self.getDeskPin(-dx, -dy))
        group.addItem(self.getDeskPin(dx, -dy))
        group.addItem(self.getDeskPin(dx, dy))
        group.addItem(self.getDeskPin(-dx, dy))

        return group

    def getDeskBounds(self, pnt1, pnt2):

        group = self.getStdGroup()

        x1, y1, z1 = pnt1.X(), pnt1.Y(), pnt1.Z()
        x2, y2, z2 = pnt2.X(), pnt2.Y(), pnt2.Z()

        group.nameHint('boundsLineN')

        group.addItem(self.getDeskLine(gp_Pnt(x1, y1, z1), gp_Pnt(x1, y2, z1), 'InfoStyle'))
        group.addItem(self.getDeskLine(gp_Pnt(x1, y2, z1), gp_Pnt(x2, y2, z1), 'InfoStyle'))
        group.addItem(self.getDeskLine(gp_Pnt(x2, y2, z1), gp_Pnt(x2, y1, z1), 'InfoStyle'))
        group.addItem(self.getDeskLine(gp_Pnt(x2, y1, z1), gp_Pnt(x1, y1, z1), 'InfoStyle'))

        group.addItem(self.getDeskLine(gp_Pnt(x1, y1, z1), gp_Pnt(x1, y1, z2), 'InfoStyle'))
        group.addItem(self.getDeskLine(gp_Pnt(x1, y2, z1), gp_Pnt(x1, y2, z2), 'InfoStyle'))
        group.addItem(self.getDeskLine(gp_Pnt(x2, y1, z1), gp_Pnt(x2, y1, z2), 'InfoStyle'))
        group.addItem(self.getDeskLine(gp_Pnt(x2, y2, z1), gp_Pnt(x2, y2, z2), 'InfoStyle'))

        group.addItem(self.getDeskLine(gp_Pnt(x1, y1, z2), gp_Pnt(x1, y2, z2), 'InfoStyle'))
        group.addItem(self.getDeskLine(gp_Pnt(x1, y2, z2), gp_Pnt(x2, y2, z2), 'InfoStyle'))
        group.addItem(self.getDeskLine(gp_Pnt(x2, y2, z2), gp_Pnt(x2, y1, z2), 'InfoStyle'))
        group.addItem(self.getDeskLine(gp_Pnt(x2, y1, z2), gp_Pnt(x1, y1, z2), 'InfoStyle'))

        return group

    def drawAxis(self, size, step):

        group = self.getStdGroup()

        group.nameHint('axisVectorN')
        group.addItem(self.getDeskVector(gp_Pnt(0, 0, 0), gp_Pnt(size, 0, 0), 'InfoStyle'))
        group.addItem(self.getDeskVector(gp_Pnt(0, 0, 0), gp_Pnt(0, size, 0), 'InfoStyle'))
        group.addItem(self.getDeskVector(gp_Pnt(0, 0, 0), gp_Pnt(0, 0, size), 'InfoStyle'))

        group.nameHint('axisLabelN')
        group.addItem(self.getDeskLabel(gp_Pnt(size, 0, 0), 'X', 'InfoStyle'))
        group.addItem(self.getDeskLabel(gp_Pnt(0, size, 0), 'Y', 'InfoStyle'))
        group.addItem(self.getDeskLabel(gp_Pnt(0, 0, size), 'Z', 'InfoStyle'))

        group.nameHint('axisPointN')
        group.addItem(self.getDeskPoint(gp_Pnt(0, 0, 0), 'InfoStyle'))
        cnt = size // step
        for i in range(1, cnt - 1):
            d = i * step
            group.addItem(self.getDeskPoint(gp_Pnt(d, 0, 0), 'InfoStyle'))
            group.addItem(self.getDeskPoint(gp_Pnt(0, d, 0), 'InfoStyle'))
            group.addItem(self.getDeskPoint(gp_Pnt(0, 0, d), 'InfoStyle'))

        return group

    # **************************************

    def getDeskDemo(self):

        group = self.getStdGroup()

        group.nameHint('desk')
        move = self.getStdMove()
        move.setTranslate(0, 0, -60)
        group.addItem(self.getDeskDrawBoard(), move)

        group.nameHint('bounds')
        group.addItem(self.getDeskBounds(gp_Pnt(-50, -50, -50), gp_Pnt(50, 50, 20)))

        group.nameHint('axis')
        axis = self.drawAxis(50, 10)
        group.addItem(axis)

        group.nameHint('demoThree')
        item = self.getStdCone(30, 0, 100)
        move = self.getStdMove()
        move.setTranslate(0, 0, -50)
        style = self.getStdStyle((50, 200, 50), 'CHROME', 0.7)
        group.addItem(item, move, style)

        return group


if __name__ == '__main__':
    deskLib = DeskDrawLib()
    deskLib.setScale(5 / 1, 'A0 M5:1')
    deskDemo = deskLib.getDeskDemo()
    # deskDemo.dump()

    screen = ScreenRenderLib()
    screen.render(deskDemo)
