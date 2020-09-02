# OpenCascade tutorial by headfire (headfire@yandex.ru)
# point and line attributes

from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Dir, gp_Vec, gp_Ax1
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
             BRepBuilderAPI_Transform, BRepBuilderAPI_MakeFace,  BRepBuilderAPI_MakeVertex)
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakeOffset, BRepOffsetAPI_ThruSections

from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopLoc import TopLoc_Location

from OCC.Core.TopAbs import (TopAbs_COMPOUND, TopAbs_COMPSOLID, TopAbs_SOLID, TopAbs_SHELL,
                      TopAbs_FACE, TopAbs_WIRE, TopAbs_EDGE, TopAbs_VERTEX, TopAbs_SHAPE)


from scene import (SceneGetNative, SceneDrawCircle, SceneDrawShape, SceneDrawPoint,
                   SceneDrawLine, SceneSetStyle,
                   SceneDrawLabel, SceneLayer, SceneLevelUp, SceneLevelDown,
                   SceneScreenInit, SceneScreenStart, SceneDrawAxis)

from math import pi




# todo 
# Переименовать переменные с указанием типа
# Cделать базовую окружность шире 

def xyz(gpPnt):
    return (gpPnt.X(), gpPnt.Y(), gpPnt.Z())

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
        
def drawPoints(pnts, label):
  if isinstance(pnts, list) or isinstance(pnts, tuple):
     i = 0 
     for pnt in pnts:
        drawPoints(pnt, label + '_' + str(i))
        i+=1
  else:    
     SceneDrawPoint(label, pnts)
     SceneDrawLabel(label)
  


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
    return gp_Pnt(0,-r/2,0)


def getShapeDaoClassic(ppBase):
    
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

def getPntsOfShapeDao(shape):
    vertexes = getShapeItems(shape, TopAbs_VERTEX)
    pnts = getPntsFromVertexes(vertexes)
    delDoublePnts(pnts)
    return pnts       


def getPntSectionUp(pnt1, pnt2):
    v1 = gp_Vec(pnt1, pnt2)
    v1.Scale(0.5)
    v2 = gp_Vec(0,0,v1.Magnitude())
    pnt = gp_Pnt(pnt1.XYZ())
    pnt.Translate(v1)
    pnt.Translate(v2)
    return pnt


def getPntsForDaoSection(pntDaoStart, pntUpLimit, pntDaoEnd, pntDownLimit, pntFocus, k):
    angleLimit = 0
    pntLimit = getPntScale(pntFocus, pntUpLimit, 1.2)
    angleStart = getAngle(pntFocus, pntLimit, pntDaoStart)
    angleEnd = getAngle(pntFocus, pntLimit, pntDaoEnd)
    kLimit = (angleLimit - angleStart)/(angleEnd - angleStart)
    #print ('kLimit')
    #print (kLimit)
    if k < kLimit: #head
       kHead = (k - 0) / (kLimit- 0)
       #print ('kHead')
       #print (kHead)
       xStart = pntUpLimit.X()
       xEnd = pntDaoStart.X()
       dx = (xEnd-xStart)*(1 - kHead)
       pnt0 = getPntTranslate(pntFocus, dx, 0, 0)
       pnt1 = getPntTranslate(pntLimit, dx, 0, 0)
    else: #tail    
        kTail = (k - kLimit) / (1 - kLimit)
        #print ('kTail')
        #print (kTail)
        angle = -angleEnd*kTail
        #print(angle)
        
        fDelta = gp_Vec(pntUpLimit, pntDownLimit).Magnitude()/3 * kTail
        #delta = 1.3 * kTail
        pnt0 = getPntTranslate(pntFocus, 0, fDelta, 0)
        pnt1 = getPntRotate(pntFocus, pntLimit, angle)
    return pnt0, pnt1

def getSectionPlane(p1, p2):
    
    h = 2
    x1, y1, z1 = xyz(p1)
    x2, y2, z2 = xyz(p2)
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
       pnts.append(tool.Point(1))
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
    


def getWireDaoSection(shapeDao, pntFocus, k):
    
    pntsDao = getPntsOfShapeDao(shapeDao)
    pntDaoStart, pntUpLimit, pntDaoEnd, pntDownLimit = pntsDao
    
    p1, p2 = getPntsForDaoSection(pntDaoStart, pntUpLimit, pntDaoEnd, pntDownLimit, pntFocus, k)
    sectionPlane = getSectionPlane(p1, p2)
    
    pnt0, pnt1 =  getPntsEdgesFacesIntersect(shapeDao, sectionPlane)
    pntUp = getPntSectionUp(pnt0, pnt1)
    circle = GC_MakeCircle(pnt0, pntUp, pnt1).Value()
    edge = BRepBuilderAPI_MakeEdge(circle).Edge()
    wire =  BRepBuilderAPI_MakeWire(edge).Wire()
    return wire

def getShapeSkin(pntStart, wires, pntEnd):
    
    # Initialize and build
    skiner = BRepOffsetAPI_ThruSections()
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
  
def PaintDao(r, bevel):
    
    
    pntsBase = getPntsBase(r)
    pntFocus = getPntDaoFocus(r)    
    SceneLayer('info')
    #drawPoints(pntsBase, 'b')
    #drawPoints(pntFocus, 'f')
    #SceneDrawCircle('c', pntsBase[4], pntsBase[5], pntsBase[6])
    
    
    shapeDaoClassic = getShapeDaoClassic(pntsBase)
    SceneLayer('base')
    #SceneDrawShape('daoClassic', shapeDaoClassic)
    
    shapeDao = getShapeOffset(shapeDaoClassic,-bevel)
    SceneLayer('base')
    #SceneDrawShape('dao', shapeDao)
    
    pntsDao = getPntsOfShapeDao(shapeDao)
    pntDaoStart, pntUpLimit, pntDaoEnd, pntDownLimit = pntsDao
    #drawPoints(pntsDao,'d')
    
    SceneLayer('base')
    #p0,p1 = getPntsForDaoSection(pntDaoStart, pntUpLimit, pntDownLimit, pntDaoEnd, pntFocus, 1)
    #SceneDrawLine('line', p0, p1)
    
    '''
    kStart = 0.03
    kEnd = 0.97
    cnt = 20
    #wires = []
    for i in range(cnt+1):
        k = i/cnt
        kkScale = kEnd - kStart
        kk = kStart + k* kkScale
        p0,p1 = getPntsForDaoSection(pntDaoStart, pntUpLimit, pntDaoEnd, pntDownLimit, pntFocus, kk)
        SceneDrawLine('line#', p0, p1)
       #wires += [ getWireDaoSection(shapeDao, pntFocus, k) ]
    '''

    '''
    p0,p1 = getPntsForDaoSection(pntDaoStart, pntUpLimit, pntDaoEnd, pntDownLimit, pntFocus, kk)
    SceneDrawLine('line#', p0, p1)
    '''
    kk = [ 3, 9 , 16, 24, 35, 50, 70, 85] 
    wires = []
 
    SceneLayer('main')
    for k in  kk:
       wire = getWireDaoSection(shapeDao, pntFocus, k/100)
       #SceneDrawShape('wire#', wire)
       wires += [wire]    
    
    
    SceneLayer('pres')
    skin = getShapeSkin(pntDaoStart, wires, pntDaoEnd)
    SceneDrawShape('skin', skin)
    
    '''
    
    SceneDrawLabel('prjC')
    for pnt in pntsPrjEnds:
       SceneDrawLine('Project_#', pntPrjCenter, pnt) 

    SceneLayer('main')
    SceneDrawShape('dao', shapeDao)
    drawPoints(pntsDao, 'd')
  
    SceneLayer('info')
    shapeDaoMirr = getShapeMirror(shapeDao,gp_Pnt(0,0,0))
    SceneDrawShape('daoMirr', shapeDaoMirr)
    '''
    
    
if __name__ == '__main__':
    
    SceneScreenInit()
    
    SceneDrawAxis('axis')
    
    PaintDao(5, 1)
    
    
    SceneScreenStart()

