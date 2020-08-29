from OCC.Core.gp import gp_Pnt
from OCC.Core.Geom import Geom_CartesianPoint

from OCC.Core.GC import  GC_MakeCircle
from OCC.Core.AIS import  AIS_Point, AIS_Circle


from scene import (SceneGetObj, SceneApplyStyle, SceneRegObj, SceneDrawAis, SceneDrawLabel,
SceneLayer, SceneSetStyle, SceneGetStyle, SceneLevelUp, SceneLevelDown,
SceneDebug, SceneStart, SceneEnd, SceneDrawAxis)



if __name__ == '__main__':
    
    
    #SceneDebug()
    SceneStart()
    
    SceneDrawAxis('axis')

    PaintCircle3p('circle', 1, 1, 10, 5, 2, 5, 5, -5, 5)
    
    
    SceneEnd()
