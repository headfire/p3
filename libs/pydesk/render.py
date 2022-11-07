from OCC.Core.GC import GC_MakeCircle
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_TypeOfColor
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_Transform
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepTools import BRepTools_WireExplorer
from OCC.Core.Graphic3d import Graphic3d_NameOfMaterial, Graphic3d_MaterialAspect
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Vec, gp_Ax1, gp_Trsf

from OCC.Display.SimpleGui import init_display

from draw import *

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
POINT_TRANSPARENCY_STYLE = 'POINT_TRANSPARENCY_STYLE'

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

    ('', POINT_RADIUS_FACTOR_STYLE, 1),
    ('', POINT_MATERIAL_STYLE, CHROME_MATERIAL),
    ('', POINT_COLOR_STYLE, NICE_YELLOW_COLOR),
    ('', POINT_TRANSPARENCY_STYLE, 0),

    ('', LINE_RADIUS_FACTOR_STYLE, 1),
    ('', LINE_MATERIAL_STYLE, CHROME_MATERIAL),
    ('', LINE_COLOR_STYLE, NICE_BLUE_COLOR),
    ('', LINE_TRANSPARENCY_STYLE, 0),

    ('', ARROW_RADIUS_FACTOR_STYLE, 1),
    ('', ARROW_LENGTH_FACTOR_STYLE, 1),

    ('', SURFACE_WIDTH_FACTOR_STYLE, 1),
    ('', SURFACE_MATERIAL_STYLE, CHROME_MATERIAL),
    ('', SURFACE_COLOR_STYLE, NICE_ORIGINAL_COLOR),
    ('', SURFACE_TRANSPARENCY_STYLE, 0),

    ('', LABEL_DELTA_FACTOR_STYLE, 1),
    ('', LABEL_HEIGHT_FACTOR_STYLE, 1),
    ('', LABEL_MATERIAL_STYLE, PLASTIC_MATERIAL),
    ('', LABEL_COLOR_STYLE, NICE_WHITE_COLOR),
    ('', LABEL_TRANSPARENCY_STYLE, 0)

]


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


def _isSubTokenOk(maskSub, nameSub):
    if maskSub == '*':
        return True

    return maskSub == nameSub


def _isTokenOk(tokenMask, tokenName):
    if tokenMask == '*':
        return True

    maskSubTokens = tokenName.split('-')
    nameSubTokens = tokenMask.split('-')
    if len(nameSubTokens) != len(maskSubTokens):
        return False

    i = 0
    while i < len(maskSubTokens):
        if not _isSubTokenOk(maskSubTokens[i], nameSubTokens[i]):
            return False

    return True


def _isMaskOk(mask, fullName):
    if mask == '':
        return True

    maskTokens = mask.split('.')
    nameTokens = fullName.split('.')

    iMask = 0
    iName = 0
    while iName < len(nameTokens) and iMask < len(maskTokens):
        if _isTokenOk(maskTokens[iMask], nameTokens[iName]):
            iMask += 1
            iName += 1
        else:
            iName += 1

    return iMask == len(maskTokens)


class StyleRules:

    def __init__(self):

        self.rules = list()

    def addRule(self, objNameMask, styleName, value):

        rule = objNameMask, styleName, value
        self.rules.append(rule)

    def extendRules(self, rules):

        self.rules.extend(rules)

    def getStyle(self, styleName, fullObjName):

        for ruleMask, ruleStyleName, ruleStyleValue in reversed(self.rules):
            if ruleStyleName == styleName and _isMaskOk(ruleMask, fullObjName):
                return ruleStyleValue

        return None


class StyledRenderLib:
            self.sceneName = None

            # device size
            self.deviceX = None
            self.deviceY = None

            # scale factor
            self.scaleA = None
            self.scaleB = None
            self.scale = None
            self.scaleStr = None

            # primitive sizes
            self.basePointRadius = None
            self.baseLineRadius = None

            # precision
            self.wirePrecision = None
            self.shapePrecision = None

            # desk position
            self.deskDX = None
            self.deskDY = None
            self.deskDZ = None

            # draw limits
            self.limitMinX = None
            self.limitMaxX = None
            self.limitMinY = None
            self.limitMaxY = None
            self.limitMinZ = None
            self.limitMaxZ = None

            # decoration flags
            self.isDesk = None
            self.isAxis = None
            self.isLimits = None

            # path to save
            self.pathToSave = None

            # default init
            self.setScale(1, 1)
            self.setDeviceSize(800, 600)
            self.setDecoration(True, True, True)
            self.setPathToSave('.')

        def setDeviceSize(self, deviceX, deviceY):
            self.deviceX = deviceX
            self.deviceY = deviceY

        def setScale(self, scaleA, scaleB):
            self.scaleA = 1
            self.scaleB = 1
            self.scale = scaleB / scaleA
            self.scaleStr = 'A0 M' + str(scaleA) + ':' + str(scaleB)

            self.basePointRadius = 5 * self.scale
            self.baseLineRadius = 3 * self.scale

            self.shapePrecision = 1 * self.scale
            self.wirePrecision = 1 * self.scale

            self.deskDX = 0
            self.deskDY = 0
            self.deskDZ = 300 * self.scale

            self.limitMinX = -200 * self.scale
            self.limitMaxX = 200 * self.scale
            self.limitMinY = -200 * self.scale
            self.limitMaxY = 200 * self.scale
            self.limitMinZ = -200 * self.scale
            self.limitMaxZ = 200 * self.scale

        def setPathToSave(self, pathToSave):
            self.pathToSave = pathToSave

        def setPrecision(self, wirePrecision, shapePrecision):
            self.wirePrecision = wirePrecision
            self.shapePrecision = shapePrecision

        def setBaseSize(self, basePointRadius, baseLineRadius):
            self.basePointRadius = basePointRadius
            self.baseLineRadius = baseLineRadius

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

    def __init__(self, scaleAB):

        scaleA, scaleB = scaleAB
        self.scale = scaleB / scaleA
        self.scaleText = 'A0 M' + str(scaleA) + ':' + str(scaleB)

        self.basePosition = None

        self.styleRules = StyleRules()
        self.styleMaterial = None
        self.styleColor = None
        self.styleTransparency = None
        self.stylePointRadius = None
        self.styleLineRadius = None
        self.styleFaceHalfWidth = None
        self.styleArrowLength = None
        self.styleArrowRadius = None
        self.styleLabelDelta = None
        self.styleLabelHeightPx = None

        self.renderPosition = Position()
        self.renderName = ''

    def initAdditionRules(self, rulesList):
        self.styleRules.extendRules(rulesList)

    def getStyle(self, styleName):
        styleValue = self.styleRules.getStyle(styleName, self.renderName)
        return styleValue

    def locatePosition(self, subPosition=Position()):
        self.basePosition = Position().next(subPosition).next(self.renderPosition)

    def brashForPoint(self):
        self.styleMaterial = self.getStyle(LINE_MATERIAL_STYLE)
        self.styleColor = self.getStyle(LINE_COLOR_STYLE)
        self.styleTransparency = self.getStyle(LINE_TRANSPARENCY_STYLE)

    def brashForLine(self):
        self.styleMaterial = self.getStyle(LINE_MATERIAL_STYLE)
        self.styleColor = self.getStyle(LINE_COLOR_STYLE)
        self.styleTransparency = self.getStyle(LINE_TRANSPARENCY_STYLE)

    def brashForSolid(self):
        self.styleMaterial = self.getStyle(SOLID_MATERIAL_STYLE)
        self.styleColor = self.getStyle(SOLID_COLOR_STYLE)
        self.styleTransparency = self.getStyle(SOLID_TRANSPARENCY_STYLE)

    def brashForSurface(self):
        self.styleMaterial = self.getStyle(SURFACE_MATERIAL_STYLE)
        self.styleColor = self.getStyle(SURFACE_COLOR_STYLE)
        self.styleTransparency = self.getStyle(SURFACE_TRANSPARENCY_STYLE)

    def brashForLabel(self):
        self.styleMaterial = self.getStyle(LABEL_MATERIAL_STYLE)
        self.styleColor = self.getStyle(LABEL_COLOR_STYLE)
        self.styleTransparency = self.getStyle(LABEL_TRANSPARENCY_STYLE)

    def brashForDeskPin(self):
        self.styleMaterial = STEEL_MATERIAL
        self.styleColor = NICE_GRAY_COLOR
        self.styleTransparency = 0

    def brashForDeskPaper(self):
        self.styleMaterial = PLASTIC_MATERIAL
        self.styleColor = PAPER_COLOR
        self.styleTransparency = 0

    def brashForDeskBoard(self):
        self.styleMaterial = PLASTIC_MATERIAL
        self.styleColor = WOOD_COLOR
        self.styleTransparency = 0

    def brashForDeskLabel(self):
        self.styleMaterial = PLASTIC_MATERIAL
        self.styleColor = NICE_ORIGINAL_COLOR
        self.styleTransparency = 0

    def sizeForPoint(self):
        self.stylePointRadius = NORMAL_POINT_RADIUS \
                                * self.getStyle(GENERAL_FACTOR_STYLE) \
                                * self.getStyle(POINT_RADIUS_FACTOR_STYLE) \
                                * self.scale

    def sizeForLine(self):
        self.stylePointRadius = NORMAL_LINE_RADIUS \
                                * self.getStyle(GENERAL_FACTOR_STYLE) \
                                * self.getStyle(LINE_RADIUS_FACTOR_STYLE) \
                                * self.scale

    def sizeForSurface(self):
        self.stylePointRadius = NORMAL_SURFACE_HALF_WIDTH \
                                * self.getStyle(GENERAL_FACTOR_STYLE) \
                                * self.getStyle(SURFACE_WIDTH_FACTOR_STYLE) \
                                * self.scale

    def sizeForLabel(self):
        self.styleLabelHeightPx = NORMAL_LABEL_HEIGHT_PX \
                                  * self.getStyle(GENERAL_FACTOR_STYLE) \
                                  * self.getStyle(SURFACE_WIDTH_FACTOR_STYLE) \
                                  * 1  # not scaled

    def sizeForArrow(self):
        self.styleArrowRadius = NORMAL_ARROW_RADIUS \
                                * self.getStyle(GENERAL_FACTOR_STYLE) \
                                * self.getStyle(ARROW_RADIUS_FACTOR_STYLE) \
                                * self.scale

        self.styleArrowLength = NORMAL_ARROW_LENGTH \
                                * self.getStyle(GENERAL_FACTOR_STYLE) \
                                * self.getStyle(ARROW_LENGTH_FACTOR_STYLE) \
                                * self.scale

    def outStart(self): pass

    def outFinish(self): pass

    def outShape(self, shape): pass

    def outLabel(self, text): pass

    def baseShape(self, shape):

        self.outShape(shape)

    def baseWire(self, wire):

        aWireRadius = self.styleLineRadius

        startPoint, tangentDir = _getWireStartPointAndTangentDir(wire)
        profileCircle = GC_MakeCircle(startPoint, tangentDir, aWireRadius).Value()
        profileEdge = BRepBuilderAPI_MakeEdge(profileCircle).Edge()
        profileWire = BRepBuilderAPI_MakeWire(profileEdge).Wire()
        shape = BRepOffsetAPI_MakePipe(wire, profileWire).Shape()

        self.outShape(shape)

    def basePrim(self, prim):

        self.outShape(prim.getShape())

    def baseLabel(self, text):

        self.outLabel(text)

    def renderStart(self):

        self.outStart()

    def renderFinish(self):

        self.outFinish()

    def renderSetPosition(self, renderPosition):

        self.renderName = renderPosition

    def renderSetName(self, renderName):

        self.renderName = renderName

    def renderSolid(self, prim):

        self.brashForSolid()
        self.locatePosition()
        self.basePrim(prim)

    def renderSurface(self, shape):

        self.brashForSurface()
        self.locatePosition()
        self.baseShape(shape)

    def renderWire(self, wire):

        self.brashForLine()
        self.sizeForLine()
        self.locatePosition()
        self.baseWire(wire)

    def renderPoint(self, pnt):

        self.brashForPoint()
        self.sizeForPoint()
        self.locatePosition(TranslateToPnt(pnt))
        self.basePrim(SpherePrim(self.stylePointRadius))

    def _renderLine(self, pnt1, pnt2):

        length = gp_Vec(pnt1, pnt2).Magnitude()

        self.locatePosition(Direct(pnt1, pnt2))
        self.basePrim(CylinderPrim(self.styleLineRadius, length))

    def renderLine(self, pnt1, pnt2):

        self.brashForLine()
        self.sizeForLine()
        self._renderLine(pnt1, pnt2)

    def renderArrow(self, pnt1, pnt2):

        self.brashForLine()
        self.sizeForLine()
        self.sizeForArrow()

        rArrow = self.styleArrowRadius
        lArrow = self.styleArrowLength

        v = gp_Vec(pnt1, pnt2)
        vLen = v.Magnitude()
        v *= (vLen - lArrow) / vLen
        pntM = pnt1.Translated(v)

        self._renderLine(pnt1, pntM)

        self.locatePosition(Direct(pntM, pnt2))
        self.basePrim(ConePrim(rArrow, 0, lArrow))

    def renderCircle(self, pnt1, pnt2, pnt3):

        self.brashForLine()
        self.sizeForLine()

        geomCircle = GC_MakeCircle(pnt1, pnt2, pnt3).Value()
        wire = BRepBuilderAPI_MakeEdge(geomCircle).Edge()

        self.locatePosition()
        self.baseWire(wire)

    def renderLabel(self, pnt, text):

        self.brashForLabel()
        self.sizeForLabel()

        delta = self.styleLabelDelta
        totalPos = Position().next(Translate(delta, delta, delta)).next(TranslateToPnt(pnt))

        self.locatePosition(totalPos)
        self.baseLabel(text)

    def _renderDeskPin(self, x, y):

        self.locatePosition(Translate(x / self.scale, y / self.scale, 0))
        self.basePrim(CylinderPrim(DESK_PIN_RADIUS / self.scale, DESK_PIN_HEIGHT / self.scale))

    def renderDesk(self):

        scale = self.scale
        labelText = self.scaleText

        paperSizeX, paperSizeY, paperSizeZ = DESK_PAPER_SIZE
        psx, psy, psz = paperSizeX / scale, paperSizeY / scale, paperSizeZ / scale
        bsx = (paperSizeX + scale * 2) / scale
        bsy = (paperSizeY + DESK_BORDER_SIZE * 2) / scale
        bsz = DESK_HEIGHT / scale

        self.brashForDeskPaper()
        self.locatePosition(Translate(-psx / 2, -psy / 2, -psz))
        self.basePrim(BoxPrim(psx, psy, psz))

        self.brashForDeskBoard()
        self.locatePosition(Translate(-bsx / 2, -bsy / 2, -psz - bsz))
        self.basePrim(BoxPrim(bsx, bsy, bsz))

        self.brashForDeskLabel()
        self.locatePosition(Translate(-bsx / 2, -bsy / 2, -psz))
        self.baseLabel(labelText)

        dx = (paperSizeX / 2 - DESK_PIN_OFFSET) / scale
        dy = (paperSizeY / 2 - DESK_PIN_OFFSET) / scale

        self.brashForDeskPin()
        self._renderDeskPin(-dx, -dy)
        self._renderDeskPin(dx, -dy)
        self._renderDeskPin(dx, dy)
        self._renderDeskPin(-dx, dy)


class ScreenRenderLib(RenderLib):

    def __init__(self, scaleAB=M_1_1_SCALE, screenX=800, screenY=600):
        super().__init__(scaleAB)

        self.screenX = screenX
        self.screenY = screenY

        self.display = None
        self.display_start = None

    def outStart(self):
        self.display, self.display_start, add_menu, add_function_to_menu = init_display(
            None, (self.screenX, self.screenY), True, [128, 128, 128], [128, 128, 128])

    def outFinish(self):
        self.display.FitAll()
        self.display_start()

    def outShape(self, shape):

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

    def outLabel(self, text):

        pnt = gp_Pnt(0, 0, 0).Transformed(self.basePosition)

        self.display.DisplayMessage(pnt, text, self.styleLabelHeightPx,
                                    self.styleColor, False)
