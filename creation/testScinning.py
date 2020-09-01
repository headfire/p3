#http://quaoar.su/blog/page/postroenie-trubki-v-open-cascade-technology
#Что ж, посмотрим, насколько такой вариант перспективен. Ниже мы пытаемся задействовать следующий код:

from scene import (SceneScreenInit, SceneDrawAxis, 
                   SceneDrawShape, SceneLayer,
                   #SceneDrawLine, SceneDrawLabel, SceneDrawPoint,  
                   SceneScreenStart)

#from OCC.Core.gp import gp_Pnt  #, gp_Vec, gp_dir
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_ThruSections
from OCC.Core.TopAbs import TopAbs_WIRE
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeVertex

from makeDaoShape import getDaoScinningWires


def MakeSkin(wires, start, end):
    
  # Initialize and build
  ThruSections = BRepOffsetAPI_ThruSections()
  ThruSections.SetSmoothing(True);
  #ThruSections.SetMaxDegree(5)
  vstart = BRepBuilderAPI_MakeVertex(start).Vertex()
  ThruSections.AddVertex(vstart)
  k = 0 
  for wire in wires:
       if wire.ShapeType() != TopAbs_WIRE:
          print("Warning: section " + str(k) + " is not a wire")
       else:
          ThruSections.AddWire( wire)
       k += 1   
  vend = BRepBuilderAPI_MakeVertex(end).Vertex()
  ThruSections.AddVertex(vend)
  ThruSections.Build()
  if ThruSections.IsDone():
     return ThruSections.Shape()
     # Return the result
  else: 
     print('Error: IsDone() false in BRepOffsetAPI_ThruSections')
     return TopoDS_Shape()

if __name__ == '__main__':
    
    SceneScreenInit()
    
    SceneDrawAxis('axis')

    wires, start, end = getDaoScinningWires(5, 0.6, 10, 0, 5)
    
    shapeDao = MakeSkin(wires, start, end)
    SceneLayer('main')
    SceneDrawShape('Dao',shapeDao)
    
    SceneScreenStart()
  