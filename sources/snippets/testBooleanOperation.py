#
#

import sys
sys.path.insert(0, "../scene")
from scene import SceneScreenInit, SceneScreenStart, SceneDrawShape, SceneDrawAxis, SceneLayer

from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox,  	BRepPrimAPI_MakeCylinder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Common, BRepAlgoAPI_Cut
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform

def getShapeTranslate(shape, x,y,z):
    transform = gp_Trsf()
    transform.SetTranslation(gp_Vec(x,y,z))
    shape =  BRepBuilderAPI_Transform(shape, transform).Shape()
    return shape


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
    
if __name__ == '__main__':
    
    SceneScreenInit()
    SceneDrawAxis('axis')

    case = getDaoCase(5,0.3,0.3,3)
    SceneLayer('pres')
    SceneDrawShape('case',case)
   
    SceneScreenStart()
  