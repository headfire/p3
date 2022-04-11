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



# *******************************************************************************
# *******************************************************************************
# *******************************************************************************
# *******************************************************************************



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
    theTransform.SetRotation(rotationAxis, angle)
    rotatedShape =  BRepBuilderAPI_Transform(theShape, theTransform).Shape()

    return rotatedShape




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



# *********************************************************************************
# *********************************************************************************
# *********************************************************************************

def drawDaoBoundCircle_XXX(sc, style, XXX ,r):

    sc.drawCircle(style, 'drawDaoBoundCircle_'+XXX, ( gp_Pnt(r,0,0), gp_Pnt(0,r,0), gp_Pnt(-r,0,0)))
    #todo drawCircle -> drawWire


def drawDaoBasePoint_NNN(sc, style):

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
        NNN = str(key)
        sc.drawPoint(style, 'DaoBasePoint_'+NNN, p[key], 'p'+NNN)

def drawDaoClassicWire(sc, style):

    a = {}
    for i in range(8):
       NNN = str(i)
       a[i] = sc.obj('DaoBasePoint_'+NNN)

    arc0 =  GC_MakeArcOfCircle(a[0],a[1],a[2]).Value()
    arc1 =  GC_MakeArcOfCircle(a[2],a[3],a[4]).Value()
    arc2 =  GC_MakeArcOfCircle(a[4],a[5],a[6]).Value()
    arc3 =  GC_MakeArcOfCircle(a[6],a[7],a[0]).Value()

    edge0 = BRepBuilderAPI_MakeEdge(arc0).Edge()
    edge1 = BRepBuilderAPI_MakeEdge(arc1).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(arc2).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(arc3).Edge()

    theWire =  BRepBuilderAPI_MakeWire(edge0, edge1, edge2, edge3).Wire()

    sc.drawWire(style, 'DaoClassicWire', theWire)
    
def drawDaoIngWire(sc, style):

    DAO_OFFSET = sc.val('DAO_OFFSET')
    DaoClassicWire = sc.obj('DaoClassicWire')

    tool = BRepOffsetAPI_MakeOffset()
    tool.AddWire(DaoClassicWire)
    tool.Perform(-DAO_OFFSET)
    DaoIngWire = tool.Shape()

    sc.drawWire(style,'DaoIngWire', DaoIngWire)

def drawDaoIngPoint_SSS(sc, style):

    theWire = sc.obj('DaoIngWire')

    thePoints = utilGetShapePoints(theWire)
    sc.drawPoint(style, 'DaoIngPoint_LEFT', thePoints[0], 'pLeft')
    sc.drawPoint(style, 'DaoIngPoint_BEGIN', thePoints[1], 'pBegin')
    sc.drawPoint(style, 'DaoIngPoint_RIGHT', thePoints[2], 'pRight')
    sc.drawPoint(style, 'DaoIngPoint_END', thePoints[3], 'pEnd')

def drawDaoYangWire(sc, style):

    DaoIngWire = sc.obj('DaoIngWire')

    DaoYangWire = utilGetZRotatedShape(DaoIngWire, pi)
    sc.drawWire(style, 'DaoYangWire', DaoYangWire)
    
def drawDaoFocusPoint(sc, style):

    r = sc.val('DAO_BASE_RADIUS')
    focusPoint = gp_Pnt(0,-r/4,0)
    sc.drawPoint(style, 'DaoFocusPoint', focusPoint, 'F0')
    
def drawDaoSliceFace_XXX(sc, style, XXX):

    h = sc.val('DAO_SLICE_FACE_HEIGHT')
    beginPoint, endPoint = sc.obj('DaoSliceLine_'+XXX)

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
    
    sc.drawSurface(style, 'DaoSliceFace_'+XXX, face)    

def  drawDaoSlicePoint_XXX_SSS(sc, style, XXX):

    theWire = sc.obj('DaoIngWire')
    theFace = sc.obj('DaoSliceFace_'+XXX)
    
    farPoint, nearPoint =  makeEdgesFacesIntersectPoints(theWire, theFace)
    
    sc.drawPoint(style, 'DaoSlicePoint_'+XXX +'_NEAR', nearPoint, 'pNear')
    sc.drawPoint(style, 'DaoSlicePoint_'+XXX +'_FAR', farPoint, 'pFar')

def drawDaoSliceWire_XXX(sc, style, XXX):

    nearPoint = sc.obj('DaoSlicePoint_'+XXX+'_NEAR')
    farPoint = sc.obj('DaoSlicePoint_'+XXX+'_FAR')

    directionVector = gp_Vec(nearPoint, farPoint)
    directionVector.Scale(0.5)
    upVector = gp_Vec(0,0,directionVector.Magnitude())
    upPoint = gp_Pnt(nearPoint.XYZ())
    upPoint.Translate(directionVector)
    upPoint.Translate(upVector)
    
    sliceCircle = GC_MakeCircle(nearPoint, upPoint, farPoint).Value()
    sliceEdge = BRepBuilderAPI_MakeEdge(sliceCircle).Edge()
    sliceWire =  BRepBuilderAPI_MakeWire(sliceEdge).Wire()
    
    sc.drawWire(style, 'DaoSliceWire_'+XXX, sliceWire)

def drawDaoSkiningSurface(sc, style):
    
    skiner = BRepOffsetAPI_ThruSections(True)
    skiner.SetSmoothing(True);
    
    beginPoint = sc.obj('DaoIngPoint_BEGIN')
    beginVertex = BRepBuilderAPI_MakeVertex(beginPoint).Vertex()
    skiner.AddVertex(beginVertex)

    ks = sc.val('DAO_SKINING_SLICES_KOEFS')
    for i in range(len(ks)):
          skiner.AddWire(sc.obj('DaoSliceWire_'+str(i)))

    endPoint = sc.obj('DaoIngPoint_END')
    endVertex = BRepBuilderAPI_MakeVertex(endPoint).Vertex()
    skiner.AddVertex(endVertex)

    skiner.Build()
    surface = skiner.Shape()
   
    sc.drawSurface(style, 'DaoSkiningSurface', surface)


def drawDaoDropsSuface_XXX_NNN(sc, XXX, offset):

    drawDaoBasePoint_NNN(sc, 'HIDE')
    drawDaoClassicWire(sc, 'HIDE')
    drawDaoIngWire(sc, 'HIDE', offset)
    drawDaoIngPoint_SSS(sc, 'HIDE', offset)
    drawDaoFocusPoint(sc, 'HIDE')

    ks = sc.val('DAO_SKINING_SLICES_KOEFS')
    for i in range(len(ks)):
        YYY = str(i)
        drawDaoSliceLine_XXX(sc, 'HIDE', XXX+'_'+YYY, ks[i]) 
        drawDaoSliceFace_XXX(sc, 'HIDE', XXX+'_'+YYY)
        drawDaoSlicePoint_XXX_SSS(sc, 'HIDE', XXX+'_'+YYY)
        drawDaoSliceWire_XXX(sc, 'HIDE', XXX+'_'+YYY)
        
    drawDaoSkiningSurface(sc, 'FOCUS')
    drawDaoIngSurface_XXX(sc, 'MAIN', XXX,(100,35,24,100))
    drawDaoYangSurface_XXX(sc, 'MAIN', XXX ,(98,100,12,100))


# **********************************************************************************
# **********************************************************************************
# **********************************************************************************

def drawDaoClassicSlide(sc):

    drawDaoBasePoint_NNN(sc, 'MAIN')
    drawDaoClassicWire(sc, 'MAIN')

    r = sc.val('DAO_BASE_RADIUS')
    drawDaoBoundCircle_XXX(sc, 'INFO', 'BASE', r)

def drawDaoOffsetSlide(sc):

    drawDaoBasePoint_NNN(sc, 'HIDE')
    drawDaoClassicWire(sc, 'HIDE')
    drawDaoIngWire(sc, 'MAIN')
    drawDaoIngPoint_SSS(sc, 'MAIN')
    drawDaoYangWire(sc, 'INFO')

    r = sc.val('DAO_BASE_RADIUS')
    offset = sc.val('DAO_OFFSET')
    drawDaoBoundCircle_XXX(sc, 'INFO', 'OFFSET', r + offset)


def drawDaoSliceLine_XXX(sc, style, XXX, sliceKoef):

    leftPoint = sc.obj('DaoIngPoint_LEFT') 
    beginPoint = sc.obj('DaoIngPoint_BEGIN') 
    rightPoint = sc.obj('DaoIngPoint_RIGHT') 
    endPoint = sc.obj('DaoIngPoint_END')

    focusPoint = sc.obj('DaoFocusPoint')
    
    limitAngle = 0
    limitPoint = getPntScale(focusPoint, rightPoint, 1.2)
    BeginAngle = getAngle(focusPoint, limitPoint, beginPoint)
    endAngle = getAngle(focusPoint, limitPoint, endPoint)
    limitKoef = (limitAngle - BeginAngle)/(endAngle - BeginAngle)
    if sliceKoef < limitKoef: #head
        headKoef = (sliceKoef - 0) / (limitKoef - 0)
        BeginX = rightPoint.X()
        endX = beginPoint.X()
        deltaX = (endX-BeginX)*(1 - headKoef)
        lineBeginPoint = getTranslatedPoint(focusPoint, deltaX, 0, 0)
        lineEndPoint = getTranslatedPoint(limitPoint, deltaX, 0, 0)
    else: #tail
        tailKoef = (sliceKoef - limitKoef) / (1 - limitKoef)
        tailAngle = -(endAngle * tailKoef)
        lineBeginPoint = focusPoint
        lineEndPoint = getPntRotate(focusPoint, limitPoint, tailAngle)

    sc.drawLine(style, 'DaoSliceLine_'+XXX, (lineBeginPoint, lineEndPoint))

    
def drawDaoExampleSliceSlide(sc):

    drawDaoBasePoint_NNN(sc, 'HIDE')
    drawDaoClassicWire(sc, 'HIDE')
    drawDaoIngWire(sc, 'MAIN')
    drawDaoIngPoint_SSS(sc, 'HIDE')
    drawDaoFocusPoint(sc, 'MAIN')

    k = sc.val('DAO_SLICE_EXAMPLE_KOEF')
    drawDaoSliceLine_XXX(sc, 'FOCUS', 'EXAMPLE', k) 
    drawDaoSliceFace_XXX(sc, 'FOCUS', 'EXAMPLE')
    drawDaoSlicePoint_XXX_SSS(sc, 'FOCUS', 'EXAMPLE')
    drawDaoSliceWire_XXX(sc, 'FOCUS', 'EXAMPLE')

def drawManySliceSlide(sc):

    drawDaoBasePoint_NNN(sc, 'HIDE')
    drawDaoClassicWire(sc, 'HIDE')
    drawDaoIngWire(sc, 'MAIN')
    drawDaoIngPoint_SSS(sc, 'HIDE')
    drawDaoFocusPoint(sc, 'MAIN')

    cnt = sc.val('DAO_SLICE_COUNT')
    bK = 1/(cnt+1)
    eK = 1 - 1/(cnt+1)
    for i in range(cnt):
        k = bK + i * (eK - bK)/(cnt-1)
        XXX = str(i)
        drawDaoSliceLine_XXX(sc, 'FOCUS', XXX, k) 
        drawDaoSliceFace_XXX(sc, 'HIDE', XXX)
        drawDaoSlicePoint_XXX_SSS(sc, 'HIDE', XXX)
        drawDaoSliceWire_XXX(sc, 'MAIN', XXX)

def  drawDaoSkiningSlide(sc):

    drawDaoBasePoint_NNN(sc, 'HIDE')
    drawDaoClassicWire(sc, 'HIDE')
    drawDaoIngWire(sc, 'MAIN')
    drawDaoIngPoint_SSS(sc, 'HIDE')
    drawDaoFocusPoint(sc, 'MAIN')

    ks = sc.val('DAO_SKINING_SLICES_KOEFS')
    for i in range(len(ks)):
        XXX = str(i)
        drawDaoSliceLine_XXX(sc, 'FOCUS', XXX, ks[i]) 
        drawDaoSliceFace_XXX(sc, 'HIDE', XXX)
        drawDaoSlicePoint_XXX_SSS(sc, 'HIDE', XXX)
        drawDaoSliceWire_XXX(sc, 'MAIN', XXX)
        
    drawDaoSkiningSurface(sc, 'FOCUS')


def drawDaoIngYangSlide (sc):

    offset = sc.val('DAO_OFFSET')
    drawDropsSurface_XXX_SSS(sc, 'MAIN', 'Standart' , offset)    
    sc.setColor('DaoDropSurface_STANDART_ING', (100,35,24,100))
    sc.setColor('DaoDropSurface_STANDART_YANG', (52,51,100,100))

def drawDaoCaseSlide (sc):

    offset = sc.val('DAO_OFFSET')
    drawDropsSurface_XXX_SSS(sc, 'MAIN', 'Standart' , offset)    
    
    sc.setColor('DaoDropsSurface_STANDART_ING', (100,35,24,100))
    sc.setColor('DaoDropsSurface_STANDART_YANG', (52,51,100,100))
    
    drawDaoCaseSurface(sc, 'MAIN')    
    sc.SetColor('DaoCaseSurface', (52,  51, 100, 100) )    


def utilShapeZScale(shape, scaleK):
    transform = gp_GTrsf()
    transform.SetAffinity(gp_Ax2(gp_Pnt(0,0,0), gp_Dir(0,0,1),gp_Dir(0,1,0)), scaleK)
    shape =  BRepBuilderAPI_GTransform(shape, transform).Shape()
    return shape

def drawDaoIngSurface(sc, style, color):
    scaleK = 0.7
    sourceSurface = sc.obj('DaoSkiningSurface')     
    scaledSurface = utilShapeZScale(sourceSurface, scaleK)
    sc.drawSurface(style,'DaoIngSurface', scaledSurface)
    sc.setColor('DaoIngSurface',color)

def drawDaoYangSurface(sc, style, color):
    scaleK = 0.7
    sourceSurface = sc.obj('DaoIngSurface')     
    rotatedSurface =  utilGetZRotatedShape(sourceSurface, pi)
    sc.drawSurface(style,'DaoYangSurface', rotatedSurface)
    sc.setColor('DaoYangSurface',color)

#todo offset to dao_gap/2
    
def drawDaoCaseSurface(sc, style):
        
    r = sc.val('DAO_BASE_RADIUS')
    r2 = r*2
    h = sc.val('DAO_CASE_HEIGHT')
    h2 = h/2
    offset = sc.val('DAO_OFFSET')
    gap = sc.val('DAO_CASE_GAP')
    rTop = r + offset + gap

    rSphere = gp_Vec(0,rTop,h2).Magnitude()
    sphere = BRepPrimAPI_MakeSphere(rSphere).Shape()

    limit = BRepPrimAPI_MakeBox( gp_Pnt(-r2, -r2, -h2), gp_Pnt(r2, r2, h2) ).Shape()
    step01Surface = BRepAlgoAPI_Common(sphere, limit).Shape()

    step02Surface = getShapeTranslate(step01Surface, 0,0,-h2)

    drawDropsSurface_XXX_SSS(sc, 'HIDE', 'WithGap', offset+gap)    
    step03Surface = BRepAlgoAPI_Cut(step02Surface, sc.obj('DaoIngYangSurface_WithGap_ING')).Shape()
    step04Surface = BRepAlgoAPI_Cut(step03Surface, sc.obj('DaoIngYangSurface_WithGap_YANG')).Shape()

    step05Surface = getShapeTranslate(step04Surface, 0,0, -h2)

    sc.drawSurface(style,'DaoCaseSurface', step05Surface)
    sc.setColor('DaoCaseSurface',color)


# **********************************************************************************
# **********************************************************************************
# **********************************************************************************

def initDaoVals(sc):

    sc.initVal('DAO_BASE_RADIUS', 40)
    sc.initVal('DAO_OFFSET', 3)
    sc.initVal('DAO_SLICE_EXAMPLE_KOEF', 0.5)
    sc.initVal('DAO_SLICE_FACE_HEIGHT', 30)
    sc.initVal('DAO_SLICE_COUNT', 10)
    sc.initVal('DAO_SKINING_SLICES_KOEFS', [0.03, 0.09 , 0.16, 0.24, 0.35, 0.50, 0.70, 0.85])
    sc.initVal('DAO_CASE_HEIGHT', 30)
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
        drawDaoSkiningSlide(sc)
    elif SLIDE_NUM == 6:
        drawDaoIngYangSlide(sc)
    elif SLIDE_NUM == 7:
        drawDaoCaseSlide(sc)

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
