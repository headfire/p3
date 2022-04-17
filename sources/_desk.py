from _std import StdLib, ScreenRenderer

from OCC.Core.gp import gp_Pnt,  gp_Vec

PAPER_SIZE_X, PAPER_SIZE_Y, PAPER_SIZE_Z = 1189, 841, 1  # A0
BOARD_BORDER_SIZE, BOARD_SIZE_Z = 60, 20
PIN_OFFSET, PIN_R, PIN_WIDTH = 30, 10, 2
INFO_LINE_R = 3

STYLES = {'BoardStyle': ((208, 117, 28), 0, 'PLASTIC'),
          'PaperStyle': ((230, 230, 230), 0, 'PLASTIC'),
          'InfoStyle': ((100, 100, 100), 50, 'PLASTIC'),
          'ConeStyle': ((50, 200, 50), 0, 'CHROME'),
          'PibStyle': ((100, 100, 100), 0, 'CHROME')
          }


class DeskLib:
 
    def __init__(self, deskLabelText='A0 M1:1', scaleK=1/1):
        self.std = StdLib()
        self.deskLabelText = deskLabelText
        self.scaleK = scaleK
        self.styles = STYLES
        
    def getStyles(self): 
        return self.styles

    # ***************************

    def getPoint(self, pnt, rLine):
        ret = self.std.getSphere(pnt, rLine*3/self.scaleK)
        return ret 

    def getLine(self, pnt1, pnt2, rLine):
        vec = gp_Vec(pnt1, pnt2)
        ret = self.std.getCylinder(rLine/self.scaleK, vec.Magnitude())
        ret.fromPointToPoint(pnt1, pnt2)   
        return ret        
        
    def getVector(self, pnt1, pnt2, rLine):
        
        rArrow = rLine*3/self.scaleK
        hArrow = rLine*15/self.scaleK
        
        v = gp_Vec(pnt1, pnt2)
        vLen = v.Magnitude()
        v *= (vLen-hArrow)/vLen
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
        ret = self.std.getLabel(pnt, text, 20)
        ret.translate(5, 5, 5)
        ret.setStyle('InfoStyle')
        return ret

    def getInfoPoint(self, pnt):
        ret = self.getPoint(pnt, INFO_LINE_R)
        ret.setStyle('InfoStyle')
        return ret 

    def getInfoLine(self, pnt1, pnt2):
        ret = self.getLine(pnt1, pnt2, INFO_LINE_R)
        ret.setStyle('InfoStyle')
        return ret 

    def getInfoVector(self, pnt1, pnt2):
        
        ret = self.getVector(pnt1, pnt2, INFO_LINE_R)
        ret.setStyle('InfoStyle')
        
        return ret 

    # **************************************

    def getPin(self, x, y, z, r, w):
        pin = self.std.getCylinder(r, w)
        pin.translate(x, y, z)
        pin.setStyle('PinStyle')
        return pin
    
    def getDesk(self):

        k = self.scaleK
 
        ret = self.std.getGroup()
 
        psx, psy, psz = PAPER_SIZE_X/k, PAPER_SIZE_Y/k, PAPER_SIZE_Z/k
        paper = self.std.getBox(psx, psy, psz)
        paper.translate(-psx/2, -psy/2, -psz)
        paper.setStyle('PaperStyle')
        ret.add(paper)
        
        bsx = (PAPER_SIZE_X+BOARD_BORDER_SIZE*2)/k
        bsy = (PAPER_SIZE_Y+BOARD_BORDER_SIZE*2)/k
        bsz = BOARD_SIZE_Z/k
        board = self.std.getBox(bsx, bsy, bsz)
        board.translate(-bsx/2, -bsy/2, -psz-bsz)
        board.setStyle('BoardStyle')
        ret.add(board)
    
        ret.add(self.getInfoLabel(gp_Pnt(-bsx/2, -bsy/2, -psz), self.deskLabelText))
        
        dx, dy, r, w = (PAPER_SIZE_X/2-PIN_OFFSET)/k, (PAPER_SIZE_Y/2-PIN_OFFSET)/k, PIN_R/k, PIN_WIDTH/k,
        ret.add(self.getPin(-dx, -dy, 0, r, w))
        ret.add(self.getPin(dx, -dy, 0, r, w))
        ret.add(self.getPin(dx, dy, 0, r, w))
        ret.add(self.getPin(-dx, dy, 0, r, w))
        
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
        cnt = size//step
        for i in range(1, cnt-1):
            d = i*step
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
        cone.setStyle('ConeStyle')
        ret.add(cone)
        
        return ret
    
    
if __name__ == '__main__':

    drawLib = DeskLib('A0 M5:1', 5/1)
    demo = drawLib.getDemo()
    styles = drawLib.getStyles()

    rend = ScreenRenderer()
    rend.render(demo, styles) 
