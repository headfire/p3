from core_consts import *


class Style:
    def __init__(self, material=None, color=None, transparency=None, sizeFactor=None, sizeSubFactor=None):
        self.material, self.color, self.transparency = material, color, transparency
        self.sizeFactor, self.sizeSubFactor = sizeFactor, sizeSubFactor

    def apply(self, style):
        if self.material is None:
            self.material = style.material
        if self.color is None:
            self.color = style.color
        if self.transparency is None:
            self.transparency = style.transparency
        if self.sizeFactor is None:
            self.sizeFactor = style.sizeFactor
        if self.sizeFactor is None:
            self.sizeSubFactor = style.sizeSubFactor
        return self

    def getSize(self, normalSize):
        factor = 1
        if self.sizeFactor is not None:
            factor = self.sizeFactor
        return normalSize * factor

    def getSubSize(self, normalSize):
        factor = 1
        if self.sizeFactor is not None:
            factor = self.sizeFactor
        return self.getSize(normalSize) * factor


DEFAULT_STYLE_RULES = [

    ('', SOLID_BRASH_STYLE, Style(GOLD_MATERIAL)),

    ('', GENERAL_FACTOR_STYLE, 1),

    ('', POINT_RADIUS_FACTOR_STYLE, 1),
    ('', POINT_BRASH_STYLE, Style(CHROME_MATERIAL, NICE_YELLOW_COLOR)),

    ('', LINE_RADIUS_FACTOR_STYLE, 1),
    ('', LINE_BRASH_STYLE, Style(CHROME_MATERIAL, NICE_BLUE_COLOR)),

    ('', ARROW_RADIUS_FACTOR_STYLE, 1),
    ('', ARROW_LENGTH_FACTOR_STYLE, 1),

    ('', SURFACE_WIDTH_FACTOR_STYLE, 1),
    ('', SURFACE_BRASH_STYLE, Style(CHROME_MATERIAL, NICE_ORIGINAL_COLOR)),

    ('', LABEL_DELTA_FACTOR_STYLE, 1),
    ('', LABEL_HEIGHT_FACTOR_STYLE, 1),
    ('', LABEL_BRASH_STYLE, Style(PLASTIC_MATERIAL, NICE_WHITE_COLOR)),
]

'''
ROOT_STYLE_PREFIX = 'Root'


class Styles:
    def __init__(self):
        self.renderName = ''  # todo delete this

    def getStyle(self, renderName):
        self.renderName = renderName  # todo  delete this
        for ruleRenderMask, ruleStyleName, ruleStyleValue in DEFAULT_STYLE_RULES:
            if ruleStyleName == styleName:
                return ruleStyleValue
        return Style()

    def set(self, path, style: Style) -> None:
        self.styleList[path] = Style
'''
