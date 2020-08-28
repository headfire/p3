from OCC.Core.gp import gp_Pnt
from OCC.Core.Geom import Geom_CartesianPoint

from OCC.Core.GC import  GC_MakeCircle
from OCC.Core.AIS import  AIS_Point, AIS_Circle


from scene import (SceneGetObj, SceneApplyStyle, SceneRegObj, SceneDrawAis, SceneDrawLabel,
SceneLayer, SceneSetStyle, SceneGetStyle, SceneLevelUp, SceneLevelDown,
SceneDebug, SceneStart, SceneEnd, SceneDrawAxis)


def  PaintCircle3p(name, x1, y1, z1, x2, y2, z2, x3, y3, z3):
    
    SceneLevelDown(name)
    
    # geometry creation
    gpPnt1 = gp_Pnt(x1, y1, z1)
    gpPnt2 = gp_Pnt(x2, y2, z2)
    gpPnt3 = gp_Pnt(x3, y3, z3)
    geomPnt1 = Geom_CartesianPoint(gpPnt1)
    geomPnt2 = Geom_CartesianPoint(gpPnt2)
    geomPnt3 = Geom_CartesianPoint(gpPnt3)
    
    # interactive objects creation
    SceneLayer('base')
    SceneDrawAis('p1', AIS_Point(geomPnt1))
    SceneDrawLabel('p1')
    SceneDrawAis('p2', AIS_Point(geomPnt2))
    SceneDrawLabel('p2')
    SceneDrawAis('p3', AIS_Point(geomPnt3))
    SceneDrawLabel('p3')
    
    geom_circle = GC_MakeCircle(gpPnt1, gpPnt2, gpPnt3).Value()
    SceneLayer('main')
    SceneDrawAis('circle', AIS_Circle(geom_circle))
    SceneDrawLabel('circle')
    
    SceneLevelUp()

if __name__ == '__main__':
    
    
    #SceneDebug()
    SceneStart()
    
    SceneDrawAxis('axis')

    PaintCircle3p('circle', 1, 1, 10, 5, 2, 5, 5, -5, 5)
    
    
    SceneEnd()
