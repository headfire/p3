from _std import DrawLib, StdDrawLib, ScreenRenderLib

from OCC.Core.gp import gp_Pnt, gp_Vec

DESK_INIT_HINTS = {

}


class DeskDrawLib(DrawLib):

    def __init__(self):
        super().__init__()
        self.std = StdDrawLib()

        self.theScale = 1 / 1
        self.theScaleText = 'A0 M1:1'

        self.theBoardMaterial = ((208, 117, 28), 0, 'PLASTIC')
        self.thePaperMaterial = ((230, 230, 230), 0, 'PLASTIC')
        self.thePinMaterial = ((100, 100, 100), 0, 'CHROME')
        self.theInfoMaterial = ((100, 100, 100), 50, 'PLASTIC')

        self.thePaperSizes = (1189, 841, 1)  # A0

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

    def getPoint(self, aPnt, aBaseLineR):
        pointR = aBaseLineR * self.thePointRFactor / self.theScale
        ret = self.std.getSphere(aPnt, pointR)
        return ret

    def getLine(self, pnt1, pnt2, baseLineR):
        scale = self.theScale

        lineR = baseLineR / scale
        vec = gp_Vec(pnt1, pnt2)
        ret = self.std.getCylinder(lineR, vec.Magnitude())
        ret.fromPointToPoint(pnt1, pnt2)

        return ret

    def getVector(self, aPnt1, aPnt2, aBaseLineR):

        rArrow = aBaseLineR * self.theArrowRFactor / self.theScale
        hArrow = aBaseLineR * self.theArrowHFactor / self.theScale
        v = gp_Vec(aPnt1, aPnt2)
        vLen = v.Magnitude()
        v *= (vLen - hArrow) / vLen
        pntM = aPnt1.Translated(v)

        ret = self.std.getGroup()

        line = self.getInfoLine(aPnt1, pntM)
        ret.add(line)

        arrow = self.std.getCone(rArrow, 0, hArrow)
        arrow.fromPointToPoint(pntM, aPnt2)
        ret.add(arrow)

        return ret

    # **************************************

    def getInfoLabel(self, aPnt, aText):

        delta = self.theInfoLabelDelta / self.theScale

        ret = self.std.getLabel(aPnt, aText, self.theInfoLabelSizePx)
        ret.translate(delta, delta, delta)
        ret.setMaterial(self.theInfoMaterial)

        return ret

    def getInfoPoint(self, aPnt):

        ret = self.getPoint(aPnt, self.theInfoLineWidth / 2)
        ret.setMaterial(self.theInfoMaterial)

        return ret

    def getInfoLine(self, aPnt1, aPnt2):

        ret = self.getLine(aPnt1, aPnt2, self.theInfoLineWidth / 2)
        ret.setMaterial(self.theInfoMaterial)

        return ret

    def getInfoVector(self, aPnt1, aPnt2):

        ret = self.getVector(aPnt1, aPnt2, self.theInfoLineWidth / 2)
        ret.setMaterial(self.theInfoMaterial)

        return ret

        # **************************************

    def getPin(self, x, y):

        pin = self.std.getCylinder(self.thePinR / self.theScale, self.thePinH / self.theScale)
        pin.translate(x, y, 0)
        pin.setMaterial(self.thePinMaterial)

        return pin

    def getDesk(self):








        ret = self.std.getGroup()

        paperSizeX, paperSizeY, paperSizeZ = self.thePaperSizes
        psx, psy, psz = paperSizeX / self.theScale, paperSizeY / self.theScale, paperSizeZ / self.theScale
        paper = self.std.getBox(psx, psy, psz)
        paper.translate(-psx / 2, -psy / 2, -psz)
        paper.setMaterial(self.thePaperMaterial)
        ret.add(paper)

        bsx = (paperSizeX + self.theBoardBorderSize * 2) / self.theScale
        bsy = (paperSizeY + self.theBoardBorderSize * 2) / self.theScale
        bsz = self.theBoardH / self.theScale
        board = self.std.getBox(bsx, bsy, bsz)
        board.translate(-bsx / 2, -bsy / 2, -psz - bsz)
        board.setMaterial(self.theBoardMaterial)
        ret.add(board)

        ret.add(self.getInfoLabel(gp_Pnt(-bsx / 2, -bsy / 2, -psz), self.theScaleText))

        dx = (paperSizeX / 2 - self.thePinOffset) / self.theScale
        dy = (paperSizeY / 2 - self.thePinOffset) / self.theScale
        ret.add(self.getPin(-dx, -dy))
        ret.add(self.getPin(dx, -dy))
        ret.add(self.getPin(dx, dy))
        ret.add(self.getPin(-dx, dy))

        return ret

    def getBounds(self, pnt1, pnt2):

        x1, y1, z1 = pnt1.X(), pnt1.Y(), pnt1.Z()
        x2, y2, z2 = pnt2.X(), pnt2.Y(), pnt2.Z()

        ret = self.std.getGroup()

        ret.add(self.getInfoLine(gp_Pnt(x1, y1, z1), gp_Pnt(x1, y2, z1)))
        ret.add(self.getInfoLine(gp_Pnt(x1, y2, z1), gp_Pnt(x2, y2, z1)))
        ret.add(self.getInfoLine(gp_Pnt(x2, y2, z1), gp_Pnt(x2, y1, z1)))
        ret.add(self.getInfoLine(gp_Pnt(x2, y1, z1), gp_Pnt(x1, y1, z1)))

        ret.add(self.getInfoLine(gp_Pnt(x1, y1, z1), gp_Pnt(x1, y1, z2)))
        ret.add(self.getInfoLine(gp_Pnt(x1, y2, z1), gp_Pnt(x1, y2, z2)))
        ret.add(self.getInfoLine(gp_Pnt(x2, y1, z1), gp_Pnt(x2, y1, z2)))
        ret.add(self.getInfoLine(gp_Pnt(x2, y2, z1), gp_Pnt(x2, y2, z2)))

        ret.add(self.getInfoLine(gp_Pnt(x1, y1, z2), gp_Pnt(x1, y2, z2)))
        ret.add(self.getInfoLine(gp_Pnt(x1, y2, z2), gp_Pnt(x2, y2, z2)))
        ret.add(self.getInfoLine(gp_Pnt(x2, y2, z2), gp_Pnt(x2, y1, z2)))
        ret.add(self.getInfoLine(gp_Pnt(x2, y1, z2), gp_Pnt(x1, y1, z2)))

        return ret

    def getAxis(self, size, step):

        ret = self.std.getGroup()

        ret.add(self.getInfoVector(gp_Pnt(0, 0, 0), gp_Pnt(size, 0, 0)))
        ret.add(self.getInfoVector(gp_Pnt(0, 0, 0), gp_Pnt(0, size, 0)))
        ret.add(self.getInfoVector(gp_Pnt(0, 0, 0), gp_Pnt(0, 0, size)))
        ret.add(self.getInfoLabel(gp_Pnt(size, 0, 0), 'X'))
        ret.add(self.getInfoLabel(gp_Pnt(0, size, 0), 'Y'))
        ret.add(self.getInfoLabel(gp_Pnt(0, 0, size), 'Z'))

        ret.add(self.getInfoPoint(gp_Pnt(0, 0, 0)))
        cnt = size // step
        for i in range(1, cnt - 1):
            d = i * step
            ret.add(self.getInfoPoint(gp_Pnt(d, 0, 0)))
            ret.add(self.getInfoPoint(gp_Pnt(0, d, 0)))
            ret.add(self.getInfoPoint(gp_Pnt(0, 0, d)))

        return ret

    # **************************************

    def getDemo(self):

        ret = self.std.getGroup()

        desk = self.getDesk()
        desk.translate(0, 0, -60)
        ret.add(desk)

        bounds = self.getBounds(gp_Pnt(-50, -50, -50), gp_Pnt(50, 50, 20))
        ret.add(bounds)

        axis = self.getAxis(50, 10)
        ret.add(axis)

        cone = self.std.getCone(30, 0, 100)
        cone.translate(0, 0, -50)
        cone.setMaterial(((50, 200, 50), 0, 'CHROME'))
        ret.add(cone)

        return ret


if __name__ == '__main__':

    deskLib = DeskDrawLib()
    deskLib.theScaleText = 'A0 M5:1'
    deskLib.theScale = 5 / 1
    demo = deskLib.getDemo()
    # demo.dump()

    screen = ScreenRenderLib()
    screen.render(demo)
