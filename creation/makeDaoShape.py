# OpenCascade tutorial by headfire (headfire@yandex.ru)
# point and line attributes

import sys
sys.path.insert(0, "../scene")

from scene import ScInit, ScPoint, ScLine, ScCircle, ScShape, ScLabel, ScStart, ScStyle

from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Dir, gp_Vec, gp_Ax1, gp_Ax2, gp_GTrsf, gp_OZ
from OCC.Core.Geom import Geom_CartesianPoint, Geom_Line, Geom_Plane, Geom_TrimmedCurve
from OCC.Core.GeomAPI import GeomAPI_IntCS
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.GeomPlate import  (GeomPlate_BuildPlateSurface, 
                                 GeomPlate_CurveConstraint, GeomPlate_MakeApprox,
                                 GeomPlate_PointConstraint)
from OCC.Core.GeomAdaptor import GeomAdaptor_HCurve

from OCC.Core.GC import GC_MakeArcOfCircle, GC_MakeCircle
from OCC.Core.AIS import AIS_Shape, AIS_Point, AIS_Circle
from OCC.Core.BRepBuilderAPI import  (BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, 
             BRepBuilderAPI_Transform, BRepBuilderAPI_GTransform, BRepBuilderAPI_MakeFace,  BRepBuilderAPI_MakeVertex)
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakeOffset, BRepOffsetAPI_ThruSections

from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopLoc import TopLoc_Location

from OCC.Core.TopAbs import (TopAbs_COMPOUND, TopAbs_COMPSOLID, TopAbs_SOLID, TopAbs_SHELL,
                      TopAbs_FACE, TopAbs_WIRE, TopAbs_EDGE, TopAbs_VERTEX, TopAbs_SHAPE)

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox,  	BRepPrimAPI_MakeCylinder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Common, BRepAlgoAPI_Cut


from math import pi


'''
def delDoublePnts(pnts) :
    iFind = 10000
    while iFind != -1:
        iFind = -1 
        for i1 in range(len(pnts)):
            for i2 in range(i1):
               if pnts[i1].IsEqual(pnts[i2], 0.001):
                   iFind = i2
        if iFind != -1:           
           pnts.pop(iFind)           
'''
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

def getPntsBase(r):
    
    r2 = r/2
    
    gpPntMinC = gp_Pnt(0,r2,0)
    
    p0 = gp_Pnt(0,0,0)      
    #p1 = anglePnt(gpPntMinC , r2, 1.25*pi)      
    p1 = getPntRotate(gpPntMinC , p0, -pi/4)      
    p2 = gp_Pnt(-r2,r2,0)      
    #p3 = anglePnt(gpPntMinC , r2, 0.75*pi)      
    p3 = getPntRotate(gpPntMinC , p0, -pi/4*3)      
    p4 = gp_Pnt(0,r,0)      
    p5 = gp_Pnt(r,0,0)      
    p6 = gp_Pnt(0,-r,0)      
    p7 = gp_Pnt(r2,-r2,0)      
    
    return p0, p1, p2, p3, p4, p5, p6, p7

def getPntDaoFocus(r):
    return gp_Pnt(0,-r/4,0)

def getWireDaoClassic(ppBase):
    
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
  
def getDaoCase(r, bevel, decor, h):
    r2 = r*2                                    
    h2 = h/2
    rTop = r + 2*bevel + decor
    rSphere = gp_Vec(0,rTop,h2).Magnitude()
    sphere = BRepPrimAPI_MakeSphere(rSphere).Shape()
    limit = BRepPrimAPI_MakeBox( gp_Pnt(-r2, -r2, -h2), gp_Pnt(r2, r2, h2) ).Shape()
    case = BRepAlgoAPI_Common(sphere, limit).Shape()
    case = getShapeTranslate(case, 0,0,-h2)
    cylOut =  BRepPrimAPI_MakeCylinder(r+bevel+decor, decor*2).Shape()
    #SceneDrawShape('out',cylOut)
    cylIn =  BRepPrimAPI_MakeCylinder(r+bevel, decor*3).Shape()
    #SceneDrawShape('in',cylIn)
    bevelTool = BRepAlgoAPI_Cut(cylOut, cylIn).Shape()
    bevelTool = getShapeTranslate(bevelTool,0,0,-bevel/2)
    #SceneDrawShape('tool',bevelTool)
    case = BRepAlgoAPI_Cut(case, bevelTool).Shape()
    return case
  
'''
******************************************************************************
******************************************************************************
******************************************************************************
******************************************************************************
'''

stInfo = ScStyle( (0.5,0.5,0.5), None,  None, None, None)
stMain = ScStyle((0.1,0.1,0.9),  None,  None,    4,    None )
stBase = ScStyle((0.9,0.1,0.1),  None,  None, None, None)
stGold = ScStyle((0.9,0.9,0.1),  None,  None, 4 ,'GOLD')
stFog = ScStyle((0.1,0.9,0.1),  0.7, None, None ,'GOLD')

def drawPoints(objNamePrefix, pnts, style):
    if isinstance(pnts, list) or isinstance(pnts, tuple):
       i = 0 
       for pnt in pnts:
          drawPoints(objNamePrefix + '_' + str(i), pnt, style)
          i+=1
    else:    
       ScPoint(pnts, style)
       ScLabel(pnts, objNamePrefix, style)


def drawCircle(r, style):
    
    ScCircle(gp_Pnt(r,0,0), gp_Pnt(0,r,0), gp_Pnt(-r,0,0), style )
 
def slide_01_DaoClassic(r):
    
    drawCircle(r, stInfo)
    pntsBase = getPntsBase(r)
    drawPoints('b', pntsBase, stBase)
    shapeDaoClassic = getWireDaoClassic(pntsBase)
    ScShape(shapeDaoClassic, stMain)

def slide_02_DaoConcept(r, bevel):
    
    drawCircle(r + bevel, stInfo)
    pntsBase = getPntsBase(r)
    wireDaoClassic = getWireDaoClassic(pntsBase)
    wireDao0 = getShapeOffset(wireDaoClassic, -bevel)
    ScShape(wireDao0, stMain)
  
    pntsDao0 = getPntsOfShape(wireDao0)
    drawPoints('d',pntsDao0, stBase)
  
    wireDao1 = getShapeOZRotate(wireDao0, pi)
    ScShape(wireDao1, stInfo)
   
def slide_03_DaoSecPrincipe(r, bevel, k, h):
    
    drawCircle(r + bevel)
    pntsBase = getPntsBase(r)
    wireDaoClassic = getWireDaoClassic(pntsBase)
    wireDao0 = getShapeOffset(wireDaoClassic, -bevel)
    SceneDrawShape('wireDao1', wireDao0)
    
    # for oure goal we need divide Dao on Head and Tail
    # Head sections is parallell
    # Tail sections is focused on focus point
    pntsDao0 = getPntsOfShape(wireDao0)
    pntDownLimit, pntDaoStart, pntUpLimit, pntDaoEnd  = pntsDao0
    
    # we need focus to determine tail sections 
    pntFocus = getPntDaoFocus(r)
    SceneDrawPoint('pntFocus', pntFocus)
    SceneDrawLabel('pntFocus','f')
  
    # we need two points to determine section
    pnt1, pnt2 = getPntsForDaoSec(pntDaoStart, pntUpLimit, pntDaoEnd, pntDownLimit, pntFocus, k)
    SceneDrawLine('lineSec',pnt1, pnt2)
    
    # !!! we need use plane to detect intercsect (not line) becouse 3D
    planeSec = getFacePlane(pnt1, pnt2, h)
    SceneDrawShape('planeSec', planeSec)

    pntSec0, pntSec1 =  getPntsEdgesFacesIntersect(wireDao0, planeSec)
    SceneDrawPoint('pntSec0', pntSec0)
    SceneDrawPoint('pntSec1', pntSec1)

def slide_03_DaoSectionsTest(r, bevel, k, h):
    
    drawCircle(r + bevel)
    pntsBase = getPntsBase(r)
    wireDaoClassic = getWireDaoClassic(pntsBase)
    wireDao0 = getShapeOffset(wireDaoClassic, -bevel)
    SceneDrawShape('wireDao1', wireDao0)
    
    # for oure goal we need divide Dao on Head and Tail
    # Head sections is parallell
    # Tail sections is focused on focus point
    pntsDao0 = getPntsOfShape(wireDao0)
    pntDownLimit, pntDaoStart, pntUpLimit, pntDaoEnd  = pntsDao0
    
    # we need focus to determine tail sections 
    pntFocus = getPntDaoFocus(r)
    SceneDrawPoint('pntFocus', pntFocus)
    SceneDrawLabel('pntFocus','f')
  
    # we need two points to determine section
    pnt1, pnt2 = getPntsForDaoSec(pntDaoStart, pntUpLimit, pntDaoEnd, pntDownLimit, pntFocus, k)
    SceneDrawLine('lineSec',pnt1, pnt2)
    
    # !!! we need use plane to detect intercsect (not line) becouse 3D
    planeSec = getFacePlane(pnt1, pnt2, h)
    SceneDrawShape('planeSec', planeSec)

    pntSec0, pntSec1 =  getPntsEdgesFacesIntersect(wireDao0, planeSec)
    SceneDrawPoint('pntSec0', pntSec0)
    SceneDrawPoint('pntSec1', pntSec1)


def slide_04_DaoManySec(r, bevel, kStart, kEnd, cnt):
    
    drawCircle(r + bevel)
    pntsBase = getPntsBase(r)
    wireDaoClassic = getWireDaoClassic(pntsBase)
    wireDao0 = getShapeOffset(wireDaoClassic, -bevel)
    SceneDrawShape('wireDao1', wireDao0)
    
    pntsDao0 = getPntsOfShape(wireDao0)
    pntDownLimit, pntDaoStart, pntUpLimit, pntDaoEnd  = pntsDao0
    
    pntFocus = getPntDaoFocus(r)
    SceneDrawPoint('pntFocus', pntFocus)
    SceneDrawLabel('pntFocus','f')
 
 
    for i in range(cnt+1):
        k = i/cnt
        kkScale = kEnd - kStart
        kk = kStart + k* kkScale
        p0,p1 = getPntsForDaoSec(pntDaoStart, pntUpLimit, pntDaoEnd, pntDownLimit, pntFocus, kk)
        #SceneDrawLine('line#', p0, p1)
        wireSec = getWireDaoSec(wireDao0, pntFocus, kk)
        SceneDrawShape('wireSec#', wireSec) 
        
def slide_05_DaoSkinning (r, bevel):
    
    drawCircle(r + bevel)
    pntsBase = getPntsBase(r)
    wireDaoClassic = getWireDaoClassic(pntsBase)
    wireDao0 = getShapeOffset(wireDaoClassic, -bevel)
    SceneDrawShape('wireDao1', wireDao0)
    
    pntsDao0 = getPntsOfShape(wireDao0)
    pntDownLimit, pntDaoStart, pntUpLimit, pntDaoEnd  = pntsDao0
    
    pntFocus = getPntDaoFocus(r)
    SceneDrawPoint('pntFocus', pntFocus)
    SceneDrawLabel('pntFocus','f')
 
    ks = [ 3, 9 , 16, 24, 35, 50, 70, 85] 
    wiresSec = []
 
    for k in  ks:
       wireSec = getWireDaoSec(wireDao0, pntFocus, k/100)
       SceneDrawShape('wireSec#', wireSec)
       wiresSec += [wireSec]    
    
    solidDao0 = getShapeSkin(pntDaoStart, wiresSec, pntDaoEnd)
    SceneDrawShape('solidDao0', solidDao0)
   
def slide_06_DaoComplete (r, bevel):
    
    drawCircle(r + bevel)
    pntsBase = getPntsBase(r)
    wireDaoClassic = getWireDaoClassic(pntsBase)
    wireDao0 = getShapeOffset(wireDaoClassic, -bevel)
    SceneDrawShape('wireDao1', wireDao0)
    
    pntsDao0 = getPntsOfShape(wireDao0)
    pntDownLimit, pntDaoStart, pntUpLimit, pntDaoEnd  = pntsDao0
    
    pntFocus = getPntDaoFocus(r)
   
    ks = [ 3, 9 , 16, 24, 35, 50, 70, 85] 
    wiresSec = []
 
    for k in  ks:
       wireSec = getWireDaoSec(wireDao0, pntFocus, k/100)
       wiresSec += [wireSec]    
    
    solidDao0 = getShapeSkin(pntDaoStart, wiresSec, pntDaoEnd)
    SceneDrawShape('solidDao0', solidDao0)
    solidDao0 = getShapeZScale(solidDao0, 0.7)
    SceneDrawShape('solidDao0', solidDao0)
    solidDao1  = getShapeOZRotate(solidDao0, pi)
    SceneDrawShape('solidDao1', solidDao1)
    
def slide_06_DaoWithCase (r, bevel, caseDecor, caseH, caseDown):
    
    pntsBase = getPntsBase(r)
    wireDaoClassic = getWireDaoClassic(pntsBase)
    wireDao0 = getShapeOffset(wireDaoClassic, -bevel)
    
    pntsDao0 = getPntsOfShape(wireDao0)
    pntDownLimit, pntDaoStart, pntUpLimit, pntDaoEnd  = pntsDao0
    
    pntFocus = getPntDaoFocus(r)
   
    ks = [ 3, 9 , 16, 24, 35, 50, 70, 85] 
    wiresSec = []
 
    for k in  ks:
       wireSec = getWireDaoSec(wireDao0, pntFocus, k/100)
       wiresSec += [wireSec]    
    
    solidDao0 = getShapeSkin(pntDaoStart, wiresSec, pntDaoEnd)
    SceneDrawShape('solidDao0', solidDao0)
    solidDao0 = getShapeZScale(solidDao0, 0.7)
    # !!! Boolean not work if not small rotate (its a bus)
    solidDao0  = getShapeOZRotate(solidDao0, pi*0.2)
    SceneDrawShape('solidDao0', solidDao0)
    solidDao1  = getShapeOZRotate(solidDao0, pi)
    SceneDrawShape('solidDao1', solidDao1)
    
    case = getDaoCase(r, bevel, caseDecor, caseH)
    case = BRepAlgoAPI_Cut(case, solidDao0).Shape()
    case = BRepAlgoAPI_Cut(case, solidDao1).Shape()
    
    case = getShapeTranslate(case, 0,0, caseDown)
    SceneDrawShape('case', case)
        
    
if __name__ == '__main__':
    
    ScInit()
    
    r = 5
    bevel = 0.3
    #slide_01_DaoClassic(r)
    slide_02_DaoConcept(r, bevel)
    #slide_03_DaoSecPrincipe(r, bevel, 0.5, 3)
    #slide_04_DaoManySec(r, bevel, 0.03, 0.97, 40)
    #slide_05_DaoSkinning (r, bevel)
    #slide_06_DaoComplete (r, bevel)
    #slide_06_DaoWithCase (r, bevel, 0.3, 3, -3)
    
    
    ScStart()


