#http://quaoar.su/blog/page/postroenie-trubki-v-open-cascade-technology
#Что ж, посмотрим, насколько такой вариант перспективен. Ниже мы пытаемся задействовать следующий код:

import sys
sys.path.insert(0, "../scene")
from scene import SceneScreenInit, SceneScreenStart, SceneDrawShape, SceneDrawAxis

from OCC.Core.gp import gp_Pnt
from OCC.Core.GC import GC_MakeCircle
from OCC.Core.BRepBuilderAPI import  BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_ThruSections
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeVertex


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

    
if __name__ == '__main__':
    
    SceneScreenInit()
    SceneDrawAxis('axis')

    circle = GC_MakeCircle(gp_Pnt(0,3,5), gp_Pnt(0,-3,5), gp_Pnt(3,0,5)).Value()
    edge = BRepBuilderAPI_MakeEdge(circle).Edge()
    wire =  BRepBuilderAPI_MakeWire(edge).Wire()
    shape = getShapeSkin(gp_Pnt(0,0,0), [wire], gp_Pnt(0,0,8))
    SceneDrawShape('skin',shape)

    
    SceneScreenStart()
  