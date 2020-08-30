# OpenCascade tutorial by headfire (headfire@yandex.ru)
# point and line attributes

from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Dir, gp_Vec, gp_Ax1
from OCC.Core.Geom import Geom_CartesianPoint, Geom_Line, Geom_Plane

from OCC.Core.GC import GC_MakeArcOfCircle, GC_MakeCircle
from OCC.Core.AIS import AIS_Shape, AIS_Point, AIS_Circle
from OCC.Core.BRepBuilderAPI import  (BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, 
             BRepBuilderAPI_Transform, BRepBuilderAPI_MakeFace)
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakeOffset
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.BRep import BRep_Tool

from OCC.Core.TopAbs import (TopAbs_COMPOUND, TopAbs_COMPSOLID, TopAbs_SOLID, TopAbs_SHELL,
                      TopAbs_FACE, TopAbs_WIRE, TopAbs_EDGE, TopAbs_VERTEX, TopAbs_SHAPE)

from scene import (SceneGetNative, SceneDrawCircle, SceneDrawShape, SceneDrawPoint,
                   SceneDrawLine, SceneSetStyle,
                   SceneDrawLabel, SceneLayer, SceneLevelUp, SceneLevelDown,
                   SceneScreenInit, SceneScreenStart, SceneDrawAxis)

from math import cos, sin, pi, atan

# todo 
# Переименовать переменные с указанием типа
# Cделать базовую окружность шире 

def xyz(gpPnt):
    return (gpPnt.X(), gpPnt.Y(), gpPnt.Z())

def rotatePnt(pCenter,  p,  angle):
   ax = gp_Ax1(pCenter, gp_Dir(0,0,1))
   result = gp_Pnt(p.XYZ())
   result.Rotate(ax, angle)
   return result

def getBasisPoints(r):
    
    r2 = r/2
    
    gpPntMinC = gp_Pnt(0,r2,0)
    
    p0 = gp_Pnt(0,0,0)      
    #p1 = anglePnt(gpPntMinC , r2, 1.25*pi)      
    p1 = rotatePnt(gpPntMinC , p0, -pi/4)      
    p2 = gp_Pnt(-r2,r2,0)      
    #p3 = anglePnt(gpPntMinC , r2, 0.75*pi)      
    p3 = rotatePnt(gpPntMinC , p0, -pi/4*3)      
    p4 = gp_Pnt(0,r,0)      
    p5 = gp_Pnt(r,0,0)      
    p6 = gp_Pnt(0,-r,0)      
    p7 = gp_Pnt(r2,-r2,0)      
    
    
    return p0, p1, p2, p3, p4, p5, p6, p7


def getDaoWireClassic(basisPoints):
    
    p0, p1, p2, p3, p4, p5, p6, p7  = basisPoints
    
    # base dao
    arc1 =  GC_MakeArcOfCircle(p0,p1,p2).Value()
    arc2 =  GC_MakeArcOfCircle(p2,p3,p4).Value()
    arc3 =  GC_MakeArcOfCircle(p4,p5,p6).Value()
    arc4 =  GC_MakeArcOfCircle(p6,p7,p0).Value()
 
    edge1 = BRepBuilderAPI_MakeEdge(arc1).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(arc2).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(arc3).Edge()
    edge4 = BRepBuilderAPI_MakeEdge(arc4).Edge()
  
    wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3, edge4).Wire()
    
    return wire
  
def getWireOffset(wire, offset):
    tool = BRepOffsetAPI_MakeOffset()
    tool.AddWire(wire)
    tool.Perform(offset)
    wireResult = tool.Shape()  
    return wireResult

def getWireMirror(wire, p0):
    transform = gp_Trsf()
    transform.SetMirror(gp_Pnt(0,0,0))
    wireResult =  BRepBuilderAPI_Transform(wire, transform).Shape()
    return wireResult

def getWireVertexes(wire):
    result = list()
    exp = TopExp_Explorer(wire, TopAbs_VERTEX)
    i = 0
    tool = BRep_Tool()
    while (exp.More()):
       vertex = exp.Current()
       if i % 2 == 0:
          gpPntVertex = tool.Pnt(vertex)
          result.append(gpPntVertex) 
       i += 1 
       exp.Next()
    return result       

def getProjectionCenter(r):
    return gp_Pnt(0,-r/2,0)

'''
def makePlaneZ(gpPnt1, gpPnt2):
    gpVec = gp_Vec(gpPnt1, gpPnt2)
    gpVecNormal = gpVec.Rotate(gp_OZ(pi/2))
    return Geom_Plane(gpPnt1, gp_Dir(gpVecNormal))
'''

def calcAngle(gpPnt1, gpPnt2):
    v1 = gp_Vec(gpPnt1, gpPnt2)
    v2 = gp_Vec(gp_Dir(1,0,0))
    return v2.AngleWithRef(v1, gp_Vec(0,0,1))

def getProjectionPoints(p0, p1, p2, lenght, sCount):
    
    result = []
    angle1 = calcAngle(p0, p1)
    angle2 = calcAngle(p0, p2)
    pBase = gp_Pnt(p0.XYZ())
    pBase.Translate(gp_Vec(lenght, 0, 0))
    SceneDrawPoint('pbase', pBase)
    
    for i in range(sCount):
        angle = angle1+(angle2-angle1)/(sCount+2)*(i+1)
        result.append(rotatePnt(p0, pBase, angle))
  
    return result

def getProjectionFace(p1, p2):
    
    x1, y1, z1 = xyz(p1)
    x2, y2, z2 = xyz(p2)
    pe0 = gp_Pnt(x1, y1, -6)
    pe1 = gp_Pnt(x1, y1, +6)
    pe2 = gp_Pnt(x2, y2, +6)
    pe3 = gp_Pnt(x2, y2, -6)
    
    '''
    arc1 =  GC_MakeLine(p0,p1,p2).Value()
    arc2 =  GC_MakeArcOfCircle(p2,p3,p4).Value()
    arc3 =  GC_MakeArcOfCircle(p4,p5,p6).Value()
    arc4 =  GC_MakeArcOfCircle(p6,p7,p0).Value()
    '''
    
    edge1 = BRepBuilderAPI_MakeEdge(pe0, pe1).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(pe1, pe2).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(pe2, pe3).Edge()
    edge4 = BRepBuilderAPI_MakeEdge(pe3, pe0).Edge()
  
    wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3, edge4).Wire()
    face = BRepBuilderAPI_MakeFace(wire).Face()
    return face

    

def PaintDaoShape(r, bevel):
    
    def drawPoints(points, prefix):
        i = 0 
        for p in points:
            SceneDrawPoint(prefix+str(i), p)
            SceneDrawLabel(prefix+str(i))
            i+=1

    basis = getBasisPoints(r)
    
    drawPoints(basis, 'b')
    wireDaoClassic = getDaoWireClassic(basis)
    wireDao = getWireOffset(wireDaoClassic,-bevel)
    wireDaoMirr = getWireOffset(wireDao,-bevel)
    pVertexes = getWireVertexes(wireDao)
    
    
    
    # draw
    SceneLayer('info')
    SceneDrawCircle('circle', basis[4],basis[5],basis[6])
    SceneLayer('info')
    SceneDrawShape('daoMirr', wireDaoMirr)
    SceneLayer('base')
    SceneDrawShape('daoClassic', wireDaoClassic)
    SceneLayer('main')
    SceneDrawShape('dao', wireDao)

    SceneLayer('fog')
    drawPoints(pVertexes, 'pv')
        
    pProjC = getProjectionCenter(r)
    SceneDrawPoint('pProjC', pProjC)
    SceneDrawLabel('pProjC')
    
    pProjs = getProjectionPoints(pProjC, pVertexes[2],pVertexes[3], 9.0, 10)
    drawPoints(pProjs,'pProjs') 
    i = 0
    for p in pProjs:
        SceneDrawLine('line'+str(i), pProjC, p) 
        i+=1

    SceneLayer('main')
    face = BRepBuilderAPI_MakeFace(wireDao).Face()
    #face = BRepBuilderAPI_MakeFace(getPlaneSurface(pProjC, pProjs[2]), 0.2).Face()
    SceneDrawShape('face', face)
    
    SceneLayer('fog')
    face0 =getProjectionFace(pProjC, pProjs[0])
    SceneDrawShape('face0', face0)
    
'''
def ExternalLine(name, namePnt1, namePnt2, k):
    gpPnt1 = SceneGetNative(namePnt1).Component().Pnt()
    gpPnt2 = SceneGetNative(namePnt2).Component().Pnt()
    gpPnt1New = ExternalPoint(gpPnt1, gpPnt2, k)
    gpPnt2New = ExternalPoint(gpPnt2, gpPnt1, k)
    SceneDrawLine(name, gpPnt1New, gpPnt2New)
    
def ExternalPoint(gpPnt1, gpPnt2, k):
    x1,y1,z1 = gpPnt1.X(), gpPnt1.Y(), gpPnt1.Z()
    x2,y2,z2 = gpPnt2.X(), gpPnt2.Y(), gpPnt2.Z()
    return gp_Pnt( x1+(x2-x1)*k, y1+(y2-y1)*k, z1+(z2-z1)*k)
'''    
  
if __name__ == '__main__':
    
    SceneScreenInit()
    
    SceneDrawAxis('axis')
    
    SceneLevelDown('dao')
    PaintDaoShape(5, 0.6)
    SceneLevelUp()
    
    SceneScreenStart()
    
    '''
    sCount = 10 #count of tail Edges
    SceneLayer('info')
    #ExternalLine('cLine1','p0','p2', 3)
    #ExternalLine('cLine2','p0','p3', 1)
    #SceneDrawLabel('cLine1')
    #SceneDrawLabel('cLine2')
    
    #intersection - not section on start and end points
    
    gpPntC = gp_Pnt(0,-r/2,0)
    SceneLayer('main')
    SceneDrawPoint('c', gpPntC)
    SceneDrawLabel('c')
    gpPnt1 = SceneGetNative('p2').Component().Pnt()
    gpPnt2 = SceneGetNative('p3').Component().Pnt()

    def angle(gpPnt1, gpPnt2):
        x1,y1,z1 = xyz(gpPnt1)
        x2,y2,z2 = xyz(gpPnt2)
        dx, dy = x2-x1, y2-y1
        angle = atan(dy/dx)
        if dx > 0 :
          return angle
        else:
          return angle+pi
            
    angle1 = angle(gpPntC, gpPnt1)
    angle2 = angle(gpPntC, gpPnt2)
    
    for i in range(sCount):
        angle = angle1+(angle2-angle1)/(sCount+2)*(i+1)
        gpPntI = anglePnt(gpPntC, 8, angle)
        SceneDrawLine('l'+str(i), gpPntC , gpPntI)  
        edge = BRepBuilderAPI_MakeEdge(gpPntC , gpPntI).Edge()
        
    
    
    arc1 =  GC_MakeArcOfCircle(p1,p2,p3).Value()
    arc2 =  GC_MakeArcOfCircle(p3,p4,p5).Value()
    arc3 =  GC_MakeArcOfCircle(p5,p6,p7).Value()
    arc4 =  GC_MakeArcOfCircle(p7,p8,p1).Value()
 
    edge1 = BRepBuilderAPI_MakeEdge(arc1).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(arc2).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(arc3).Edge()
    edge4 = BRepBuilderAPI_MakeEdge(arc4).Edge()
    '''
    

