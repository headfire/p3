# OpenCascade tutorial by headfire (headfire@yandex.ru)
# point and line attributes

import os

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

def getPntRotate(pCenter,  p,  angle):
   ax = gp_Ax1(pCenter, gp_Dir(0,0,1))
   pnt = gp_Pnt(p.XYZ())
   pnt.Rotate(ax, angle)
   return pnt

def dao_01_scene(r):

    #compute primitives

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

    arc1 =  GC_MakeArcOfCircle(p0,p1,p2).Value()
    arc2 =  GC_MakeArcOfCircle(p2,p3,p4).Value()
    arc3 =  GC_MakeArcOfCircle(p4,p5,p6).Value()
    arc4 =  GC_MakeArcOfCircle(p6,p7,p0).Value()

    edge1 = BRepBuilderAPI_MakeEdge(arc1).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(arc2).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(arc3).Edge()
    edge4 = BRepBuilderAPI_MakeEdge(arc4).Edge()

    daoWire =  BRepBuilderAPI_MakeWire(edge1, edge2, edge3, edge4).Wire()

    # scene template
    sc = new Scene

    # scene transform
    sc.Circle('baseCircle',gp_Pnt(r,0,0), gp_Pnt(0,r,0), gp_Pnt(-r,0,0), 'stInfo')

    sc.Point('p0', p0)
    sc.Point('p1', p0)
    sc.Point('p2', p0)
    sc.Point('p3', p0)
    sc.Point('p4', p0)
    sc.Point('p5', p0)
    sc.Point('p6', p0)
    sc.Point('p7', p0)

    sc.Wire('daoWire', daoWire)

    # styling
    sc.Styling('baseCircle','stInfo')

    return sc

if __name__ == '__main__':

    r = 40
    sc = dao_01_scene(r)
    # sc.RenderToNull();
    # sc.RenderToScreen();
    # sc.RenderToWeb('dao_01_test');
    # sc.RenderToStl();

    #please, uncooment only one string

    #do('test', 'slide_01_DaoClassic')
    #do('test', 'slide_02_DaoConcept')
    #do('test', 'slide_03_DaoSecPrincipe')
    #do('test', 'slide_04_DaoManySec')
    #do('test', 'slide_05_DaoSkinning')
    #do('test', 'slide_06_DaoComplete')
    #do('test', 'slide_07_DaoWithCase')

    do('screen', 'slide_01_DaoClassic')
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

