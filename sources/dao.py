# OpenCascade tutorial by headfire (headfire@yandex.ru)
# point and line attributes

EQUAL_POINTS_PRECISION = 0.001


from _scene import Scene

from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Dir, gp_Vec, gp_Ax1, gp_Ax2, gp_GTrsf, gp_OZ
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



def getXYZ(gpPnt):
    return (gpPnt.X(), gpPnt.Y(), gpPnt.Z())

def isPointExistInPoints(findingPoint, thePoints):
    for thePoint in thePoints:
        if thePoint.IsEqual(findingPoint, EQUAL_POINTS_PRECISION):
            return True
    return False

def getUniquePoints(thePoints) :
    uniquePoints = []
    for thePoint in thePoints:
      if not isPointExistInPoints(thePoint, uniquePoints):
         uniquePoints += [thePoint]
    return uniquePoints

def getPntRotate(pCenter,  p,  angle):
   ax = gp_Ax1(pCenter, gp_Dir(0,0,1))
   pnt = gp_Pnt(p.XYZ())
   pnt.Rotate(ax, angle)
   return pnt

def getPntScale(pCenter,  p, scale):
   pnt = gp_Pnt(p.XYZ())
   pnt.Scale(pCenter, scale)
   return pnt

def getTranslatedPoint(thePoint, deltaX, deltaY, deltaZ):
   translatedPoint = gp_Pnt(thePoint.XYZ())
   translatedPoint.Translate(gp_Vec(deltaX, deltaY, deltaZ))
   return translatedPoint

def getAngle(gpPnt0, gpPnt1, gpPnt2 ):
    v1 = gp_Vec(gpPnt0, gpPnt1)
    v2 = gp_Vec(gpPnt0, gpPnt2)
    return v2.AngleWithRef(v1, gp_Vec(0,0,1))

def getShapeItems(shape, topoType):
   items = []
   ex = TopExp_Explorer(shape, topoType)
   while ex.More():
       items.append(ex.Current())
       ex.Next()
   return items

def getPointsFromVertexes(vertexes):
    pnts = []
    for v in vertexes:
        pnts += [BRep_Tool.Pnt(v)]
    return pnts


#********************************************************
#********************************************************
#********************************************************
#********************************************************


def getShapeMirror(shape, p0):
    transform = gp_Trsf()
    transform.SetMirror(gp_Pnt(0,0,0))
    shape =  BRepBuilderAPI_Transform(shape, transform).Shape()
    return shape






def getShapeTranslate(shape, x,y,z):
    transform = gp_Trsf()
    transform.SetTranslation(gp_Vec(x,y,z))
    shape =  BRepBuilderAPI_Transform(shape, transform).Shape()
    return shape


def getShapeZScale(shape, s):
    transform = gp_GTrsf()
    transform.SetAffinity(gp_Ax2(gp_Pnt(0,0,0), gp_Dir(0,0,1),gp_Dir(0,1,0)), s)
    shape =  BRepBuilderAPI_GTransform(shape, transform).Shape()
    return shape

# *******************************************************************************
# *******************************************************************************
# *******************************************************************************
# *******************************************************************************

def makeSkiningSurface(pntStart, wires, pntEnd):

    skiner = BRepOffsetAPI_ThruSections(True)
    skiner.SetSmoothing(True);

    vstart = BRepBuilderAPI_MakeVertex(pntStart).Vertex()
    skiner.AddVertex(vstart)

    for wire in wires:
          skiner.AddWire( wire)

    vend = BRepBuilderAPI_MakeVertex(pntEnd).Vertex()
    skiner.AddVertex(vend)

    skiner.Build()

    return skiner.Shape()


def makeSliceCircle3Points(intersectPoints):
    firstPoint = intersectPoints[0]
    secondPoint = intersectPoints[1]
    directionVector = gp_Vec(firstPoint, secondPoint)
    directionVector.Scale(0.5)
    upVector = gp_Vec(0,0,directionVector.Magnitude())
    upPoint = gp_Pnt(firstPoint.XYZ())
    upPoint.Translate(directionVector)
    upPoint.Translate(upVector)
    return firstPoint, upPoint, secondPoint

def makeVerticalPlaneFace(baseLine2Points, h):

    pnt1, pnt2 = baseLine2Points

    x1, y1, z1 = getXYZ(pnt1)
    x2, y2, z2 = getXYZ(pnt2)
    pe0 = gp_Pnt(x1, y1, -h)
    pe1 = gp_Pnt(x1, y1, +h)
    pe2 = gp_Pnt(x2, y2, +h)
    pe3 = gp_Pnt(x2, y2, -h)

    edge1 = BRepBuilderAPI_MakeEdge(pe0, pe1).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(pe1, pe2).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(pe2, pe3).Edge()
    edge4 = BRepBuilderAPI_MakeEdge(pe3, pe0).Edge()

    wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3, edge4).Wire()
    face = BRepBuilderAPI_MakeFace(wire).Face()
    return face



def makeEdgesFacesIntersectPoints(edgesShape, facesShape):

    def findIntersectPoints(curve, surface):
        pnts = []
        tool = GeomAPI_IntCS(curve, surface)
        pCount = tool.NbPoints();
        for i in range(1,pCount+1):
           pnts += [tool.Point(i)]
        return pnts

    intersectPoints = []
    theEdges = getShapeItems(edgesShape, TopAbs_EDGE)
    theFaces = getShapeItems(facesShape, TopAbs_FACE)
    for theEdge in theEdges:
        for theFace in theFaces:
            edgeCurves = BRep_Tool.Curve(theEdge)
            edgeTrimmedCurve = Geom_TrimmedCurve(edgeCurves[0],edgeCurves[1],edgeCurves[2])
            faceSurface = BRep_Tool.Surface(theFace)
            findedIntersectPoints = findIntersectPoints(edgeTrimmedCurve, faceSurface)
            intersectPoints += findedIntersectPoints
    return intersectPoints

def utilGetShapePoints(shape):
    shapeVertexes = getShapeItems(shape, TopAbs_VERTEX)
    shapePoints = getPointsFromVertexes(shapeVertexes)
    return getUniquePoints(shapePoints)


def makeOffsetWire(theWire, offset):
    tool = BRepOffsetAPI_MakeOffset()
    tool.AddWire(theWire)
    tool.Perform(offset)
    theOffsetWire = tool.Shape()
    return theOffsetWire

def utilGetZRotatedShape(theShape, angle):

    theTransform = gp_Trsf()

    rotationAxis = gp_OZ()
    #variant *** rotationAxis = gp_Ax1(gp_Pnt(0,0,0), gp_Dir(0,0,1))

    theTransform.SetRotation(rotationAxis, angle)

    rotatedShape =  BRepBuilderAPI_Transform(theShape, theTransform).Shape()

    return rotatedShape

def makeDao8Points(r):

    r2 = r/2

    gpPntMinC = gp_Pnt(0,r2,0)

    p1 = gp_Pnt(0,0,0)
    p2 = getPntRotate(gpPntMinC , p1, -pi/4)
    p3 = gp_Pnt(-r2,r2,0)
    p4 = getPntRotate(gpPntMinC , p1, -pi/4*3)
    p5 = gp_Pnt(0,r,0)
    p6 = gp_Pnt(r,0,0)
    p7 = gp_Pnt(0,-r,0)
    p8 = gp_Pnt(r2,-r2,0)

    return  p1, p2, p3, p4, p5, p6, p7, p8


def makeDaoWire(the8Points):

    p1, p2, p3, p4, p5, p6, p7, p8  = the8Points

    arc1 =  GC_MakeArcOfCircle(p1,p2,p3).Value()
    arc2 =  GC_MakeArcOfCircle(p3,p4,p5).Value()
    arc3 =  GC_MakeArcOfCircle(p5,p6,p7).Value()
    arc4 =  GC_MakeArcOfCircle(p7,p8,p1).Value()

    edge1 = BRepBuilderAPI_MakeEdge(arc1).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(arc2).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(arc3).Edge()
    edge4 = BRepBuilderAPI_MakeEdge(arc4).Edge()

    theWire =  BRepBuilderAPI_MakeWire(edge1, edge2, edge3, edge4).Wire()

    return theWire

def makeDaoSliceLine2Points(wirePoints,  focusPoint, sliceKoef):

    daoLeftPoint, daoStartPoint, daoRightPoint, daoEndPoint  = wirePoints
    limitAngle = 0
    limitPoint = getPntScale(focusPoint, daoRightPoint, 1.2)
    startAngle = getAngle(focusPoint, limitPoint, daoStartPoint)
    endAngle = getAngle(focusPoint, limitPoint, daoEndPoint)
    limitKoef = (limitAngle - startAngle)/(endAngle - startAngle)
    if sliceKoef < limitKoef: #head
        headKoef = (sliceKoef - 0) / (limitKoef - 0)
        startX = daoRightPoint.X()
        endX = daoStartPoint.X()
        deltaX = (endX-startX)*(1 - headKoef)
        startLinePoint = getTranslatedPoint(focusPoint, deltaX, 0, 0)
        endLinePoint = getTranslatedPoint(limitPoint, deltaX, 0, 0)
    else: #tail
        tailKoef = (sliceKoef - limitKoef) / (1 - limitKoef)
        tailAngle = -(endAngle * tailKoef)
        startLinePoint = focusPoint
        endLinePoint = getPntRotate(focusPoint, limitPoint, tailAngle)
    return startLinePoint, endLinePoint


def getSolidDao(r, offset):

    pntsBase = getPntsBase(r)
    wireDaoClassic = getWireDaoClassic(pntsBase)
    wireDao = getShapeOffset(wireDaoClassic, -offset)

    pntsDao = getPntsOfShape(wireDao)
    pntDownLimit, pntDaoStart, pntUpLimit, pntDaoEnd  = pntsDao

    pntFocus = getPntDaoFocus(r)

    ks = [ 3, 9 , 16, 24, 35, 50, 70, 85]
    wiresSec = []

    for k in  ks:
       wireSec = getWireDaoSec(wireDao, pntFocus, k/100)
       wiresSec += [wireSec]

    solidDao = getShapeSkin(pntDaoStart, wiresSec, pntDaoEnd)
    solidDao = getShapeZScale(solidDao, 0.7)
    return solidDao

def getDaoCase(r, offset, h):
    r2 = r*2
    h2 = h/2
    rTop = r + offset
    rSphere = gp_Vec(0,rTop,h2).Magnitude()
    sphere = BRepPrimAPI_MakeSphere(rSphere).Shape()
    limit = BRepPrimAPI_MakeBox( gp_Pnt(-r2, -r2, -h2), gp_Pnt(r2, r2, h2) ).Shape()
    case = BRepAlgoAPI_Common(sphere, limit).Shape()
    case = getShapeTranslate(case, 0,0,-h2)


    solidDao0 = getSolidDao(r, offset)
    solidDao1  = getShapeOZRotate(solidDao0, pi)

    case = BRepAlgoAPI_Cut(case, solidDao0).Shape()
    case = BRepAlgoAPI_Cut(case, solidDao1).Shape()

    return case

def slide_04_DaoManySec(sc, r, offset, kStart, kEnd, cnt):

    drawCircle(sc, 'baseOffset', r + offset, 'StyleInfo')
    pntsBase = getPntsBase(r)
    wireDaoClassic = getWireDaoClassic(pntsBase)
    wireDao0 = getShapeOffset(wireDaoClassic, -offset)
    sc.shape(wireDao0, 'StyleMain')

    pntsDao0 = getPntsOfShape(wireDao0)
    pntDownLimit, pntDaoStart, pntUpLimit, pntDaoEnd  = pntsDao0

    pntFocus = getPntDaoFocus(r)

    for i in range(cnt+1):
        k = i/cnt
        kkScale = kEnd - kStart
        kk = kStart + k* kkScale
        p0,p1 = getPntsForDaoSec(pntDaoStart, pntUpLimit, pntDaoEnd, pntDownLimit, pntFocus, kk)
        sc.line(p0, p1, 'StyleFocus')
        wireSec = getWireDaoSec(wireDao0, pntFocus, kk)
        sc.shape(wireSec, 'StyleMain')

def slide_05_DaoSkinning (sc, r, offset):

    drawCircle(sc, 'baseOffset', r + offset, 'StyleInfo')
    pntsBase = getPntsBase(r)
    wireDaoClassic = getWireDaoClassic(pntsBase)
    wireDao0 = getShapeOffset(wireDaoClassic, -offset)
    sc.shape(wireDao0, 'StyleMain')

    pntsDao0 = getPntsOfShape(wireDao0)
    pntDownLimit, pntDaoStart, pntUpLimit, pntDaoEnd  = pntsDao0

    pntFocus = getPntDaoFocus(r)
    drawPoints(sc, pntFocus, 'StyleMain')

    ks = [ 3, 9 , 16, 24, 35, 50, 70, 85]
    wiresSec = []

    for k in  ks:
       wireSec = getWireDaoSec(wireDao0, pntFocus, k/100)
       ScShape(wireSec, 'StyleMain')
       wiresSec += [wireSec]

    solidDao0 = getShapeSkin(pntDaoStart, wiresSec, pntDaoEnd)
    sc.shape(solidDao0, 'StyleFocus')

def slide_06_DaoComplete (sc, r, offset):

    solidDao0 = getSolidDao(r, offset)
    sc.shape(solidDao0, stDao0)
    solidDao1  = getShapeOZRotate(solidDao0, pi)
    sc.shape(solidDao1, stDao1)

def slide_07_DaoWithCase (sc, r, offset, caseH, caseZMove,gap):

    solidDao0 = getSolidDao(r, offset+gap)
    sc.shape(solidDao0, 'StyleDaoIng')
    solidDao1  = getShapeOZRotate(solidDao0, pi)
    sc.shape(solidDao1, 'StyleDaoYang')

    case = getDaoCase(r, offset, caseH)

    case = getShapeTranslate(case, 0,0, caseZMove)
    sc.shape(case, 'StyleDaoCase')

def makeGorizontalCircle3Points(r):
    return gp_Pnt(r,0,0), gp_Pnt(0,r,0), gp_Pnt(-r,0,0)


def makeSlicesWires(ingWire, ingWirePoints, daoFocusPoint, slicePlaneHeight, slicesKoefs):

    slicesWires = []
    i = 1

    for sliceKoef in slicesKoefs:

        sliceLine2Points = makeDaoSliceLine2Points(ingWirePoints, daoFocusPoint, sliceKoef)

        #todo no height
        slicePlaneFace = makeVerticalPlaneFace(sliceLine2Points, slicePlaneHeight)
        sliceIntersectPoints =  makeEdgesFacesIntersectPoints(ingWire, slicePlaneFace)
        sliceCircle3Points = makeSliceCircle3Points(sliceIntersectPoints)

        circlePoint1, circlePoint2, circlePoint3 = sliceCircle3Points
        sliceCircle = GC_MakeCircle(circlePoint1, circlePoint2, circlePoint3).Value()
        sliceEdge = BRepBuilderAPI_MakeEdge(sliceCircle).Edge()
        sliceWire =  BRepBuilderAPI_MakeWire(sliceEdge).Wire()
        sc.drawWire('sliceWire'+str(i), sliceWire)
        i += 1
     
        slicesWires += [sliceWire]
        
    return slicesWires


def drawManySliceSlide(sc):

    offsetCirclePoints = makeGorizontalCircle3Points(sc.val('DAO_BASE_RADIUS') + sc.val('DAO_OFFSET'))
    sc.drawCircle('offsetCircle', offsetCirclePoints)

    dao8Points = makeDao8Points(sc.val('DAO_BASE_RADIUS'))
    daoWire = makeDaoWire(dao8Points)
    ingWire = makeOffsetWire(daoWire, -sc.val('DAO_OFFSET'))
    sc.drawWire('ingWire', ingWire)

    ingWirePoints = makeShapePoints(ingWire)
    daoLeftPoint, daoStartPoint, daoRightPoint, daoEndPoint  = ingWirePoints

    daoFocusPoint = makeDaoFocusPoint(sc.val('DAO_BASE_RADIUS'))
    sc.drawPoint('daoFocusPoint', daoFocusPoint)
    sc.drawLabel('daoFocusPointLabel', daoFocusPoint,  'F')

    for i in range(sc.val('DAO_SLICE_COUNT')+1):

        sliceKoef = sc.val('DAO_SLICE_START_KOEF') + i * (sc.val('DAO_SLICE_END_KOEF') - sc.val('DAO_SLICE_START_KOEF'))/sc.val('DAO_SLICE_COUNT')
        sliceLine2Points = makeDaoSliceLine2Points(ingWirePoints, daoFocusPoint, sliceKoef)
        sc.drawLine('sliceLine'+str(i), sliceLine2Points)

        slicePlaneFace = makeVerticalPlaneFace(sliceLine2Points, sc.val('DAO_SLICE_PLANE_HEIGHT'))
        sliceIntersectPoints =  makeEdgesFacesIntersectPoints(ingWire, slicePlaneFace)
        sliceCircle3Points = makeSliceCircle3Points(sliceIntersectPoints)
        sc.drawCircle('sliceCircle'+str(i), sliceCircle3Points)

    sc.setStyle('offsetCircle', 'Info')
    sc.setStyle('sliceLine', 'Focus')

def  drawSkiningSurface(sc):

        offsetCirclePoints = makeGorizontalCircle3Points(sc.val('DAO_BASE_RADIUS') + sc.val('DAO_OFFSET'))
        sc.drawCircle('offsetCircle', offsetCirclePoints)

        dao8Points = makeDao8Points(sc.val('DAO_BASE_RADIUS'))
        daoWire = makeDaoWire(dao8Points)
        ingWire = makeOffsetWire(daoWire, -sc.val('DAO_OFFSET'))
        sc.drawWire('ingWire', ingWire)

        ingWirePoints = makeShapePoints(ingWire)

        daoFocusPoint = makeDaoFocusPoint(sc.val('DAO_BASE_RADIUS'))
        sc.drawPoint('daoFocusPoint', daoFocusPoint)
        sc.drawLabel('daoFocusPointLabel', daoFocusPoint,  'F')

        skiningWires = makeSlicesWires(ingWire, ingWirePoints, daoFocusPoint, sc.val('DAO_SLICE_PLANE_HEIGHT'), sc.val('DAO_SKINING_SLICES_KOEFS'))

        daoLeftPoint, daoStartPoint, daoRightPoint, daoEndPoint  = ingWirePoints
        ingSurface = makeSkiningSurface(daoStartPoint, skiningWires, daoEndPoint)
        sc.drawSurface('ingSurface', ingSurface)
        
def drawCenteredXYCircle(sc, style, key ,r):

    sc.drawCircle(style, key, ( gp_Pnt(r,0,0), gp_Pnt(0,r,0), gp_Pnt(-r,0,0)))
    #todo drawCircle -> drawWire


# *********************************************************************************
# *********************************************************************************
# *********************************************************************************

def drawDaoBaseCircle(sc, style):
    
    DAO_BASE_RADIUS = sc.val('DAO_BASE_RADIUS')
    DAO_OFFSET = sc.val('DAO_OFFSET')
 
    drawCenteredXYCircle(sc, style, 'DaoOffsetCircle', DAO_BASE_RADIUS)


def drawDaoBasePoints(sc, style):

    r = sc.val('DAO_BASE_RADIUS')
    r2 = r/2

    gpPntMinC = gp_Pnt(0,r2,0)
    
    p = {}
    p[0] = gp_Pnt(0,0,0)
    p[1] = getPntRotate(gpPntMinC , p[0], -pi/4)
    p[2] = gp_Pnt(-r2,r2,0)
    p[3] = getPntRotate(gpPntMinC , p[0], -pi/4*3)
    p[4] = gp_Pnt(0,r,0)
    p[5] = gp_Pnt(r,0,0)
    p[6] = gp_Pnt(0,-r,0)
    p[7] = gp_Pnt(r2,-r2,0)

    for key in p:
        sc.drawPoint(style, 'DaoBasePoints'+str(key), p[key], 'p'+str(key))

def drawDaoClassicWire(sc, style):

    a = {}
    for i in range(8):
       a[i] = sc.obj('DaoBasePoints'+str(i))

    arc0 =  GC_MakeArcOfCircle(a[0],a[1],a[2]).Value()
    arc1 =  GC_MakeArcOfCircle(a[2],a[3],a[4]).Value()
    arc2 =  GC_MakeArcOfCircle(a[4],a[5],a[6]).Value()
    arc3 =  GC_MakeArcOfCircle(a[6],a[7],a[0]).Value()

    edge0 = BRepBuilderAPI_MakeEdge(arc0).Edge()
    edge1 = BRepBuilderAPI_MakeEdge(arc1).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(arc2).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(arc3).Edge()

    daoWire =  BRepBuilderAPI_MakeWire(edge0, edge1, edge2, edge3).Wire()

    sc.drawWire(style, 'DaoClassicWire', daoWire)
    
def drawDaoIngWire(sc, style):

    DAO_OFFSET = sc.val('DAO_OFFSET')
    DaoClassicWire = sc.obj('DaoClassicWire')

    tool = BRepOffsetAPI_MakeOffset()
    tool.AddWire(DaoClassicWire)
    tool.Perform(-DAO_OFFSET)
    DaoIngWire = tool.Shape()

    sc.drawWire(style,'DaoIngWire', DaoIngWire)

    ''' todo

    '''
def drawDaoIngPoints(sc, style):

    DaoIngWire = sc.obj('DaoIngWire')

    DaoIngPoints = utilGetShapePoints(DaoIngWire)
    sc.drawPoint(style, 'DaoIngPointsLeft', DaoIngPoints[0], 'pL')
    sc.drawPoint(style, 'DaoIngPointsBegin', DaoIngPoints[1], 'pB')
    sc.drawPoint(style, 'DaoIngPointsRight', DaoIngPoints[2], 'pR')
    sc.drawPoint(style, 'DaoIngPointsEnd', DaoIngPoints[3], 'pE')

def drawDaoYangWire(sc, style):

    DaoIngWire = sc.obj('DaoIngWire')

    DaoYangWire = utilGetZRotatedShape(DaoIngWire, pi)
    sc.drawWire(style, 'DaoYangWire', DaoYangWire)

def drawDaoOffsetCircle(sc, style):
    
    DAO_BASE_RADIUS = sc.val('DAO_BASE_RADIUS')
    DAO_OFFSET = sc.val('DAO_OFFSET')
 
    drawCenteredXYCircle(sc, style, 'DaoOffsetCircle', DAO_BASE_RADIUS + DAO_OFFSET,)

# **********************************************************************************
# **********************************************************************************
# **********************************************************************************

def drawDaoClassicSlide(sc):
    drawDaoBasePoints(sc, 'MAIN')
    drawDaoIngClassicWire(sc, 'MAIN')
    drawDaoBaseCircle(sc,'INFO')

def drawDaoOffsetSlide(sc):
    drawDaoBasePoints(sc, 'HIDE')
    drawDaoClassicWire(sc, 'HIDE')
    drawDaoIngWire(sc, 'MAIN')
    drawDaoIngPoints(sc, 'MAIN')
    drawDaoYangWire(sc, 'INFO')
    drawDaoOffsetCircle(sc, 'INFO')

def drawFocusPoint(sc, style):

    DAO_BASE_RADIUS = sc.val('DAO_BASE_RADIUS')
    
    DaoFocusPoint = gp_Pnt(0,-DAO_BASE_RADIUS/4,0)
    sc.drawPoint(style, 'DaoFocusPoint', DaoFocusPoint, 'F0')

def drawDaoXXXSliceLine(sc, style, XXX, sliceKoef):

    DaoIngPointsLeft = sc.obj('DaoIngPointsLeft') 
    DaoIngPointsBegin = sc.obj('DaoIngPointsBegin') 
    DaoIngPointsRight = sc.obj('DaoIngPointsRight') 
    DaoIngPointsEnd = sc.obj('DaoIngPointsEnd')

    DaoFocusPoint = sc.obj('DaoFocusPoint')
    
    limitAngle = 0
    limitPoint = getPntScale(DaoFocusPoint, DaoIngPointsRight, 1.2)
    BeginAngle = getAngle(DaoFocusPoint, limitPoint, DaoIngPointsBegin)
    endAngle = getAngle(DaoFocusPoint, limitPoint, DaoIngPointsEnd)
    limitKoef = (limitAngle - BeginAngle)/(endAngle - BeginAngle)
    if sliceKoef < limitKoef: #head
        headKoef = (sliceKoef - 0) / (limitKoef - 0)
        BeginX = DaoIngPointsRight.X()
        endX = DaoIngPointsBegin.X()
        deltaX = (endX-BeginX)*(1 - headKoef)
        linePointsBegin = getTranslatedPoint(DaoFocusPoint, deltaX, 0, 0)
        linePointsEnd = getTranslatedPoint(limitPoint, deltaX, 0, 0)
    else: #tail
        tailKoef = (sliceKoef - limitKoef) / (1 - limitKoef)
        tailAngle = -(endAngle * tailKoef)
        linePointsBegin = DaoFocusPoint
        linePointsEnd = getPntRotate(DaoFocusPoint, limitPoint, tailAngle)

    sc.drawLine(style, key, (Dao+'XXX'+SliceLine, linePointsEnd))
    

def drawDaoExampleSliceSlide(sc):

    drawDaoBasePoints(sc, 'HIDE')
    drawDaoClassicWire(sc, 'HIDE')
    drawDaoIngWire(sc, 'MAIN')
    drawDaoIngPoints(sc, 'HIDE')
    drawFocusPoint(sc, 'MAIN')

    DAO_SLICE_EXAMPLE_KOEF = sc.val('DAO_SLICE_EXAMPLE_KOEF')
    drawDaoXXXSliceLine(sc, 'FOCUS', 'Example', DAO_SLICE_EXAMPLE_KOEF) 

    ''' 
    slicePlaneFace = makeVerticalPlaneFace(sliceLine2Points, sc.val('DAO_SLICE_PLANE_HEIGHT'))
    sc.drawWire('sliceFace', slicePlaneFace)

    sliceIntersectPoints =  makeEdgesFacesIntersectPoints(ingWire, slicePlaneFace)
    sc.drawPoints('sliceIntersectPoints',sliceIntersectPoints)

    sliceCircle3Points = makeSliceCircle3Points(sliceIntersectPoints)
    sc.drawCircle('sliceCircle', sliceCircle3Points)

    sc.setStyle('offsetCircle', 'Info')
    sc.setStyle('yangWire', 'Info')
    sc.setStyle('slice', 'Focus')
    '''
# **********************************************************************************
# **********************************************************************************
# **********************************************************************************

def initDaoVals(sc):

    sc.initVal('DAO_BASE_RADIUS', 40)
    sc.initVal('DAO_OFFSET', 3)
    sc.initVal('DAO_SLICE_EXAMPLE_KOEF', 0.5)
    sc.initVal('DAO_SLICE_PLANE_HEIGHT', 30)
    sc.initVal('DAO_SLICE_START_KOEF', 0.03) #todo eliniate
    sc.initVal('DAO_SLICE_END_KOEF', 0.97) #todo eliniate
    sc.initVal('DAO_SLICE_COUNT', 20)
    sc.initVal('DAO_SKINING_SLICES_KOEFS', [0.03, 0.09 , 0.16, 0.24, 0.35, 0.50, 0.70, 0.85])
    sc.initVal('DAO_CASE_HEIGHT', 30)
    sc.initVal('DAO_CASE_DELTA_Z', -20)
    sc.initVal('DAO_CASE_GAP', 1)


if __name__ == '__main__':

    sc = Scene()

    sc.initVal('SLIDE_NUM', 7)
    sc.initVal('SLIDE_NAME', 'dao')

    sc.initVal('SysDecorIsDesk', True)
    sc.initVal('SysDecorIsAxis', True)
    sc.initVal('SysDecorScale', 1)
    sc.initVal('SysDecorScaleB', 5)
    sc.initXYZ('SysDecorDeskD', 0, 0, -60)
    #todo uppercase and only dz param
    
    initDaoVals(sc)
    
    SLIDE_NUM = sc.val('SLIDE_NUM')
    print(SLIDE_NUM) 
    if SLIDE_NUM == 1:
        drawDaoClassicSlide(sc)
    elif SLIDE_NUM == 2:
        drawDaoOffsetSlide(sc)
    elif SLIDE_NUM == 3:
        drawDaoExampleSliceSlide(sc)
    elif SLIDE_NUM == 4:
        drawManySliceSlide(sc)
    elif SLIDE_NUM == 5:
        drawSkiningSurface(sc)

    sc.setColor('ingSurface',(100,35,24,100))
    sc.setColor('yangSurface',(98,100,12,100))
    sc.setColor('caseSurface',(52,51,100,100))

    sc.render()


    '''
               #      r%    g%     b%     op%     pnt  line   mat
    if styleVal == 'StyleInfo':
       styleVal = (   30,   30,   30,    100,     3,     2,  'PLASTIC' )
    elif styleVal == 'StyleMain':
       styleVal = (   10,   10,   90,    100,      3,     4,  'PLASTIC' )
    elif styleVal == 'StyleFocus':
       styleVal = (   90,   10,   10,     30,      3,     2,  'CHROME' )
    elif styleVal == 'stGold':
       styleVal = (   90,   90,   10,    100,      3,     4,  'GOLD'    )
    elif styleVal == 'stFog':
       styleVal = (   90,   90,   90,    30,       3,      4,   'PLASTIC'  )


               #      r%    g%     b%     op%     pnt  line   mat
    if styleVal == 'StyleInfo':
       styleVal = (   30,   30,   30,    100,     3,     2,  'PLASTIC' )
    elif styleVal == 'StyleMain':
       styleVal = (   10,   10,   90,    100,      3,     4,  'PLASTIC' )
    elif styleVal == 'StyleFocus':
       styleVal = (   90,   10,   10,     30,      3,     2,  'CHROME' )
    elif styleVal == 'stGold':
       styleVal = (   90,   90,   10,    100,      3,     4,  'GOLD'    )
    elif styleVal == 'stGold':
       styleVal = (   90,   90,   10,    100,      3,     4,  'GOLD'    )
    elif styleVal == 'stFog':
       styleVal = (   90,   90,   90,    30,       3,      4,   'PLASTIC'  )
    '''
