from OCC.Core.AIS import AIS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_TypeOfColor
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.Graphic3d import Graphic3d_MaterialAspect

from OCC.Display.SimpleGui import init_display

from core_consts import *
from core_draw import Draw, ShapeDraw, LabelDraw
from core_position import Position
from core_style import Style


class RenderLib:
    def __init__(self):
        self.rootDrawCounter = 0
        self.renderPosition = Position()
        self.renderStyle = Style
        self.renderNativeSuccess = False

    def _renderNative(self, draw, renderPosition, renderStyle, renderName, level): pass

    def _renderItems(self, draw, renderPosition, renderStyle, renderName, level):
        for itemName, itemDraw in draw.items.items():
            print('*** render sizeFactor ***', renderStyle.sizeFactor)
            mergedRenderName = renderName + '.' + itemName
            mergedStyle = Style().apply(renderStyle).apply(itemDraw.style)  # parent first logic
            mergedPosition = Position().next(itemDraw.position).next(renderPosition)  # child first logic
            self._render(itemDraw, mergedPosition, mergedStyle, mergedRenderName, level+1)

    def _render(self, draw, renderPosition, renderStyle, renderName, level):
        print(renderName)
        self._renderNative(draw, renderPosition, renderStyle, renderName, level)
        if not self.renderNativeSuccess:
            self._renderItems(draw, renderPosition, renderStyle, renderName, level)

    def render(self, draw: Draw):
        self.rootDrawCounter += 1
        self._render(draw, draw.position, draw.style, 'Object'+str(self.rootDrawCounter), 0)

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

        if style.material is not None:
            aspect = Graphic3d_MaterialAspect(style.material)
            ais.SetMaterial(aspect)

        if style.transparency is not None:
            ais.SetTransparency(style.transparency)

        if style.color is not None:
            r, g, b = style.color
            qColor = Quantity_Color(r, g, b,
                                    Quantity_TypeOfColor(Quantity_TypeOfColor.Quantity_TOC_RGB))
            ais.SetColor(qColor)

        self.display.Context.Display(ais, False)

    def _nativeLabel(self, pnt, text, position: Position, style: Style):
        labelPnt = pnt.Transformed(position.trsf)
        heightPx = NORMAL_LABEL_HEIGHT_PX * style.sizeFactor
        self.display.DisplayMessage(labelPnt, text, heightPx, style.color, False)

    def _renderNative(self, draw, renderPosition, renderStyle, renderName, level):
        self.renderNativeSuccess = True
        if isinstance(draw, ShapeDraw):
            print('-> nativeShape()')
            self._nativeShape(draw.shape, renderPosition, renderStyle)
        elif isinstance(draw, LabelDraw):
            print('-> nativeLabel()')
            self._nativeLabel(draw.pnt, draw.text, renderPosition, renderStyle)
        else:
            self.renderNativeSuccess = False
