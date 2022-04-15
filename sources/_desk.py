# OpenCascade tutorial by headfire (headfire@yandex.ru)
# point and line attributes

EQUAL_POINTS_PRECISION = 0.001


from _scene import *

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

BOUNDS = -50,-50, 10, 50,50, 100
A0 = 1189, 841


POINT_RADIUS = 2

STYLES =  { 'TableStyle': ((208,117,28),0,'PLASTIC'),   
            'PaperStyle': ((230,230,230),0,'PLASTIC'), 
            'InfoStyle': ((100,100,100),50,'PLASTIC'), 
            'CnopStyle': ((100,100,100),0,'CHROME') }  

def DEF_SCALE(bounds, a0): 

    x1,y1,z1, x2,y2,z2 = bounds
    xSize, ySize = A0
    draftXScale = (x2-x1)/xSize
    draftYScale = (y2-y1)/ySize
    draftScale = max(draftXScale, draftYScale)
    print(draftScale)    

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
    return minKey, scales[minKey]

SCALE_STR, SCALE_K = DEF_SCALE(BOUNDS, A0) 
INFO_LINE_WIDTH = 5*SCALE_K

def putLine(nm, pnt1, pnt2):
    getCylinder(pnt1, pnt2, INFO_LINE_WIDTH)
    setStyle('InfoStyle')
    put(nm)

def getDesk():
    
    bx1,by1,bz1, bx2,by2,bz2 = BOUNDS
    scale = 1
    dx, dy, dz = 1500*SCALE_K, 1000*SCALE_K, 40*SCALE_K
    paperWidth = 2*SCALE_K     

    getBox(gp_Pnt(-dx/2, -dy/2, -bz2*SCALE_K-dz-paperWidth), gp_Pnt(dx/2, dy/2, -bz2*SCALE_K-paperWidth))
    setStyle('TableStyle')
    put('Table')
    getLabel(gp_Pnt(-dx/2, -dy/2, 0), 'M'+SCALE_STR, 20, 10)
    setStyle('PaperStyle')
    put('ScaleLabel')

    dx, dy, dz = 1189*SCALE_K, 841*SCALE_K, paperWidth;
           
    getBox(gp_Pnt(-dx/2, -dy/2, -dz), gp_Pnt(dx/2, dy/2, 0))
    setStyle('PaperStyle')
    put('Paper')
   
    dx, dy = (1189-40)*SCALE_K/2, (841-40)*SCALE_K/2
    cr = 10*SCALE_K
    cw = 2*SCALE_K
    i = 0
    for x in (-dx,+dx):
        for y in (-dy,+dy):
            getCylinder(gp_Pnt(x,y,0),gp_Pnt(x,y,2*SCALE_K), cr)
            setStyle('CnopStyle')
            put('Cnop'+str(i))
            i += 1 
    
    x1,y1,z1, x2,y2,z2 = BOUNDS
    putLine('L1',gp_Pnt(x1,y1,z1),gp_Pnt(x1,y2,z1))
    putLine('L2',gp_Pnt(x1,y2,z1),gp_Pnt(x2,y2,z1))
    putLine('L3',gp_Pnt(x2,y2,z1),gp_Pnt(x2,y1,z1))
    putLine('L4',gp_Pnt(x2,y1,z1),gp_Pnt(x1,y1,z1))
   
    putLine('L5',gp_Pnt(x1,y1,z1),gp_Pnt(x1,y1,z2))
    putLine('L6',gp_Pnt(x1,y2,z1),gp_Pnt(x1,y2,z2))
    putLine('L7',gp_Pnt(x2,y1,z1),gp_Pnt(x2,y1,z2))
    putLine('L8',gp_Pnt(x2,y2,z1),gp_Pnt(x2,y2,z2))
 
    putLine('L9',gp_Pnt(x1,y1,z2),gp_Pnt(x1,y2,z2))
    putLine('L10',gp_Pnt(x1,y2,z2),gp_Pnt(x2,y2,z2))
    putLine('L11',gp_Pnt(x2,y2,z2),gp_Pnt(x2,y1,z2))
    putLine('L12',gp_Pnt(x2,y1,z2),gp_Pnt(x1,y1,z2))
   
    putLine('oX',gp_Pnt(0,0,0),gp_Pnt(x2,0,0))
    putLine('oY',gp_Pnt(0,0,0),gp_Pnt(0,y2,0))
    putLine('oZ',gp_Pnt(0,0,0),gp_Pnt(0,0,z2))
    
    getGroup()


sceneInit()

getDesk()
put('Desk')

sceneRender('slide', STYLES)

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
