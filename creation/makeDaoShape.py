# OpenCascade tutorial by headfire (headfire@yandex.ru)
# point and line attributes

from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Dir, gp_Vec
from OCC.Core.Geom import Geom_CartesianPoint, Geom_Line

from OCC.Core.GC import GC_MakeArcOfCircle, GC_MakeCircle
from OCC.Core.AIS import AIS_Shape, AIS_Point, AIS_Circle
from OCC.Core.BRepBuilderAPI import  BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_Transform 
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakeOffset
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.BRep import BRep_Tool

from OCC.Core.TopAbs import (TopAbs_COMPOUND, TopAbs_COMPSOLID, TopAbs_SOLID, TopAbs_SHELL,
                      TopAbs_FACE, TopAbs_WIRE, TopAbs_EDGE, TopAbs_VERTEX, TopAbs_SHAPE)

from scene import (SceneGetNative, SceneDrawCircle3, SceneDrawShape, SceneDrawPoint,
                   SceneDrawLine,
                   SceneDrawLabel, SceneLayer, SceneLevelUp, SceneLevelDown,
                   SceneScreenInit, SceneScreenStart, SceneDrawAxis)

from math import cos, sin, pi, atan

# todo 
# Переименовать переменные с указанием типа
# Cделать базовую окружность шире 

def xyz(gpPnt):
    return (gpPnt.X(), gpPnt.Y(), gpPnt.Z())

def anglePnt(gpPnt, r, angle):
   x,y,z = xyz(gpPnt) 
   return gp_Pnt(x + r*cos(angle), y +r*sin(angle), z)

def PaintDaoShape(r, l):
  
    # base points    
    r2 = r/2
    
    gpPntMinC = gp_Pnt(0,r2,0)
    
    p1 = gp_Pnt(0,0,0)      
    p2 = anglePnt(gpPntMinC , r2, 1.25*pi)      
    p3 = gp_Pnt(-r2,r2,0)      
    p4 = anglePnt(gpPntMinC , r2, 0.75*pi)      
    p5 = gp_Pnt(0,r,0)      
    p6 = gp_Pnt(r,0,0)      
    p7 = gp_Pnt(0,-r,0)      
    p8 = gp_Pnt(r2,-r2,0)      
 
    # base circle
    SceneLayer('info')
    SceneDrawCircle3('circle', p5,p6,p7)
  
    # base dao
    arc1 =  GC_MakeArcOfCircle(p1,p2,p3).Value()
    arc2 =  GC_MakeArcOfCircle(p3,p4,p5).Value()
    arc3 =  GC_MakeArcOfCircle(p5,p6,p7).Value()
    arc4 =  GC_MakeArcOfCircle(p7,p8,p1).Value()
 
    edge1 = BRepBuilderAPI_MakeEdge(arc1).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(arc2).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(arc3).Edge()
    edge4 = BRepBuilderAPI_MakeEdge(arc4).Edge()
  
    wireDaoBase = BRepBuilderAPI_MakeWire(edge1, edge2, edge3, edge4).Wire()
    SceneLayer('base')
    SceneDrawShape('dao_base', wireDaoBase)
    
    # dao with offset
    offset = BRepOffsetAPI_MakeOffset()
    offset.AddWire(wireDaoBase)
    offset.Perform(-l)
    wireDao = offset.Shape()  
    SceneLayer('main')
    SceneDrawShape('dao', wireDao)
    
    # mirrored dao
    transform = gp_Trsf()
    transform.SetMirror(gp_Pnt(0,0,0))
    
    wireDaoMirr =  BRepBuilderAPI_Transform(wireDao, transform).Shape()
    SceneLayer('info')
    SceneDrawShape('dao_mirr', wireDaoMirr)
    
    
def DetectBasePoints(name)     :
    
    dao = SceneGetNative(name)
    shape = dao.Shape()
    exp = TopExp_Explorer(shape, TopAbs_VERTEX)
    i = 0
    while (exp.More()):
       vertex = exp.Current()
       tool = BRep_Tool()
       pnt = tool.Pnt(vertex)
       SceneLayer('base')
       if i % 2 == 0:
          vind =  str(int(i/2))
          vname = 'p'+vind
          SceneDrawPoint(vname, pnt)
          SceneDrawLabel(vname)
       i += 1 
       exp.Next()
       
       

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
    
  
if __name__ == '__main__':
    
    SceneScreenInit()
    
    SceneDrawAxis('axis')
    
    SceneLevelDown('dao_draw')

    r = 5
    bevel = 0.3     

    PaintDaoShape(r,bevel)
    DetectBasePoints('dao')
    SceneLayer('info')
    #ExternalLine('cLine1','p0','p2', 3)
    #ExternalLine('cLine2','p0','p3', 1)
    #SceneDrawLabel('cLine1')
    #SceneDrawLabel('cLine2')
    
    #intersection
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
    for i in range(0,11):
        angle = angle1+(angle2-angle1)/10*i
        gpPntI = anglePnt(gpPntC, 8, angle)
        SceneDrawLine('l'+str(i), gpPntC , gpPntI)  
    
    SceneLevelUp()
    
    SceneScreenStart()

