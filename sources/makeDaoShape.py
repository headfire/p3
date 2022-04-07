# OpenCascade tutorial by headfire (headfire@yandex.ru)
# point and line attributes


from scene import Scene

from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Dir, gp_Vec, gp_Ax1, gp_Ax2, gp_GTrsf
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

def getXYZ(gpPnt):
    return (gpPnt.X(), gpPnt.Y(), gpPnt.Z())


def getPntExistInPnts(pnts, pntToFind):
    for pnt in pnts:
        if pnt.IsEqual(pntToFind, 0.001):
            return True
    return False    

def getPntsUni(pnts) :
    pntsUni = []
    for pnt in pnts:
      if not getPntExistInPnts(pntsUni, pnt):
         pntsUni += [pnt]      
    return pntsUni     

def getPntRotate(pCenter,  p,  angle):
   ax = gp_Ax1(pCenter, gp_Dir(0,0,1))
   pnt = gp_Pnt(p.XYZ())
   pnt.Rotate(ax, angle)
   return pnt

def getPntScale(pCenter,  p, scale):
   pnt = gp_Pnt(p.XYZ())
   pnt.Scale(pCenter, scale)
   return pnt

def getPntTranslate(p, dx, dy, dz):
   pnt = gp_Pnt(p.XYZ())
   pnt.Translate(gp_Vec(dx,dy,dz))
   return pnt

def getAngle(gpPnt0, gpPnt1, gpPnt2 ):
    v1 = gp_Vec(gpPnt0, gpPnt1)
    v2 = gp_Vec(gpPnt0, gpPnt2)
    return v2.AngleWithRef(v1, gp_Vec(0,0,1))

def getShapeItems(shape, topoType):
   items = [] 
   ex = TopExp_Explorer(shape, topoType)
   while ex.More():
       items.append(ex.Current())
       ex.Next()
   return items


def getPntsFromVertexes(vertexes):
    pnts = []
    for v in vertexes:
        pnts += [BRep_Tool.Pnt(v)] 
    return pnts    
        
def getPntsOfShape(shape):
    vertexes = getShapeItems(shape, TopAbs_VERTEX)
    pnts = getPntsFromVertexes(vertexes)
    return getPntsUni(pnts)
  

def getShapeOffset(shape, offset):
    tool = BRepOffsetAPI_MakeOffset()
    tool.AddWire(shape)
    tool.Perform(offset)
    shape = tool.Shape()  
    return shape

def getShapeMirror(shape, p0):
    transform = gp_Trsf()
    transform.SetMirror(gp_Pnt(0,0,0))
    shape =  BRepBuilderAPI_Transform(shape, transform).Shape()
    return shape

def getPntSectionUp(pnt1, pnt2):
    v1 = gp_Vec(pnt1, pnt2)
    v1.Scale(0.5)
    v2 = gp_Vec(0,0,v1.Magnitude())
    pnt = gp_Pnt(pnt1.XYZ())
    pnt.Translate(v1)
    pnt.Translate(v2)
    return pnt

def getFacePlane(pnt1, pnt2, h):
    
    x1, y1, z1 = getXYZ(pnt1)
    x2, y2, z2 = getXYZ(pnt2)
    pe0 = gp_Pnt(x1, y1, -h)
    pe1 = gp_Pnt(x1, y1, +h)
    pe2 = gp_Pnt(x2, y2, +h)
    pe3 = gp_Pnt(x2, y2, -h)
    
    edge1 = BRepBuilderAPI_MakeEdge(pe0, pe1).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(pe1, pe2).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(pe2, pe3).Edge()
    edge4 = BRepBuilderAPI_MakeEdge(pe3, pe0).Edge()
  
    wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3, edge4).Wire()
    face = BRepBuilderAPI_MakeFace(wire).Face()
    return face

def getPntsCurveSurfaceIntersect(curve, surface):
    pnts = []
    tool = GeomAPI_IntCS(curve, surface)
    pCount = tool.NbPoints();
    for i in range(pCount):
       pnts += [tool.Point(1)]
    return pnts   

def getPntsEdgesFacesIntersect(edgesShape, facesShape):
    pnts = []
    faces = getShapeItems(facesShape, TopAbs_FACE)
    edges = getShapeItems(edgesShape, TopAbs_EDGE)
    for edge in edges:
        for face in faces:
            curve3 = BRep_Tool.Curve(edge)
            curve = Geom_TrimmedCurve(curve3[0],curve3[1],curve3[2])
            surface = BRep_Tool.Surface(face)
            pntsToAdd = getPntsCurveSurfaceIntersect(curve, surface)       
            pnts += pntsToAdd
    return pnts   

def getShapeSkin(pntStart, wires, pntEnd):
    
    # Initialize and build
    skiner = BRepOffsetAPI_ThruSections(True)
    skiner.SetSmoothing(True);
      #skiner.SetMaxDegree(5)
  
    vstart = BRepBuilderAPI_MakeVertex(pntStart).Vertex()
    skiner.AddVertex(vstart)
  
    for wire in wires:
          skiner.AddWire( wire)
          
    vend = BRepBuilderAPI_MakeVertex(pntEnd).Vertex()
    skiner.AddVertex(vend)

    skiner.Build()
    
    return skiner.Shape()


def getShapeTranslate(shape, x,y,z):
    transform = gp_Trsf()
    transform.SetTranslation(gp_Vec(x,y,z))
    shape =  BRepBuilderAPI_Transform(shape, transform).Shape()
    return shape

def getShapeOZRotate(shape, angle):
    transform = gp_Trsf()
    transform.SetRotation(gp_Ax1(gp_Pnt(0,0,0), gp_Dir(0,0,1)), angle)
    #transform.SetRotation(gp_OZ(), angle)
    shape =  BRepBuilderAPI_Transform(shape, transform).Shape()
    return shape

def getShapeZScale(shape, s):
    transform = gp_GTrsf()
    transform.SetAffinity(gp_Ax2(gp_Pnt(0,0,0), gp_Dir(0,0,1),gp_Dir(0,1,0)), s)
    shape =  BRepBuilderAPI_GTransform(shape, transform).Shape()
    return shape

'''
**************************************************'
**************************************************'
**************************************************'

'''

def crDaoPoints(r):
    
    r2 = r/2
    
    gpPntMinC = gp_Pnt(0,r2,0)
    
    p0 = gp_Pnt(0,0,0)      
    p1 = getPntRotate(gpPntMinC , p0, -pi/4)      
    p2 = gp_Pnt(-r2,r2,0)      
    p3 = getPntRotate(gpPntMinC , p0, -pi/4*3)      
    p4 = gp_Pnt(0,r,0)      
    p5 = gp_Pnt(r,0,0)      
    p6 = gp_Pnt(0,-r,0)      
    p7 = gp_Pnt(r2,-r2,0)      
    
    return ( p0, p1, p2, p3, p4, p5, p6, p7 )

def getPntDaoFocus(r):
    return gp_Pnt(0,-r/4,0)

def crDaoWire(ppBase):
    
    p0, p1, p2, p3, p4, p5, p6, p7  = ppBase
    
    # base dao
    arc1 =  GC_MakeArcOfCircle(p0,p1,p2).Value()
    arc2 =  GC_MakeArcOfCircle(p2,p3,p4).Value()
    arc3 =  GC_MakeArcOfCircle(p4,p5,p6).Value()
    arc4 =  GC_MakeArcOfCircle(p6,p7,p0).Value()
 
    edge1 = BRepBuilderAPI_MakeEdge(arc1).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(arc2).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(arc3).Edge()
    edge4 = BRepBuilderAPI_MakeEdge(arc4).Edge()
  
    shape =  BRepBuilderAPI_MakeWire(edge1, edge2, edge3, edge4).Wire()
    
    return shape

def getPntsForDaoSec(pntDaoStart, pntUpLimit, pntDaoEnd, pntDownLimit, pntFocus, k):
    angleLimit = 0
    pntLimit = getPntScale(pntFocus, pntUpLimit, 1.2)
    angleStart = getAngle(pntFocus, pntLimit, pntDaoStart)
    angleEnd = getAngle(pntFocus, pntLimit, pntDaoEnd)
    kLimit = (angleLimit - angleStart)/(angleEnd - angleStart)
    if k < kLimit: #head
        kHead = (k - 0) / (kLimit- 0)
        xStart = pntUpLimit.X()
        xEnd = pntDaoStart.X()
        dx = (xEnd-xStart)*(1 - kHead)
        pnt0 = getPntTranslate(pntFocus, dx, 0, 0)
        pnt1 = getPntTranslate(pntLimit, dx, 0, 0)
    else: #tail    
        kTail = (k - kLimit) / (1 - kLimit)
        angle = -angleEnd*kTail
        pnt0 = pntFocus
        pnt1 = getPntRotate(pntFocus, pntLimit, angle)
    return pnt0, pnt1


def getWireDaoSec(shapeDao, pntFocus, k):
    
    pntsDao = getPntsOfShape(shapeDao)
    pntDownLimit, pntDaoStart, pntUpLimit, pntDaoEnd = pntsDao
    
    p1, p2 = getPntsForDaoSec(pntDaoStart, pntUpLimit, pntDaoEnd, pntDownLimit, pntFocus, k)
    sectionPlane = getFacePlane(p1, p2, 3)
    
    pnt0, pnt1 =  getPntsEdgesFacesIntersect(shapeDao, sectionPlane)
    pntUp = getPntSectionUp(pnt0, pnt1)
    circle = GC_MakeCircle(pnt0, pntUp, pnt1).Value()
    edge = BRepBuilderAPI_MakeEdge(circle).Edge()
    wire =  BRepBuilderAPI_MakeWire(edge).Wire()
    return wire

def getSolidDao(r, offset):
    
    pntsBase = getPntsBase(r)
    wireDaoClassic = getWireDaoClassic(pntsBase)
    wireDao = getShapeOffset(wireDaoClassic, -offset)
    
    pntsDao = getPntsOfShape(wireDao)
    pntDownLimit, pntDaoStart, pntUpLimit, pntDaoEnd  = pntsDao
    
    pntFocus = getPntDaoFocus(r)
   
    ks = [ 3, 9 , 16, 24, 35, 50, 70, 85] 
    wiresSec = []
 
    for k in  ks:
       wireSec = getWireDaoSec(wireDao, pntFocus, k/100)
       wiresSec += [wireSec]    
    
    solidDao = getShapeSkin(pntDaoStart, wiresSec, pntDaoEnd)
    solidDao = getShapeZScale(solidDao, 0.7)
    return solidDao
  
def getDaoCase(r, offset, h):
    r2 = r*2                                    
    h2 = h/2
    rTop = r + offset
    rSphere = gp_Vec(0,rTop,h2).Magnitude()
    sphere = BRepPrimAPI_MakeSphere(rSphere).Shape()
    limit = BRepPrimAPI_MakeBox( gp_Pnt(-r2, -r2, -h2), gp_Pnt(r2, r2, h2) ).Shape()
    case = BRepAlgoAPI_Common(sphere, limit).Shape()
    case = getShapeTranslate(case, 0,0,-h2)
 
    
    solidDao0 = getSolidDao(r, offset)
    solidDao1  = getShapeOZRotate(solidDao0, pi)
   
    case = BRepAlgoAPI_Cut(case, solidDao0).Shape()
    case = BRepAlgoAPI_Cut(case, solidDao1).Shape()
  
    return case
  
'''
******************************************************************************
******************************************************************************
******************************************************************************
******************************************************************************
'''

#                    r%    g%     b%     op%      pnt  line   mat 
#                    100   100   100     100       3      1  'DEFAULT'


def drawCircle(sc, key, r, style):
    
    sc.circle(key, gp_Pnt(r,0,0), gp_Pnt(0,r,0), gp_Pnt(-r,0,0), style )

 
def slide_01_DaoClassic(sc, r):
    
    drawCircle(sc, 'base', r, 'StyleInfo')
    pntsBase = getPntsBase(r)
    drawPoints(sc, pntsBase, 'StyleFocus', 'b')
    wireDaoClassic = getWireDaoClassic(pntsBase)
    sc.shape('wireDaoClassic', wireDaoClassic, 'StyleMain')

def slide_02_DaoConcept(sc, r, offset):
    
    drawCircle(sc, 'baseOffset', r + offset, 'StyleInfo')
    pntsBase = getPntsBase(r)
    wireDaoClassic = getWireDaoClassic(pntsBase)
    wireDaoIng = getShapeOffset(wireDaoClassic, -offset)
    sc.shape('wireDaoIng', wireDaoIng, 'StyleMain')

    pntsDaoIng = getPntsOfShape(wireDaoIng)
    drawPoints(sc, pntsDao0, 'StyleFocus', 'd')
  
    wireDaoYang = getShapeOZRotate(wireDaoIng, pi)
    sc.shape('wireDaoYang', wireDaoYang, 'StyleInfo')

def slide_03_DaoSecPrincipe(sc, r, offset, k, h):
    
    drawCircle(sc, 'baseOffset', r + offset, 'StyleInfo')
    pntsBase = getPntsBase(r)
    wireDaoClassic = getWireDaoClassic(pntsBase)
    wireDaoIng = getShapeOffset(wireDaoClassic, -offset)
    sc.shape('wireDaoIng', wireDaoIng, 'StyleMain')
    
    # for oure goal we need divide Dao on Head and Tail
    # Head sections is parallell
    # Tail sections is focused on focus point
    pntsDaoIng = getPntsOfShape(wireDaoIng)
    pntDownLimit, pntDaoStart, pntUpLimit, pntDaoEnd  = pntsDao0
    
    # we need focus to determine tail sections 
    pntFocus = getPntDaoFocus(r)
    sc.point('f', pntFocus, 'StyleMain')
    
    # we need two points to determine section
    pnt1, pnt2 = getPntsForDaoSec(pntDaoStart, pntUpLimit, pntDaoEnd, pntDownLimit, pntFocus, k)
    sc.line('lineDiv', pnt1, pnt2, 'StyleFocus')
    
    # !!! we need use plane to detect intercsect (not line) becouse 3D
    planeSec = getFacePlane(pnt1, pnt2, h)
    sc.shape(planeSec, 'StyleFocus')

    pntsSec =  getPntsEdgesFacesIntersect(wireDao0, planeSec)
    drawPoints(sc, pntsSec, 'StyleFocus')
    
    wireSec = getWireDaoSec(wireDao0, pntFocus, k)
    sc.shape('wireSec', wireSec, 'StyleFocus') 
      

def slide_04_DaoManySec(sc, r, offset, kStart, kEnd, cnt):
    
    drawCircle(sc, 'baseOffset', r + offset, 'StyleInfo')
    pntsBase = getPntsBase(r)
    wireDaoClassic = getWireDaoClassic(pntsBase)
    wireDao0 = getShapeOffset(wireDaoClassic, -offset)
    sc.shape(wireDao0, 'StyleMain')
    
    pntsDao0 = getPntsOfShape(wireDao0)
    pntDownLimit, pntDaoStart, pntUpLimit, pntDaoEnd  = pntsDao0
    
    pntFocus = getPntDaoFocus(r)
    
    for i in range(cnt+1):
        k = i/cnt
        kkScale = kEnd - kStart
        kk = kStart + k* kkScale
        p0,p1 = getPntsForDaoSec(pntDaoStart, pntUpLimit, pntDaoEnd, pntDownLimit, pntFocus, kk)
        sc.line(p0, p1, 'StyleFocus')
        wireSec = getWireDaoSec(wireDao0, pntFocus, kk)
        sc.shape(wireSec, 'StyleMain') 
        
def slide_05_DaoSkinning (sc, r, offset):
    
    drawCircle(sc, 'baseOffset', r + offset, 'StyleInfo')
    pntsBase = getPntsBase(r)
    wireDaoClassic = getWireDaoClassic(pntsBase)
    wireDao0 = getShapeOffset(wireDaoClassic, -offset)
    sc.shape(wireDao0, 'StyleMain')
    
    pntsDao0 = getPntsOfShape(wireDao0)
    pntDownLimit, pntDaoStart, pntUpLimit, pntDaoEnd  = pntsDao0
    
    pntFocus = getPntDaoFocus(r)
    drawPoints(sc, pntFocus, 'StyleMain')
  
    ks = [ 3, 9 , 16, 24, 35, 50, 70, 85] 
    wiresSec = []
 
    for k in  ks:
       wireSec = getWireDaoSec(wireDao0, pntFocus, k/100)
       ScShape(wireSec, 'StyleMain')
       wiresSec += [wireSec]    
    
    solidDao0 = getShapeSkin(pntDaoStart, wiresSec, pntDaoEnd)
    sc.shape(solidDao0, 'StyleFocus')
   
def slide_06_DaoComplete (sc, r, offset):
    
    solidDao0 = getSolidDao(r, offset)
    sc.shape(solidDao0, stDao0)
    solidDao1  = getShapeOZRotate(solidDao0, pi)
    sc.shape(solidDao1, stDao1)
    
def slide_07_DaoWithCase (sc, r, offset, caseH, caseZMove,gap):
    
    solidDao0 = getSolidDao(r, offset+gap)
    sc.shape(solidDao0, 'StyleDaoIng')
    solidDao1  = getShapeOZRotate(solidDao0, pi)
    sc.shape(solidDao1, 'StyleDaoYang')
    
    case = getDaoCase(r, offset, caseH)
    
    case = getShapeTranslate(case, 0,0, caseZMove)
    sc.shape(case, 'StyleDaoCase')

def crPlanarCirclePoints(r):
    return gp_Pnt(r,0,0), gp_Pnt(0,r,0), gp_Pnt(-r,0,0)

def daoMakeSlide(sc): 

	slideN = sc.getParam('SlideN',7)
	slideR = sc.getParam('SlideR',40)
	slideOffset = sc.getParam('SlideOffset',3)
	slideKExample = sc.getParam('SlideKExample',0.5)
	slideHPlane = sc.getParam('SlideHPlane',30)

	slideKStart = sc.getParam('SlideKStart',0.03)
	slideKEnd = sc.getParam('SlideKEnd',0.97)
	slideCntSec = sc.getParam('SlideCntSec',0.97)

	slideCaseH = sc.getParam('SlideCaseH',30)
	slideCaseZMove = sc.Param('SlideCaseZMove', -20)
	slideGap = sc.initParam('SlideGap', 1)


	if slideN >= 1:
	
		daoCirclePoints = crPlanarCirclePoints(SlideR)
		sc.drawCircle('daoCircle', baseCirclePoints)
		sc.setStyle('daoCircle', 'Info')
		
		daoPoints = crDaoPoints(SlideR)
		sc.drawPoints('daoPoints', daoPoints)
		sc.drawLabels('daoLabels', daoPoints, 'a')
		
		daoWire = crDaoWire(daoPoints)
		sc.drawWire('daoWire', daoWire)

	if slideN >= 2:

		sc.setVisible('dao', false)

		offsetCirclePoints = crPlanarCirclePoints(slideR + slideOffset)
		sc.drawCircle('offsetCircle', offsetCirclePoints)
		ingWire = crShapeOffset(daoWire, -offset)
		sc.drawWire('ingWire', wireDaoIng)

		ingPoints = crWirePoints(daoIngWire)
		sc.drawPoints('ingPoints', ingPoints,  'b')

		yangWire = crZRotateWire(ingWire, pi)
		sc.drawWire('yangWire', yangWire)
		cs.setStyle('yangWire', 'Info')

	'''
	if slideN  2:
		slide_02_DaoConcept(sc, SlideR, SlideOffset)
	elif SlideN == 3:
	   slide_03_DaoSecPrincipe(sc, SlideR, SlideOffset, SlideKExample, SlideHPlane)
	elif SlideN == 4:
	   slide_04_DaoManySec(sc, SlideR, SlideOffset, SlideKStart, SlideKEnd, SlideCntSec)
	elif SlideN == 5:
	   slide_05_DaoSkinning (sc, SlideR, SlideOffset)
	elif SlideN == 6:
	   slide_06_DaoComplete (sc, SlideR, SlideOffset)
	elif SlideN == 7:
	   slide_07_DaoWithCase (sc, SlideR, SlideOffset, SlideCaseH, SlideCaseZMove ,SlideGap)
	'''

def dao_styles(sc):

        '''     
                   #      r%    g%     b%     op%     pnt  line   mat 
        if styleVal == 'StyleInfo':
           styleVal = (   30,   30,   30,    100,     3,     2,  'PLASTIC' )
        elif styleVal == 'StyleMain':
           styleVal = (   10,   10,   90,    100,      3,     4,  'PLASTIC' )
        elif styleVal == 'StyleFocus':
           styleVal = (   90,   10,   10,     30,      3,     2,  'CHROME' )
        elif styleVal == 'stGold':
           styleVal = (   90,   90,   10,    100,      3,     4,  'GOLD'    )
        elif styleVal == 'stFog':
           styleVal = (   90,   90,   90,    30,       3,      4,   'PLASTIC'  )


                   #      r%    g%     b%     op%     pnt  line   mat 
        if styleVal == 'StyleInfo':
           styleVal = (   30,   30,   30,    100,     3,     2,  'PLASTIC' )
        elif styleVal == 'StyleMain':
           styleVal = (   10,   10,   90,    100,      3,     4,  'PLASTIC' )
        elif styleVal == 'StyleFocus':
           styleVal = (   90,   10,   10,     30,      3,     2,  'CHROME' )
        elif styleVal == 'stGold':
           styleVal = (   90,   90,   10,    100,      3,     4,  'GOLD'    )
        elif styleVal == 'stGold':
           styleVal = (   90,   90,   10,    100,      3,     4,  'GOLD'    )
        elif styleVal == 'stFog':
           styleVal = (   90,   90,   90,    30,       3,      4,   'PLASTIC'  )
        '''
 
if __name__ == '__main__':
    
    sc = Scene('dao')

    sc.initParam('SysDecorIsDesk', True)
    sc.initParam('SysDecorIsAxis', True)
    sc.initParam('SysDecorScaleA', 1)
    sc.initParam('SysDecorScaleB', 5)
    sc.initXYZ('SysDecorDeskD', 0, 0, -60)

    st = sc.getParams('TemplStyleChrome')
    st['SurfaceR'] = 100;  st['SurfaceG'] = 35;  st['SurfaceB'] = 24
    sc.initParams('StyleDaoIng',st)
    
    st = sc.getParams('TemplStyleChrome')
    st['SurfaceR'] = 98;  st['SurfaceG'] = 100;  st['SurfaceB'] = 12
    sc.initParams('StyleDaoYang',st)

    st = sc.getParams('TemplStyleChrome')
    st['SurfaceR'] = 52;  st['SurfaceG'] = 51;  st['SurfaceB'] = 100;
    sc.initParams('StyleDaoCase',st)
    
    sc.initParam('SlideN',1)
    
    daoMakeSlide(sc)
    sc.render()
    
    #please, uncooment only one string
    
    #do('test', 'slide_01_DaoClassic')
    #do('test', 'slide_02_DaoConcept')
    #do('test', 'slide_03_DaoSecPrincipe')
    #do('test', 'slide_04_DaoManySec')
    #do('test', 'slide_05_DaoSkinning')
    #do('test', 'slide_06_DaoComplete')
    #do('test', 'slide_07_DaoWithCase')

    #do('screen', 'slide_01_DaoClassic')
    #do('screen', 'slide_02_DaoConcept')
    #do('screen', 'slide_03_DaoSecPrincipe')
    #do('screen', 'slide_04_DaoManySec')
    #do('screen', 'slide_05_DaoSkinning')
    #do('screen', 'slide_06_DaoComplete')
    #do('screen', 'slide_07_DaoWithCase')
    
    #do('web', 'slide_01_DaoClassic')
    #do('web', 'slide_02_DaoConcept')
    #do('web', 'slide_03_DaoSecPrincipe')
    #do('web', 'slide_04_DaoManySec')
    #do('web', 'slide_05_DaoSkinning')
    #do('web', 'slide_06_DaoComplete')
    #do('web', 'slide_07_DaoWithCase')
    
    #do('stl', 'slide_07_DaoWithCase')
    