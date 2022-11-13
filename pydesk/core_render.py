from OCC.Core.AIS import AIS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_TypeOfColor
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.Graphic3d import Graphic3d_MaterialAspect

from OCC.Display.SimpleGui import init_display

# from core_consts import *
from core_draw import Draw, Styler, FinalShapeDraw, FinalLabelDraw
from core_position import Position
from core_style import Brash


class RenderLib:
    def __init__(self):
        self.rootDrawCounter = 0
        self.renderPosition = Position()
        self.renderBrash = Brash
        self.renderNativeSuccess = False
        self.styler = Styler()

    def _renderNative(self, draw, renderPosition, renderBrash, renderName, level): pass

    def _renderItems(self, draw, renderPosition, renderBrash, renderName, level):
        for itemName, itemContainer in draw.items.items():
            itemDraw, itemPosition, itemBrash = itemContainer
            mergedRenderName = renderName + '->' + itemName + ':' + itemDraw.__class__.__name__
            mergedBrash = Brash().apply(renderBrash).apply(itemBrash)  # parent first logic
            mergedPosition = Position().next(itemPosition).next(renderPosition)  # child first logic
            self._render(itemDraw, mergedPosition, mergedBrash, mergedRenderName, level+1)

    def _render(self, draw, renderPosition, renderBrash, renderName, level):
        print(renderName)
        self._renderNative(draw, renderPosition, renderBrash, renderName, level)
        if not self.renderNativeSuccess:
            print('***** Render items ***')
            draw.addStyledItems(self.styler)
            self._renderItems(draw, renderPosition, renderBrash, renderName, level)

    def render(self, draw: Draw, position=Position(), brash=Brash(), nm=''):
        if nm == '':
            self.rootDrawCounter += 1
            nm = 'renderObj' + str(self.rootDrawCounter) + ':' + draw.__class__.__name__
        self._render(draw, position, brash, nm, 0)

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

    def _nativeShape(self, shape, position: Position, brash: Brash):
        shapeTr = BRepBuilderAPI_Transform(shape, position.trsf).Shape()
        ais = AIS_Shape(shapeTr)

        if brash.material is not None:
            aspect = Graphic3d_MaterialAspect(brash.material)
            ais.SetMaterial(aspect)

        if brash.transparency is not None:
            ais.SetTransparency(brash.transparency)

        if brash.color is not None:
            r, g, b = brash.color
            qColor = Quantity_Color(r, g, b,
                                    Quantity_TypeOfColor(Quantity_TypeOfColor.Quantity_TOC_RGB))
            ais.SetColor(qColor)

        self.display.Context.Display(ais, False)

    def _nativeLabel(self, pnt, text, heightPx, position: Position, brash: Brash):
        labelPnt = pnt.Transformed(position.trsf)
        self.display.DisplayMessage(labelPnt, text, heightPx, brash.color, False)

    def _renderNative(self, draw, renderPosition, renderBrash, renderName, level):
        self.renderNativeSuccess = True
        if isinstance(draw, FinalShapeDraw):
            print('-> nativeShape()')
            self._nativeShape(draw.shape, renderPosition, renderBrash)
        elif isinstance(draw, FinalLabelDraw):
            print('-> nativeLabel()')
            self._nativeLabel(draw.pnt, draw.text, draw.textHeightPx, renderPosition, renderBrash)
        else:
            self.renderNativeSuccess = False
