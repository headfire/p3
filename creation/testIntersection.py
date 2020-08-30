from scene import (SceneScreenInit, SceneDrawAxis, SceneScreenStart, SceneErase, SceneTempName
                   SceneGetNative, SceneDrawCircle3, SceneDrawShape, SceneDrawPoint,
                   SceneDrawLine,
                   SceneDrawLabel, SceneLayer, SceneLevelUp, SceneLevelDown,
                   )

from gp import gp_Pnt, gpVec, gp_dir

from makeDaoShape import PaintDaoShape, detectBasePoints

def getDaoShape():
    
    SceneLevelDown()
    
    PaintDaoShape(5, 0.3)
    shape = SceneGetNative('dao').Shape()
    DetectBasePoints('dao')
    gpPnt1 = SceneGetNative('p2').Component().Pnt()
    gpPnt2 = SceneGetNative('p3').Component().Pnt()

    SceneLevelUp()
    
    return shape, gpPnt1, gpPnt2
    


def intersectWireAndPlane(shape, plane)

   BRepBuilderAPI_MakePolygon polygon;
   Geom_Plane aplane = Geom_Plane(1.,0.,0.,0.);
   planeShape = BRepBuilderAPI_MakeFace(aplane).Face();

   TopExp_Explorer Ex;
   for (Ex.Init(S,TopAbs_EDGE); Ex.More(); Ex.Next())
     { Handle(Geom_Surface) sFirst = BRep_Tool::Surface(TopoDS::Face(planeShape));
Standard_Real First=0,Last=180.0;
Handle(Geom_Curve) myCurve = BRep_Tool::Curve(TopoDS::Edge(Ex.Current()),First,Last);

GeomAPI_IntCS Intersector(myCurve, sFirst);
Standard_Integer nb = Intersector.NbPoints();
if(nb>0)
{
gp_Pnt P = Intersector.Point(1);
polygon.Add(P);
}
}
polygon.Close();
TopoDS_Wire wire = polygon.Wire();
TopoDS_Face face = BRepBuilderAPI_MakeFace(wire);
myAISContext->Display(new AIS_Shape(wire), Standard_False);
}

if __name__ == '__main__':
    
    #SceneScreenInit()
    
    DrawAxis('axis')
    
    getDaoShape()

   S = Shape

    
    SceneScreenStart()
  