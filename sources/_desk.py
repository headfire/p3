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
        self.theBoardStyle = self.getStdStyle(WOOD_COLOR, MATE, 0)

        self.thePaperSizes = AO_SIZE_XYZ
        self.thePaperStyle = self.getStdStyle(PAPER_COLOR, MATE, 0)

        self.thePinOffset = 30
        self.thePinR = 10
        self.thePinH = 2
        self.thePinStyle = self.getStdStyle(STEEL_COLOR, CHROME, 0)

    def getBaseRadius(self, aDeskStyleName):
        return self.theStyleSizeValues[aDeskStyleName][0] / self.theScale

    def getLabelHeightPx(self, aDeskStyleName):
        return self.theStyleSizeValues[aDeskStyleName][1]  # not scaled

    def getLabelDelta(self, aDeskStyleName):
        return self.theStyleSizeValues[aDeskStyleName][2] / self.theScale

    def getDeskStyle(self, aDeskStyleName, aDeskGeomType):
        return self.theStyleValues[aDeskStyleName + aDeskGeomType]

    def getDeskPoint(self, aPnt, aDeskStyleName):

        group = self.getStdGroup()

        pointR = self.getBaseRadius(aDeskStyleName) * self.thePointRFactor
        item = self.getStdSphere(pointR)
        move = self.getStdMove()
        move.setTranslate(aPnt.X(), aPnt.Y(), aPnt.Z())
        style = self.getDeskStyle(aDeskStyleName, 'PointGeom')
        group.addItem(item, move, style, 'pointSphere')

        return group

    def getDeskLine(self, pnt1, pnt2, aDeskStyleName):

        group = self.getStdGroup()

        lineR = self.getBaseRadius(aLibStyleName)
        vec = gp_Vec(pnt1, pnt2)

        item = self.getStdCylinder(lineR, vec.Magnitude())
        move = self.getStdMove()
        move.setDirection(pnt1, pnt2)
        style = self.getDeskStyle(aDeskStyleName, 'LineGeom')
        group.addItem(item, move, style,'lineCylinder')

        return group

    def getDeskCircle(self, aPnt1, aPnt2, aPnt3, aDeskStyleName):

        group = self.getStdGroup()

        item = self.getStdCircle(aPnt1, aPnt2, aPnt3, self.getBaseRadius(aDeskStyleName))
        move = self.getStdMove()
        style = self.getDeskStyle(aDeskStyleName, 'LineGeom')
        group.addItem(item, move, style, 'lineCylinder')

        return group

    def drawVector(self, aPnt1, aPnt2, aLibStyleName):

        rArrow = self.getBaseRadius(aLibStyleName) * self.theArrowRFactor
        hArrow = self.getBaseRadius(aLibStyleName) * self.theArrowHFactor
        v = gp_Vec(aPnt1, aPnt2)
        vLen = v.Magnitude()
        v *= (vLen - hArrow) / vLen
        pntM = aPnt1.Translated(v)

        group = self.getStdGroup()

        item = self.drawLine(aPnt1, pntM, aLibStyleName)
        group.addItem(item)

        item = self.getStdCone(rArrow, 0, hArrow)
        move = self.getStdMove()
        move.setDirection(pntM, aPnt2)
        style = self.getDeskStyle(aDeskStyleName, 'LineGeom')
        group.addItem(item, move, style)

        return group


        arrow.setAsCone(rArrow, 0, hArrow)
        arrow.setDirection(pntM, aPnt2)
        self.applyLibStyle(arrow, aLibStyleName, 'LineGeom')
        draw.add(arrow)

        return draw

    # **************************************

    def drawLabel(self, aPnt, aText, aLibStyleName):
        draw = self.drawPrimitive()
        delta = self.getLabelDelta(aLibStyleName)
        draw.setAsLabel(aText, self.getLabelHeightPx(aLibStyleName))
        draw.setTranslate(aPnt.X() + delta, aPnt.Y() + delta, aPnt.Z() + delta)
        self.applyLibStyle(draw, aLibStyleName, 'LabelGeom')
        return draw

    def drawWire(self, aWire, aLibStyleName):
        draw = self.drawPrimitive()
        draw.setAsWire(aWire, self.getBaseRadius(aLibStyleName))
        self.applyLibStyle(draw, aLibStyleName, 'LineGeom')
        return draw

        # **************************************

    def drawPin(self, x, y):
        draw = self.drawPrimitive()
        draw.setAsCylinder(self.thePinR / self.theScale, self.thePinH / self.theScale)
        draw.setTranslate(x, y, 0)
        self.applyStyle(draw, self.thePinStyle)
        return draw

    def drawDesk(self):
        draw = self.drawGroup()

        paper = self.drawPrimitive()
        paperSizeX, paperSizeY, paperSizeZ = self.thePaperSizes
        psx, psy, psz = paperSizeX / self.theScale, paperSizeY / self.theScale, paperSizeZ / self.theScale
        paper.setAsBox(psx, psy, psz)
        paper.setTranslate(-psx / 2, -psy / 2, -psz)
        self.applyStyle(paper, self.thePaperStyle)
        draw.add(paper)

        board = self.drawPrimitive()
        bsx = (paperSizeX + self.theBoardBorderSize * 2) / self.theScale
        bsy = (paperSizeY + self.theBoardBorderSize * 2) / self.theScale
        bsz = self.theBoardH / self.theScale
        board.setAsBox(bsx, bsy, bsz)
        board.setTranslate(-bsx / 2, -bsy / 2, -psz - bsz)
        self.applyStyle(board, self.theBoardStyle)
        draw.add(board)

        draw.add(self.drawLabel(gp_Pnt(-bsx / 2, -bsy / 2, -psz), self.theScaleText, 'InfoStyle'))

        dx = (paperSizeX / 2 - self.thePinOffset) / self.theScale
        dy = (paperSizeY / 2 - self.thePinOffset) / self.theScale
        draw.add(self.drawPin(-dx, -dy))
        draw.add(self.drawPin(dx, -dy))
        draw.add(self.drawPin(dx, dy))
        draw.add(self.drawPin(-dx, dy))

        return draw

    def drawBounds(self, pnt1, pnt2):
        draw = self.drawGroup()

        x1, y1, z1 = pnt1.X(), pnt1.Y(), pnt1.Z()
        x2, y2, z2 = pnt2.X(), pnt2.Y(), pnt2.Z()

        draw.add(self.drawLine(gp_Pnt(x1, y1, z1), gp_Pnt(x1, y2, z1), 'InfoStyle'))
        draw.add(self.drawLine(gp_Pnt(x1, y2, z1), gp_Pnt(x2, y2, z1), 'InfoStyle'))
        draw.add(self.drawLine(gp_Pnt(x2, y2, z1), gp_Pnt(x2, y1, z1), 'InfoStyle'))
        draw.add(self.drawLine(gp_Pnt(x2, y1, z1), gp_Pnt(x1, y1, z1), 'InfoStyle'))

        draw.add(self.drawLine(gp_Pnt(x1, y1, z1), gp_Pnt(x1, y1, z2), 'InfoStyle'))
        draw.add(self.drawLine(gp_Pnt(x1, y2, z1), gp_Pnt(x1, y2, z2), 'InfoStyle'))
        draw.add(self.drawLine(gp_Pnt(x2, y1, z1), gp_Pnt(x2, y1, z2), 'InfoStyle'))
        draw.add(self.drawLine(gp_Pnt(x2, y2, z1), gp_Pnt(x2, y2, z2), 'InfoStyle'))

        draw.add(self.drawLine(gp_Pnt(x1, y1, z2), gp_Pnt(x1, y2, z2), 'InfoStyle'))
        draw.add(self.drawLine(gp_Pnt(x1, y2, z2), gp_Pnt(x2, y2, z2), 'InfoStyle'))
        draw.add(self.drawLine(gp_Pnt(x2, y2, z2), gp_Pnt(x2, y1, z2), 'InfoStyle'))
        draw.add(self.drawLine(gp_Pnt(x2, y1, z2), gp_Pnt(x1, y1, z2), 'InfoStyle'))

        return draw

    def drawAxis(self, size, step):
        draw = self.drawGroup()

        draw.add(self.drawVector(gp_Pnt(0, 0, 0), gp_Pnt(size, 0, 0), 'InfoStyle'))
        draw.add(self.drawVector(gp_Pnt(0, 0, 0), gp_Pnt(0, size, 0), 'InfoStyle'))
        draw.add(self.drawVector(gp_Pnt(0, 0, 0), gp_Pnt(0, 0, size), 'InfoStyle'))
        draw.add(self.drawLabel(gp_Pnt(size, 0, 0), 'X', 'InfoStyle'))
        draw.add(self.drawLabel(gp_Pnt(0, size, 0), 'Y', 'InfoStyle'))
        draw.add(self.drawLabel(gp_Pnt(0, 0, size), 'Z', 'InfoStyle'))

        draw.add(self.drawPoint(gp_Pnt(0, 0, 0), 'InfoStyle'))
        cnt = size // step
        for i in range(1, cnt - 1):
            d = i * step
            draw.add(self.drawPoint(gp_Pnt(d, 0, 0), 'InfoStyle'))
            draw.add(self.drawPoint(gp_Pnt(0, d, 0), 'InfoStyle'))
            draw.add(self.drawPoint(gp_Pnt(0, 0, d), 'InfoStyle'))

        return draw

    # **************************************

    def drawDemoScene(self):
        draw = self.drawGroup()

        desk = self.drawDesk()
        desk.setTranslate(0, 0, -60)
        draw.add(desk)

        bounds = self.drawBounds(gp_Pnt(-50, -50, -50), gp_Pnt(50, 50, 20))
        draw.add(bounds)

        axis = self.drawAxis(50, 10)
        draw.add(axis)

        cone = self.drawPrimitive()
        cone.setAsCone(30, 0, 100)
        cone.setTranslate(0, 0, -50)
        self.applyStyle(cone, [(50, 200, 50), 'CHROME', 0.7])
        draw.add(cone)

        return draw


if __name__ == '__main__':
    deskLib = DeskDrawLib()
    deskLib.theScaleText = 'A0 M5:1'
    deskLib.theScale = 5 / 1
    demoScene = deskLib.drawDemoScene()
    # demoScene.dump()

    screen = ScreenRenderLib()
    screen.render(demoScene)
