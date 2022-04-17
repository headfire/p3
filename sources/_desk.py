from _std import DrawLib, StdDrawLib, ScreenRenderLib

from OCC.Core.gp import gp_Pnt, gp_Vec


DESK_INIT_HINTS = {

    'scale': 1 / 1,
    'scaleText': 'A0 M1:1',

    'boardMaterial': ((208, 117, 28), 0, 'PLASTIC'),
    'paperMaterial': ((230, 230, 230), 0, 'PLASTIC'),
    'pinMaterial': ((100, 100, 100), 0, 'CHROME'),
    'infoMaterial': ((100, 100, 100), 50, 'PLASTIC'),

    'paperSizes': (1189, 841, 1),  # A0

    'boardH': 20,
    'boardBorderSize': 60,

    'pinOffset': 30,
    'pinR': 10,
    'pinH': 2,

    'infoLineWidth': 6,
    'mainLineWidth': 8,

    'pointRFactor': 3,
    'arrowRFactor': 3,
    'arrowHFactor': 15,

    'infoLabelSizePx': 20,  # not scaled
    'infoLabelDelta': 15

}


class DeskDrawLib(DrawLib):

    def __init__(self):
        super().__init__()
        self.std = StdDrawLib()
        self.initHints(DESK_INIT_HINTS)

    # ***************************

    def getPoint(self, pnt, baseLineR):

        scale = self.getHint('scale')
        pointWidthFactor = self.getHint('pointRFactor')

        pointR = baseLineR * pointWidthFactor / scale
        ret = self.std.getSphere(pnt, pointR)

        return ret

    def getLine(self, pnt1, pnt2, baseLineR):

        scale = self.getHint('scale')

        lineR = baseLineR / scale
        vec = gp_Vec(pnt1, pnt2)
        ret = self.std.getCylinder(lineR, vec.Magnitude())
        ret.fromPointToPoint(pnt1, pnt2)

        return ret

    def getVector(self, pnt1, pnt2, baseLineR):

        scale = self.getHint('scale')
        arrowRFactor = self.getHint('arrowRFactor')
        arrowHFactor = self.getHint('arrowHFactor')

        rArrow = baseLineR * arrowRFactor / scale
        hArrow = baseLineR * arrowHFactor / scale
        v = gp_Vec(pnt1, pnt2)
        vLen = v.Magnitude()
        v *= (vLen - hArrow) / vLen
        pntM = pnt1.Translated(v)

        ret = self.std.getGroup()

        line = self.getInfoLine(pnt1, pntM)
        ret.add(line)

        arrow = self.std.getCone(rArrow, 0, hArrow)
        arrow.fromPointToPoint(pntM, pnt2)
        ret.add(arrow)

        return ret

    # **************************************

    def getInfoLabel(self, pnt, text):

        scale = self.getHint('scale')
        infoMaterial = self.getHint('infoMaterial')
        infoLabelDelta = self.getHint('infoLabelDelta')
        infoLabelSizePx = self.getHint('infoLabelSizePx')  # not scaled

        delta = infoLabelDelta / scale
        ret = self.std.getLabel(pnt, text, infoLabelSizePx)
        ret.translate(delta, delta, delta)
        ret.setMaterial(infoMaterial)
        return ret

    def getInfoPoint(self, pnt):

        infoMaterial = self.getHint('infoMaterial')
        infoLineWidth = self.getHint('infoLineWidth')

        ret = self.getPoint(pnt, infoLineWidth/2)
        ret.setMaterial(infoMaterial)

        return ret

    def getInfoLine(self, pnt1, pnt2):

        infoMaterial = self.getHint('infoMaterial')
        infoLineWidth = self.getHint('infoLineWidth')

        ret = self.getLine(pnt1, pnt2, infoLineWidth/2)
        ret.setMaterial(infoMaterial)
        return ret

    def getInfoVector(self, pnt1, pnt2):
        infoMaterial = self.getHint('infoMaterial')
        infoLineWidth = self.getHint('infoLineWidth')

        ret = self.getVector(pnt1, pnt2, infoLineWidth/2)
        ret.setMaterial(infoMaterial)

        return ret

        # **************************************

    def getPin(self, x, y):

        scale = self.getHint('scale')
        pinMaterial = self.getHint('pinMaterial')
        pinR = self.getHint('pinR')
        pinH = self.getHint('pinH')
        pinZ = 0

        pin = self.std.getCylinder(pinR/scale, pinH/scale)
        pin.translate(x, y, pinZ)
        pin.setMaterial(pinMaterial)

        return pin

    def getDesk(self):
        
        scale = self.getHint('scale')
        scaleText = self.getHint('scaleText')
        boardMaterial = self.getHint('boardMaterial')
        paperMaterial = self.getHint('paperMaterial')
        paperSizeX, paperSizeY, paperSizeZ = self.getHint('paperSizes')
        boardBorderSize = self.getHint('boardBorderSize')
        boardH = self.getHint('boardH')
        pinOffset = self.getHint('pinOffset')

        ret = self.std.getGroup()

        psx, psy, psz = paperSizeX/scale, paperSizeY/scale, paperSizeZ/scale
        paper = self.std.getBox(psx, psy, psz)
        paper.translate(-psx / 2, -psy / 2, -psz)
        paper.setMaterial(paperMaterial)
        ret.add(paper)

        bsx = (paperSizeX + boardBorderSize * 2) / scale
        bsy = (paperSizeY + boardBorderSize * 2) / scale
        bsz = boardH / scale
        board = self.std.getBox(bsx, bsy, bsz)
        board.translate(-bsx / 2, -bsy / 2, -psz - bsz)
        board.setMaterial(boardMaterial)
        ret.add(board)

        ret.add(self.getInfoLabel(gp_Pnt(-bsx / 2, -bsy / 2, -psz), scaleText))

        dx = (paperSizeX / 2 - pinOffset) / scale
        dy = (paperSizeY / 2 - pinOffset) / scale
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
    deskLib.setHint('scaleText', 'A0 M5:1')
    deskLib.setHint('scale', 5 / 1)
    demo = deskLib.getDemo()
    # demo.dump()

    screen = ScreenRenderLib()
    screen.render(demo)
