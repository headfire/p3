# OpenCascade tutorial by headfire (headfire@yandex.ru)
# point and line attributes

EQUAL_POINTS_PRECISION = 0.001

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
        'CnopStyle': ((100,100,100),0,'CHROME') }

class DeskLib:
 
    def __init__(self, boundPnt1, boundPnt2):
        self.std = StandartLib()  
        self.boundPnt1, self.boundPnt2 = boundPnt1,boundPnt2
        self.scaleStr, self.scaleK = self._getFitScale()
        print(self.scaleStr, self.scaleK)
        
    def _getFitScale(self): 
        x1,y1 = self.boundPnt1.X(),self.boundPnt1.Y()
        x2,y2 = self.boundPnt2.X(),self.boundPnt2.Y()
        draftXScale = (x2-x1)/PAPER_SIZE_X
        draftYScale = (y2-y1)/PAPER_SIZE_Y
        draftScale = max(draftXScale, draftYScale)
        print('draftXScale',draftXScale)    
        print('draftYScale',draftYScale)    
        print('draftScale',draftXScale)    

        scales = dict()
        for i in (1,2,5):
            for k in (1,10,100,1000,10000):
                scales['1:'+str(i*k)] = (i*k)
                scales[str(i*k)+':1'] = 1/(i*k)

        print(scales)    
        minE = 10   
        minKey = None
        for key in scales:
            if draftScale-scales[key] > 0:
                curE = 1-(draftScale-scales[key])/scales[key]
                print(key,curE)
                if curE < minE:
                    minE = curE
                    minKey = key
        minKey = '5:1'
        #todo
        return minKey, scales[minKey]
        
    def getStyles(self): 
        return STYLES

    def getDesk(self):
    
        zLevel = self.boundPnt1.Z()        
        xOffset = self.boundPnt1.X() #todo        
        yOffset = self.boundPnt1.Z() #todo       
        
        desk = self.std.getGroup()
        k = self.scaleK
        psx, psy, psz = PAPER_SIZE_X*k, PAPER_SIZE_Y*k, PAPER_SIZE_Z*k;
               
        paper = self.std.getBox(gp_Pnt(-psx/2, -psy/2, zLevel-psz), gp_Pnt(psx/2, psy/2, zLevel))
        paper.setStyle('PaperStyle')
        desk.add(paper)
        
        zLevel-=psz

        bsx, bsy, bsz = (PAPER_SIZE_X+BOARD_BORDER_SIZE*2)*k, (PAPER_SIZE_Y+BOARD_BORDER_SIZE*2)*k, BOARD_SIZE_Z*k;
        board = self.std.getBox(gp_Pnt(-bsx/2, -bsy/2, zLevel-bsz), gp_Pnt(bsx/2, bsy/2, zLevel))
        board.setStyle('BoardStyle')
        desk.add(board)
        
        scaleLabel = self.std.getLabel(gp_Pnt(-bsx/2, -bsy/2, 0), 'M'+self.scaleStr, 20, 10)
        scaleLabel.setStyle('PaperStyle')
        desk.add(scaleLabel)
        
        dx, dy, r, w = (PAPER_SIZE_X/2-CNOP_OFFSET)*k, (PAPER_SIZE_Y/2-CNOP_OFFSET)*k, CNOP_R*k, CNOP_WIDTH*k, 
        desk.add(self.getCnop(-dx, -dy, zLevel, r, w))
        desk.add(self.getCnop(dx, -dy, zLevel, r, w))
        desk.add(self.getCnop(dx, dy, zLevel, r, w))
        desk.add(self.getCnop(-dx, dy, zLevel, r, w))
        
        return desk;

    def getCnop(self, x, y, z, r, w):
        cnop = self.std.getCylinder(gp_Pnt(x,y,z),gp_Pnt(x,y,z+w), r) 
        cnop.setStyle('CnopStyle')                            
        return cnop

    def getInfoLine(self, pnt1,pnt2):
        line = self.std.getCylinder(pnt1,pnt2, INFO_LINE_R*self.scaleK)
        line.setStyle('InfoStyle')
        return line 
        
    def getBounds(self):
        x1,y1,z1 = self.boundPnt1.X(), self.boundPnt1.Y(), self.boundPnt1.Z()
        x2,y2,z2 = self.boundPnt2.X(), self.boundPnt2.Y(), self.boundPnt2.Z()
        
        bounds = self.std.getGroup()
        bounds.add(self.getInfoLine(gp_Pnt(x1,y1,z1),gp_Pnt(x1,y2,z1)))
        bounds.add(self.getInfoLine(gp_Pnt(x1,y2,z1),gp_Pnt(x2,y2,z1)))
        bounds.add(self.getInfoLine(gp_Pnt(x2,y2,z1),gp_Pnt(x2,y1,z1)))
        bounds.add(self.getInfoLine(gp_Pnt(x2,y1,z1),gp_Pnt(x1,y1,z1)))
       
        bounds.add(self.getInfoLine(gp_Pnt(x1,y1,z1),gp_Pnt(x1,y1,z2)))
        bounds.add(self.getInfoLine(gp_Pnt(x1,y2,z1),gp_Pnt(x1,y2,z2)))
        bounds.add(self.getInfoLine(gp_Pnt(x2,y1,z1),gp_Pnt(x2,y1,z2)))
        bounds.add(self.getInfoLine(gp_Pnt(x2,y2,z1),gp_Pnt(x2,y2,z2)))
     
        bounds.add(self.getInfoLine(gp_Pnt(x1,y1,z2),gp_Pnt(x1,y2,z2)))
        bounds.add(self.getInfoLine(gp_Pnt(x1,y2,z2),gp_Pnt(x2,y2,z2)))
        bounds.add(self.getInfoLine(gp_Pnt(x2,y2,z2),gp_Pnt(x2,y1,z2)))
        bounds.add(self.getInfoLine(gp_Pnt(x2,y1,z2),gp_Pnt(x1,y1,z2)))
       
        bounds.add(self.getInfoLine(gp_Pnt(0,0,0),gp_Pnt(x2,0,0)))
        bounds.add(self.getInfoLine(gp_Pnt(0,0,0),gp_Pnt(0,y2,0)))
        bounds.add(self.getInfoLine(gp_Pnt(0,0,0),gp_Pnt(0,0,z2)))
        
        return bounds 
        
    def getAxis(self):
        return self.std.getFoo()

    def getDemo(self):
    
        demo = self.std.getGroup()
        demo.add(self.getDesk())
        demo.add(self.getBounds())
        demo.add(self.getAxis())
        return demo
         
        '''          
        scale = 1
        dx, dy, dz = 1500*SCALE_K, 1000*SCALE_K, 40*SCALE_K
        paperWidth = 2*SCALE_K     


       
        
        
        getGroup()
        '''
if __name__ == '__main__':
    demo = DeskLib(gp_Pnt(-50,-50,-60), gp_Pnt(50,50,10)).getDemo()
    #print(demo.childs)
    ScreenRenderer(STYLES).render(demo) 


'''
        
            var deskTexture = THREE.ImageUtils.loadTexture( texturePath + 'wood.jpg', undefined, zdeskRender);
            deskTexture.minFilter = THREE.LinearFilter;
            var deskMaterial = new THREE.MeshBasicMaterial( {  map: deskTexture } );
            deskMesh = new THREE.Mesh( deskGeometry, deskMaterial );
            deskMesh.position.set(param.deskDX, param.deskDY, param.deskDZ-22*scale); 
            zdeskScene.add( deskMesh );

            // zdeskXLabel((-1500/2 + 20)*scale + param.deskDX, (1000/2 + 20)*scale + param.deskDY, param.deskDZ, 'A0 M'+zdeskScaleB+':'+zdeskScaleA, 0xbbbbbb);

            
            paperTexture = THREE.ImageUtils.loadTexture(texturePath + 'paper.jpg', undefined, zdeskRender);
            paperTexture.minFilter = THREE.LinearFilter;
            paperTexture.wrapS = THREE.RepeatWrapping;
            paperTexture.wrapT = THREE.RepeatWrapping;
            paperTexture.repeat.set( 4, 4 );
            var paperMaterial = new THREE.MeshBasicMaterial( {  map: paperTexture } );
            paperMesh = new THREE.Mesh( paperGeometry, paperMaterial );
            paperMesh.position.set(param.deskDX, param.deskDY, param.deskDZ-1.9*scale); // not 2 for flat surfaces visible
            zdeskScene.add( paperMesh );
    
            var cnopGeometry = new THREE.CylinderGeometry( 10*scale, 10*scale, 6*scale, 12, 1 );
            var cnopMaterial =  new THREE.MeshLambertMaterial( { color:0x707070 } ); // shading: THREE.FlatShading

            cnopMesh = new THREE.Mesh( cnopGeometry, cnopMaterial );
            cnopMesh.position.set(param.deskDX+564*scale,param.deskDY+390*scale,param.deskDZ+0);
            cnopMesh.rotation.x = Math.PI/2;
            zdeskScene.add( cnopMesh );
            
            cnopMesh = new THREE.Mesh( cnopGeometry, cnopMaterial );
            cnopMesh.position.set(param.deskDX-564*scale,param.deskDX+390*scale,param.deskDZ);
            cnopMesh.rotation.x = Math.PI/2;
            zdeskScene.add( cnopMesh );

            cnopMesh = new THREE.Mesh( cnopGeometry, cnopMaterial );
            cnopMesh.position.set(param.deskDX+564*scale,param.deskDY-390*scale,param.deskDZ);
            cnopMesh.rotation.x = Math.PI/2;
            zdeskScene.add( cnopMesh );

            cnopMesh = new THREE.Mesh( cnopGeometry, cnopMaterial );
            cnopMesh.position.set(param.deskDX-564*scale,param.deskDY-390*scale,param.deskDZ);
            cnopMesh.rotation.x = Math.PI/2;
            zdeskScene.add( cnopMesh );
            
'''
