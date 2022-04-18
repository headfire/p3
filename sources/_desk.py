from _std import DrawLib, StdDrawLib, ScreenRenderLib
from OCC.Core.gp import gp_Pnt, gp_Vec

WOOD_RGB256 = 208, 117, 28
PAPER_RGB256 = 230, 230, 230
STEEL_RGB256 = 100, 100, 100

GRAY_RGB256 = 100, 100, 100

HALF_TRANSPARENCY_ALPHA = 100

BLUE_RGB256 = 100, 100, 255
YELLOW_RGB256 = 255, 255, 100

AO_SIZE_XYZ = 1189, 841, 1


class DeskDrawLib(DrawLib):

    def __init__(self):
        super().__init__()

        self.std = StdDrawLib()

        self.theScale = 1 / 1
        self.theScaleText = 'A0 M1:1'

        self.theBoardMaterial = self.mt(WOOD_RGB256, 'PLASTIC')
        self.thePaperMaterial = self.mt(PAPER_RGB256, 'PLASTIC')
        self.thePinMaterial = self.mt(STEEL_RGB256, 'CHROME')
        self.theMainPointMaterial = self.mt(YELLOW_RGB256, 'CHROME')  # yellow
        self.theMainWireMaterial = self.mt(BLUE_RGB256, 'CHROME')  # blue

        self.theInfoMaterial = self.mt(GRAY_RGB256, 'PLASTIC', HALF_TRANSPARENCY_ALPHA)

        self.thePaperSizes = AO_SIZE_XYZ

        self.theBoardH = 20
        self.theBoardBorderSize = 60

        self.thePinOffset = 30
        self.thePinR = 10
        self.thePinH = 2

        self.theInfoLineWidth = 6
        self.theMainLineWidth = 8

        self.thePointRFactor = 3
        self.theArrowRFactor = 3
        self.theArrowHFactor = 15

        self.theInfoLabelSizePx = 20  # not scaled
        self.theInfoLabelDelta = 15

    def drawPoint(self, aPnt, aBaseLineR):
        pointR = aBaseLineR * self.thePointRFactor / self.theScale
        ret = self.std.drawSphere(pointR)
        ret.translate(aPnt.X(), aPnt.Y(), aPnt.Z())
        return ret

    def drawLine(self, pnt1, pnt2, baseLineR):
        scale = self.theScale

        lineR = baseLineR / scale
        vec = gp_Vec(pnt1, pnt2)
        ret = self.std.drawCylinder(lineR, vec.Magnitude())
        ret.fromPointToPoint(pnt1, pnt2)

        return ret

    def drawCircle(self, aPnt1, aPnt2, aPnt3, aBaseLineR):
        draw = self.std.drawTor(aPnt1, aPnt2, aPnt3, aBaseLineR / self.theScale)

        return draw

    def drawVector(self, aPnt1, aPnt2, aBaseLineR):
        rArrow = aBaseLineR * self.theArrowRFactor / self.theScale
        hArrow = aBaseLineR * self.theArrowHFactor / self.theScale
        v = gp_Vec(aPnt1, aPnt2)
        vLen = v.Magnitude()
        v *= (vLen - hArrow) / vLen
        pntM = aPnt1.Translated(v)

        ret = self.std.drawGroup()

        line = self.drawInfoLine(aPnt1, pntM)
        ret.add(line)

        arrow = self.std.drawCone(rArrow, 0, hArrow)
        arrow.fromPointToPoint(pntM, aPnt2)
        ret.add(arrow)

        return ret

    # **************************************

    def drawInfoLabel(self, aPnt, aText):
        delta = self.theInfoLabelDelta / self.theScale

        ret = self.std.drawLabel(aText, self.theInfoLabelSizePx)
        ret.translate(aPnt.X() + delta, aPnt.Y() + delta, aPnt.Z() + delta)
        ret.setMaterial(self.theInfoMaterial)

        return ret

    def drawInfoPoint(self, aPnt):
        ret = self.drawPoint(aPnt, self.theInfoLineWidth / 2)
        ret.setMaterial(self.theInfoMaterial)

        return ret

    def drawInfoCircle(self, aPnt1, aPnt2, aPnt3):
        draw = self.std.drawTor(aPnt1, aPnt2, aPnt3, self.theMainLineWidth)

        return draw

    def drawMainPoint(self, aPnt):
        ret = self.drawPoint(aPnt, self.theMainLineWidth / 2)
        ret.setMaterial(self.theMainPointMaterial)

        return ret

    def drawInfoLine(self, aPnt1, aPnt2):
        ret = self.drawLine(aPnt1, aPnt2, self.theInfoLineWidth / 2)
        ret.setMaterial(self.theInfoMaterial)

        return ret

    def drawMainWire(self, aWire):
        draw = self.std.drawWire(aWire, self.theMainLineWidth / 2)
        draw.setMaterial(self.theMainWireMaterial)

        return draw

    def drawInfoWire(self, aWire):
        draw = self.std.drawWire(aWire, self.theInfoLineWidth / 2)
        draw.setMaterial(self.theInfoMaterial)

        return draw

    def drawInfoVector(self, aPnt1, aPnt2):
        ret = self.drawVector(aPnt1, aPnt2, self.theInfoLineWidth / 2)
        ret.setMaterial(self.theInfoMaterial)

        return ret

        # **************************************

    def drawPin(self, x, y):
        pin = self.std.drawCylinder(self.thePinR / self.theScale, self.thePinH / self.theScale)
        pin.translate(x, y, 0)
        pin.setMaterial(self.thePinMaterial)

        return pin

    def drawDesk(self):
        ret = self.std.drawGroup()

        paperSizeX, paperSizeY, paperSizeZ = self.thePaperSizes
        psx, psy, psz = paperSizeX / self.theScale, paperSizeY / self.theScale, paperSizeZ / self.theScale
        paper = self.std.drawBox(psx, psy, psz)
        paper.translate(-psx / 2, -psy / 2, -psz)
        paper.setMaterial(self.thePaperMaterial)
        ret.add(paper)

        bsx = (paperSizeX + self.theBoardBorderSize * 2) / self.theScale
        bsy = (paperSizeY + self.theBoardBorderSize * 2) / self.theScale
        bsz = self.theBoardH / self.theScale
        board = self.std.drawBox(bsx, bsy, bsz)
        board.translate(-bsx / 2, -bsy / 2, -psz - bsz)
        board.setMaterial(self.theBoardMaterial)
        ret.add(board)

        ret.add(self.drawInfoLabel(gp_Pnt(-bsx / 2, -bsy / 2, -psz), self.theScaleText))

        dx = (paperSizeX / 2 - self.thePinOffset) / self.theScale
        dy = (paperSizeY / 2 - self.thePinOffset) / self.theScale
        ret.add(self.drawPin(-dx, -dy))
        ret.add(self.drawPin(dx, -dy))
        ret.add(self.drawPin(dx, dy))
        ret.add(self.drawPin(-dx, dy))

        return ret

    def drawBounds(self, pnt1, pnt2):
        x1, y1, z1 = pnt1.X(), pnt1.Y(), pnt1.Z()
        x2, y2, z2 = pnt2.X(), pnt2.Y(), pnt2.Z()

        ret = self.std.drawGroup()

        ret.add(self.drawInfoLine(gp_Pnt(x1, y1, z1), gp_Pnt(x1, y2, z1)))
        ret.add(self.drawInfoLine(gp_Pnt(x1, y2, z1), gp_Pnt(x2, y2, z1)))
        ret.add(self.drawInfoLine(gp_Pnt(x2, y2, z1), gp_Pnt(x2, y1, z1)))
        ret.add(self.drawInfoLine(gp_Pnt(x2, y1, z1), gp_Pnt(x1, y1, z1)))

        ret.add(self.drawInfoLine(gp_Pnt(x1, y1, z1), gp_Pnt(x1, y1, z2)))
        ret.add(self.drawInfoLine(gp_Pnt(x1, y2, z1), gp_Pnt(x1, y2, z2)))
        ret.add(self.drawInfoLine(gp_Pnt(x2, y1, z1), gp_Pnt(x2, y1, z2)))
        ret.add(self.drawInfoLine(gp_Pnt(x2, y2, z1), gp_Pnt(x2, y2, z2)))

        ret.add(self.drawInfoLine(gp_Pnt(x1, y1, z2), gp_Pnt(x1, y2, z2)))
        ret.add(self.drawInfoLine(gp_Pnt(x1, y2, z2), gp_Pnt(x2, y2, z2)))
        ret.add(self.drawInfoLine(gp_Pnt(x2, y2, z2), gp_Pnt(x2, y1, z2)))
        ret.add(self.drawInfoLine(gp_Pnt(x2, y1, z2), gp_Pnt(x1, y1, z2)))

        return ret

    def drawAxis(self, size, step):
        ret = self.std.drawGroup()

        ret.add(self.drawInfoVector(gp_Pnt(0, 0, 0), gp_Pnt(size, 0, 0)))
        ret.add(self.drawInfoVector(gp_Pnt(0, 0, 0), gp_Pnt(0, size, 0)))
        ret.add(self.drawInfoVector(gp_Pnt(0, 0, 0), gp_Pnt(0, 0, size)))
        ret.add(self.drawInfoLabel(gp_Pnt(size, 0, 0), 'X'))
        ret.add(self.drawInfoLabel(gp_Pnt(0, size, 0), 'Y'))
        ret.add(self.drawInfoLabel(gp_Pnt(0, 0, size), 'Z'))

        ret.add(self.drawInfoPoint(gp_Pnt(0, 0, 0)))
        cnt = size // step
        for i in range(1, cnt - 1):
            d = i * step
            ret.add(self.drawInfoPoint(gp_Pnt(d, 0, 0)))
            ret.add(self.drawInfoPoint(gp_Pnt(0, d, 0)))
            ret.add(self.drawInfoPoint(gp_Pnt(0, 0, d)))

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
    demoScene.dump()

    screen = ScreenRenderLib()
    screen.renderScene(demoScene)
