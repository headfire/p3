from core_consts import *


class Brash:
    def __init__(self, material=None, color=None, transparency=None):
        if isinstance(material, tuple):
            self.material, self.color, self.transparency = material
        else:
            self.material, self.color, self.transparency = material, color, transparency

    def getMaterial(self):
        return self.material

    def getColor(self):
        return self.color

    def getTransparency(self):
        return self.transparency


DEFAULT_STYLE_RULES = [

    ('', GENERAL_FACTOR_STYLE, 1),

    ('', POINT_RADIUS_FACTOR_STYLE, 1),
    ('', POINT_BRASH_STYLE, Brash(CHROME_MATERIAL, NICE_YELLOW_COLOR)),

    ('', LINE_RADIUS_FACTOR_STYLE, 1),
    ('', LINE_BRASH_STYLE, Brash(CHROME_MATERIAL, NICE_BLUE_COLOR)),

    ('', ARROW_RADIUS_FACTOR_STYLE, 1),
    ('', ARROW_LENGTH_FACTOR_STYLE, 1),

    ('', SURFACE_WIDTH_FACTOR_STYLE, 1),
    ('', SURFACE_BRASH_STYLE, Brash(CHROME_MATERIAL, NICE_ORIGINAL_COLOR)),

    ('', LABEL_DELTA_FACTOR_STYLE, 1),
    ('', LABEL_HEIGHT_FACTOR_STYLE, 1),
    ('', LABEL_BRASH_STYLE, Brash(PLASTIC_MATERIAL, NICE_WHITE_COLOR)),
]


class Styles:
    def __init__(self):
        self.renderName = ''

    @staticmethod
    def getScale():
        return 1

    def setRenderName(self, renderName: str):
        self.renderName = renderName

    def getStyle(self, styleName: str):
        for ruleRenderMask, ruleStyleName, ruleStyleValue in DEFAULT_STYLE_RULES:
            if ruleStyleName == styleName and self.renderName is not None:
                return ruleStyleValue
