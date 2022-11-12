from core_consts import *


class Style:
    def __init__(self, material=None, color=None, transparency=None, sizeFactor=1, lengthFactor=1):
        self.material, self.color, self.transparency = material, color, transparency
        self.sizeFactor, self.lengthFactor = sizeFactor, lengthFactor

    def getMaterial(self):
        return self.material

    def getColor(self):
        return self.color

    def getTransparency(self):
        return self.transparency

    def mergeWithParent(self, parentBrash):
        if parentBrash.material is not None:
            self.material = parentBrash.material
        if parentBrash.color is not None:
            self.color = parentBrash.color
        if parentBrash.material is not None:
            self.transparency = parentBrash.transparency


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
    ('', SURFACE_BRASH_STYLE, Style('DefSurfaceBrash', CHROME_MATERIAL, NICE_ORIGINAL_COLOR, None)),

    ('', LABEL_DELTA_FACTOR_STYLE, 1),
    ('', LABEL_HEIGHT_FACTOR_STYLE, 1),
    ('', LABEL_BRASH_STYLE, Style('DefLabelBrash', PLASTIC_MATERIAL, NICE_WHITE_COLOR, None)),
]


class Styles:
    def __init__(self):
        self.renderName = ''

    @staticmethod
    def getScale():
        return 1

    @staticmethod
    def _getStyle(styleName: str):
        for ruleRenderMask, ruleStyleName, ruleStyleValue in DEFAULT_STYLE_RULES:
            if ruleStyleName == styleName:
                return ruleStyleValue
        return None

    def setRenderName(self, renderName: str):
        self.renderName = renderName

    def getScaledSize(self, normalSize, factorStyleName):
        scale = self.getScale()
        generalFactor = self._getStyle(GENERAL_FACTOR_STYLE)
        localFactor = self._getStyle(factorStyleName)
        return normalSize * scale * generalFactor * localFactor

    def getBrash(self, styleName):
        brash = self._getStyle(styleName)
        if not isinstance(brash, Style):
            raise NameError('No brash style with name ' + styleName)
        return brash
