from OCC.Core.GC import GC_MakeCircle
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_TypeOfColor
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_Transform
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeBox, \
    BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeCone, BRepPrimAPI_MakeTorus
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepTools import BRepTools_WireExplorer
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Vec
from OCC.Core.Graphic3d import Graphic3d_NameOfMaterial, Graphic3d_MaterialAspect

from device import WebDevice, StlDevice

from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Vec, gp_Ax1, gp_Trsf
from OCC.Display.SimpleGui import init_display


DEFAULT_NORMED_COLOR = 0.5, 0.5, 0.5
DEFAULT_MATERIAL_TYPE = 'CHROME'
DEFAULT_NORMED_TRANSPARENCY = 0.0

WOOD_COLOR = 208, 117, 28
PAPER_COLOR = 230, 230, 230
STEEL_COLOR = 100, 100, 100

NICE_WHITE_COLOR = 240, 240, 240
NICE_GRAY_COLOR = 100, 100, 100
NICE_RED_COLOR = 200, 30, 30
NICE_BLUE_COLOR = 100, 100, 255
NICE_YELLOW_COLOR = 255, 255, 100
NICE_ORIGINAL_COLOR = 241, 79, 160

AO_SIZE_XYZ = 1189, 841, 1

BRASS_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_BRASS,
BRONZE_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_BRONZE,
COPPER_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_COPPER,
GOLD_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_GOLD,
PEWTER_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_PEWTER,
PLASTER_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_PLASTER,
PLASTIC_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_PLASTIC,
SILVER_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_SILVER,
STEEL_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_STEEL,
STONE_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_STONE,
SHINY_PLASTIC_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_SHINY_PLASTIC,
SATIN_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_SATIN,
METALIZED_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_METALIZED,
NEON_GNC_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_NEON_GNC,
CHROME_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_CHROME,
ALUMINIUM_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_ALUMINIUM,
OBSIDIAN_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_OBSIDIAN,
NEON_PHC_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_NEON_PHC,
JADE_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_JADE,
CHARCOAL_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_CHARCOAL,
WATER_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_WATER,
GLASS_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_GLASS,
DIAMOND_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_DIAMOND,
TRANSPARENT_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_TRANSPARENT,
DEFAULT_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_DEFAULT

def _checkObj(aObj, aClass):
    if not isinstance(aObj, aClass):
        raise Exception('EXPECTED ' + aClass.__name__ + '  - REAL ' + aObj.__class__.__name__)


def _getValue(aValue, aDefaultValue):
    if aValue is not None:
        return aValue
    return aDefaultValue


def _getVectorTangentToCurveAtPoint(edge, uRatio):
    aCurve, aFP, aLP = BRep_Tool.Curve(edge)
    aP = aFP + (aLP - aFP) * uRatio
    v1 = gp_Vec()
    p1 = gp_Pnt()
    aCurve.D1(aP, p1, v1)
    return v1


def _getWireStartPointAndTangentDir(wire):
    ex = BRepTools_WireExplorer(wire)
    edge = ex.Current()
    vertex = ex.CurrentVertex()
    v = _getVectorTangentToCurveAtPoint(edge, 0)
    return BRep_Tool.Pnt(vertex), gp_Dir(v)


class Position:
    def __init__(self):
        self.trsf = gp_Trsf()

    def next(self, nextChange):
        self.trsf *= nextChange.trsf
        return self

    def _dump(self):
        for iRow in range(1, 4):
            prn = ''
            for iCol in range(1, 5):
                prn += '  ' + str(self.trsf.Value(iRow, iCol))
            print(prn)

class Translate(Position):
    def __init__(self, dx, dy, dz):
        super().__init__()
        self.trsf.SetTranslation(gp_Vec(dx, dy, dz))

class Rotate(Position):
    def __init__(self, pntAxFrom, pntAxTo, angle):
        super().__init__()
        ax1 = gp_Ax1(pntAxFrom, gp_Dir(gp_Vec(pntAxFrom, pntAxTo)))
        self.trsf.SetRotation(ax1, angle)

class Direct(Position):
    def __init__(self, pntFrom, pntTo):
        super().__init__()

        dirVec = gp_Vec(pntFrom, pntTo)
        targetDir = gp_Dir(dirVec)

        rotateAngle = gp_Dir(0, 0, 1).Angle(targetDir)
        if not gp_Dir(0, 0, 1).IsParallel(targetDir, 0.001):
            rotateDir = gp_Dir(0, 0, 1)
            rotateDir.Cross(targetDir)
        else:
            rotateDir = gp_Dir(0, 1, 0)

        self.trsf.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), rotateDir), rotateAngle)
        self.trsf.SetTranslationPart(gp_Vec(gp_Pnt(0, 0, 0), pntFrom))


DESK_HEIGHT = 20
DESK_BORDER_SIZE = 60
DESK_PAPER_SIZE = 1189, 841, 1
DESK_PIN_OFFSET = 30
DESK_PIN_RADIUS = 10
DESK_PIN_HEIGHT = 2
DESK_DEFAULT_DRAW_AREA_SIZE = 400

BASE_POINT_RADIUS = 5
BASE_LINE_RADIUS = BASE_POINT_RADIUS * 0.6
BASE_FACE_HALF_WIDTH = BASE_POINT_RADIUS * 0.3

GENERAL_FACTOR_STYLE = 'GENERAL_FACTOR_STYLE'

POINT_RADIUS_FACTOR_STYLE = 'POINT_RADIUS_FACTOR_STYLE'
POINT_MATERIAL_STYLE = 'POINT_MATERIAL_STYLE'
POINT_COLOR_STYLE = 'POINT_COLOR_STYLE'
POINT_TRANSPARENCY_STYLE = 'POINT_TRANSP_STYLE'

LINE_RADIUS_FACTOR_STYLE = 'LINE_RADIUS_FACTOR_STYLE'
LINE_ARROW_RADIUS_FACTOR_STYLE = 'LINE_ARROW_RADIUS_FACTOR_STYLE'
LINE_ARROW_LENGTH_FACTOR_STYLE = 'LINE_ARROW_LENGTH_FACTOR_STYLE'
LINE_MATERIAL_STYLE = 'LINE_MATERIAL_STYLE'
LINE_COLOR_STYLE = 'LINE_COLOR_STYLE'
LINE_TRANSPARENCY_STYLE = 'LINE_TRANSPARENCY_STYLE'

SURFACE_WIDTH_FACTOR_STYLE = 'SURFACE_WIDTH_FACTOR_STYLE'
SURFACE_MATERIAL_STYLE = 'SURFACE_MATERIAL_STYLE'
SURFACE_COLOR_STYLE = 'SURFACE_COLOR_STYLE'
SURFACE_TRANSPARENCY_STYLE = 'SURFACE_TRANSPARENCY_STYLE'

LABEL_HEIGHT_FACTOR_STYLE = 'TEXT_HEIGHT_FACTOR_STYLE'
LABEL_DELTA_FACTOR_STYLE = 'TEXT_DELTA_FACTOR_STYLE'
LABEL_MATERIAL_STYLE = 'TEXT_MATERIAL_STYLE'
LABEL_COLOR_STYLE = 'TEXT_COLOR_STYLE'
LABEL_TRANSPARENCY_STYLE = 'TEXT_TRANSPARENCY_STYLE'

DEFAULT_STYLE_RULES = [

    ('', GENERAL_FACTOR_STYLE, 1),

    ('', POINT_RADIUS_FACTOR_STYLE,  1),
    ('', POINT_MATERIAL_STYLE,  CHROME_MATERIAL),
    ('', POINT_COLOR_STYLE,  NICE_YELLOW_COLOR),
    ('', POINT_TRANSPARENCY_STYLE,  0),

    ('', LINE_RADIUS_FACTOR_STYLE,  1),
    ('', LINE_ARROW_RADIUS_FACTOR_STYLE,  1),
    ('', LINE_ARROW_LENGTH_FACTOR_STYLE,  1),
    ('', LINE_MATERIAL_STYLE, CHROME_MATERIAL),
    ('', LINE_COLOR_STYLE,  NICE_BLUE_COLOR),
    ('', LINE_TRANSPARENCY_STYLE,  0),

    ('', SURFACE_WIDTH_FACTOR_STYLE,  1),
    ('', SURFACE_MATERIAL_STYLE,  CHROME_MATERIAL),
    ('', SURFACE_COLOR_STYLE,  NICE_ORIGINAL_COLOR),
    ('', SURFACE_TRANSPARENCY_STYLE,  0),

    ('', LABEL_DELTA_FACTOR_STYLE,  1),
    ('', LABEL_HEIGHT_FACTOR_STYLE,  1),
    ('', LABEL_MATERIAL_STYLE,  PLASTIC_MATERIAL),
    ('', LABEL_COLOR_STYLE,  NICE_WHITE_COLOR),
    ('', LABEL_TRANSPARENCY_STYLE, 0)

]


def isSubTokenOk(maskSub, nameSub):
    if maskSub == '*':
        return True
    return maskSub == nameSub


def isTokenOk(tokenMask, tokenName):

    if tokenMask == '*':
        return True

    maskSubTokens = tokenName.split('-')
    nameSubTokens = tokenMask.split('-')
    if len(nameSubTokens) != len(maskSubTokens):
        return False

    i = 0
    while i<len(maskSubTokens):
        if not isSubTokenOk(maskSubTokens[i],nameSubTokens[i]):
            return False
    return True

def isMaskOk(mask, fullName):

    if mask == '':
        return True

    maskTokens = mask.split('.')
    nameTokens = fullName.split('.')

    iMask = 0
    iName = 0
    while iName<len(nameTokens) and iMask<len(maskTokens):
        if isTokenOk(maskTokens[iMask],nameTokens[iName]):
            iMask+=1
            iName+=1
        else:
            iName+=1

    return iMask == len(maskTokens)

class StyleRules:

    def __init__(self):
        self.rules = list

    def addRule(self, objNameMask, styleName, value):
        self.rules.append((objNameMask, styleName, value))

    def extendRules(self, rules):
        self.rules.extend(rules)

    def getStyle(self, styleName, fullObjName):
        for ruleMask, ruleStyleName, ruleStyleValue in self.rules.reverse():
            if ruleStyleName == styleName and isMaskOk(ruleMask, fullObjName):
                return ruleStyleValue
        return None

class RenderComplex:
    def __init__(self, renderLib, renderName, renderPosition):
        self.renderLib = renderLib
        self.renderPosition = renderPosition
        self.renderName = renderName

    def setRenderName(self, subName):
        self.renderLib.setRenderName(self.renderName + '.' + subName)

    def setRenderPosition(self, subPosition):
        position = Position().next(subPosition).next(self.renderPosition)
        self.renderLib.setRenderPosition(position)


class DeskComplex(RenderComplex):

    def renderPin(self, pinName ,x, y):
        scale = self.renderLib.scale
        pinMove = Translate(x/self.scale, y/self.scale, 0)
        self.setRenderName(pinName)
        self.setRenderPosition(pinMove)
        self.renderLib.renderCylinder(self.pinR / self.scale, self.pinH / self.scale)

    def render(self):

        scale = self.renderLib.scale
        labelText = self.renderLib.formatLabelText

        paperSizeX, paperSizeY, paperSizeZ = DESK_PAPER_SIZE
        psx, psy, psz = paperSizeX / scale, paperSizeY / scale, paperSizeZ / scale
        bsx = (paperSizeX + scale * 2) / scale
        bsy = (paperSizeY + DESK_BORDER_SIZE * 2) / scale
        bsz = DESK_HEIGHT / scale

        self.setRenderName('Paper')
        self.setRenderPosition(Translate(-psx / 2, -psy / 2, -psz))
        self.renderLib.renderBox(psx, psy, psz)

        self.setRenderName('Board')
        self.setRenderPosition(Translate((-bsx / 2, -bsy / 2, -psz - bsz)))
        self.renderLib.renderBox(bsx, bsy, bsz)

        self.setRenderName('Label')
        self.setRenderPosition(Position())
        self.renderLib.renderLabel(gp_Pnt(-bsx / 2, -bsy / 2, -psz), labelText)

        dx = (paperSizeX / 2 - self.aPinOffset) / self.aScale
        dy = (paperSizeY / 2 - self.aPinOffset) / self.aScale

        self.drawPin('Pin-1',-dx, -dy)
        self.drawPin('Pin-2',dx, -dy)
        self.drawPin('Pin-3',dx, dy)
        self.drawPin('Pin-4',-dx, dy)



class RenderHints:
    def __init__(self, sceneName='', scaleA=1, scaleB=1):

        # device size

        # scale factor



        # path to save
        self.pathToSave = None

    def setDeviceSize(self, deviceX, deviceY):
        self.deviceX = deviceX
        self.deviceY = deviceY

    def setPathToSave(self, pathToSave):
        self.pathToSave = pathToSave


M_1_1_SCALE = (1, 1)
M_5_1_SCALE = (5, 1)


class RenderLib:
    def __init__(self, scaleAB=M_1_1_SCALE):

        # scale setting
        scaleA, scaleB = scaleAB
        self.scale = scaleB / scaleA
        self.formatLabelText = 'A0 M' + str(scaleA) + ':' + str(scaleB)

        # decoration setting
        limit =  (DESK_DEFAULT_DRAW_AREA_SIZE / 2) * self.scale
        self.limitMinX = -limit
        self.limitMaxX = limit
        self.limitMinY = -limit
        self.limitMaxY = limit
        self.limitMinZ = -limit
        self.limitMaxZ = limit
        self.deskDX = 0
        self.deskDY = 0
        self.deskDZ = -limit * 1.2 * self.scale
        self.isDesk = True
        self.isAxis = True
        self.isLimits = True

        # render precision setting
        self.shapePrecision = 1 * self.scale
        self.wirePrecision = 1 * self.scale

        # style rules
        self.styleRules = StyleRules()

        # render interface stateful variable
        self.renderPosition = Position()
        self.renderName = ''

    def setDeskPosition(self, deskDX, deskDY, deskDZ):
        self.deskDX = deskDX
        self.deskDY = deskDY
        self.deskDZ = deskDZ

    def setDrawLimits(self, limitMinX, limitMaxX, limitMinY, limitMaxY, limitMinZ, limitMaxZ):
        self.limitMinX = limitMinX
        self.limitMaxX = limitMaxX
        self.limitMinY = limitMinY
        self.limitMaxY = limitMaxY
        self.limitMinZ = limitMinZ
        self.limitMaxZ = limitMaxZ

    def setDecoration(self, isDesk, isAxis, isLimits):
        self.isDesk = isDesk
        self.isAxis = isAxis
        self.isLimits = isLimits

    def setPrecision(self, wirePrecision, shapePrecision):
        self.wirePrecision = wirePrecision
        self.shapePrecision = shapePrecision

    def setRenderPosition(self, renderPosition):
        self.renderName = renderPosition

    def setRenderName(self, renderName):
        self.renderName = renderName

    def getStyle(self, styleName):
        self.styleRules.getStyle(styleName, self.renderName)

    def extendStyles(self, exRulesList):
        self.styleRules.extendRules(exRulesList)


class ScreenRenderLib(RenderLib):

    def __init__(self, scaleAB=M_1_1_SCALE, screenX=800, screenY=600):
        super().__init__(scaleAB)

        # device setting
        self.screenX = screenX
        self.screenY = screenY
        self.display = None
        self.start_display_call = None

        # ais render stateful
        self.aisPosition = None
        self.aisColor = None
        self.aisTransparency = None


    def renderStart(self):
        def __init__(self, hints):
            self.display, self.start_display_call, add_menu, add_function_to_menu = init_display(
                None, (hints.deviceX, hints.deviceY), True, [128, 128, 128], [128, 128, 128]
            )
        self.renderDecoration()

    def renderFinish(self):
        self.display.FitAll()
        self.start_display_call()

    def aisShape(self, shape):
        shapeTr = BRepBuilderAPI_Transform(shape, self.aisPosition.getTrsf()).Shape()
        ais = AIS_Shape(shapeTr)
        r, g, b = self.aisColor
        qColor = Quantity_Color(r, g, b,
                                  Quantity_TypeOfColor(Quantity_TypeOfColor.Quantity_TOC_RGB))
        ais.SetColor(qColor)
        ais.SetTransparency(self.aisTransparency)
        aspect = Graphic3d_MaterialAspect(self.aisMaterial)
        ais.SetMaterial(aspect)
        self.display.Context.Display(ais, False)

    def baseCylinder(self, radius, height):
        self.aisShape = BRepPrimAPI_MakeCylinder(radius, height).Shape()
        self.aisPosition = Position().next(basePosition).next(renderPosition)
        self.aisColor = self.baseColor
        self.aisMaterial = self.baseMaterial
        self.aisTransparency = self.baseTransparency
        self.aisShape()

    def renderShape(self, aShape):
        self.renderShapeObj(aShape, self.aStyle.faceMaterial)

    def renderWire(self, aWire):
        aWireRadius = self.aStyle.lineRadius
        startPoint, tangentDir = _getWireStartPointAndTangentDir(aWire)
        profileCircle = GC_MakeCircle(startPoint, tangentDir, aWireRadius).Value()
        profileEdge = BRepBuilderAPI_MakeEdge(profileCircle).Edge()
        profileWire = BRepBuilderAPI_MakeWire(profileEdge).Wire()

        shape = BRepOffsetAPI_MakePipe(aWire, profileWire).Shape()

        self.renderShapeObj(shape, self.aStyle.lineMaterial)

    def renderBox(self, aSizeX, aSizeY, aSizeZ):
        shape = BRepPrimAPI_MakeBox(aSizeX, aSizeY, aSizeZ).Shape()
        self.renderShapeObj(shape, self.aStyle.faceMaterial)
        self.resetMoveAndStyle()

    def renderSphere(self, aRadius):
        shape = BRepPrimAPI_MakeSphere(aRadius).Shape()
        self.renderShapeObj(shape, self.aStyle.faceMaterial)
        self.resetMoveAndStyle()

    def renderCone(self, aRadius1, aRadius2, aHeight):
        shape = BRepPrimAPI_MakeCone(aRadius1, aRadius2, aHeight).Shape()
        self.renderShapeObj(shape, self.aStyle.faceMaterial)
        self.resetMoveAndStyle()

    def renderCylinder(self, aRadius, aHeight):
        shape = BRepPrimAPI_MakeCylinder(aRadius, aHeight).Shape()
        self.renderShapeObj(shape, self.aStyle.faceMaterial)
        self.resetMoveAndStyle()

    def renderTorus(self, aRadius1, aRadius2):
        shape = BRepPrimAPI_MakeTorus(aRadius1, aRadius2).Shape()
        self.renderShapeObj(shape, self.aStyle.faceMaterial)
        self.resetMoveAndStyle()

    def renderPoint(self, aPnt):
        aisShape = BRepPrimAPI_MakeSphere(self.aStyle.pointRadius).Shape()
        aisPosition = Position().next(Translate(aPnt.X, aPnt.Y, aPnt.Z)).next(self.renderPosition())
        aisMaterial = self.getStyle(POINT_MATERIAL_STYLE)
        aisColor = self.getStyle(POINT_COLOR_STYLE)
        aisTransparency = self.getStyle(POINT_TRANSPARENCY_STYLE)
        self.renderShapeAis(aisShape, aisPosition, aisMaterial, aisColor, aisTransparency)
        self.resetMoveAndStyle()

    def renderLine(self, pnt1, pnt2):
        vec = gp_Vec(pnt1, pnt2)
        self.localMove.setDirect(pnt1, pnt2)
        r = BASE_LINE_RADIUS * self.getStyle(GENERAL_FACTOR_STYLE) * self.getStyle(LINE_RADIUS_FACTOR_STYLE)
        self.renderCylinder(r, vec.Magnitude())

    def renderVector(self, aPnt1, aPnt2):
        rArrow = self.aStyle.getArrowRadius(self.hints.scale)
        hArrow = self.aStyle.getArrowHeight(self.hints.scale)
        v = gp_Vec(aPnt1, aPnt2)
        vLen = v.Magnitude()
        v *= (vLen - hArrow) / vLen
        pntM = aPnt1.Translated(v)
        self.resetMoveAndStyle()

        self.renderLine(aPnt1, pntM)
        self.localMove.setDirect(pntM, aPnt2)
        self.renderCone(rArrow, 0, hArrow)
        self.localMove = Move()
        self.resetMoveAndStyle()

    def renderCircle(self, aPnt1, aPnt2, aPnt3):
        geomCircle = GC_MakeCircle(aPnt1, aPnt2, aPnt3).Value()
        wire = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
        self.renderWireObj(wire)
        self.resetMoveAndStyle()

    def renderLabel(self, aPnt, aText):
        self.localMove.setMove(aPnt.X, aPnt.Y, aPnt.Z)
        aHeightPx = self.aStyle.getLabelHeight()
        pnt = gp_Pnt(0, 0, 0).Transformed(self.aMove.getTrsf())
        self.device.display.DisplayMessage(pnt, aText, aHeightPx, self.aStyle.getNormedColor(), False)
        self.resetMoveAndStyle()

    def render(self, aDraw, aMove = None, aStyle = None):
        aDraw.drawTo(self, aMove, aStyle)

    def renderDecoration(self):
        if self.hints.isDesk:
            DeskComplex(scale).drawTo(self, Move().applyMove(self.deskDX, self.deskDY, self.deskDZ))
        if self.hints.isAxis:
            AxisComplex(self.limits).drawTo(self)
        if self.hints.isLimits:
            LimitsComplex(self.limits).drawTo(self)


    def resetMoveAndStyle(self):
        self.aMove = None
        self.aStyle = None


class ScreenRenderLib(RenderLib): pass

class WebRenderLib(RenderLib):

    def startRender(self):
        self.device = WebDevice(self.hints)

    def renderTextObj(self, aText, aHeightPx):
        pnt = gp_Pnt(0, 0, 0).Transformed(self.aMove.getTrsf())
        color = self.aStyle.getNormedColor()
        self.device.drawLabel(pnt, aText, color)

    def renderShapeObj(self, aShape):
        shapeTr = BRepBuilderAPI_Transform(aShape, self.aMove.getTrsf()).Shape()
        color = self.aStyle.getNormedColor()
        transparency = self.aStyle.getNormedTransparency()
        self.device.drawShape(shapeTr, color, transparency)

    def finishRender(self):
        self.device.save()


class WebFastRenderLib(WebRenderLib):
    pass


class StlRenderLibParams:
    def __init__(self, scaleA=1, scaleB=1):
        self.scaleA = scaleA
        self.scaleB = scaleB
        self.scale = scaleB/scaleA
        self.shapePrecision = 1*self.scale
        self.wirePrecision = 1*self.scale


class StlRenderLib(RenderLib):

    def startRender(self):
        self.device = StlDevice(self.hints)

    def renderShapeObj(self, aShape):
        shapeTr = BRepBuilderAPI_Transform(aShape, self.aMove.getTrsf()).Shape()
        self.device.drawShape(shapeTr)

    def finishRender(self):
        self.device.save()
