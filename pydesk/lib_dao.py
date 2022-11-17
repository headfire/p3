from core_draw import *

from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Dir, gp_Vec, gp_Ax1, gp_OZ, gp_GTrsf, gp_Ax2
from OCC.Core.Geom import Geom_TrimmedCurve
from OCC.Core.GeomAPI import GeomAPI_IntCS
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_VERTEX, TopAbs_FACE, TopAbs_EDGE

from OCC.Core.GC import GC_MakeArcOfCircle

from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire,
                                     BRepBuilderAPI_Transform, BRepBuilderAPI_MakeFace,
                                     BRepBuilderAPI_MakeVertex, BRepBuilderAPI_GTransform)
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakeOffset, BRepOffsetAPI_ThruSections
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Common, BRepAlgoAPI_Cut

from math import pi


EQUAL_POINTS_PRECISION = 0.001


def getXYZ(gpPnt):
    return gpPnt.X(), gpPnt.Y(), gpPnt.Z()


def isPointExistInPoints(findingPoint, aPoints):
    for aPoint in aPoints:
        if aPoint.IsEqual(findingPoint, EQUAL_POINTS_PRECISION):
            return True
    return False


def getUniquePoints(aPoints):
    uniquePoints = []
    for aPoint in aPoints:
        if not isPointExistInPoints(aPoint, uniquePoints):
            uniquePoints += [aPoint]
    return uniquePoints


def getPntRotate(pCenter, p, angle):
    ax = gp_Ax1(pCenter, gp_Dir(0, 0, 1))
    pnt = gp_Pnt(p.XYZ())
    pnt.Rotate(ax, angle)
    return pnt


def getPntScale(pCenter, p, scale):
    pnt = gp_Pnt(p.XYZ())
    pnt.Scale(pCenter, scale)
    return pnt


def getTranslatedPoint(aPoint, deltaX, deltaY, deltaZ):
    translatedPoint = gp_Pnt(aPoint.XYZ())
    translatedPoint.Translate(gp_Vec(deltaX, deltaY, deltaZ))
    return translatedPoint


def getAngle(gpPnt0, gpPnt1, gpPnt2):
    v1 = gp_Vec(gpPnt0, gpPnt1)
    v2 = gp_Vec(gpPnt0, gpPnt2)
    return v2.AngleWithRef(v1, gp_Vec(0, 0, 1))


def getShapeItems(shape, topologyType):
    items = []
    ex = TopExp_Explorer(shape, topologyType)
    while ex.More():
        items.append(ex.Current())
        ex.Next()
    return items


def getPointsFromVertexes(vertexes):
    ps = []
    for v in vertexes:
        ps += [BRep_Tool.Pnt(v)]
    return ps


# ********************************************************
# ********************************************************
# ********************************************************


def getShapeMirror(shape):
    transform = gp_Trsf()
    transform.SetMirror(gp_Pnt(0, 0, 0))
    shape = BRepBuilderAPI_Transform(shape, transform).Shape()
    return shape


def getShapeTranslate(shape, x, y, z):
    transform = gp_Trsf()
    transform.SetTranslation(gp_Vec(x, y, z))
    shape = BRepBuilderAPI_Transform(shape, transform).Shape()
    return shape

# *******************************************************************************
# *******************************************************************************
# *******************************************************************************


def makeEdgesFacesIntersectPoints(edgesShape, facesShape):
    def findIntersectPoints(curve, surface):
        ps = []
        tool = GeomAPI_IntCS(curve, surface)
        pCount = tool.NbPoints()
        for i in range(1, pCount + 1):
            ps += [tool.Point(i)]
        return ps

    intersectPoints = []
    aEdges = getShapeItems(edgesShape, TopAbs_EDGE)
    aFaces = getShapeItems(facesShape, TopAbs_FACE)
    for aEdge in aEdges:
        for aFace in aFaces:
            # noinspection PyTypeChecker
            edgeCurves = BRep_Tool.Curve(aEdge)
            edgeTrimmedCurve = Geom_TrimmedCurve(edgeCurves[0], edgeCurves[1], edgeCurves[2])
            # noinspection PyTypeChecker
            faceSurface = BRep_Tool.Surface(aFace)
            foundIntersectPoints = findIntersectPoints(edgeTrimmedCurve, faceSurface)
            intersectPoints += foundIntersectPoints
    return intersectPoints


def utilGetShapePoints(shape):
    shapeVertexes = getShapeItems(shape, TopAbs_VERTEX)
    shapePoints = getPointsFromVertexes(shapeVertexes)
    return getUniquePoints(shapePoints)


def makeOffsetWire(aWire, offset):
    tool = BRepOffsetAPI_MakeOffset()
    tool.AddWire(aWire)
    tool.Perform(offset)
    aOffsetWire = tool.Shape()
    return aOffsetWire


def utilGetZRotatedShape(aShape, angle):
    aTransform = gp_Trsf()
    rotationAxis = gp_OZ()
    aTransform.SetRotation(rotationAxis, angle)
    rotatedShape = BRepBuilderAPI_Transform(aShape, aTransform).Shape()

    return rotatedShape


def utilShapeZScale(shape, scaleK):
    transform = gp_GTrsf()
    transform.SetAffinity(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1), gp_Dir(0, 1, 0)), scaleK)
    shape = BRepBuilderAPI_GTransform(shape, transform).Shape()
    return shape


def getPointsDraw(pointsDict, prefix, pointsCls):

    dr = Draw('daoPointsDraw:dao-slide')
    for key in pointsDict:
        dr.addItem(PointDraw(pointsDict[key]).doCls(pointsCls))

    for key in pointsDict:
        dr.addItem(LabelDraw(pointsDict[key], prefix + str(key)).doCls('info'))

    return dr


# *********************************************************************************
# *********************************************************************************
# *********************************************************************************


class DaoDrawLib(DrawLib):

    def __init__(self):
        self.scaleA = 5
        self.scaleB = 1
        # super().__init__(self.scaleA / self.scaleB, 'A0 M5:1')
        super().__init__()

        self.aBaseRadius = 40
        self.aOffset = 3
        self.aSliceFaceHeight = 30
        self.aSkinningSlicesKs = [0.03, 0.09, 0.16, 0.24, 0.35, 0.50, 0.70, 0.85]
        self.aSliceExampleK = 0.5
        self.aSliceCount = 20
        self.aSurfaceZScale = 0.7
        self.aCaseHeight = 30
        self.aCaseGap = 1

    def getDaoBasePoints(self):

        r = self.aBaseRadius

        r2 = r / 2

        gpPntMinC = gp_Pnt(0, r2, 0)

        origin = gp_Pnt(0, 0, 0)

        ps = {
            0: origin,
            1: getPntRotate(gpPntMinC, origin, -pi / 4),
            2: gp_Pnt(-r2, r2, 0),
            3: getPntRotate(gpPntMinC, origin, -pi / 4 * 3),
            4: gp_Pnt(0, r, 0),
            5: gp_Pnt(r, 0, 0),
            6: gp_Pnt(0, -r, 0),
            7: gp_Pnt(r2, -r2, 0)
        }
        return ps

    def getDaoClassicWire(self):

        p = self.getCached('getDaoBasePoints')

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

    def getDaoOffsetWire(self, offset):

        classicWire = self.getCached('getDaoClassicWire')

        tool = BRepOffsetAPI_MakeOffset()
        tool.AddWire(classicWire)
        tool.Perform(-offset)
        offsetWire = tool.Shape()

        return offsetWire

    def getDaoOffsetPnts(self, offset):

        aWire = self.getCached('getDaoOffsetWire', offset)

        p = utilGetShapePoints(aWire)

        namedPoints = {
            'Left': p[0],
            'Begin': p[1],
            'Right': p[2],
            'End': p[3]
        }

        return namedPoints

    def getDaoSecondOffsetWire(self, offset):

        firstWire = self.getCached('getDaoOffsetWire', offset)
        secondWire = utilGetZRotatedShape(firstWire, pi)

        return secondWire

    def getDaoFocusPnt(self):

        r = self.aBaseRadius

        focusPoint = gp_Pnt(0, -r / 4, 0)

        return focusPoint

    def getDaoSliceLinePnt2(self, offset, sliceK):

        limitPoints = self.getCached('getDaoOffsetPnts', offset)

        beginPoint = limitPoints['Begin']
        rightPoint = limitPoints['Right']
        endPoint = limitPoints['End']

        focusPoint = self.getCached('getDaoFocusPnt')

        limitAngle = 0
        limitPoint = getPntScale(focusPoint, rightPoint, 1.2)
        BeginAngle = getAngle(focusPoint, limitPoint, beginPoint)
        endAngle = getAngle(focusPoint, limitPoint, endPoint)
        limitK = (limitAngle - BeginAngle) / (endAngle - BeginAngle)
        if sliceK < limitK:  # head
            headK = (sliceK - 0) / (limitK - 0)
            BeginX = rightPoint.X()
            endX = beginPoint.X()
            deltaX = (endX - BeginX) * (1 - headK)
            lineBeginPoint = getTranslatedPoint(focusPoint, deltaX, 0, 0)
            lineEndPoint = getTranslatedPoint(limitPoint, deltaX, 0, 0)
        else:  # tail
            tailK = (sliceK - limitK) / (1 - limitK)
            tailAngle = -(endAngle * tailK)
            lineBeginPoint = focusPoint
            lineEndPoint = getPntRotate(focusPoint, limitPoint, tailAngle)

        return lineBeginPoint, lineEndPoint

    def getDaoSliceFacePnts(self, offset, sliceK):

        h = self.aSliceFaceHeight
        beginPoint, endPoint = self.getCached('getDaoSliceLinePnt2', offset, sliceK)

        x1, y1, z1 = getXYZ(beginPoint)
        x2, y2, z2 = getXYZ(endPoint)

        pnt0 = gp_Pnt(x1, y1, -h)
        pnt1 = gp_Pnt(x1, y1, +h)
        pnt2 = gp_Pnt(x2, y2, +h)
        pnt3 = gp_Pnt(x2, y2, -h)

        return [pnt0, pnt1, pnt2, pnt3]

    def getDaoSlicePnts(self, offset, sliceK):

        aWire = self.getCached('getDaoOffsetWire', offset)
        aFacePnts = self.getCached('getDaoSliceFacePnts', offset, sliceK)
        aFace = helperFaceFromPnts(aFacePnts)

        farPoint, nearPoint = makeEdgesFacesIntersectPoints(aWire, aFace)

        return {'Near': nearPoint, 'Far': farPoint}

    def getDaoSliceCirclePnt3(self, offset, sliceK):

        slicePoints = self.getCached('getDaoSlicePnts', offset, sliceK)
        nearPoint = slicePoints['Near']
        farPoint = slicePoints['Far']

        directionVector = gp_Vec(nearPoint, farPoint)
        directionVector.Scale(0.5)
        upVector = gp_Vec(0, 0, directionVector.Magnitude())
        upPoint = gp_Pnt(nearPoint.XYZ())
        upPoint.Translate(directionVector)
        upPoint.Translate(upVector)

        return nearPoint, upPoint, farPoint

    def getDaoSliceCircleWire(self, offset, sliceK):
        pnt1, pnt2, pnt3 = self.getCached('getDaoSliceCirclePnt3', offset, sliceK)
        return helperCircleWire(pnt1, pnt2, pnt3)

    def getDaoSkinningSurface(self, offset):

        limitPoints = self.getCached('getDaoOffsetPnts', offset)
        beginPoint = limitPoints['Begin']
        endPoint = limitPoints['End']

        skinner = BRepOffsetAPI_ThruSections(True)
        skinner.SetSmoothing(True)

        beginVertex = BRepBuilderAPI_MakeVertex(beginPoint).Vertex()
        skinner.AddVertex(beginVertex)

        ks = self.aSkinningSlicesKs
        for i in range(len(ks)):
            sliceWire = self.getCached('getDaoSliceCircleWire', offset, ks[i])
            skinner.AddWire(sliceWire)

        endVertex = BRepBuilderAPI_MakeVertex(endPoint).Vertex()
        skinner.AddVertex(endVertex)

        skinner.Build()
        surface = skinner.Shape()

        return surface

    def getDaoIngSurface(self, offset):
        scale = self.aSurfaceZScale
        sourceSurface = self.getCached('getDaoSkinningSurface', offset)
        scaledSurface = utilShapeZScale(sourceSurface, scale)
        return scaledSurface

    def getDaoYangSurface(self, offset):
        sourceSurface = self.getCached('getDaoIngSurface', offset)
        rotatedSurface = utilGetZRotatedShape(sourceSurface, pi)
        return rotatedSurface

    def getDaoCaseSurface(self):

        r = self.aBaseRadius
        r2 = r * 2
        h = self.aCaseHeight
        h2 = h / 2
        offset = self.aOffset
        gap = self.aCaseGap
        rTop = r + offset + gap

        rSphere = gp_Vec(0, rTop, h2).Magnitude()
        sphere = BRepPrimAPI_MakeSphere(rSphere).Shape()

        limit = BRepPrimAPI_MakeBox(gp_Pnt(-r2, -r2, -h2), gp_Pnt(r2, r2, h2)).Shape()
        step01Surface = BRepAlgoAPI_Common(sphere, limit).Shape()

        step02Surface = getShapeTranslate(step01Surface, 0, 0, -h2)

        cutIngSurface = self.getCached('getDaoIngSurface', offset - gap)
        cutYangSurface = self.getCached('getDaoYangSurface', offset - gap)
        step03Surface = BRepAlgoAPI_Cut(step02Surface, cutIngSurface).Shape()
        step04Surface = BRepAlgoAPI_Cut(step03Surface, cutYangSurface).Shape()

        step05Surface = getShapeTranslate(step04Surface, 0, 0, -h2)

        return step05Surface

    def getDaoBoundPnt3(self, offset):
        r = self.aBaseRadius + offset
        return gp_Pnt(r, 0, 0), gp_Pnt(0, r, 0), gp_Pnt(-r, 0, 0)

    # **********************************************************************************
    # **********************************************************************************
    # **********************************************************************************

    def getDaoClassicSlide(self):

        dr = Draw()

        basePoints = self.getCached('getDaoBasePoints')
        dr.addItem(getPointsDraw(basePoints, 'p', 'main'))

        classicWire = self.getCached('getDaoClassicWire')
        dr.addItem(WireDraw(classicWire).doCls('main'))

        bPnt1, bPnt2, bPnt3 = self.getCached('getDaoBoundPnt3', 0)
        dr.addItem(CircleDraw(bPnt1, bPnt2, bPnt3).doCls('info'))

        return dr

    def getDaoOffsetSlide(self):

        dr = Draw()

        firstWire = self.getCached('getDaoOffsetWire', self.aOffset)
        dr.addItem(WireDraw(firstWire).doCls('main'))

        firstWirePoints = self.getCached('getDaoOffsetPnts', self.aOffset)
        dr.addItem(getPointsDraw(firstWirePoints, 'p', 'main'))

        secondWire = self.getCached('getDaoSecondOffsetWire', self.aOffset)
        dr.addItem(WireDraw(secondWire).doCls('info'))

        bPnt1, bPnt2, bPnt3 = self.getCached('getDaoBoundPnt3', self.aOffset)
        dr.addItem(CircleDraw(bPnt1, bPnt2, bPnt3).doCls('info'))

        return dr

    def getDaoExampleSliceSlide(self):

        dr = Draw()

        # main dao curve
        wire = self.getCached('getDaoOffsetWire', self.aOffset)
        dr.addItem(WireDraw(wire).doCls('main'))

        # focus point
        focus = self.getCached('getDaoFocusPnt')
        dr.addItem(PointDraw(focus).doCls('main'))
        dr.addItem(LabelDraw(focus, 'F').doCls('main'))

        # slice
        k = self.aSliceExampleK

        sliceLineP1, sliceLineP2 = self.getCached('getDaoSliceLinePnt2', self.aOffset, k)
        dr.addItem(LineDraw(sliceLineP1, sliceLineP2).doCls('focus'))

        sliceFacePnts = self.getCached('getDaoSliceFacePnts', self.aOffset, k)
        dr.addItem(FaceDraw(sliceFacePnts).doCls('focus'))

        slicePoints = self.getCached('getDaoSlicePnts', self.aOffset, k)
        dr.addItem(getPointsDraw(slicePoints, 's', 'main'))

        sliceCirclePnt1, sliceCirclePnt2, sliceCirclePnt3 = self.getCached('getDaoSliceCirclePnt3', self.aOffset, k)
        dr.addItem(CircleDraw(sliceCirclePnt1, sliceCirclePnt2, sliceCirclePnt3).doCls('focus'))

        # bound
        bPnt1, bPnt2, bPnt3 = self.getCached('getDaoBoundPnt3', self.aOffset)
        dr.addItem(CircleDraw(bPnt1, bPnt2, bPnt3).doCls('info'))

        return dr

    def getManySliceSlide(self):

        dr = Draw()

        wire = self.getCached('getDaoOffsetWire', self.aOffset)
        dr.addItem(WireDraw(wire).doCls('main'))

        focus = self.getCached('getDaoFocusPnt')
        dr.addItem(PointDraw(focus).doCls('focus'))
        dr.addItem(LabelDraw(focus, 'F').doCls('main'))

        cnt = self.aSliceCount
        bK = 1 / (cnt + 1)
        eK = 1 - 1 / (cnt + 1)
        for i in range(cnt):

            k = bK + i * (eK - bK) / (cnt - 1)

            sliceLineP1, sliceLineP2 = self.getCached('getDaoSliceLinePnt2', self.aOffset, k)
            dr.addItem(LineDraw(sliceLineP1, sliceLineP2).doCls('focus'))

            sPnt1, sPnt2, sPnt3 = self.getCached('getDaoSliceCirclePnt3', self.aOffset, k)
            dr.addItem(CircleDraw(sPnt1, sPnt2, sPnt3).doCls('main'))

        bPnt1, bPnt2, bPnt3 = self.getCached('getDaoBoundPnt3', self.aOffset)
        dr.addItem(CircleDraw(bPnt1, bPnt2, bPnt3).doCls('info'))

        return dr

    def getDaoSkinningSlide(self):

        dr = Draw()

        focus = self.getCached('getDaoFocusPnt')
        dr.addItem(PointDraw(focus).doCls('focus'))
        dr.addItem(LabelDraw(focus, 'F').doCls('main'))

        ks = self.aSkinningSlicesKs
        for i in range(len(ks)):

            k = ks[i]

            sliceLineP1, sliceLineP2 = self.getCached('getDaoSliceLinePnt2', self.aOffset, k)
            dr.addItem(LineDraw(sliceLineP1, sliceLineP2).doCls('focus'))

            sPnt1, sPnt2, sPnt3 = self.getCached('getDaoSliceCirclePnt3', self.aOffset, k)
            dr.addItem(CircleDraw(sPnt1, sPnt2, sPnt3).doCls('main'))

        skinningSurface = self.getCached('getDaoSkinningSurface', self.aOffset)
        dr.addItem(SurfaceDraw(skinningSurface).doCls('focus'))

        bPnt1, bPnt2, bPnt3 = self.getCached('getDaoBoundPnt3', self.aOffset)
        dr.addItem(CircleDraw(bPnt1, bPnt2, bPnt3).doCls('info'))

        return dr

    def getDaoIngYangSlide(self):

        dr = Draw()

        ingSurface = self.getCached('getDaoIngSurface', self.aOffset)
        style = Style(CHROME_MATERIAL, (141/255, 241/255, 95/255))
        dr.addItem(SurfaceDraw(ingSurface).doStl(style))

        yangSurface = self.getCached('getDaoYangSurface', self.aOffset)
        style = Style(CHROME_MATERIAL, (255/255, 100/255, 255/255))
        dr.addItem(SurfaceDraw(yangSurface).doStl(style))

        return dr

    def getDaoCaseSlide(self):

        dr = Draw()

        ingSurface = self.getCached('getDaoIngSurface', self.aOffset)
        style = Style(CHROME_MATERIAL, (141/255, 241/255, 95/255))
        dr.addItem(SurfaceDraw(ingSurface).doStl(style))

        yangSurface = self.getCached('getDaoYangSurface', self.aOffset)
        style = Style(CHROME_MATERIAL, (255/255, 100/255, 255/255))
        dr.addItem(SurfaceDraw(yangSurface).doStl(style))

        caseSurface = self.getCached('getDaoCaseSurface')
        style = Style(CHROME_MATERIAL, (100/255, 100/255, 100/255))
        dr.addItem(SurfaceDraw(caseSurface).doStl(style))

        return dr

    @staticmethod
    def getStyles():
        return [
            ('*:info', Style().do(COLOR, NICE_GRAY_COLOR).do(TRANSPARENCY, 0.5).do(SCALE_GEOM, 0.5)),
            ('*:focus', Style().do(COLOR, NICE_RED_COLOR).do(SCALE_GEOM, 0.7)),
            ('*:focus-surface', Style().do(COLOR, NICE_RED_COLOR).do(TRANSPARENCY, 0.5))
        ]
