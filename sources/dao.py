# OpenCascade tutorial by headfire (headfire@yandex.ru)
# point and line attributes

EQUAL_POINTS_PRECISION = 0.001


from _scene import Scene

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



def getXYZ(gpPnt):
    return (gpPnt.X(), gpPnt.Y(), gpPnt.Z())

def isPointExistInPoints(findingPoint, thePoints):
    for thePoint in thePoints:
        if thePoint.IsEqual(findingPoint, EQUAL_POINTS_PRECISION):
            return True
    return False    

def getUniquePoints(thePoints) :
    uniquePoints = []
    for thePoint in thePoints:
      if not isPointExistInPoints(thePoint, uniquePoints):
         uniquePoints += [thePoint]      
    return uniquePoints     

def getPntRotate(pCenter,  p,  angle):
   ax = gp_Ax1(pCenter, gp_Dir(0,0,1))
   pnt = gp_Pnt(p.XYZ())
   pnt.Rotate(ax, angle)
   return pnt

def getPntScale(pCenter,  p, scale):
   pnt = gp_Pnt(p.XYZ())
   pnt.Scale(pCenter, scale)
   return pnt

def getTranslatedPoint(thePoint, deltaX, deltaY, deltaZ):
   translatedPoint = gp_Pnt(p.XYZ())
   translatedPoint.Translate(gp_Vec(deltaX, deltaY, deltaZ))
   return translatedPoint

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

def getPointsFromVertexes(vertexes):
    pnts = []
    for v in vertexes:
        pnts += [BRep_Tool.Pnt(v)] 
    return pnts    


#********************************************************
#********************************************************
#********************************************************
#********************************************************
        

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

def makeVerticalPlaneFace(baseLine2Points, h):

    pnt1, pnt2 = baseLine2Points
    
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

def makeShapePoints(shape):
    shapeVertexes = getShapeItems(shape, TopAbs_VERTEX)
    shapePoints = getPointsFromVertexes(shapeVertexes)
    return getUniquePoints(shapePoints)
  

def makeOffsetWire(theWire, offset):
    tool = BRepOffsetAPI_MakeOffset()
    tool.AddWire(theWire)
    tool.Perform(offset)
    theOffsetWire = tool.Shape()  
    return theOffsetWire

def makeZRotatedShape(theShape, angle):

    theTransform = gp_Trsf()
    
    rotationAxis = gp_OZ()
    #variant *** rotationAxis = gp_Ax1(gp_Pnt(0,0,0), gp_Dir(0,0,1))
    
    theTransform.SetRotation(rotationAxis, angle)
    
    rotatedShape =  BRepBuilderAPI_Transform(theShape, theTransform).Shape()
    
    return rotatedShape

def makeDao8Points(r):
    
    r2 = r/2
    
    gpPntMinC = gp_Pnt(0,r2,0)
    
    p1 = gp_Pnt(0,0,0)      
    p2 = getPntRotate(gpPntMinC , p1, -pi/4)      
    p3 = gp_Pnt(-r2,r2,0)      
    p4 = getPntRotate(gpPntMinC , p1, -pi/4*3)      
    p5 = gp_Pnt(0,r,0)      
    p6 = gp_Pnt(r,0,0)      
    p7 = gp_Pnt(0,-r,0)      
    p8 = gp_Pnt(r2,-r2,0)      
    
    return  p1, p2, p3, p4, p5, p6, p7, p8 

def makeDaoFocusPoint(r):
    return gp_Pnt(0,-r/4,0)

def makeDaoWire(the8Points):
    
    p1, p2, p3, p4, p5, p6, p7, p8  = the8Points
    
    arc1 =  GC_MakeArcOfCircle(p1,p2,p3).Value()
    arc2 =  GC_MakeArcOfCircle(p3,p4,p5).Value()
    arc3 =  GC_MakeArcOfCircle(p5,p6,p7).Value()
    arc4 =  GC_MakeArcOfCircle(p7,p8,p1).Value()
 
    edge1 = BRepBuilderAPI_MakeEdge(arc1).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(arc2).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(arc3).Edge()
    edge4 = BRepBuilderAPI_MakeEdge(arc4).Edge()
  
    theWire =  BRepBuilderAPI_MakeWire(edge1, edge2, edge3, edge4).Wire()
    
    return theWire

def makeDaoSectionLine2Points(daoStartPoint, daoEndPoint, daoLeftPoint, daoRightPoint,  focusPoint, sectionKoef):
    limitAngle = 0
    limitPoint = getPntScale(focusPoint, daoRightPoint, 1.2)
    startAngle = getAngle(focusPoint, limitPoint, daoStartPoint)
    endAngle = getAngle(focusPoint, limitPoint, daoEndPoint)
    limitKoef = (limitAngle - startAngle)/(endAngle - startAngle)
    if sectionKoef < limitKoef: #head
        headKoef = (sectionKoef - 0) / (limitKoef - 0)
        startX = daoRightPoint.X()
        endX = daoStartPoint.X()
        deltaX = (endX-startX)*(1 - headKoef)
        startLinePoint = getTranslatedPoint(focusPoint, deltaX, 0, 0)
        endLinePoint = getTranslatedPoint(limitPoint, deltaX, 0, 0)
    else: #tail    
        tailKoef = (sectionKoef - limitKoef) / (sectionKoef - limitKoef)
        tailAngle = -(endAngle * tailKoef)
        startLinePoint = focusPoint
        endLinePoint = getPntRotate(focusPoint, limitPoint, tailAngle)
    return startLinePoint, endLinePoint


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

def makeGorizontalCircle3Points(r):
    return gp_Pnt(r,0,0), gp_Pnt(0,r,0), gp_Pnt(-r,0,0)


if __name__ == '__main__':

    GEOM_BASE_RADIUS = 40
    GEOM_OFFSET = 3
    GEOM_SECTION_EXAMPLE_KOEF = 0.5
    GEOM_SECTION_PLANE_HEGIHT = 30
    GEOM_SECTIONS_START_KOEF = 0.03
    GEOM_SECTIONS_END_KOEF = 0.97
    GEOM_SECTIONS_COUNT = 30
    GEOM_CASE_HEIGHT = 30
    GEOM_CASE_DELTA_Z = -20
    GEOM_CASE_GAP = 1

    SLIDE_CLASSIC_DAO_NUM = 1
    SLIDE_OFFSET_DAO_NUM = 2
    SLIDE_EXAMPLE_SECTION_NUM = 3
    SLIDE_DEFAULT_NUM = 3

    SCENE_SCALE_A = 1
    SCENE_SCALE_B = 5
    SCENE_DESK_DZ = -60

    
    sc = Scene()
    sc.setScale(SCENE_SCALE_A, SCENE_SCALE_B)
    sc.drawDesk('mainDesk',0, 0, SCENE_DESK_DZ)
    sc.drawAxis('mainAxis',0, 0, 0)

    sc.initParam('SysDecorIsDesk', True)
    sc.initParam('SysDecorIsAxis', True)
    sc.initParam('SysDecorScaleA', SCENE_SCALE_A)
    sc.initParam('SysDecorScaleB', SCENE_SCALE_B)
    sc.initXYZ('SysDecorDeskD', 0, 0, SCENE_DESK_DZ)

    st = sc.getParams('TemplStyleChrome')
    st['SurfaceR'] = 100;  st['SurfaceG'] = 35;  st['SurfaceB'] = 24
    sc.initParams('StyleDaoIng',st)

    st = sc.getParams('TemplStyleChrome')
    st['SurfaceR'] = 98;  st['SurfaceG'] = 100;  st['SurfaceB'] = 12
    sc.initParams('StyleDaoYang',st)

    st = sc.getParams('TemplStyleChrome')
    st['SurfaceR'] = 52;  st['SurfaceG'] = 51;  st['SurfaceB'] = 100;
    sc.initParams('StyleDaoCase',st)

    SlideNum = sc.getParam('SlideNum',SLIDE_DEFAULT_NUM)

    if SlideNum == SLIDE_CLASSIC_DAO_NUM:

        daoCircle3Points = makeGorizontalCircle3Points(GEOM_BASE_RADIUS)
        dao8Points = makeDao8Points(GEOM_BASE_RADIUS)
        daoWire = makeDaoWire(dao8Points)

        sc.drawCircle('daoCircle', daoCircle3Points)
        sc.drawPoints('daoPoints', dao8Points)
        sc.drawLabels('daoLabels', dao8Points, 'a')
        sc.drawWire('daoWire', daoWire)

        sc.setStyle('daoCircle', 'Info')
        
    elif SlideNum == SLIDE_OFFSET_DAO_NUM:

        dao8Points = makeDao8Points(GEOM_BASE_RADIUS)
        daoWire = makeDaoWire(dao8Points)
        offsetCirclePoints = makeGorizontalCircle3Points(GEOM_BASE_RADIUS + GEOM_OFFSET)
        ingWire = makeOffsetWire(daoWire, -GEOM_OFFSET)
        ingWirePoints = makeShapePoints(ingWire)
        yangWire = makeZRotatedShape(ingWire, pi)

        sc.drawCircle('offsetCircle', offsetCirclePoints)
        sc.drawWire('ingWire', ingWire)
        sc.drawPoints('ingWirePoints', ingWirePoints)
        sc.drawLabels('ingWireLabels', ingWirePoints,  'b')
        sc.drawWire('yangWire', yangWire)

        sc.setStyle('offsetCircle', 'Info')
        sc.setStyle('yangWire', 'Info')

    elif SlideNum == SLIDE_EXAMPLE_SECTION_NUM:
    
        dao8Points = makeDao8Points(GEOM_BASE_RADIUS)
        daoWire = makeDaoWire(dao8Points)
        offsetCirclePoints = makeGorizontalCircle3Points(GEOM_BASE_RADIUS + GEOM_OFFSET)
        ingWire = makeOffsetWire(daoWire, -GEOM_OFFSET)
    
        # for oure goal we need divide Dao on Head and Tail
        # Head sections is parallell
        # Tail sections is focused on focus point
        ingWirePoints = makeShapePoints(ingWire)
        daoLeftPoint, daoStartPoint, daoRirgtPoint, daoEndPoint  = ingWirePoints
        
        # we need focus to determine tail sections 
        daoFocusPoint = makeDaoFocusPoint(GEOM_BASE_RADIUS)
        
        # we need two points to determine section
        sectionLine2Points = makeDaoSectionLine2Points(daoStartPoint, daoEndPoint, daoLeftPoint, daoRirgtPoint, daoFocusPoint, GEOM_SECTION_EXAMPLE_KOEF)
        
        # !!! we need use plane to detect intercsect (not line) becouse 3D
        sectionPlaneFace = getVerticalPlaneFace(sectionLine2Points, GEOM_SECTION_PLANE_HEGIHT)

        pntsSec =  getPntsEdgesFacesIntersect(wireDao0, planeSec)
        drawPoints(sc, pntsSec, 'StyleFocus')
        
        wireSec = getWireDaoSec(wireDao0, pntFocus, k)
        sc.shape('wireSec', wireSec, 'StyleFocus') 

        sc.drawCircle('offsetCircle', offsetCirclePoints)
        sc.drawWire('ingWire', ingWire)
        sc.drawPoint('daoFocusPoint', daoFocusPoint)
        sc.drawLine('sectionLine', sectionLine2Points)
        sc.drawShape('sectionFace', sectionPlaneFace)

        sc.setStyle('offsetCircle', 'Info')
        sc.setStyle('yangWire', 'Info')
        sc.setStyle('sectionLine', 'Focus')
        sc.setStyle('sectionFace', 'Focus')
      
    #styling and render
    sc.render('dao_' + '{:02}'.format(SlideNum) + '_test')


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
