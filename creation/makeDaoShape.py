# OpenCascade tutorial by headfire (headfire@yandex.ru)
# point and line attributes

from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Dir, gp_Vec, gp_Ax1
from OCC.Core.Geom import Geom_CartesianPoint, Geom_Line, Geom_Plane, Geom_TrimmedCurve
from OCC.Core.GeomAPI import GeomAPI_IntCS
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.GeomPlate import  (GeomPlate_BuildPlateSurface, 
                                 GeomPlate_CurveConstraint, GeomPlate_MakeApprox,
                                 GeomPlate_PointConstraint)
from OCC.Core.GeomAdaptor import GeomAdaptor_HCurve

from OCC.Core.GC import GC_MakeArcOfCircle, GC_MakeCircle
from OCC.Core.AIS import AIS_Shape, AIS_Point, AIS_Circle
from OCC.Core.BRepBuilderAPI import  (BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, 
             BRepBuilderAPI_Transform, BRepBuilderAPI_MakeFace)
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakeOffset
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopLoc import TopLoc_Location

from OCC.Core.TopAbs import (TopAbs_COMPOUND, TopAbs_COMPSOLID, TopAbs_SOLID, TopAbs_SHELL,
                      TopAbs_FACE, TopAbs_WIRE, TopAbs_EDGE, TopAbs_VERTEX, TopAbs_SHAPE)


from scene import (SceneGetNative, SceneDrawCircle, SceneDrawShape, SceneDrawPoint,
                   SceneDrawLine, SceneSetStyle,
                   SceneDrawLabel, SceneLayer, SceneLevelUp, SceneLevelDown,
                   SceneScreenInit, SceneScreenStart, SceneDrawAxis)

from math import cos, sin, pi, atan

TOPO_TYPES = ['TopAbs_COMPOUND', 'TopAbs_COMPSOLID', 'TopAbs_SOLID', 'TopAbs_SHELL',
                      'TopAbs_FACE', 'TopAbs_WIRE', 'TopAbs_EDGE', 'TopAbs_VERTEX', 'TopAbs_SHAPE']


# todo 
# Переименовать переменные с указанием типа
# Cделать базовую окружность шире 

def xyz(gpPnt):
    return (gpPnt.X(), gpPnt.Y(), gpPnt.Z())

def getPntRotate(pCenter,  p,  angle):
   ax = gp_Ax1(pCenter, gp_Dir(0,0,1))
   pnt = gp_Pnt(p.XYZ())
   pnt.Rotate(ax, angle)
   return pnt

def getAngle(gpPnt1, gpPnt2):
    v1 = gp_Vec(gpPnt1, gpPnt2)
    v2 = gp_Vec(gp_Dir(1,0,0))
    return v2.AngleWithRef(v1, gp_Vec(0,0,1))

def getShapeItems(shape, topoType):
   items = [] 
   ex = TopExp_Explorer(shape, topoType)
   while ex.More():
       items.append(ex.Current())
       ex.Next()
   return items

def printShapeItems(shape):
    for TYPE in TOPO_TYPES:
        items = getShapeItems(shape, TOPO_TYPES.index(TYPE))  
        print(TYPE +':'+str(len(items)))   

def getPntsFromVertexes(vertexes):
    pnts = []
    for v in vertexes:
        pnts += [BRep_Tool.Pnt(v)] 
    return pnts    

def delDoublePnts(pnts) :
    iFind = 10000
    while iFind != -1:
        iFind = -1 
        for i1 in range(len(pnts)):
            for i2 in range(i1):
               if pnts[i1].IsEqual(pnts[i2], 0.001):
                   iFind = i2
        if iFind != -1:           
           pnts.pop(iFind)           
        
def drawPoints(pnts, prefix):
    for i in range(len(pnts)):
       if isinstance(pnts[i],list) :
           drawPoints(pnts[i], prefix+'_'+str(i))
       else:    
           SceneDrawPoint(prefix+'_'+str(i), pnts[i])
           SceneDrawLabel(prefix+'_'+str(i))


'''
**************************************************'
**************************************************'
**************************************************'

'''

def getPntsBase(r):
    
    r2 = r/2
    
    gpPntMinC = gp_Pnt(0,r2,0)
    
    p0 = gp_Pnt(0,0,0)      
    #p1 = anglePnt(gpPntMinC , r2, 1.25*pi)      
    p1 = getPntRotate(gpPntMinC , p0, -pi/4)      
    p2 = gp_Pnt(-r2,r2,0)      
    #p3 = anglePnt(gpPntMinC , r2, 0.75*pi)      
    p3 = getPntRotate(gpPntMinC , p0, -pi/4*3)      
    p4 = gp_Pnt(0,r,0)      
    p5 = gp_Pnt(r,0,0)      
    p6 = gp_Pnt(0,-r,0)      
    p7 = gp_Pnt(r2,-r2,0)      
    
    
    return p0, p1, p2, p3, p4, p5, p6, p7


def getShapeDaoClassic(ppBase):
    
    p0, p1, p2, p3, p4, p5, p6, p7  = ppBase
    
    # base dao
    arc1 =  GC_MakeArcOfCircle(p0,p1,p2).Value()
    arc2 =  GC_MakeArcOfCircle(p2,p3,p4).Value()
    arc3 =  GC_MakeArcOfCircle(p4,p5,p6).Value()
    arc4 =  GC_MakeArcOfCircle(p6,p7,p0).Value()
 
    edge1 = BRepBuilderAPI_MakeEdge(arc1).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(arc2).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(arc3).Edge()
    edge4 = BRepBuilderAPI_MakeEdge(arc4).Edge()
  
    shape =  BRepBuilderAPI_MakeWire(edge1, edge2, edge3, edge4).Wire()
    
    return shape
  
def getShapeOffset(shape, offset):
    tool = BRepOffsetAPI_MakeOffset()
    tool.AddWire(shape)
    tool.Perform(offset)
    shape = tool.Shape()  
    return shape

def getShapeMirror(shape, p0):
    transform = gp_Trsf()
    transform.SetMirror(gp_Pnt(0,0,0))
    shape =  BRepBuilderAPI_Transform(shape, transform).Shape()
    return shape

def getPntsOfShapeDao(shape):
    vertexes = getShapeItems(shape, TopAbs_VERTEX)
    pnts = getPntsFromVertexes(vertexes)
    delDoublePnts(pnts)
    return pnts       

def getPntPrjCenter(r):
    return gp_Pnt(0,-r/2,0)


def getPntsPrjEnds(p0, p1, p2, lenght, sCount):
    
    result = []
    angle1 = getAngle(p0, p1)
    angle2 = getAngle(p0, p2)
    pBase = gp_Pnt(p0.XYZ())
    pBase.Translate(gp_Vec(lenght, 0, 0))
    
    for i in range(sCount):
        angle = angle1+(angle2-angle1)/(sCount+2)*(i+1)
        result.append(getPntRotate(p0, pBase, angle))
  
    return result

def getShapePrjPlane(p1, p2):
    
    x1, y1, z1 = xyz(p1)
    x2, y2, z2 = xyz(p2)
    pe0 = gp_Pnt(x1, y1, -6)
    pe1 = gp_Pnt(x1, y1, +6)
    pe2 = gp_Pnt(x2, y2, +6)
    pe3 = gp_Pnt(x2, y2, -6)
    
    edge1 = BRepBuilderAPI_MakeEdge(pe0, pe1).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(pe1, pe2).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(pe2, pe3).Edge()
    edge4 = BRepBuilderAPI_MakeEdge(pe3, pe0).Edge()
  
    wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3, edge4).Wire()
    face = BRepBuilderAPI_MakeFace(wire).Face()
    return face


def getPntsCurveSurfaceIntersect(curve, surface):
    pnts = []
    tool = GeomAPI_IntCS(curve, surface)
    pCount = tool.NbPoints();
    for i in range(pCount):
       pnts.append(tool.Point(1))
    return pnts   

def getPntsEdgesFacesIntersect(edgesShape, facesShape):
    pnts = []
    faces = getShapeItems(facesShape, TopAbs_FACE)
    edges = getShapeItems(edgesShape, TopAbs_EDGE)
    for edge in edges:
        for face in faces:
            curve3 = BRep_Tool.Curve(edge)
            curve = Geom_TrimmedCurve(curve3[0],curve3[1],curve3[2])
            surface = BRep_Tool.Surface(face)
            pntsToAdd = getPntsCurveSurfaceIntersect(curve, surface)       
            pnts += pntsToAdd
    return pnts   
    
def getPntPrjZ(pnt1, pnt2):
    v1 = gp_Vec(pnt1, pnt2)
    v1.Scale(0.5)
    v2 = gp_Vec(0,0,v1.Magnitude())
    pnt = gp_Pnt(pnt1.XYZ())
    pnt.Translate(v1)
    pnt.Translate(v2)
    return pnt

def getShapeDao3d(pntssForCircles, pntStart, pntEnd):
    '''
    curves = []
    for pnts in pntssForCircles:
        curveCyrcle = GC_MakeCircle(pnts[0], pnts[1], pnts[2]).Value()
        curves += [curveCyrcle]
        
    #Initialize a BuildPlateSurface 
    BPSurf = GeomPlate_BuildPlateSurface(3,15,2)
    
    #Create the curve constraints 
    for curve in curves:
      gAdaptor = GeomAdaptor_HCurve(curve, 0, 180)
      cCont = GeomPlate_CurveConstraint(gAdaptor,0)
      BPSurf.Add(cCont)
    
    pCont1 = GeomPlate_PointConstraint(pntStart,0)
    pCont2 = GeomPlate_PointConstraint(pntEnd,0)
    BPSurf.Add(pCont1)
    BPSurf.Add(pCont2)
    
    #Compute the Plate surface 
    BPSurf.Perform()
    
    #Approximation of the Plate surface 
    MaxSeg=9
    MaxDegree=8
    CritOrder=0
    PSurf = BPSurf.Surface()
    dmax = max(0.0001,10*BPSurf.G0Error())
    Tol=0.0001
    Mapp = GeomPlate_MakeApprox(PSurf,Tol,MaxSeg,MaxDegree,dmax,CritOrder)
    Surf=Mapp.Surface()
    
    
    #create a face corresponding to the approximated Plate 
    Umin, Umax, Vmin, Vmax = PSurf.Bounds()
    face = BRepBuilderAPI_MakeFace (Surf, Umin, Umax, Vmin, Vmax)
    return face.Shape()
    '''
    pass 

def getDaoScinningWires(r, bevel, countTailPrjs, start, end) :
    
    pntsBase = getPntsBase(r)
     
    shapeDaoClassic = getShapeDaoClassic(pntsBase)
    shapeDao = getShapeOffset(shapeDaoClassic, -bevel)
    pntsDao = getPntsOfShapeDao(shapeDao)
    pntDaoStart, pntDaoEnd = pntsDao[0], pntsDao[2]
         
    pntPrjCenter = getPntPrjCenter(r)
    pntsPrjEnds = getPntsPrjEnds(pntPrjCenter, pntDaoStart, pntDaoEnd, r*2, countTailPrjs)
    
    
    pntssCar = []
    for pnt in  pntsPrjEnds :
        shapePlane = getShapePrjPlane(pntPrjCenter, pnt)
        pntsIntersect = getPntsEdgesFacesIntersect(shapeDao, shapePlane)
        pnt0 = pntsIntersect[0]
        pnt1 = getPntPrjZ(pntsIntersect[0],pntsIntersect[1])
        pnt2 = pntsIntersect[1]
        pntssCar += [[pnt0, pnt1, pnt2]]
      
    #drawPoints(pntssCar, 'Car')
  
    wires = [] 
    for pnts in pntssCar:
       circle = GC_MakeCircle(pnts[0], pnts[1], pnts[2]).Value()
       edge = BRepBuilderAPI_MakeEdge(circle).Edge()
       wire =  BRepBuilderAPI_MakeWire(edge).Wire()
       wires += [wire]
       
       
    return wires[start:end], pntDaoStart, pntDaoEnd

def PaintDao(r, bevel, countTailPrjs):
    
    '''
    wires = getDaoScinningWires(r, bevel, countTailPrjs)
    for wire in wires :
        SceneDrawShape('sh_#',wire)
    '''
    '''
    pntsBase = getPntsBase(r)
     
    shapeDaoClassic = getShapeDaoClassic(pntsBase)
    shapeDao = getShapeOffset(shapeDaoClassic,-bevel)
    shapeDaoMirr = getShapeMirror(shapeDao,gp_Pnt(0,0,0))
    pntsDao = getPntsOfShapeDao(shapeDao)
    pntDaoStart, pntDaoEnd = pntsDao[0], pntsDao[2]
         
    pntPrjCenter = getPntPrjCenter(r)
    pntsPrjEnds = getPntsPrjEnds(pntPrjCenter, pntDaoStart, pntDaoEnd, r*2, countTailPrjs)
    
    pntssCar = []
    for pnt in  pntsPrjEnds :
        shapePlane = getShapePrjPlane(pntPrjCenter, pnt)
        pntsIntersect = getPntsEdgesFacesIntersect(shapeDao, shapePlane)
        pnt0 = pntsIntersect[0]
        pnt1 = getPntPrjZ(pntsIntersect[0],pntsIntersect[1])
        pnt2 = pntsIntersect[1]
        v = gp_Vec(0,10,0)
        pnt0.Translate(v)
        pnt1.Translate(v)
        pnt2.Translate(v)
        
        #v1 =  gp_Vec(pntPrjCenter, pntsIntersect[0])
        #v2 =  gp_Vec(pntPrjCenter, pntsIntersect[1])
        #if v1.Magnitude() > v2.Magnitude():
        if True:    
             pntssCar += [[pnt0, pnt1, pnt2]]
        else:                 
             pntssCar += [
                         [ pntsIntersect[1],    
                           getPntPrjZ(pntsIntersect[0],pntsIntersect[1]),
                           pntsIntersect[0] ]   
                         ] 
    wires = [] 
    for pnts in pntssCarcase:
       circle = GeomCirecle(pnts[0], pnts[1], pnts[2])
        geomCircle = GC_MakeCircle(gpPnt1, gpPnt2, gpPnt3).Value()
       SceneDrawCircle('Carcase_#',pnts[0], pnts[1], pnts[2])

    #shapeDao3D = getShapeDao3d(pntssCar, pntDaoStart, pntDaoEnd)    
    #SceneDrawShape(shapeDao3D)
    pass
    
    SceneLayer('info')
    
    #drawPoints(pntsBase, 'b')
    SceneDrawCircle('c', pntsBase[4], pntsBase[5], pntsBase[6])
    SceneDrawShape('daoMirr', shapeDaoMirr)
    #SceneLayer('base')
    #SceneDrawShape('daoClassic', shapeDaoClassic)
    
    SceneDrawPoint('prjCenter', pntPrjCenter)
    SceneDrawLabel('prjC')
    for pnt in pntsPrjEnds:
       SceneDrawLine('Project_#', pntPrjCenter, pnt) 

    SceneLayer('main')
    SceneDrawShape('dao', shapeDao)
    drawPoints(pntsDao, 'd')
    '''
    #drawPoints(pntssCar, 'Car')
    '''
    for pnts in pntssCarcase:
       SceneDrawCircle('Carcase_#',pnts[0], pnts[1], pnts[2])
    '''   
    '''
    #printShapeItems(shapeDao)
    '''
    
if __name__ == '__main__':
    
    SceneScreenInit()
    
    SceneDrawAxis('axis')
    
    #PaintDao(5, 0.6, 20)
    wires = getDaoScinningWires(5, 0.6, 20, 10, 12)
    for wire in wires:
        SceneDrawShape('wire#',wire)
    
    SceneScreenStart()

