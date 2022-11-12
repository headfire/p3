from OCC.Core.AIS import AIS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_TypeOfColor
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.Graphic3d import Graphic3d_MaterialAspect

from OCC.Display.SimpleGui import init_display

from core_draw import Draw, ShapeDraw, LabelDraw
from core_position import Position
from core_styles import Style, Styles


class RenderLib:
    def __init__(self, styles: Styles = Styles()):
        self.styles = styles

    def render(self, draw: Draw, position=Position(), brash=Style(), renderName: str = 'Object'):
        print(renderName)
        self.styles.setRenderName(renderName)
        scene = draw.getStyledScene(self.styles)
        for itemName, item in scene.items():
            itemDraw, itemPosition, itemBrash = item
            itemBrash.mergeWithParent(brash)
            itemPosition.mergeWithParent(position)
            newRenderName = renderName + '.' + itemName
            self.render(itemDraw, itemPosition, itemBrash, newRenderName)

    def renderStart(self):
        pass

    def renderFinish(self):
        pass


class ScreenRenderLib(RenderLib):
    def __init__(self, screenX: int = 800, screenY: int = 600, styles=Styles()):
        super().__init__(styles)

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

    def _outShapeDraw(self, draw: ShapeDraw, position: Position, brash: Style):
        shapeTr = BRepBuilderAPI_Transform(draw.shape, position.getTrsf()).Shape()
        ais = AIS_Shape(shapeTr)

        material = brash.getMaterial()
        if material is not None:
            aspect = Graphic3d_MaterialAspect(material)
            ais.SetMaterial(aspect)

        transparency = brash.getTransparency()
        if transparency is not None:
            ais.SetTransparency(brash.getTransparency())

        color = brash.getColor()
        if color is not None:
            r, g, b = brash.getColor()
            qColor = Quantity_Color(r, g, b,
                                    Quantity_TypeOfColor(Quantity_TypeOfColor.Quantity_TOC_RGB))
            ais.SetColor(qColor)

        self.display.Context.Display(ais, False)

    def _outLabelDraw(self, draw: LabelDraw, position: Position, brash: Style):
        pnt = draw.pnt.Transformed(position.getTrsf())
        self.display.DisplayMessage(pnt, draw.text, draw.hPx, brash.getColor(), False)

    def render(self, draw: Draw, position: Position = Position(), brash: Style = Style(),
               renderName: str = 'Object') -> None:
        if isinstance(draw, ShapeDraw):
            print(renderName, '-> outShape')
            self._outShapeDraw(draw, position, brash)
        elif isinstance(draw, LabelDraw):
            print(renderName, '-> outLabel')
            self._outLabelDraw(draw, position, brash)
        else:
            super().render(draw, position, brash, renderName)
