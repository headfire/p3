#https://www.opencascade.com/doc/occt-7.3.0/overview/html/occt_user_guides__modeling_algos.html
#Let us create a Plate surface and approximate it from a polyline as a curve constraint and a point constraint

import sys
sys.path.insert(0, "../scene")
from scene import (SceneScreenInit, SceneDrawAxis, 
                   SceneDrawShape, SceneDrawPoint,  
                   SceneScreenStart)

from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace
from OCC.Core.GeomPlate import GeomPlate_BuildPlateSurface, GeomPlate_PointConstraint, GeomPlate_MakeApprox
from OCC.Core.BRepTools import BRepTools_WireExplorer
from OCC.Core.BRepFill import BRepFill_CurveConstraint
from OCC.Core.BRepAdaptor import BRepAdaptor_HCurve


def getTestFace():
    
    P1 = gp_Pnt (0.,0.,0.)
    P12 = gp_Pnt (0.,2.,2.)
    P2 = gp_Pnt (0.,10.,0.)
    P3 = gp_Pnt (0.,10.,10.) 
    P4 = gp_Pnt (0.,0.,10.)
    P5 = gp_Pnt (5.,5.,5.)
    SceneDrawPoint('p1',P1)
    SceneDrawPoint('p12',P12)
    SceneDrawPoint('p2',P2)
    SceneDrawPoint('p3',P3)
    SceneDrawPoint('p4',P4)
    SceneDrawPoint('p5',P5)
    W = BRepBuilderAPI_MakePolygon() 
    W.Add(P1)
    W.Add(P12)
    W.Add(P2)
    W.Add(P3)
    W.Add(P4)
    W.Add(P1)
    
    SceneDrawShape('w',W.Shape())
    
    # Initialize a BuildPlateSurface 
    BPSurf = GeomPlate_BuildPlateSurface (3,15,2)

    
    # Create the curve constraints 
    anExp = BRepTools_WireExplorer()
    anExp.Init(W.Wire())
    
    while anExp.More():
        E = anExp.Current()
        C = BRepAdaptor_HCurve()
        C.ChangeCurve().Initialize(E)
        Cont = BRepFill_CurveConstraint(C,0)
        BPSurf.Add(Cont)
        anExp.Next()
     
    # Point constraint 
    PCont = GeomPlate_PointConstraint(P5,0)
    BPSurf.Add(PCont)
    
    # Compute the Plate surface 
    BPSurf.Perform()
    
    # Approximation of the Plate surface 
    MaxSeg=9
    MaxDegree=8
    CritOrder=0
    PSurf = BPSurf.Surface()
    dmax = max(0.0001,10*BPSurf.G0Error())
    Tol=0.0001
    Mapp = GeomPlate_MakeApprox(PSurf,Tol,MaxSeg,MaxDegree,dmax,CritOrder)
    Surf = Mapp.Surface()
    # create a face corresponding to the approximated Plate Surface 
    Umin, Umax, Vmin, Vmax = PSurf.Bounds()
    #MF = BRepBuilderAPI_MakeFace (Surf, Umin, Umax, Vmin, Vmax, Tol) 
    MF = BRepBuilderAPI_MakeFace (Surf, Tol) 
    return MF

if __name__ == '__main__':
    
    SceneScreenInit()
    
    SceneDrawAxis('axis')
    
    face = getTestFace()
    SceneDrawShape('Face',face.Shape())
    
    SceneScreenStart()
  