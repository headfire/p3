from core_consts import *


class Style:
    def __init__(self, material=None, color=None, transparency=None, sizeFactor=1, sizeSubFactor=1):
        self.material, self.color, self.transparency = material, color, transparency
        self.sizeFactor, self.sizeSubFactor = sizeFactor, sizeSubFactor

    def next(self, nextStyle):
        if nextStyle.material is not None:
            self.material = nextStyle.material
        if nextStyle.color is not None:
            self.color = nextStyle.color
        if nextStyle.transparency is not None:
            self.transparency = nextStyle.transparency


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


class Styles:
    def __init__(self):
        self.renderName = ''  # todo delete this

    def getStyle(self, renderName):
        self.renderName = renderName  # todo  delete this
        for ruleRenderMask, ruleStyleName, ruleStyleValue in DEFAULT_STYLE_RULES:
            if ruleStyleName == styleName:
                return ruleStyleValue
        return Style()
