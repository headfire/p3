# from core_brash import *
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_TypeOfColor
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.Graphic3d import Graphic3d_MaterialAspect

from OCC.Display.SimpleGui import init_display

# from core_consts import *
# from core_draw import Draw, Styler, FinalShapeDraw, FinalTextDraw
# from core_position import Position
from core_draw import *
from core_mask import isMask

from OCC.Core.Graphic3d import Graphic3d_NameOfMaterial


BRASS_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_BRASS
BRONZE_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_BRONZE
COPPER_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_COPPER
GOLD_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_GOLD
PEWTER_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_PEWTER
PLASTER_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_PLASTER
PLASTIC_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_PLASTIC
SILVER_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_SILVER
STEEL_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_STEEL
STONE_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_STONE
SHINY_PLASTIC_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_SHINY_PLASTIC
SATIN_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_SATIN
METALIZED_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_METALIZED
NEON_GNC_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_NEON_GNC
CHROME_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_CHROME
ALUMINIUM_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_ALUMINIUM
OBSIDIAN_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_OBSIDIAN
NEON_PHC_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_NEON_PHC
JADE_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_JADE
CHARCOAL_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_CHARCOAL
WATER_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_WATER
GLASS_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_GLASS
DIAMOND_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_DIAMOND
TRANSPARENT_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_TRANSPARENT
DEFAULT_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_DEFAULT

WOOD_COLOR = 208/255, 117/255, 28/255
PAPER_COLOR = 230/255, 230/255, 230/255
STEEL_COLOR = 100/255, 100/255, 100/255

NICE_WHITE_COLOR = 240/255, 240/255, 240/255
NICE_GRAY_COLOR = 100/255, 100/255, 100/255
NICE_RED_COLOR = 200/255, 30/255, 30/255
NICE_BLUE_COLOR = 100/255, 100/255, 255/255
NICE_YELLOW_COLOR = 255/255, 255/255, 100/255
NICE_ORIGINAL_COLOR = 241/255, 79/255, 160/255

LABEL_STYLE = Style(SILVER_MATERIAL)
POINT_STYLE = Style(CHROME_MATERIAL, NICE_YELLOW_COLOR)
LINE_STYLE = Style(CHROME_MATERIAL, NICE_BLUE_COLOR)
# FACE_STYLE = Style(CHROME_MATERIAL, NICE_BLUE_COLOR) todo
SOLID_STYLE = Style(GOLD_MATERIAL)
SURFACE_STYLE = Style(PLASTIC_MATERIAL, NICE_GRAY_COLOR)

STANDARD_STYLES = [
    ('*:label', LABEL_STYLE),
    ('*:point', POINT_STYLE),
    ('*:line', LINE_STYLE),
    ('*:solid', SOLID_STYLE),
    ('*:surface', SURFACE_STYLE)
    #  ('*:face', FACE_STYLE) todo
]


class Styler:
    def __init__(self):
        self.styles = []

    def addStyles(self, rulesList):
        self.styles.extend(rulesList)

    def getStyle(self, renderPath):
        style = Style()
        for rule in reversed(self.styles):
            ruleMask, ruleStyle = rule
            if isMask(ruleMask, renderPath):
                style.mergeAll(ruleStyle)
        return style


class RenderLib:
    def __init__(self):
        self.renderNativeSuccess = False
        self.styler = Styler()
        self.styler.addStyles(STANDARD_STYLES)

    def _renderNative(self, draw, renderPosition, renderStyle, renderName): pass

    def _render(self, draw, renderPosition, renderStyle, renderName):
        mergedRenderName = renderName + '>' + draw.getNameWithCls()
        print(mergedRenderName)
        stylerStyle = self.styler.getStyle(renderName)
        mergedStyle = Style().mergeAll(renderStyle).mergeAll(draw.style).mergeAll(stylerStyle)  # parent first logic
        mergedPosition = Position().next(draw.position).next(renderPosition)  # child first logic
        draw.addStyledItems(mergedStyle)
        self._renderNative(draw, mergedPosition, mergedStyle, mergedRenderName)
        if not self.renderNativeSuccess:
            # item render mode if native mode not success
            for itemDraw in draw.items:
                self._render(itemDraw, mergedPosition, mergedStyle, mergedRenderName)

    def render(self, draw: Draw):
        self._render(draw, Position(), Style(), 'root')

    def renderStart(self):
        pass

    def renderFinish(self):
        pass


class ScreenRenderLib(RenderLib):
    def __init__(self, screenX: int = 800, screenY: int = 600):
        super().__init__()

        self.screenX = screenX
        self.screenY = screenY

        self.display = None
        self.display_start = None

    def renderStart(self):
        self.display, self.display_start, add_menu, add_function_to_menu = init_display(
            None, (self.screenX, self.screenY), True, [128, 128, 128], [128, 128, 128])

    def renderFinish(self):
        self.display.FitAll()
        self.display_start()

    def _nativeShape(self, shape, position: Position, style: Style):
        shapeTr = BRepBuilderAPI_Transform(shape, position.trsf).Shape()
        ais = AIS_Shape(shapeTr)

        material = style.get(MATERIAL)
        if material is not None:
            aspect = Graphic3d_MaterialAspect(material)
            ais.SetMaterial(aspect)

        transparency = style.get(TRANSPARENCY)
        if transparency is not None:
            ais.SetTransparency(transparency)

        color = style.get(COLOR)
        if color is not None:
            r, g, b = color
            qColor = Quantity_Color(r, g, b,
                                    Quantity_TypeOfColor(Quantity_TypeOfColor.Quantity_TOC_RGB))
            ais.SetColor(qColor)

        self.display.Context.Display(ais, False)

    def _nativeLabel(self, pnt, text, heightPx, position: Position, style: Style):
        labelPnt = pnt.Transformed(position.trsf)
        self.display.DisplayMessage(labelPnt, text, heightPx, style.get(COLOR, (0.7, 0.7, 0.7)), False)

    def _renderNative(self, draw, renderPosition, renderBrash, renderName):
        self.renderNativeSuccess = True
        if isinstance(draw, FinalShapeDraw):
            print('-> nativeShape()')
            self._nativeShape(draw.shape, renderPosition, renderBrash)
        elif isinstance(draw, FinalTextDraw):
            print('-> nativeLabel()')
            self._nativeLabel(draw.pnt, draw.text, draw.textHeightPx, renderPosition, renderBrash)
        else:
            self.renderNativeSuccess = False
