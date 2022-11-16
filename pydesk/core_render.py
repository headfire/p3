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

    def _renderNative(self, draw, renderPosition, renderStyle, renderName):
        self.renderNativeSuccess = True
        if isinstance(draw, FinalShapeDraw):
            print('-> nativeShape()')
            self._nativeShape(draw.shape, renderPosition, renderStyle)
        elif isinstance(draw, FinalTextDraw):
            print('-> nativeLabel()')
            self._nativeLabel(draw.pnt, draw.text, draw.textHeightPx, renderPosition, renderStyle)
        else:
            self.renderNativeSuccess = False
