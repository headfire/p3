# OpenCascade tutorial by headfire (headfire@yandex.ru)
# point and line attributes

from _standart import StandartLib, ScreenRenderer

from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Dir, gp_Vec, gp_Ax1, gp_Ax2, gp_GTrsf, gp_OZ
from OCC.Core.Geom import Geom_TrimmedCurve
from OCC.Core.GeomAPI import GeomAPI_IntCS
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import  TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX

from OCC.Core.GC import GC_MakeArcOfCircle, GC_MakeCircle

from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepBuilderAPI import  (BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire,
             BRepBuilderAPI_Transform, BRepBuilderAPI_GTransform, BRepBuilderAPI_MakeFace,  BRepBuilderAPI_MakeVertex)
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakeOffset, BRepOffsetAPI_ThruSections
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Common, BRepAlgoAPI_Cut

from math import pi

PAPER_SIZE_X, PAPER_SIZE_Y, PAPER_SIZE_Z = 1189, 841, 1 #A0
BOARD_BORDER_SIZE, BOARD_SIZE_Z = 60, 20
CNOP_OFFSET, CNOP_R, CNOP_WIDTH = 30, 10, 2
INFO_LINE_R = 3

STYLES =  { 'BoardStyle': ((208,117,28),0,'PLASTIC'),   
        'PaperStyle': ((230,230,230),0,'PLASTIC'), 
        'InfoStyle': ((100,100,100),50,'PLASTIC'), 
        'YellowStyle': ((50,200,50),0,'CHROME'), 
        'CnopStyle': ((100,100,100),0,'CHROME') }

class DeskLib():
 
    def __init__(self, deskLabelText = 'A0 M1:1', scaleK = 1/1):
        self.std = StandartLib()  
        self.deskLabelText = deskLabelText
        self.scaleK = scaleK
        
    def getStyles(self): 
        return STYLES

    #*************************** 

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
        
        pnt = gp_Vec(pnt1, pnt2)
        vec = gp_Vec(pnt1, pnt2)
        len = vec.Magnitude()
        vec *= (len-hArrow)/len
        pntM = pnt1.Translated(vec)
        
        ret = self.std.getGroup()

        line = self.getInfoLine(pnt1, pntM)
        ret.add(line)
        
        arrow = self.std.getCone(rArrow,0,hArrow)
        arrow.fromPointToPoint(pntM,pnt2)
        ret.add(arrow)
        
        return ret 

    #**************************************
    
    def getInfoLabel(self, pnt, text):
        ret = self.std.getLabel(pnt, text, 20)
        ret.translate(5,5,5)
        ret.setStyle('InfoStyle')
        return ret

    def getInfoPoint(self, pnt):
        ret = self.getPoint(pnt, INFO_LINE_R)
        ret.setStyle('InfoStyle')
        return ret 

    def getInfoLine(self, pnt1,pnt2):
        ret = self.getLine(pnt1, pnt2, INFO_LINE_R)
        ret.setStyle('InfoStyle')
        return ret 

    def getInfoVector(self, pnt1, pnt2):
        
        ret = self.getVector(pnt1, pnt2, INFO_LINE_R)
        ret.setStyle('InfoStyle')
        
        return ret 

    #**************************************

    def getCnop(self, x, y, z, r, w):
        cnop = self.std.getCylinder(r, w)
        cnop.translate(x, y, z)        
        cnop.setStyle('CnopStyle')                            
        return cnop
    
    def getDesk(self):
    
            
        k = self.scaleK
 
        ret = self.std.getGroup()
 
        psx, psy, psz = PAPER_SIZE_X/k, PAPER_SIZE_Y/k, PAPER_SIZE_Z/k;
        paper = self.std.getBox(psx, psy, psz)
        paper.translate(-psx/2, -psy/2, -psz)
        paper.setStyle('PaperStyle')
        ret.add(paper)
        
        bsx, bsy, bsz = (PAPER_SIZE_X+BOARD_BORDER_SIZE*2)/k, (PAPER_SIZE_Y+BOARD_BORDER_SIZE*2)/k, BOARD_SIZE_Z/k;
        board = self.std.getBox(bsx, bsy, bsz)
        board.translate(-bsx/2, -bsy/2, -psz-bsz)
        board.setStyle('BoardStyle')
        ret.add(board)
    
        ret.add(self.getInfoLabel(gp_Pnt(-bsx/2, -bsy/2, -psz), self.deskLabelText))
        
        dx, dy, r, w = (PAPER_SIZE_X/2-CNOP_OFFSET)/k, (PAPER_SIZE_Y/2-CNOP_OFFSET)/k, CNOP_R/k, CNOP_WIDTH/k, 
        ret.add(self.getCnop(-dx, -dy, 0 ,r, w))
        ret.add(self.getCnop(dx, -dy, 0, r, w))
        ret.add(self.getCnop(dx, dy, 0, r, w))
        ret.add(self.getCnop(-dx, dy, 0, r, w))
        
        return ret;

    
  
    def getBounds(self, pnt1, pnt2):
    
        x1,y1,z1 = pnt1.X(), pnt1.Y(), pnt1.Z()
        x2,y2,z2 = pnt2.X(), pnt2.Y(), pnt2.Z()
        
        ret = self.std.getGroup()
        
        ret.add(self.getInfoLine(gp_Pnt(x1,y1,z1),gp_Pnt(x1,y2,z1)))
        ret.add(self.getInfoLine(gp_Pnt(x1,y2,z1),gp_Pnt(x2,y2,z1)))
        ret.add(self.getInfoLine(gp_Pnt(x2,y2,z1),gp_Pnt(x2,y1,z1)))
        ret.add(self.getInfoLine(gp_Pnt(x2,y1,z1),gp_Pnt(x1,y1,z1)))
       
        ret.add(self.getInfoLine(gp_Pnt(x1,y1,z1),gp_Pnt(x1,y1,z2)))
        ret.add(self.getInfoLine(gp_Pnt(x1,y2,z1),gp_Pnt(x1,y2,z2)))
        ret.add(self.getInfoLine(gp_Pnt(x2,y1,z1),gp_Pnt(x2,y1,z2)))
        ret.add(self.getInfoLine(gp_Pnt(x2,y2,z1),gp_Pnt(x2,y2,z2)))
     
        ret.add(self.getInfoLine(gp_Pnt(x1,y1,z2),gp_Pnt(x1,y2,z2)))
        ret.add(self.getInfoLine(gp_Pnt(x1,y2,z2),gp_Pnt(x2,y2,z2)))
        ret.add(self.getInfoLine(gp_Pnt(x2,y2,z2),gp_Pnt(x2,y1,z2)))
        ret.add(self.getInfoLine(gp_Pnt(x2,y1,z2),gp_Pnt(x1,y1,z2)))
        
        return ret 
        
    def getAxis(self, size, step):
       
        ret = self.std.getGroup()
        ret.add(self.getInfoVector(gp_Pnt(0,0,0),gp_Pnt(size,0,0)))
        ret.add(self.getInfoVector(gp_Pnt(0,0,0),gp_Pnt(0,size,0)))
        ret.add(self.getInfoVector(gp_Pnt(0,0,0),gp_Pnt(0,0,size)))
        ret.add(self.getInfoLabel(gp_Pnt(size,0,0),'X'))
        ret.add(self.getInfoLabel(gp_Pnt(0,size,0),'Y'))
        ret.add(self.getInfoLabel(gp_Pnt(0,0,size),'Z'))
        
        ret.add(self.getInfoPoint(gp_Pnt(0,0,0)))
        cnt = size//step
        for i in range(1,cnt-1):
            d = i*step
            ret.add(self.getInfoPoint(gp_Pnt(d,0,0)))
            ret.add(self.getInfoPoint(gp_Pnt(0,d,0)))
            ret.add(self.getInfoPoint(gp_Pnt(0,0,d)))
            
        return ret

    #**************************************
    
    def getDemo(self):
    
        ret = self.std.getGroup()

        desk = self.getDesk()
        desk.translate(0,0,0)
        ret.add(desk)
 
        bounds = self.getBounds(gp_Pnt(-50,-50,-50),gp_Pnt(50,50,20))
        #ret.add(bounds)
        
        #axis = self.getAxis(50, 10)
        #ret.add(axis)
        
        cone = self.std.getCone(30,0,100)
        cone.setStyle('YellowStyle')
        ret.add(cone)
        
        return ret
    
    
if __name__ == '__main__':
    drawLib = DeskLib('A0 M5:1', 5/1)
    demo = drawLib.getDemo()
    styles = drawLib.getStyles()
    rend = ScreenRenderer() 
    rend.render(demo, styles) 
