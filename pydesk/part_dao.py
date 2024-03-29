from core_desk import *

from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Dir, gp_Vec, gp_Ax1, gp_OZ, gp_GTrsf, gp_Ax2
from OCC.Core.Geom import Geom_TrimmedCurve
from OCC.Core.GeomAPI import GeomAPI_IntCS
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_VERTEX, TopAbs_FACE, TopAbs_EDGE

from OCC.Core.GC import GC_MakeArcOfCircle

from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace,
                                     BRepBuilderAPI_Transform,
                                     BRepBuilderAPI_MakeVertex, BRepBuilderAPI_GTransform)
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakeOffset, BRepOffsetAPI_ThruSections
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Common, BRepAlgoAPI_Cut

# ***************************************
# Dao setting
# ***************************************

DAO_BASE_RADIUS = 'DAO_BASE_RADIUS'
DAO_OFFSET = 'DAO_OFFSET'
DAO_SLICE_FACE_HEIGHT = 'DAO_SLICE_FACE_HEIGHT'
DAO_SKINNING_SLICES_KS = 'DAO_SKINNING_SLICES_KS'
DAO_SLICE_EXAMPLE_K = 'DAO_SLICE_EXAMPLE_K'
DAO_SLICE_COUNT = 'DAO_SLICE_COUNT'
DAO_SURFACE_Z_SCALE = 'DAO_SURFACE_Z_SCALE'
DAO_CASE_HEIGHT = 'DAO_CASE_HEIGHT'
DAO_CASE_GAP = 'DAO_CASE_GAP'


DAO_DEFAULT = {
    DAO_BASE_RADIUS: 40,
    DAO_OFFSET: 3,
    DAO_SLICE_FACE_HEIGHT: 30,
    DAO_SKINNING_SLICES_KS: [0.03, 0.09, 0.16, 0.24, 0.35, 0.50, 0.70, 0.85],
    DAO_SLICE_EXAMPLE_K: 0.5,
    DAO_SLICE_COUNT: 20,
    DAO_SURFACE_Z_SCALE: 0.7,
    DAO_CASE_HEIGHT: 30,
    DAO_CASE_GAP: 1,
}


def _isPointExistInPoints(findingPoint, aPoints):
    for aPoint in aPoints:
        if IsEqualPnt(aPoint, findingPoint):
            return True
    return False


def _getUniquePoints(aPoints):
    uniquePoints = []
    for aPoint in aPoints:
        if not _isPointExistInPoints(aPoint, uniquePoints):
            uniquePoints += [aPoint]
    return uniquePoints


def _getPntRotate(pCenter, p, angle):
    ax = gp_Ax1(pCenter, gp_Dir(0, 0, 1))
    pnt = gp_Pnt(p.XYZ())
    pnt.Rotate(ax, angle)
    return pnt


def _getPntScale(pCenter, p, scale):
    pnt = gp_Pnt(p.XYZ())
    pnt.Scale(pCenter, scale)
    return pnt


def _getTranslatedPoint(aPoint, deltaX, deltaY, deltaZ):
    translatedPoint = gp_Pnt(aPoint.XYZ())
    translatedPoint.Translate(gp_Vec(deltaX, deltaY, deltaZ))
    return translatedPoint


def _getAngle(gpPnt0, gpPnt1, gpPnt2):
    v1 = gp_Vec(gpPnt0, gpPnt1)
    v2 = gp_Vec(gpPnt0, gpPnt2)
    return v2.AngleWithRef(v1, gp_Vec(0, 0, 1))


def _getShapeItems(shape, topologyType):
    items = []
    ex = TopExp_Explorer(shape, topologyType)
    while ex.More():
        items.append(ex.Current())
        ex.Next()
    return items


def _getPointsFromVertexes(vertexes):
    ps = []
    for v in vertexes:
        ps += [BRep_Tool.Pnt(v)]
    return ps


def _getShapeTranslate(shape, x, y, z):
    transform = gp_Trsf()
    transform.SetTranslation(gp_Vec(x, y, z))
    shape = BRepBuilderAPI_Transform(shape, transform).Shape()
    return shape


def _getIntersectPoints(curve, surface):
    ps = []
    tool = GeomAPI_IntCS(curve, surface)
    pCount = tool.NbPoints()
    for i in range(1, pCount + 1):
        ps += [tool.Point(i)]
    return ps


def _getEdgesFacesIntersectPoints(edgesShape, facesShape):

    intersectPoints = []
    aEdges = _getShapeItems(edgesShape, TopAbs_EDGE)
    aFaces = _getShapeItems(facesShape, TopAbs_FACE)
    for aEdge in aEdges:
        for aFace in aFaces:
            # noinspection PyTypeChecker
            edgeCurves = BRep_Tool.Curve(aEdge)
            edgeTrimmedCurve = Geom_TrimmedCurve(edgeCurves[0], edgeCurves[1], edgeCurves[2])
            # noinspection PyTypeChecker
            faceSurface = BRep_Tool.Surface(aFace)
            foundIntersectPoints = _getIntersectPoints(edgeTrimmedCurve, faceSurface)
            intersectPoints += foundIntersectPoints
    return intersectPoints


def _getShapePoints(shape):
    shapeVertexes = _getShapeItems(shape, TopAbs_VERTEX)
    shapePoints = _getPointsFromVertexes(shapeVertexes)
    return _getUniquePoints(shapePoints)


def _getZRotatedShape(aShape, angle):
    aTransform = gp_Trsf()
    rotationAxis = gp_OZ()
    aTransform.SetRotation(rotationAxis, angle)
    rotatedShape = BRepBuilderAPI_Transform(aShape, aTransform).Shape()

    return rotatedShape


def _getShapeZScale(shape, scaleK):
    transform = gp_GTrsf()
    transform.SetAffinity(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1), gp_Dir(0, 1, 0)), scaleK)
    shape = BRepBuilderAPI_GTransform(shape, transform).Shape()
    return shape


def _getCircleWire(pnt1, pnt2, pnt3):
    geomCircle = GC_MakeCircle(pnt1, pnt2, pnt3).Value()
    edge = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
    return BRepBuilderAPI_MakeWire(edge).Wire()


def _getFaceFromPnts(pnts):
    bWire = BRepBuilderAPI_MakeWire()
    for i in range(len(pnts)):
        bEdge = BRepBuilderAPI_MakeEdge(pnts[i - 1], pnts[i])
        bWire.Add(bEdge.Edge())

    wire = bWire.Wire()
    return BRepBuilderAPI_MakeFace(wire).Face()


# *********************************************************************************
# Compute section
# *********************************************************************************


def ComputeDaoBasePoints():

    r = GetVar(DAO_BASE_RADIUS)

    r2 = r / 2

    gpPntMinC = gp_Pnt(0, r2, 0)

    origin = gp_Pnt(0, 0, 0)

    ps = {
        0: origin,
        1: _getPntRotate(gpPntMinC, origin, -PI / 4),
        2: gp_Pnt(-r2, r2, 0),
        3: _getPntRotate(gpPntMinC, origin, -PI / 4 * 3),
        4: gp_Pnt(0, r, 0),
        5: gp_Pnt(r, 0, 0),
        6: gp_Pnt(0, -r, 0),
        7: gp_Pnt(r2, -r2, 0)
    }
    return ps


def ComputeDaoClassicWire():

    p = Compute(ComputeDaoBasePoints)

    arc0 = GC_MakeArcOfCircle(p[0], p[1], p[2]).Value()
    arc1 = GC_MakeArcOfCircle(p[2], p[3], p[4]).Value()
    arc2 = GC_MakeArcOfCircle(p[4], p[5], p[6]).Value()
    arc3 = GC_MakeArcOfCircle(p[6], p[7], p[0]).Value()

    edge0 = BRepBuilderAPI_MakeEdge(arc0).Edge()
    edge1 = BRepBuilderAPI_MakeEdge(arc1).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(arc2).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(arc3).Edge()

    aWire = BRepBuilderAPI_MakeWire(edge0, edge1, edge2, edge3).Wire()

    return aWire


def ComputeDaoOffsetWire(offset):

    classicWire = Compute(ComputeDaoClassicWire)

    tool = BRepOffsetAPI_MakeOffset()
    tool.AddWire(classicWire)
    tool.Perform(-offset)
    offsetWire = tool.Shape()

    return offsetWire


def ComputeDaoOffsetPnts(offset):

    aWire = Compute(ComputeDaoOffsetWire, offset)

    p = _getShapePoints(aWire)

    namedPoints = {
        'Left': p[0],
        'Begin': p[1],
        'Right': p[2],
        'End': p[3]
    }

    return namedPoints


def ComputeDaoSecondOffsetWire(offset):

    firstWire = Compute(ComputeDaoOffsetWire, offset)
    secondWire = _getZRotatedShape(firstWire, PI)

    return secondWire


def ComputeDaoFocusPnt():

    r = GetVar(DAO_BASE_RADIUS)

    focusPoint = gp_Pnt(0, -r / 4, 0)

    return focusPoint


def ComputeDaoSliceLinePnt2(offset, sliceK):

    limitPoints = Compute(ComputeDaoOffsetPnts, offset)

    beginPoint = limitPoints['Begin']
    rightPoint = limitPoints['Right']
    endPoint = limitPoints['End']

    focusPoint = Compute(ComputeDaoFocusPnt)

    limitAngle = 0
    limitPoint = _getPntScale(focusPoint, rightPoint, 1.2)
    beginAngle = _getAngle(focusPoint, limitPoint, beginPoint)
    endAngle = _getAngle(focusPoint, limitPoint, endPoint)
    limitK = (limitAngle - beginAngle) / (endAngle - beginAngle)
    if sliceK < limitK:  # head
        headK = (sliceK - 0) / (limitK - 0)
        BeginX = rightPoint.X()
        endX = beginPoint.X()
        deltaX = (endX - BeginX) * (1 - headK)
        lineBeginPoint = _getTranslatedPoint(focusPoint, deltaX, 0, 0)
        lineEndPoint = _getTranslatedPoint(limitPoint, deltaX, 0, 0)
    else:  # tail
        tailK = (sliceK - limitK) / (1 - limitK)
        tailAngle = -(endAngle * tailK)
        lineBeginPoint = focusPoint
        lineEndPoint = _getPntRotate(focusPoint, limitPoint, tailAngle)

    return lineBeginPoint, lineEndPoint


def ComputeDaoSliceFacePnts(offset, sliceK):

    h = GetVar(DAO_SLICE_FACE_HEIGHT)
    beginPoint, endPoint = Compute(ComputeDaoSliceLinePnt2, offset, sliceK)

    x1, y1, z1 = beginPoint.X(), beginPoint.Y(), beginPoint.Z()
    x2, y2, z2 = endPoint.X(), endPoint.Y(), endPoint.Z()

    pnt0 = gp_Pnt(x1, y1, -h)
    pnt1 = gp_Pnt(x1, y1, +h)
    pnt2 = gp_Pnt(x2, y2, +h)
    pnt3 = gp_Pnt(x2, y2, -h)

    return [pnt0, pnt1, pnt2, pnt3]


def ComputeDaoSlicePnts(offset, sliceK):

    aWire = Compute(ComputeDaoOffsetWire, offset)
    aFacePnts = Compute(ComputeDaoSliceFacePnts, offset, sliceK)
    aFace = _getFaceFromPnts(aFacePnts)

    farPoint, nearPoint = _getEdgesFacesIntersectPoints(aWire, aFace)

    return {'Near': nearPoint, 'Far': farPoint}


def ComputeDaoSliceCirclePnt3(offset, sliceK):

    slicePoints = Compute(ComputeDaoSlicePnts, offset, sliceK)
    nearPoint = slicePoints['Near']
    farPoint = slicePoints['Far']

    directionVector = gp_Vec(nearPoint, farPoint)
    directionVector.Scale(0.5)
    upVector = gp_Vec(0, 0, directionVector.Magnitude())
    upPoint = gp_Pnt(nearPoint.XYZ())
    upPoint.Translate(directionVector)
    upPoint.Translate(upVector)

    return nearPoint, upPoint, farPoint


def ComputeDaoSliceCircleWire(offset, sliceK):
    pnt1, pnt2, pnt3 = Compute(ComputeDaoSliceCirclePnt3, offset, sliceK)
    return _getCircleWire(pnt1, pnt2, pnt3)


def ComputeDaoSkinningSurface(offset):

    limitPoints = Compute(ComputeDaoOffsetPnts, offset)
    beginPoint = limitPoints['Begin']
    endPoint = limitPoints['End']

    skinner = BRepOffsetAPI_ThruSections(True)
    skinner.SetSmoothing(True)

    beginVertex = BRepBuilderAPI_MakeVertex(beginPoint).Vertex()
    skinner.AddVertex(beginVertex)

    ks = GetVar(DAO_SKINNING_SLICES_KS)
    for i in range(len(ks)):
        sliceWire = Compute(ComputeDaoSliceCircleWire, offset, ks[i])
        skinner.AddWire(sliceWire)

    endVertex = BRepBuilderAPI_MakeVertex(endPoint).Vertex()
    skinner.AddVertex(endVertex)

    skinner.Build()
    surface = skinner.Shape()

    return surface


def ComputeDaoIngSurface(offset):
    scale = GetVar(DAO_SURFACE_Z_SCALE)
    sourceSurface = Compute(ComputeDaoSkinningSurface, offset)
    scaledSurface = _getShapeZScale(sourceSurface, scale)
    return scaledSurface


def ComputeDaoYangSurface(offset):
    sourceSurface = Compute(ComputeDaoIngSurface, offset)
    rotatedSurface = _getZRotatedShape(sourceSurface, PI)
    return rotatedSurface


def ComputeDaoCaseSurface():

    r = GetVar(DAO_BASE_RADIUS)
    r2 = r * 2
    h = GetVar(DAO_CASE_HEIGHT)
    h2 = h / 2
    offset = GetVar(DAO_OFFSET)
    gap = GetVar(DAO_CASE_GAP)
    rTop = r + offset + gap

    rSphere = gp_Vec(0, rTop, h2).Magnitude()
    sphere = BRepPrimAPI_MakeSphere(rSphere).Shape()

    limit = BRepPrimAPI_MakeBox(gp_Pnt(-r2, -r2, -h2), gp_Pnt(r2, r2, h2)).Shape()
    step01Surface = BRepAlgoAPI_Common(sphere, limit).Shape()

    step02Surface = _getShapeTranslate(step01Surface, 0, 0, -h2)

    cutIngSurface = Compute(ComputeDaoIngSurface, offset - gap)
    cutYangSurface = Compute(ComputeDaoYangSurface, offset - gap)
    step03Surface = BRepAlgoAPI_Cut(step02Surface, cutIngSurface).Shape()
    step04Surface = BRepAlgoAPI_Cut(step03Surface, cutYangSurface).Shape()

    step05Surface = _getShapeTranslate(step04Surface, 0, 0, -h2)

    return step05Surface


def ComputeDaoBoundPnt3(offset):
    r = GetVar(DAO_BASE_RADIUS) + offset
    return gp_Pnt(r, 0, 0), gp_Pnt(0, r, 0), gp_Pnt(-r, 0, 0)


# *********************************************************************************
# Draw section
# *********************************************************************************


def DrawDaoPoints(pointsDict, prefix):
    for key in pointsDict:
        DrawPoint(pointsDict[key])

    for key in pointsDict:
        DrawLabel(pointsDict[key], prefix + str(key))


def DrawDaoClassicSlide():

    SetStyle(DESK_MAIN_STYLE)

    basePoints = Compute(ComputeDaoBasePoints)
    DrawDaoPoints(basePoints, 'p')

    classicWire = Compute(ComputeDaoClassicWire)
    DrawWire(classicWire)

    SetStyle(DESK_INFO_STYLE)

    bPnt1, bPnt2, bPnt3 = Compute(ComputeDaoBoundPnt3, 0)
    DrawCircle(bPnt1, bPnt2, bPnt3)


def DrawDaoOffsetSlide():

    SetStyle(DESK_MAIN_STYLE)

    firstWire = Compute(ComputeDaoOffsetWire, GetVar(DAO_OFFSET))
    DrawWire(firstWire)

    firstWirePoints = Compute(ComputeDaoOffsetPnts, GetVar(DAO_OFFSET))
    DrawDaoPoints(firstWirePoints, 'p')

    SetStyle(DESK_INFO_STYLE)

    secondWire = Compute(ComputeDaoSecondOffsetWire, GetVar(DAO_OFFSET))
    DrawWire(secondWire)

    bPnt1, bPnt2, bPnt3 = Compute(ComputeDaoBoundPnt3, GetVar(DAO_OFFSET))
    DrawCircle(bPnt1, bPnt2, bPnt3)


def DrawDaoExampleSliceSlide():

    SetStyle(DESK_MAIN_STYLE)

    # main dao curve
    wire = Compute(ComputeDaoOffsetWire, GetVar(DAO_OFFSET))
    DrawWire(wire)

    # focus point
    focus = Compute(ComputeDaoFocusPnt)
    DrawPoint(focus)
    DrawLabel(focus, 'F')

    # slice
    k = GetVar(DAO_SLICE_EXAMPLE_K)

    SetStyle(DESK_FOCUS_STYLE)

    sliceLineP1, sliceLineP2 = Compute(ComputeDaoSliceLinePnt2, GetVar(DAO_OFFSET), k)
    DrawLine(sliceLineP1, sliceLineP2)

    sliceFacePnts = Compute(ComputeDaoSliceFacePnts, GetVar(DAO_OFFSET), k)
    face = _getFaceFromPnts(sliceFacePnts)
    DrawSurface(face)

    SetStyle(DESK_MAIN_STYLE)

    slicePoints = Compute(ComputeDaoSlicePnts, GetVar(DAO_OFFSET), k)
    DrawDaoPoints(slicePoints, 's')

    SetStyle(DESK_FOCUS_STYLE)

    sliceCirclePnt1, sliceCirclePnt2, sliceCirclePnt3 = Compute(ComputeDaoSliceCirclePnt3, GetVar(DAO_OFFSET), k)
    DrawCircle(sliceCirclePnt1, sliceCirclePnt2, sliceCirclePnt3)

    SetStyle(DESK_INFO_STYLE)

    # bound
    bPnt1, bPnt2, bPnt3 = Compute(ComputeDaoBoundPnt3, GetVar(DAO_OFFSET))
    DrawCircle(bPnt1, bPnt2, bPnt3)


def DrawManySliceSlide():

    SetStyle(DESK_MAIN_STYLE)

    wire = Compute(ComputeDaoOffsetWire, GetVar(DAO_OFFSET))
    DrawWire(wire)

    focus = Compute(ComputeDaoFocusPnt)
    DrawPoint(focus)
    DrawLabel(focus, 'F')

    cnt = GetVar(DAO_SLICE_COUNT)
    bK = 1 / (cnt + 1)
    eK = 1 - 1 / (cnt + 1)
    for i in range(cnt):

        k = bK + i * (eK - bK) / (cnt - 1)

        SetStyle(DESK_FOCUS_STYLE)

        sliceLineP1, sliceLineP2 = Compute(ComputeDaoSliceLinePnt2, GetVar(DAO_OFFSET), k)
        DrawLine(sliceLineP1, sliceLineP2)

        SetStyle(DESK_MAIN_STYLE)

        sPnt1, sPnt2, sPnt3 = Compute(ComputeDaoSliceCirclePnt3, GetVar(DAO_OFFSET), k)
        DrawCircle(sPnt1, sPnt2, sPnt3)

    SetStyle(DESK_INFO_STYLE)

    bPnt1, bPnt2, bPnt3 = Compute(ComputeDaoBoundPnt3, GetVar(DAO_OFFSET))
    DrawCircle(bPnt1, bPnt2, bPnt3)


def DrawDaoSkinningSlide():

    SetStyle(DESK_MAIN_STYLE)

    focus = Compute(ComputeDaoFocusPnt)
    DrawPoint(focus)
    DrawLabel(focus, 'F')

    ks = GetVar(DAO_SKINNING_SLICES_KS)
    for i in range(len(ks)):

        k = ks[i]

        SetStyle(DESK_FOCUS_STYLE)

        sliceLineP1, sliceLineP2 = Compute(ComputeDaoSliceLinePnt2, GetVar(DAO_OFFSET), k)
        DrawLine(sliceLineP1, sliceLineP2)

        SetStyle(DESK_MAIN_STYLE)

        sPnt1, sPnt2, sPnt3 = Compute(ComputeDaoSliceCirclePnt3, GetVar(DAO_OFFSET), k)
        DrawCircle(sPnt1, sPnt2, sPnt3)

    SetStyle(DESK_FOCUS_STYLE)

    skinningSurface = Compute(ComputeDaoSkinningSurface, GetVar(DAO_OFFSET))
    DrawSurface(skinningSurface)

    SetStyle(DESK_INFO_STYLE)

    bPnt1, bPnt2, bPnt3 = Compute(ComputeDaoBoundPnt3, GetVar(DAO_OFFSET))
    DrawCircle(bPnt1, bPnt2, bPnt3)


def DrawDaoIngYangSlide():

    ingSurface = Compute(ComputeDaoIngSurface, GetVar(DAO_OFFSET))
    SetSolidBrash(ChromeBrash(DARK_MAGENTA_COLOR))
    DrawSolid(ingSurface)

    yangSurface = Compute(ComputeDaoYangSurface, GetVar(DAO_OFFSET))
    SetSolidBrash(ChromeBrash(DARK_CYAN_COLOR))
    DrawSolid(yangSurface)


def DrawDaoCaseSlide():

    ingSurface = Compute(ComputeDaoIngSurface, GetVar(DAO_OFFSET))
    SetSolidBrash(ChromeBrash(DARK_MAGENTA_COLOR))
    DrawSolid(ingSurface)

    yangSurface = Compute(ComputeDaoYangSurface, GetVar(DAO_OFFSET))
    SetSolidBrash(ChromeBrash(DARK_CYAN_COLOR))
    DrawSolid(yangSurface)

    caseSurface = Compute(ComputeDaoCaseSurface)
    SetSolidBrash(ChromeBrash(DARK_GRAY_COLOR))
    DrawSolid(caseSurface)


SetStyle(DAO_DEFAULT)


# *********************************************************************************
# Test section
# *********************************************************************************


if __name__ == "__main__":

    SetScale(5, 1)
    DrawDesk(-50)
    # DrawDaoClassicSlide()
    # DrawDaoOffsetSlide()
    # DrawDaoExampleSliceSlide()
    # DrawManySliceSlide()
    # DrawDaoSkinningSlide()
    # DrawDaoIngYangSlide()
    DrawDaoCaseSlide()
    Show()
