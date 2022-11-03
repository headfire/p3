
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
from device import WebSaverLib, StlSaverLib

from std import Style, Move


MATERIAL_CONSTS = {
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


class RenderHints:
    def __init__(self):

        self.sceneName = None

        # device size
        self.deviceX = None
        self.sdeviceY = None

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

        self.basePointRadius = 5*self.scale
        self.baseLineRadius = 3*self.scale

        self.shapePrecision = 1*self.scale
        self.wirePrecision = 1*self.scale

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


class RenderLib:
    def __init__(self, hints=RenderHints()):
        self.hints = hints
        self.aStyle = Style()
        self.aMove = Move()
        self.device = None

    def startRender(self): pass

    def render(self, aDraw, aMove, aStyle):
        aDraw.renderTo(self, aMove, aStyle)

    def finishRender(self): pass

    def setMoveAndStyle(self, aMove, aStyle):
        self.aStyle = aStyle
        self.aMove = aMove

    def renderTextObj(self, aText, aHeightPx): pass

    def renderShapeObj(self, aShape): pass

    def renderWireObj(self, aWire, aWireRadius): pass

    def renderLabel(self, aText, aHeightPx):
        self.renderTextObj(aText, aHeightPx)

    def renderBox(self, aSizeX, aSizeY, aSizeZ):
        shape = BRepPrimAPI_MakeBox(aSizeX, aSizeY, aSizeZ).Shape()
        self.renderShapeObj(shape)

    def renderSphere(self, aRadius):
        shape = BRepPrimAPI_MakeSphere(aRadius).Shape()
        self.renderShapeObj(shape)

    def renderCone(self, aRadius1, aRadius2, aHeight):
        shape = BRepPrimAPI_MakeCone(aRadius1, aRadius2, aHeight).Shape()
        self.renderShapeObj(shape)

    def renderCylinder(self, aRadius, aHeight):
        shape = BRepPrimAPI_MakeCylinder(aRadius, aHeight).Shape()
        self.renderShapeObj(shape)

    def renderTorus(self, aRadius1, aRadius2):
        shape = BRepPrimAPI_MakeTorus(aRadius1, aRadius2).Shape()
        self.renderShapeObj(shape)

    def renderWire(self, aWire, aWireRadius):
        self.renderWireObj(aWire, aWireRadius)

    def renderSurface(self, aSurface):
        self.renderShapeObj(aSurface)

    def renderPoint(self, aPnt, aPointRadius):
        Move().setMove(aPnt.X, aPnt.Y, aPnt.Z)
        self.renderSphere(aPointRadius)

    def renderLine(self, aPnt1, aPnt2, aLineRadius):
        Move().setMove(aPnt1.X, aPnt1.Y, aPnt1.Z)
        Move().setMove(aPnt2.X, aPnt2.Y, aPnt2.Z)
        self.renderCylinder(aLineRadius, 10)

    def renderCircle(self, aPnt1, aPnt2, aPnt3, aLineWidth):
        geomCircle = GC_MakeCircle(aPnt1, aPnt2, aPnt3).Value()
        wire = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
        self.renderWireObj(wire, aLineWidth)

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


class ScreenRenderLibParams:
    def __init__(self, xSize=800, ySize=600):
        self.xSize = xSize
        self.ySize = ySize


class ScreenRenderLib(RenderLib):

    def startRender(self):
        self.device = ScreenDevice(hints)

    def finishRender(self):
        self.device.display.FitAll()
        self.device.start_display()

    def renderTextObj(self, aText, aHeightPx):
        pnt = gp_Pnt(0, 0, 0).Transformed(self.aMove.getTrsf())
        self.device.display.DisplayMessage(pnt, aText, aHeightPx, self.aStyle.getNormedColor(), False)

    def renderShapeObj(self, aShape):
        shapeTr = BRepBuilderAPI_Transform(aShape, self.aMove.getTrsf()).Shape()
        ais = AIS_Shape(shapeTr)
        r, g, b = self.aStyle.getNormedColor()
        aisColor = Quantity_Color(r, g, b,
                                  Quantity_TypeOfColor(Quantity_TypeOfColor.Quantity_TOC_RGB))
        ais.SetColor(aisColor)
        ais.SetTransparency(self.aStyle.getNormedTransparency())
        aspect = Graphic3d_MaterialAspect(MATERIAL_CONSTS[self.aStyle.getMaterial()])
        ais.SetMaterial(aspect)
        self.device.display.Context.Display(ais, False)

    def renderWireObj(self, aWire, aWireRadius):
        startPoint, tangentDir = _getWireStartPointAndTangentDir(aWire)
        profileCircle = GC_MakeCircle(startPoint, tangentDir, aWireRadius).Value()
        profileEdge = BRepBuilderAPI_MakeEdge(profileCircle).Edge()
        profileWire = BRepBuilderAPI_MakeWire(profileEdge).Wire()

        shape = BRepOffsetAPI_MakePipe(aWire, profileWire).Shape()

        self.renderShapeObj(shape)


class WebRenderLib(RenderLib):

    def startRender(self):
        self.saver = WebSaverLib(self.hints)

    def renderTextObj(self, aText, aHeightPx):
        pnt = gp_Pnt(0, 0, 0).Transformed(self.aMove.getTrsf())
        color = self.aStyle.getNormedColor()
        self.saver.drawLabel(pnt, aText, color)

    def renderShapeObj(self, aShape):
        shapeTr = BRepBuilderAPI_Transform(aShape, self.aMove.getTrsf()).Shape()
        color = self.aStyle.getNormedColor()
        transparency = self.aStyle.getNormedTransparency()
        self.saver.drawShape(shapeTr, color, transparency)

    def finishRender(self):
        self.saver.save()


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
        self.saver = StlSaverLib(self.hints)

    def renderShapeObj(self, aShape):
        shapeTr = BRepBuilderAPI_Transform(aShape, self.aMove.getTrsf()).Shape()
        self.saver.drawShape(shapeTr)

    def finishRender(self):
        self.saver.save()
