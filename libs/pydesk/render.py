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

from device import ScreenDevice, WebDevice, StlDevice

from std import Move

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

MATE = 'PLASTIC'
CHROME = 'CHROME'

MATERIAL_TYPE_CONSTS = {
    'BRASS': Graphic3d_NameOfMaterial.Graphic3d_NOM_BRASS,
    'BRONZE': Graphic3d_NameOfMaterial.Graphic3d_NOM_BRONZE,
    'COPPER': Graphic3d_NameOfMaterial.Graphic3d_NOM_COPPER,
    'GOLD': Graphic3d_NameOfMaterial.Graphic3d_NOM_GOLD,
    'PEWTER': Graphic3d_NameOfMaterial.Graphic3d_NOM_PEWTER,
    'PLASTER': Graphic3d_NameOfMaterial.Graphic3d_NOM_PLASTER,
    'PLASTIC': Graphic3d_NameOfMaterial.Graphic3d_NOM_PLASTIC,
    'SILVER': Graphic3d_NameOfMaterial.Graphic3d_NOM_SILVER,
    'STEEL': Graphic3d_NameOfMaterial.Graphic3d_NOM_STEEL,
    'STONE': Graphic3d_NameOfMaterial.Graphic3d_NOM_STONE,
    'SHINY_PLASTIC': Graphic3d_NameOfMaterial.Graphic3d_NOM_SHINY_PLASTIC,
    'SATIN': Graphic3d_NameOfMaterial.Graphic3d_NOM_SATIN,
    'METALIZED': Graphic3d_NameOfMaterial.Graphic3d_NOM_METALIZED,
    'NEON_GNC': Graphic3d_NameOfMaterial.Graphic3d_NOM_NEON_GNC,
    'CHROME': Graphic3d_NameOfMaterial.Graphic3d_NOM_CHROME,
    'ALUMINIUM': Graphic3d_NameOfMaterial.Graphic3d_NOM_ALUMINIUM,
    'OBSIDIAN': Graphic3d_NameOfMaterial.Graphic3d_NOM_OBSIDIAN,
    'NEON_PHC': Graphic3d_NameOfMaterial.Graphic3d_NOM_NEON_PHC,
    'JADE': Graphic3d_NameOfMaterial.Graphic3d_NOM_JADE,
    'CHARCOAL': Graphic3d_NameOfMaterial.Graphic3d_NOM_CHARCOAL,
    'WATER': Graphic3d_NameOfMaterial.Graphic3d_NOM_WATER,
    'GLASS': Graphic3d_NameOfMaterial.Graphic3d_NOM_GLASS,
    'DIAMOND': Graphic3d_NameOfMaterial.Graphic3d_NOM_DIAMOND,
    'TRANSPARENT': Graphic3d_NameOfMaterial.Graphic3d_NOM_TRANSPARENT,
    'DEFAULT': Graphic3d_NameOfMaterial.Graphic3d_NOM_DEFAULT
}


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

class Material:
    def __init__(self, aColor, aType, aTransp):
        self.aColor, self.aType,  self.aTransp = aColor, aType, aTransp


class Style:
    def __init__(self):

        self.pointRadius = 3
        self.lineRadius = 5
        self.faceHalfWidth = 1.5
        self.arrowRadius = 3
        self.arrowLen = 15
        self.labelDelta = 5
        self.labelHeightPx = 20

        self.pointMaterial = Material(NICE_YELLOW_COLOR, CHROME, 0.0)
        self.lineMaterial = Material(NICE_BLUE_COLOR, CHROME, 0.0)
        self.faceMaterial = Material(NICE_ORIGINAL_COLOR, CHROME, 0.0)
        self.labelMaterial = Material(NICE_ORIGINAL_COLOR, CHROME, 0.0)

    def scale(self, scale):
        self.pointRadius *= scale
        self.lineRadius *= scale
        self.faceHalfWidth *= scale
        self.arrowRadius *= scale
        self.arrowLen *= scale
        self.labelDelta *= scale


class RenderHints:
    def __init__(self, sceneName='', scaleA=1, scaleB=1):

        # device size
        self.deviceX = 800
        self.deviceY = 600

        # scale factor
        scale = scaleB / scaleA
        self.sceneLabel = sceneName + '- A0 M' + str(scaleA) + ':' + str(scaleB)

        self.basePointRadius = 5 * scale
        self.baseLineRadius = 3 * scale

        self.shapePrecision = 1 * scale
        self.wirePrecision = 1 * scale

        self.deskDX = 0 * scale
        self.deskDY = 0 * scale
        self.deskDZ = 300 * scale

        self.limitMinX = -200 * scale
        self.limitMaxX = 200 * scale
        self.limitMinY = -200 * scale
        self.limitMaxY = 200 * scale
        self.limitMinZ = -200 * scale
        self.limitMaxZ = 200 * scale

        # desk position
        self.deskDX = 0
        self.deskDY = 0
        self.deskDZ = -250 * scale

        # decoration flags
        self.isDesk = True
        self.isAxis = True
        self.isLimits = True

        # path to save
        self.pathToSave = None

        # styles
        mainStyle = Style()
        mainStyle.scale(scale * 1)

        infoStyle = Style()
        infoStyle.scale(scale * 0.7)
        infoStyle.pointMaterial = Material(NICE_GRAY_COLOR, MATE, 0.5)
        infoStyle.lineMaterial = Material(NICE_GRAY_COLOR, MATE, 0.5)
        infoStyle.faceMaterial = Material(NICE_GRAY_COLOR, MATE, 0.5)
        infoStyle.labelMaterial = Material(NICE_GRAY_COLOR, MATE, 0.0)

        focusStyle = Style()
        focusStyle.scale(scale * 0.7)
        focusStyle.pointMaterial = Material(NICE_RED_COLOR, MATE, 0.0)
        focusStyle.lineMaterial = Material(NICE_RED_COLOR, MATE, 0.0)
        focusStyle.faceMaterial = Material(NICE_RED_COLOR, MATE, 0.5)
        focusStyle.labelMaterial = Material(NICE_RED_COLOR, MATE, 0.0)

        self.styles = {
            'MainStyle': mainStyle,
            'InfoStyle': infoStyle,
            'FocusStyle': focusStyle,
        }

        self.aBoardH = 20 * scale
        self.aBoardBorderSize = 60 * scale
        self.aBoardWoodStyle = Material(WOOD_COLOR, MATE, 0)

        self.aPaperSizes = 1189 * scale, 841* scale, 1* scale
        self.aPaperStyle = Material(PAPER_COLOR, MATE, 0)

        self.aPinOffset = 30 * scale
        self.aPinR = 10 * scale
        self.aPinH = 2 * scale
        self.aPinStyle = Material(STEEL_COLOR, CHROME, 0)

    def setDeviceSize(self, deviceX, deviceY):
        self.deviceX = deviceX
        self.deviceY = deviceY

    def setPathToSave(self, pathToSave):
        self.pathToSave = pathToSave

    def setPrecision(self, wirePrecision, shapePrecision):
        self.wirePrecision = wirePrecision
        self.shapePrecision = shapePrecision

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


class RenderLib():

    def __init__(self, hints=RenderHints()):
        self.hints = hints
        self.aStyle = Style()
        self.aMove = Move()
        self.device = None
        self.localMove = Move()

    def startRender(self):
        self.device = ScreenDevice(self.hints)

    def finishRender(self):
        self.device.display.FitAll()
        self.device.start_display()

    def renderShapeObj(self, aShape, aMaterial):
        shapeTr = BRepBuilderAPI_Transform(aShape, self.aMove.getTrsf()).Shape()
        ais = AIS_Shape(shapeTr)
        r, g, b = aMaterial.aColor
        aisColor = Quantity_Color(r, g, b,
                                  Quantity_TypeOfColor(Quantity_TypeOfColor.Quantity_TOC_RGB))
        ais.SetColor(aisColor)
        ais.SetTransparency(self.aStyle.getNormedTransparency())
        aspect = Graphic3d_MaterialAspect(MATERIAL_TYPE_CONSTS[self.aStyle.getMaterial()])
        ais.SetMaterial(aspect)
        self.device.display.Context.Display(ais, False)

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

    def renderSphere(self, aRadius):
        shape = BRepPrimAPI_MakeSphere(aRadius).Shape()
        self.renderShapeObj(shape, self.aStyle.faceMaterial)

    def renderCone(self, aRadius1, aRadius2, aHeight):
        shape = BRepPrimAPI_MakeCone(aRadius1, aRadius2, aHeight).Shape()
        self.renderShapeObj(shape, self.aStyle.faceMaterial)

    def renderCylinder(self, aRadius, aHeight):
        shape = BRepPrimAPI_MakeCylinder(aRadius, aHeight).Shape()
        self.renderShapeObj(shape, self.aStyle.faceMaterial)

    def renderTorus(self, aRadius1, aRadius2):
        shape = BRepPrimAPI_MakeTorus(aRadius1, aRadius2).Shape()
        self.renderShapeObj(shape, self.aStyle.faceMaterial)

    def renderPoint(self, aPnt):
        self.localMove.setMove(aPnt.X, aPnt.Y, aPnt.Z)
        shape = BRepPrimAPI_MakeSphere(self.aStyle.pointRadius).Shape()
        self.renderShapeObj(shape, self.aStyle.faceMaterial)

    def renderLine(self, aPnt1, aPnt2):

        vec = gp_Vec(aPnt1, aPnt2)
        self.localMove.setDirect(aPnt1, aPnt2)
        self.renderCylinder(self.aStyle.lineRadius, vec.Magnitude())
        shape = BRepPrimAPI_MakeCylinder(aRadius, aHeight).Shape()
        self.renderShapeObj(shape, self.aStyle.lineMaterial)

    def renderVector(self, aPnt1, aPnt2):
        rArrow = self.aStyle.getArrowRadius(self.hints.scale)
        hArrow = self.aStyle.getArrowHeight(self.hints.scale)
        v = gp_Vec(aPnt1, aPnt2)
        vLen = v.Magnitude()
        v *= (vLen - hArrow) / vLen
        pntM = aPnt1.Translated(v)

        self.renderLine(aPnt1, pntM)
        self.localMove.setDirect(pntM, aPnt2)
        self.renderCone(rArrow, 0, hArrow)
        self.localMove = Move()

    def renderCircle(self, aPnt1, aPnt2, aPnt3):
        geomCircle = GC_MakeCircle(aPnt1, aPnt2, aPnt3).Value()
        wire = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
        self.renderWireObj(wire)

    def renderLabel(self, aPnt, aText):
        self.localMove.setMove(aPnt.X, aPnt.Y, aPnt.Z)
        aHeightPx = self.aStyle.getLabelHeight()
        pnt = gp_Pnt(0, 0, 0).Transformed(self.aMove.getTrsf())
        self.device.display.DisplayMessage(pnt, aText, aHeightPx, self.aStyle.getNormedColor(), False)


    def render(self, aDraw, aMove=Move(), aStyle=Style()):
        aDraw.drawTo(self, aMove, aStyle)


    def renderDesk(self): pass
    def renderAxis(self): pass
    def renderLimits(self): pass

    def renderDecoration(self):
        if self.hints.isDesk:
            self.renderDesk()
        if self.hints.isAxis:
            self.renderAxis()
        if self.hints.isLimits:
            self.renderLimits()

    def setMoveAndStyle(self, aMove, aStyle):
        self.aStyle = aStyle
        self.aMove = aMove

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
