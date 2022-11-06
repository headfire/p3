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

class TranslateToPnt(Translate):
    def __init__(self, pnt):
        super().__init__(pnt.X, pnt.Y, pnt.Z)

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

M_1_1_SCALE = (1, 1)
M_5_1_SCALE = (5, 1)

DESK_HEIGHT = 20
DESK_BORDER_SIZE = 60
DESK_PAPER_SIZE = 1189, 841, 1
DESK_PIN_OFFSET = 30
DESK_PIN_RADIUS = 10
DESK_PIN_HEIGHT = 2
DESK_DEFAULT_DRAW_AREA_SIZE = 400


NORMAL_POINT_RADIUS = 5
NORMAL_LINE_RADIUS = NORMAL_POINT_RADIUS * 0.6
NORMAL_SURFACE_HALF_WIDTH = NORMAL_POINT_RADIUS * 0.3
NORMAL_ARROW_RADIUS = NORMAL_POINT_RADIUS
NORMAL_ARROW_LENGTH = NORMAL_ARROW_RADIUS * 3
NORMAL_LABEL_HEIGHT_PX = 20

GENERAL_FACTOR_STYLE = 'GENERAL_FACTOR_STYLE'

POINT_RADIUS_FACTOR_STYLE = 'POINT_RADIUS_FACTOR_STYLE'
POINT_MATERIAL_STYLE = 'POINT_MATERIAL_STYLE'
POINT_COLOR_STYLE = 'POINT_COLOR_STYLE'
POINT_TRANSPARENCY_STYLE = 'POINT_TRANSP_STYLE'

LINE_RADIUS_FACTOR_STYLE = 'LINE_RADIUS_FACTOR_STYLE'
LINE_MATERIAL_STYLE = 'LINE_MATERIAL_STYLE'
LINE_COLOR_STYLE = 'LINE_COLOR_STYLE'
LINE_TRANSPARENCY_STYLE = 'LINE_TRANSPARENCY_STYLE'

ARROW_RADIUS_FACTOR_STYLE = 'LINE_ARROW_RADIUS_FACTOR_STYLE'
ARROW_LENGTH_FACTOR_STYLE = 'LINE_ARROW_LENGTH_FACTOR_STYLE'

SURFACE_WIDTH_FACTOR_STYLE = 'SURFACE_WIDTH_FACTOR_STYLE'
SURFACE_MATERIAL_STYLE = 'SURFACE_MATERIAL_STYLE'
SURFACE_COLOR_STYLE = 'SURFACE_COLOR_STYLE'
SURFACE_TRANSPARENCY_STYLE = 'SURFACE_TRANSPARENCY_STYLE'

SOLID_WIDTH_FACTOR_STYLE = 'SOLID_WIDTH_FACTOR_STYLE'
SOLID_MATERIAL_STYLE = 'SOLID_MATERIAL_STYLE'
SOLID_COLOR_STYLE = 'SOLID_COLOR_STYLE'
SOLID_TRANSPARENCY_STYLE = 'SOLID_TRANSPARENCY_STYLE'

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
    ('', LINE_MATERIAL_STYLE, CHROME_MATERIAL),
    ('', LINE_COLOR_STYLE,  NICE_BLUE_COLOR),
    ('', LINE_TRANSPARENCY_STYLE,  0),

    ('', ARROW_RADIUS_FACTOR_STYLE, 1),
    ('', ARROW_LENGTH_FACTOR_STYLE, 1),

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



class Prim:
    def getShape(self): pass


class BoxPrim(Prim):
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z


class SpherePrim(Prim):
    def __init__(self, r):
        self.r = r


class SpherePrim(Prim):
    def __init__(self, r):
        self.r = r


class ConePrim(Prim):
    def __init__(self, r1, r2, h):
        self.r1, self.r2, self.h = r1, r2, h


class CylinderPrim(Prim):
    def __init__(self, r, h):
        self.r, self.h = r, h


class TorusPrim(Prim):
    def __init__(self, r1, r2):
        self.r1, self.r2 = r1, r2


class RenderLib:
    def __init__(self):

        # render stateful
        self.renderPosition = Position()
        self.renderName = ''

    def renderSetPosition(self, renderPosition):
        self.renderName = renderPosition

    def renderSetName(self, renderName):
        self.renderName = renderName

    def renderStart(self):
        self.deviceStart()
        self.renderDecoration()

    def renderFinish(self):
        self.deviceFinish()

    def deviceStart(self): pass
    def deviceFinish(self): pass

    def renderDecor(self, shape): pass
    def renderShape(self, shape): pass
    def renderSolid(self, prim): pass
    def renderWire(self, wire): pass
    def renderPoint(self, pnt): pass
    def renderLine(self, pnt1, pnt2): pass
    def renderArrow(self, pnt1, pnt2): pass
    def renderCircle(self, pnt1, pnt2, pnt3): pass
    def renderLabel(self, pnt, text): pass


class StyledRenderLib(RenderLib):
    def __init__(self, scaleAB=M_1_1_SCALE):
        super().__init__()

        # style rules
        self.styleRules = StyleRules()

        # scale setting
        scaleA, scaleB = scaleAB
        self.styleScale = scaleB / scaleA
        self.styleFormatLabelText = 'A0 M' + str(scaleA) + ':' + str(scaleB)

        # decoration setting
        limit =  (DESK_DEFAULT_DRAW_AREA_SIZE / 2) * self.styleScale
        self.styleLimitMinX = -limit
        self.styleLimitMaxX = limit
        self.styleLimitMinY = -limit
        self.styleLimitMaxY = limit
        self.styleLimitMinZ = -limit
        self.styleLimitMaxZ = limit
        self.styleDeskDX = 0
        self.styleDeskDY = 0
        self.styleDeskDZ = -limit * 1.2
        self.styleIsDesk = True
        self.styleIsAxis = True
        self.styleIsLimits = True

        # style stateful
        self.styleMaterial = None
        self.styleColor = None
        self.styleTransparent = None
        self.stylePointRadius = None
        self.styleLineRadius = None
        self.styleFaceHalfWidth = None
        self.styleArrowLength = None
        self.styleArrowRadius = None
        self.styleLabelDelta = None
        self.styleLabelHeightPx = None

    def initDeskPosition(self, deskDX, deskDY, deskDZ):
        self.styleDeskDX = deskDX
        self.styleDeskDY = deskDY
        self.styleDeskDZ = deskDZ

    def initDrawLimits(self, limitMinX, limitMaxX, limitMinY, limitMaxY, limitMinZ, limitMaxZ):
        self.styleLimitMinX = limitMinX
        self.styleLimitMaxX = limitMaxX
        self.styleLimitMinY = limitMinY
        self.styleLimitMaxY = limitMaxY
        self.styleLimitMinZ = limitMinZ
        self.styleLimitMaxZ = limitMaxZ

    def initDecor(self, isDesk, isAxis, isLimits):
        self.styleIsDesk = isDesk
        self.styleIsAxis = isAxis
        self.styleIsLimits = isLimits

    def initAdditionRules(self, rulesList):
        self.styleRules.extendRules(rulesList)

    def styleGet(self, styleName):
        styleValue = self.styleRules.getStyle(styleName, self.renderName)
        self.log('getStyle: %s = %s' % (styleName, styleValue))
        return styleValue

    def styleBrashForPoint(self):
        self.styleMaterial = self.styleGet(LINE_MATERIAL_STYLE)
        self.styleColor = self.styleGet(LINE_COLOR_STYLE)
        self.styleTransparent = self.styleGet(LINE_TRANSPARENCY_STYLE)

    def styleBrashForLine(self):
        self.styleMaterial = self.styleGet(LINE_MATERIAL_STYLE)
        self.styleColor = self.styleGet(LINE_COLOR_STYLE)
        self.styleTransparent = self.styleGet(LINE_TRANSPARENCY_STYLE)

    def styleBrashForSolid(self):
        self.styleMaterial = self.styleGet(SOLID_MATERIAL_STYLE)
        self.styleColor = self.styleGet(SOLID_COLOR_STYLE)
        self.styleTransparent = self.styleGet(SOLID_TRANSPARENCY_STYLE)

    def styleBrashForSurface(self):
        self.styleMaterial = self.styleGet(SURFACE_MATERIAL_STYLE)
        self.styleColor = self.styleGet(SURFACE_COLOR_STYLE)
        self.styleTransparent = self.styleGet(SURFACE_TRANSPARENCY_STYLE)

    def styleBrashForLabel(self):
        self.styleMaterial = self.styleGet(LABEL_MATERIAL_STYLE)
        self.styleColor = self.styleGet(LABEL_COLOR_STYLE)
        self.styleTransparency = self.styleGet(LABEL_TRANSPARENCY_STYLE)

    def styleSizeForPoint(self):
        self.stylePointRadius = NORMAL_POINT_RADIUS \
                                * self.styleGet(GENERAL_FACTOR_STYLE) \
                                * self.styleGet(POINT_RADIUS_FACTOR_STYLE) \
                                * self.styleScale

    def styleSizeForLine(self):
        self.stylePointRadius = NORMAL_LINE_RADIUS \
                                * self.styleGet(GENERAL_FACTOR_STYLE) \
                                * self.styleGet(LINE_RADIUS_FACTOR_STYLE) \
                                * self.styleScale

    def styleSizeForSurface(self):
        self.stylePointRadius = NORMAL_SURFACE_HALF_WIDTH \
                                * self.styleGet(GENERAL_FACTOR_STYLE) \
                                * self.styleGet(SURFACE_WIDTH_FACTOR_STYLE)\
                                * self.styleScale

    def styleSizeForLabel(self):
        self.styleLabelHeightPx = NORMAL_LABEL_HEIGHT_PX \
                                * self.styleGet(GENERAL_FACTOR_STYLE) \
                                * self.styleGet(SURFACE_WIDTH_FACTOR_STYLE)\
                                * 1  # not scaled

    def styleSizeForArrow(self):
        self.styleArrowRadius = NORMAL_ARROW_RADIUS \
                                * self.styleGet(GENERAL_FACTOR_STYLE) \
                                * self.styleGet(ARROW_RADIUS_FACTOR_STYLE)\
                                * self.styleScale

        self.styleArrowLength = NORMAL_ARROW_LENGTH \
                                * self.styleGet(GENERAL_FACTOR_STYLE) \
                                * self.styleGet(ARROW_LENGTH_FACTOR_STYLE)\
                                * self.styleScale

    def styleDesk(self): pass
    def styleAxis(self): pass
    def styleLimits(self): pass
    def styleShape(self, shape): pass
    def stylePrim(self, prim): pass
    def styleWire(self, wire): pass
    def stylePoint(self, pnt): pass
    def styleLine(self, pnt1, pnt2): pass
    def styleArrow(self, pnt1, pnt2): pass
    def styleCircle(self, pnt1, pnt2, pnt3): pass
    def styleLabel(self, pnt, text): pass

    def renderDecoration(self):
        if self.styleIsDesk:
            self.styleDesk()
        if self.styleIsAxis:
            self.styleAxis()
        if self.styleIsLimits:
            self.styleLimits()

    def renderSolid(self, prim):
        self.styleBrashForSolid()
        self.stylePrim(prim)

    def renderSphere(self, r):
        self.styleBrashForSolid()
        self.styleSphere(r)

    def renderCone(self, r1, r2, h):
        self.styleBrashForSolid()
        self.styleCone(r1, r2, h)

    def renderCylinder(self, r, h):
        self.styleBrashForSolid()
        self.styleCylinder(r, h)

    def renderTorus(self, r1, r2):
        self.styleBrashForSolid()
        self.styleTorus(r1, r2)

    def renderPoint(self, pnt):
        self.styleBrashForPoint()
        self.styleSizeForPoint()
        self.stylePoint(pnt)

    def renderLine(self, pnt1, pnt2):
        self.styleBrashForLine()
        self.styleSizeForLine()
        self.styleLine(pnt1, pnt2)

    def renderArrow(self, pnt1, pnt2):
        self.styleBrashForLine()
        self.styleSizeForLine()
        self.styleSizeForArrow()
        self.styleArrow(pnt1, pnt2)

    def renderCircle(self, pnt1, pnt2, pnt3):
        self.styleBrashForLine()
        self.styleSizeForLine()
        self.styleCircle(pnt1, pnt2, pnt3)

    def renderLabel(self, pnt, text):
        self.styleBrashForLabel()
        self.styleSizeForLabel()
        self.styleCircle(pnt, text)


class BaseRenderLib(StyledRenderLib):
    def __init__(self, scaleAB=M_1_1_SCALE):
        super().__init__(scaleAB)
        self.basePosition = None

    def baseSetPosition(self, subPosition=Position()):
        self.basePosition = Position().next(subPosition).next(self.renderPosition)

    def baseStart(self): pass
    def baseFinish(self): pass
    def baseShape(self, shape): pass
    def baseWire(self, wire): pass
    def basePrim(self, prim): pass
    def baseLabel(self, pnt, text): pass

    def styleStart(self):
        self.baseStart()

    def styleFinish(self):
        self.baseFinish()

    def styleDesk(self): pass
    def styleAxis(self): pass
    def styleLimit(self): pass

    def styleSolid(self, shape):
        self.baseSetStyleBrash()
        self.baseSetPosition()
        self.baseShape(shape)

    def styleSurface(self, shape):
        self.baseSetStyleBrash()
        self.baseSetPosition()
        self.baseShape(shape)

    def styleWire(self, wire):
        self.baseSetStyleBrash()
        self.baseSetPosition()
        self.baseWire(wire)

    def stylePrim(self, prim):
        self.baseSetStyleBrash()
        self.baseSetPosition()
        self.basePrim(prim)

    def stylePoint(self, pnt):
        self.baseSetStyleBrash()
        self.baseSetPosition(TranslateToPnt(pnt))
        self.basePrim(SpherePrim(self.stylePointRadius))

    def _styleLine(self, pnt1, pnt2):
        length = gp_Vec(pnt1, pnt2).Magnitude()
        self.basePrim(CylinderPrim(self.styleLineRadius, length))

    def styleLine(self, pnt1, pnt2):
        self.baseSetStyleBrash()
        self.baseSetPosition(Direct(pnt1, pnt2))
        self._styleLine(pnt1, pnt2)

    def styleArrow(self, pnt1, pnt2):

        self.baseSetStyleBrash()

        rArrow = self.styleArrowRadius
        hArrow = self.styleArrowHeigth
        v = gp_Vec(pnt1, pnt2)
        vLen = v.Magnitude()
        v *= (vLen - hArrow) / vLen
        pntM = pnt1.Translated(v)

        self.baseSetPosition()
        self._styleLine(pnt1, pntM)

        self.self.baseSetPosition(Direct(pntM, pnt2))
        self.basePrim(ConePrim(rArrow, 0, hArrow))

    def styleCircle(self, pnt1, pnt2, pnt3):

        self.baseSetStyleBrash()
        self.baseSetPosition()

        geomCircle = GC_MakeCircle(pnt1, pnt2, pnt3).Value()
        wire = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
        self.baseWire(wire)

    def styleLabel(self, pnt, text):
        delta = self.styleLabelDelta
        self.baseSetPosition(Position().next(Translate(delta, delta, delta)).next(TranslateToPnt(pnt)))
        aHeightPx = self.styleLabelHeightPx
        self.baseLabel(text, aHeightPx)

class FineRenderLib(BaseRenderLib):

    def fineShape(self, shape):pass
    def fineLabel(self, text): pass

    def baseStart(self): pass
    def baseFinish(self): pass

    def baseShape(self, shape):
        self.fineShape(shape)

    def baseWire(self, wire):
        aWireRadius = self.styleLineRadius
        startPoint, tangentDir = _getWireStartPointAndTangentDir(wire)
        profileCircle = GC_MakeCircle(startPoint, tangentDir, aWireRadius).Value()
        profileEdge = BRepBuilderAPI_MakeEdge(profileCircle).Edge()
        profileWire = BRepBuilderAPI_MakeWire(profileEdge).Wire()
        shape = BRepOffsetAPI_MakePipe(wire, profileWire).Shape()
        self.fineShape(shape)

    def basePrim(self, prim):
        self.fineShape(prim.getShape())



class ScreenRenderLib(FineRenderLib):
    def __init__(self, scaleAB=M_1_1_SCALE, screenX=800, screenY=600):
        super().__init__(scaleAB)
        self.screenX = screenX
        self.screenY = screenY
        self.display = None
        self.start_display_call = None

    def deviceStart(self):
       self.display, self.start_display_call, add_menu, add_function_to_menu = init_display(
                None, (hints.deviceX, hints.deviceY), True, [128, 128, 128], [128, 128, 128]

    def deviceFinish(self):
        self.display.FitAll()
        self.start_display_call()

    def fineShape(self, shape):
        shapeTr = BRepBuilderAPI_Transform(shape, self.basePosition.getTrsf()).Shape()
        ais = AIS_Shape(shapeTr)
        r, g, b = self.styleColor
        qColor = Quantity_Color(r, g, b,
                    Quantity_TypeOfColor(Quantity_TypeOfColor.Quantity_TOC_RGB))
        ais.SetColor(qColor)
        ais.SetTransparency(self.styleTransparency)
        aspect = Graphic3d_MaterialAspect(self.styleMaterial)
        ais.SetMaterial(aspect)
        self.display.Context.Display(ais, False)

    def fineLabel(self, text):
        pnt = gp_Pnt(0, 0, 0).Transformed(self.basePosition)
        self.device.display.DisplayMessage(pnt, text, self.styleLabelHeightPx,
                                           self.styleColor, False)


