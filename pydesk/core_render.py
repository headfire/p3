from core_brash import *
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_TypeOfColor
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.Graphic3d import Graphic3d_MaterialAspect

from OCC.Display.SimpleGui import init_display

# from core_consts import *
# from core_draw import Draw, Styler, FinalShapeDraw, FinalTextDraw
from core_position import Position
from core_draw import *

POINT_CLASSES = [PointDraw]
SOLID_CLASSES = [BoxDraw, SphereDraw, ConeDraw, TorusDraw, CylinderDraw]
LINE_CLASSES = [VectorDraw, ArrowDraw, LineDraw, Circle3Draw, WireDraw]
FACE_CLASSES = [SurfaceDraw]
LABEL_CLASSES = [LabelDraw]

LABEL_STYLE: Style(SILVER_MATERIAL)
POINT_STYLE: Style(CHROME_MATERIAL, NICE_YELLOW_COLOR)
LINE_STYLE: Style(CHROME_MATERIAL, NICE_BLUE_COLOR)
FACE_STYLE: Style(CHROME_MATERIAL, NICE_BLUE_COLOR)
SOLID_STYLE: Style(GOLD_MATERIAL)
SURFACE_STYLE: Style(PLASTIC_MATERIAL, NICE_GRAY_COLOR)


class MaskStep:
    def __init__(self, names=None, nums=None, classes=None):
        self.names = names
        self.nums = nums
        self.classes = classes

    def checkName(self, objName):
        if self.names is None:
            return True
        for nm in self.names:
            if nm == objName:
                return True
        return False

    def checkNum(self, objNum):
        if self.nums is None:
            return True
        for num in self.nums:
            if num == objNum:
                return True
        return False

    def checkClass(self, objClass):
        if self.classes is None:
            return True
        for cls in self.classes:
            if cls == objClass:
                return True
        return False

    def check(self, objName, objNumber, objClass):
       return  self.checkName() and self.checkNum() and self.checkClass()




class Styler:
    def __init__(self):
        self.rules = []
        self.addRule(Mask(classes=POINT_CLASSES), POINT_STYLE)
        self.addRule(Mask(classes=LINE_CLASSES), LINE_STYLE)
        self.addRule(Mask(classes=SOLID_CLASSES), SOLID_STYLE)
        self.addRule(Mask(classes=SURFACE_CLASSES), SURFACE_STYLE)
        self.addRule(Mask(classes=FACE_CLASSES), FACE_STYLE)

        self.addRule(':VectorDraw, ArrowDraw, LineDraw, Circle3Draw, WireDraw]', MATERIAL_STYLE, CHROME_MATERIAL)
        self.addRule(':VectorDraw, ArrowDraw, LineDraw, Circle3Draw, WireDraw]', COLOR_STYLE, NICE_BLUE_COLOR)


    def addRule(self, mask, styleName, styleValue):
        self.rules.append((mask, styleName, styleValue))

    def isRuleMath(self, ruleMaskPath, renderPath):
        i = 0
        while i < len(renderPath) and i < (ruleMaskPath):

            i++

    def get(self, renderPath):
        style = Style()
        for rule in reversed(self.rules):
            ruleMaskPath, ruleStyle = rule
            if self.isRuleMatch(ruleMaskPath, renderPath):
                style.mergeAll(ruleStyle)


        style = Style()
        for rule in self.rules:
            mask, styleName, styleValue = rule
            if _isMask(mask, renderName):
                style.set(styleName, styleValue)
        return style


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
        elif isinstance(draw, FinalTextDraw):
            print('-> nativeLabel()')
            self._nativeLabel(draw.pnt, draw.text, draw.textHeightPx, renderPosition, renderBrash)
        else:
            self.renderNativeSuccess = False
