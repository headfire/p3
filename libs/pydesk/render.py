from OCC.Core.AIS import AIS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_TypeOfColor
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.Graphic3d import Graphic3d_MaterialAspect

from OCC.Display.SimpleGui import init_display

from draw import Draw, ShapeDraw, LabelDraw
from position import Position
from styles import Brash, Styles


class RenderLib:
    def __init__(self, styles: Styles = Styles()):
        self.styles = styles

    def render(self, draw: Draw, position: Position = Position(), brash: Brash = None, renderName: str = ''):
        self.styles.setRenderName(renderName)
        scene = draw.getStyledScene(self.styles)
        for sceneItemName, sceneItem in scene.items():
            sceneItemDraw, sceneItemPosition, sceneItemBrash = sceneItem
            if brash is not None:
                sceneItemBrash = brash
            self.render(sceneItemDraw, sceneItemPosition, sceneItemBrash, renderName + ',' + sceneItemName)

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

    def renderShapeDraw(self, draw: ShapeDraw, position: Position, brash: Brash):
        shapeTr = BRepBuilderAPI_Transform(draw.shape, position.getTrsf()).Shape()
        ais = AIS_Shape(shapeTr)

        ais.SetTransparency(brash.getTransparency())
        # todo None color - original material color
        r, g, b = brash.getColor()
        qColor = Quantity_Color(r, g, b,
                                Quantity_TypeOfColor(Quantity_TypeOfColor.Quantity_TOC_RGB))
        ais.SetColor(qColor)

        aspect = Graphic3d_MaterialAspect(brash.getMaterial())
        ais.SetMaterial(aspect)


        self.display.Context.Display(ais, False)

    def renderLabelDraw(self, draw: LabelDraw, position: Position, brash: Brash):
        pnt = draw.pnt.Transformed(position.getTrsf())
        self.display.DisplayMessage(pnt, draw.text, draw.hPx, brash.getColor(), False)

    def render(self, draw: Draw, position: Position = Position(), brash: Brash = None, renderName: str = ''):
        if isinstance(draw, ShapeDraw):
            self.renderShapeDraw(draw, position, brash)
        elif isinstance(draw, LabelDraw):
            self.renderLabelDraw(draw, position, brash)
        else:
            super().render(draw, position, brash, renderName)
