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
NICE_ORIGINAL_COLOR = 241,79,160

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

        self.theStyleValues = {
            # [color, material, transparency]

            'MainStylePointGeom': [NICE_YELLOW_COLOR, CHROME, 0.0],
            'MainStyleLineGeom': [NICE_BLUE_COLOR, CHROME, 0.0],
            'MainStyleFaceGeom': [NICE_ORIGINAL_COLOR, CHROME, 0.0],
            'MainStyleLabelGeom': [NICE_WHITE_COLOR, MATE, 0.0],

            'InfoStylePointGeom': [NICE_GRAY_COLOR, MATE, 0.5],
            'InfoStyleLineGeom': [NICE_GRAY_COLOR, MATE,  0.5],
            'InfoStyleFaceGeom': [NICE_GRAY_COLOR, MATE,  0.5],
            'InfoStyleLabelGeom': [NICE_GRAY_COLOR, MATE, 0.0],

            'FocusStylePointGeom': [NICE_RED_COLOR, MATE, 0],
            'FocusStyleLineGeom': [NICE_RED_COLOR, MATE, 0],
            'FocusStyleFaceGeom': [NICE_RED_COLOR, MATE, 0.5],
            'FocusStyleLabelGeom': [NICE_RED_COLOR, MATE, 0.0],
        }

        self.theBoardColor = WOOD_COLOR
        self.thePaperColor = PAPER_COLOR,
        self.thePinColor = STEEL_COLOR

        self.thePaperSizes = AO_SIZE_XYZ

        self.theBoardH = 20
        self.theBoardBorderSize = 60

        self.thePinOffset = 30
        self.thePinR = 10
        self.thePinH = 2

        self.thePointRFactor = 3
        self.theArrowRFactor = 3
        self.theArrowHFactor = 15

    def getStyleBaseRadius(self, aStyle):
        return self.theStyleSizeValues[aStyle][0]

    def getStyleTextHeightPx(self, aStyle):
        return self.theStyleSizeValues[aStyle][1]

    def getStyleTextDelta(self, aStyle):
        return self.theStyleSizeValues[aStyle][2]

    def getStyleColor(self,  aStyle, aDrawType):
        return self.theStyleValues[aStyle+aDrawType][0]

    def getStyleMaterial(self, aStyle, aDrawType):
        return self.theStyleValues[aStyle + aDrawType][1]

    def getStyleTransparency(self, aStyle,  aDrawType):
        return self.theStyleValues[aStyle+aDrawType][2]

    def doStyle(self, draw, aStyle, aGeomType):
        draw.setColor(self.getStyleColor(aStyle, aGeomType))
        draw.setMaterial(self.getStyleMaterial(aStyle, aGeomType))
        draw.setTransparency(self.getStyleTransparency(aStyle, aGeomType))

    def drawPoint(self, aPnt, style):

        draw = self.drawPrimitive()

        pointR = self.getStyleBaseRadius(style) * self.thePointRFactor / self.theScale
        draw.setAsSphere(pointR)
        draw.translate(aPnt.X(), aPnt.Y(), aPnt.Z())

        self.doStyle(draw, style, 'PointScale')

        return draw

    def drawLine(self, pnt1, pnt2, style):

        draw = self.drawPrimitive()

        scale = self.theScale
        lineR = self.getStyleBaseRadius(style) / scale
        vec = gp_Vec(pnt1, pnt2)
        draw.setAsCylinder(lineR, vec.Magnitude())
        draw.setDirection(pnt1, pnt2)

        self.doStyle(draw, style, 'LineGeom')
        return draw


    def drawCircle(self, aPnt1, aPnt2, aPnt3, aStyle):

        draw = self.drawPrimitive()

        draw.setAsCircle(aPnt1, aPnt2, aPnt3, self.getStyleBaseRadius(aStyle) / self.theScale)

        self.doLineStyle(draw, aStyle, 'LineGeom')
        return draw

    def drawVector(self, aPnt1, aPnt2, style):

        draw = self.drawGroup()

        rArrow = self.getStyleBaseRadius(style) * self.theArrowRFactor
        hArrow = self.getStyleBaseRadius(style) * self.theArrowHFactor
        v = gp_Vec(aPnt1, aPnt2)
        vLen = v.Magnitude()
        v *= (vLen - hArrow) / vLen
        pntM = aPnt1.Translated(v)

        line = self.drawLine(aPnt1, pntM, style)
        draw.add(line)

        arrow = self.drawPrimitive()
        arrow.setAsCone(rArrow, 0, hArrow)
        arrow.setDirection(pntM, aPnt2)
        self.doStyle(arrow, style, 'LineGeom')
        draw.add(arrow)

        return draw

    # **************************************

    def drawLabel(self, aPnt, aText, style):

        draw = self.drawPrimitive()

        delta = self.getStyleTextDelta()

        draw.setAsLabel(aText, self.getStyleTextHeightPx[style])
        draw.setTranslate(aPnt.X() + delta, aPnt.Y() + delta, aPnt.Z() + delta)

        self.doStyle(draw, 'TextGeom')
        return draw


    def drawWire(self, aWire, style):

        draw = self.drawPrimitive()
        draw.setAsWire(aWire, self.getStyleBaseRadius())
        self.doStyle(draw, style)

        return draw

        # **************************************

    def drawPin(self, x, y):

        draw = self.drawPrimitive()
        draw.setAsCylinder(self.thePinR / self.theScale, self.thePinH / self.theScale)
        draw.setTranslate(x, y, 0)

        draw.setColor(self.thePinColor)
        draw.setMaterial(CHROME)

        return draw

    def drawDesk(self):

        draw = self.std.drawGroup()

        paper = self.drawPrimitive()
        paperSizeX, paperSizeY, paperSizeZ = self.thePaperSizes
        psx, psy, psz = paperSizeX / self.theScale, paperSizeY / self.theScale, paperSizeZ / self.theScale
        paper.setAsBox(psx, psy, psz)
        paper.translate(-psx / 2, -psy / 2, -psz)
        paper.setMaterial(self.theMate)
        paper.setColor(self.thePaperColor)
        draw.add(paper)

        board = self.drawPrimitive()
        bsx = (paperSizeX + self.theBoardBorderSize * 2) / self.theScale
        bsy = (paperSizeY + self.theBoardBorderSize * 2) / self.theScale
        bsz = self.theBoardH / self.theScale
        board.setAsBox(bsx, bsy, bsz)
        board.translate(-bsx / 2, -bsy / 2, -psz - bsz)
        board.setMaterial(self.theMate)
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
        ret = self.std.drawGroup()

        ret.add(self.drawVector(gp_Pnt(0, 0, 0), gp_Pnt(size, 0, 0), 'InfoStyle'))
        ret.add(self.drawVector(gp_Pnt(0, 0, 0), gp_Pnt(0, size, 0), 'InfoStyle'))
        ret.add(self.drawVector(gp_Pnt(0, 0, 0), gp_Pnt(0, 0, size), 'InfoStyle'))
        ret.add(self.drawLabel(gp_Pnt(size, 0, 0), 'X', 'InfoStyle'))
        ret.add(self.drawLabel(gp_Pnt(0, size, 0), 'Y', 'InfoStyle'))
        ret.add(self.drawLabel(gp_Pnt(0, 0, size), 'Z', 'InfoStyle'))

        ret.add(self.drawPoint(gp_Pnt(0, 0, 0)), 'InfoStyle')
        cnt = size // step
        for i in range(1, cnt - 1):
            d = i * step
            ret.add(self.drawInfoPoint(gp_Pnt(d, 0, 0)),'InfoStyle')
            ret.add(self.drawInfoPoint(gp_Pnt(0, d, 0)),'InfoStyle')
            ret.add(self.drawInfoPoint(gp_Pnt(0, 0, d)),'InfoStyle')

        return ret

    # **************************************

    def drawDemoScene(self):
        ret = self.std.drawGroup()

        desk = self.drawDesk()
        desk.translate(0, 0, -60)
        ret.add(desk)

        bounds = self.drawBounds(gp_Pnt(-50, -50, -50), gp_Pnt(50, 50, 20))
        ret.add(bounds)

        axis = self.drawAxis(50, 10)
        ret.add(axis)

        cone = self.std.drawCone(30, 0, 100)
        cone.translate(0, 0, -50)
        cone.setMaterial(self.mt((50, 200, 50), 'CHROME'))
        ret.add(cone)

        return ret


if __name__ == '__main__':
    deskLib = DeskDrawLib()
    deskLib.theScaleText = 'A0 M5:1'
    deskLib.theScale = 5 / 1
    demoScene = deskLib.drawDemoScene()
    #demoScene.dump()

    screen = ScreenRenderLib()
    screen.renderScene(demoScene)
