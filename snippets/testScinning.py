#
#
import sys
sys.path.insert(0, "../scene")
from scene import SceneScreenInit, SceneScreenStart, SceneDrawShape, SceneDrawAxis

from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Common
    
if __name__ == '__main__':
    
    SceneScreenInit()
    SceneDrawAxis('axis')

    sphere = BRepPrimAPI_MakeSphere(10).Shape()
    ball = sphere
    limit = BRepPrimAPI_MakeBox(gp_Pnt(-20, -20, -5), gp_Pnt(20, 20, 5)).Shape()
    tumb = BRepAlgoAPI_Common(sphere, limit).Shape()
    SceneDrawShape('tumb',tumb)
   
    SceneScreenStart()
  