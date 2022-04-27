from _desk import DeskDrawLib
from _std import Screen

from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Dir, gp_Vec, gp_Ax1, gp_OZ  # gp_Ax2, gp_GTrsf
# from OCC.Core.Geom import Geom_TrimmedCurve
# from OCC.Core.GeomAPI import GeomAPI_IntCS
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_VERTEX  # TopAbs_FACE, TopAbs_EDGE,

from OCC.Core.GC import GC_MakeArcOfCircle, GC_MakeCircle

from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire,
                                     BRepBuilderAPI_Transform, BRepBuilderAPI_MakeFace
                                     )  # BRepBuilderAPI_GTransform, BRepBuilderAPI_MakeVertex
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakeOffset  # BRepOffsetAPI_ThruSections
# from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox
# from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Common, BRepAlgoAPI_Cut

from math import pi

EQUAL_POINTS_PRECISION = 0.001


def makeCircleWire(aPoint1, aPoint2, aPoint3):
    aCircle = GC_MakeCircle(aPoint1, aPoint2, aPoint3).Value()
    aEdge = BRepBuilderAPI_MakeEdge(aCircle).Edge()
    aWire = BRepBuilderAPI_MakeWire(aEdge).Wire()
    return aWire


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


def getShapeItems(shape, topoType):
    items = []
    ex = TopExp_Explorer(shape, topoType)
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
# *******************************************************************************

'''
def makeEdgesFacesIntersectPoints(edgesShape, facesShape):
    def findIntersectPoints(curve, surface):
        pnts = []
        tool = GeomAPI_IntCS(curve, surface)
        pCount = tool.NbPoints()
        for i in range(1, pCount + 1):
            pnts += [tool.Point(i)]
        return pnts

    intersectPoints = []
    aEdges = getShapeItems(edgesShape, TopAbs_EDGE)
    aFaces = getShapeItems(facesShape, TopAbs_FACE)
    for aEdge in aEdges:
        for aFace in aFaces:
            edgeCurves = BRep_Tool.Curve(aEdge)
            edgeTrimmedCurve = Geom_TrimmedCurve(edgeCurves[0], edgeCurves[1], edgeCurves[2])
            faceSurface = BRep_Tool.Surface(aFace)
            findedIntersectPoints = findIntersectPoints(edgeTrimmedCurve, faceSurface)
            intersectPoints += findedIntersectPoints
    return intersectPoints
'''


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


'''
def slide_06_DaoComplete(sc, r, offset):
    solidDao0 = getSolidDao(r, offset)
    sc.shape(solidDao0, stDao0)
    solidDao1 = getShapeOZRotate(solidDao0, pi)
    sc.shape(solidDao1, stDao1)


def slide_07_DaoWithCase(sc, r, offset, caseH, caseZMove, gap):
    solidDao0 = getSolidDao(r, offset + gap)
    sc.shape(solidDao0, 'StyleDaoIng')
    solidDao1 = getShapeOZRotate(solidDao0, pi)
    sc.shape(solidDao1, 'StyleDaoYang')

    case = getDaoCase(r, offset, caseH)

    case = getShapeTranslate(case, 0, 0, caseZMove)
    sc.shape(case, 'StyleDaoCase')

'''
# *********************************************************************************
# *********************************************************************************
# *********************************************************************************

Todo = None
DAO_BASE_RADIUS = 40
DAO_OFFSET = 3
DAO_SLICE_FACE_HEIGHT = 30
DAO_SKINNING_SLICES_KS = [0.03, 0.09, 0.16, 0.24, 0.35, 0.50, 0.70, 0.85]

'''
def initDaoVals(sc):
    sc.setVal('DAO_BASE_RADIUS', 40)
    sc.setVal('DAO_OFFSET', 3)
    sc.setVal('DAO_SLICE_EXAMPLE_K', 0.5)
    sc.setVal('DAO_SLICE_FACE_HEIGHT', 30)
    sc.setVal('DAO_SLICE_COUNT', 10)
    sc.setVal('DAO_SKINING_SLICES_KS', )
    sc.setVal('DAO_CASE_HEIGHT', 30)
    sc.setVal('DAO_CASE_GAP', 1)
'''


class DaoDrawLib(DeskDrawLib):

    def __init__(self):
        super().__init__(5 / 1, 'A0 M5:1')
        self.aBaseRadius = DAO_BASE_RADIUS
        self.aOffset = DAO_OFFSET
        self.aSliceFaceHeight = DAO_SLICE_FACE_HEIGHT
        self.aSkinningSlicesKs = DAO_SKINNING_SLICES_KS

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

    def getDaoBoundCircleWire(self, offset):

        r = self.aBaseRadius + offset
        return makeCircleWire(gp_Pnt(r, 0, 0), gp_Pnt(0, r, 0), gp_Pnt(-r, 0, 0))

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

    def getDaoOffsetPoints(self, offset):

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

    def getDaoFocusPoint(self):

        r = self.aBaseRadius

        focusPoint = gp_Pnt(0, -r / 4, 0)

        return focusPoint

    def getDaoSliceLine(self, offset, sliceK):

        limitPoints = self.getCached('getDaoOffsetPoints', offset)

        beginPoint = limitPoints['Begin']
        rightPoint = limitPoints['Right']
        endPoint = limitPoints['End']

        focusPoint = self.getCached('getDaoFocusPoint')

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

    def getDaoSliceSurface(self, offset, sliceK):

        h = self.aSliceFaceHeight
        beginPoint, endPoint = self.getCached('getDaoSliceLine', offset, sliceK)

        x1, y1, z1 = getXYZ(beginPoint)
        x2, y2, z2 = getXYZ(endPoint)
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

    '''
    def getDaoSlicePoints(self, offset, sliceK):

        aWire = self.getCached('getDaoOffsetWire', offset)
        aFace = self.getCached('getDaoSliceSurface', offset, sliceK)

        farPoint, nearPoint = makeEdgesFacesIntersectPoints(aWire, aFace)

        return {'Near': nearPoint, 'Far': farPoint}
    '''

    def getDaoSliceWire(self, offset, sliceK):

        slicePoints = self.getCached('getDaoSlicePoints', offset, sliceK)
        nearPoint = slicePoints['Near']
        farPoint = slicePoints['Far']

        directionVector = gp_Vec(nearPoint, farPoint)
        directionVector.Scale(0.5)
        upVector = gp_Vec(0, 0, directionVector.Magnitude())
        upPoint = gp_Pnt(nearPoint.XYZ())
        upPoint.Translate(directionVector)
        upPoint.Translate(upVector)

        return makeCircleWire(nearPoint, upPoint, farPoint)

    '''
    def getDaoSkinningSurface(self, offset):

        limitPoints = self.getCached('getDaoOffsetPoints', offset)
        beginPoint = limitPoints['Begin']
        endPoint = limitPoints['End']

        skinner = BRepOffsetAPI_ThruSections(True)
        skinner.SetSmoothing(True);

        beginVertex = BRepBuilderAPI_MakeVertex(beginPoint).Vertex()
        skinner.AddVertex(beginVertex)

        ks = sc.getVal('')
        for i in range(len(ks)):
            sliceWire = self.getCached('getDaoSliceWire', offset, ks[i])
            skinner.AddWire(sliceWire)

        endVertex = BRepBuilderAPI_MakeVertex(endPoint).Vertex()
        skinner.AddVertex(endVertex)

        skiner.Build()
        surface = skiner.Shape()

        return surface

    '''

    # **********************************************************************************
    # **********************************************************************************
    # **********************************************************************************

    def getDaoPointsDraw(self, pointsDict, prefix, styleName):

        dr = self.makeDraw()
        dr.nm('Point')
        for key in pointsDict:
            dr.add(self.getDeskPoint(pointsDict[key], styleName))

        dr.nm('Label')
        for key in pointsDict:
            dr.add(self.getDeskLabel(pointsDict[key], prefix + str(key), 'InfoStyle'))

        return dr

    def getDaoClassicSlide(self):

        basePoints = self.getCached('getDaoBasePoints')
        classicWire = self.getCached('getDaoClassicWire')
        boundCircleWire = self.getCached('getDaoBoundCircleWire', 0)

        dr = self.makeDraw()

        dr.nm('BasePoints')
        dr.add(self.getDaoPointsDraw(basePoints, 'p', 'MainStyle'))

        dr.nm('ClassicWire')
        dr.add(self.getDeskWire(classicWire, 'MainStyle'))

        dr.nm('BoundCircleWire')
        dr.add(self.getDeskWire(boundCircleWire, 'InfoStyle'))

        return dr

    ''' 
    def getDaoOffsetSlide(sc):
        offset = self.aOffset

        sc.style('Main')
        sc.draw('DaoOffsetWire', offset)

        sc.label('p')
        sc.draw('DaoOffsetPoints', offset)

        sc.style('Info')
        sc.draw('DaoSecondOffsetWire', offset)
        sc.draw('DaoBoundCircleWire', offset)


    def drawDaoExampleSliceSlide(sc):
        offset = sc.getVal('DAO_OFFSET')

        sc.style('Main')
        sc.draw('DaoOffsetWire', offset)

        sc.label('F')
        sc.draw('DaoFocusPoint')

        sc.style('Focus')
        k = sc.getVal('DAO_SLICE_EXAMPLE_K')
        sc.draw('DaoSliceLine', offset, k)
        sc.draw('DaoSliceSurface', offset, k)
        sc.label('x')
        sc.draw('DaoSlicePoints', offset, k)

        sc.draw('DaoSliceWire', offset, k)


    def drawManySliceSlide(sc):
        offset = sc.getVal('DAO_OFFSET')

        sc.style('Main')
        sc.draw('DaoOffsetWire', offset)

        sc.label('F')
        sc.draw('DaoFocusPoint')

        cnt = sc.getVal('DAO_SLICE_COUNT')
        bK = 1 / (cnt + 1)
        eK = 1 - 1 / (cnt + 1)
        for i in range(cnt):
            k = bK + i * (eK - bK) / (cnt - 1)
            sc.style('Focus')
            sc.draw('DaoSliceLine', offset, k)
            sc.style('Main')
            sc.draw('DaoSliceWire', offset, k)


    def drawDaoSkiningSlide(sc):
        offset = sc.getVal('DAO_OFFSET')

        sc.style('Main')
        sc.draw('DaoOffsetWire', offset)

        sc.label('F')
        sc.draw('DaoFocusPoint')

        ks = sc.getVal('DAO_SKINING_SLICES_KS')
        for i in range(len(ks)):
            sc.style('Focus')
            sc.draw('DaoSliceLine', offset, ks[i])
            sc.style('Main')
            sc.draw('DaoSliceWire', offset, ks[i])

        sc.style('Focus')
        sc.draw('DaoSkiningSurface', offset)


    def drawDaoIngYangSlide(sc):
        offset = sc.getVal('DAO_OFFSET')
        sc.style('Main', (100, 35, 24))
        sc.draw('DaoIngSurface', offset)
        sc.style('Main', (52, 51, 100))
        sc.draw('DaoYangSurface', offset)


    def drawDaoCaseSlide(sc):
        offset = sc.getVal('DAO_OFFSET')
        sc.style('Main', (100, 35, 24))
        sc.draw('DaoIngSurface', offset)
        sc.style('Main', (52, 51, 100))
        sc.draw('DaoYangSurface', offset)
        sc.style('Main', (50, 50, 50))
        sc.draw('DaoCaseSurface')


    def utilShapeZScale(shape, scaleK):
        transform = gp_GTrsf()
        transform.SetAffinity(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1), gp_Dir(0, 1, 0)), scaleK)
        shape = BRepBuilderAPI_GTransform(shape, transform).Shape()
        return shape


    def getDaoIngSurface(offset):
        # todo to const
        scaleK = 0.7
        sourceSurface = sc.get('DaoSkiningSurface', offset)
        scaledSurface = utilShapeZScale(sourceSurface, scaleK)
        return scaledSurface


    def getDaoYangSurface(offset):
        sourceSurface = sc.get('DaoIngSurface', offset)
        rotatedSurface = utilGetZRotatedShape(sourceSurface, pi)
        return rotatedSurface

    def getDaoCaseSurface():
        r = sc.getVal('DAO_BASE_RADIUS')
        r2 = r * 2
        h = sc.getVal('DAO_CASE_HEIGHT')
        h2 = h / 2
        offset = sc.getVal('DAO_OFFSET')
        gap = sc.getVal('DAO_CASE_GAP')
        rTop = r + offset + gap

        rSphere = gp_Vec(0, rTop, h2).Magnitude()
        sphere = BRepPrimAPI_MakeSphere(rSphere).Shape()

        limit = BRepPrimAPI_MakeBox(gp_Pnt(-r2, -r2, -h2), gp_Pnt(r2, r2, h2)).Shape()
        step01Surface = BRepAlgoAPI_Common(sphere, limit).Shape()

        step02Surface = getShapeTranslate(step01Surface, 0, 0, -h2)

        cutIngSurface = sc.get('DaoIngSurface', offset - gap)
        cutYangSurface = sc.get('DaoYangSurface', offset - gap)
        step03Surface = BRepAlgoAPI_Cut(step02Surface, cutIngSurface).Shape()
        step04Surface = BRepAlgoAPI_Cut(step03Surface, cutYangSurface).Shape()

        step05Surface = getShapeTranslate(step04Surface, 0, 0, -h2)

        return step05Surface


        # **********************************************************************************
        # **********************************************************************************
        # **********************************************************************************
    
        def initDaoVals(sc):
            sc.setVal('DAO_BASE_RADIUS', 40)
            sc.setVal('DAO_OFFSET', 3)
            sc.setVal('DAO_SLICE_EXAMPLE_K', 0.5)
            sc.setVal('DAO_SLICE_FACE_HEIGHT', 30)
            sc.setVal('DAO_SLICE_COUNT', 10)
            sc.setVal('DAO_SKINING_SLICES_KS', [0.03, 0.09, 0.16, 0.24, 0.35, 0.50, 0.70, 0.85])
            sc.setVal('DAO_CASE_HEIGHT', 30)
            sc.setVal('DAO_CASE_GAP', 1)
    
        '''


if __name__ == '__main__':
    daoLib = DaoDrawLib()
    slide = daoLib.getDaoClassicSlide()
    desk = daoLib.getDeskDrawBoard()
    screen = Screen()
    slide.drawTo(screen)
    desk.drawTo(screen, daoLib.makeMove().setMove(0, 0, -60))
    screen.show()

    ''' 
        sc = Scene(globals())

        sc.setVal('SLIDE_NUM', 2)
        sc.setVal('SLIDE_NAME', 'dao')

        sc.setVal('SCENE_SCALE', '5:1')
        sc.setVal('SCENE_ORIGIN', (0, 0, 60))

        initDaoVals(sc)

        SLIDE_NUM = sc.getVal('SLIDE_NUM')
        if SLIDE_NUM == 0:
            drawDaoClassicSlide(sc)
        elif SLIDE_NUM == 1:
            drawDaoOffsetSlide(sc)
        elif SLIDE_NUM == 2:
            drawDaoExampleSliceSlide(sc)
        elif SLIDE_NUM == 3:
            drawManySliceSlide(sc)
        elif SLIDE_NUM == 4:
            drawDaoSkiningSlide(sc)
        elif SLIDE_NUM == 5:
            drawDaoIngYangSlide(sc)
        elif SLIDE_NUM == 6:
            drawDaoCaseSlide(sc)

        sc.render()

        self.getVal('SLIDE_NAME'), self.getVal('SLIDE_NUM')
            self.setVal('RENDER_TARGET', 'screen')
    
            self.setVal('SCENE_SCALE', '1:1')
            self.setVal('SCENE_IS_DESK', True)
            self.setVal('SCENE_IS_AXIS', True)
            self.setVal('SCENE_ORIGIN', (0,0,0))
    
            self.setVal('SLIDE_NUM', 0)
            self.setVal('SLIDE_NAME', 'noname')
    
            self.styler.setBounds(self.getVal('SCENE_SCALE'), self.getVal('SCENE_ORIGIN'))
    
            self.styler.setStyle('Info')
    
            if self.getVal('SCENE_IS_DESK'):
                self.putToRender( Desk(None, self.styler) )         
            if self.getVal('SCENE_IS_AXIS'):
                self.putToRender( Axis(None, self.styler) )
        '''
