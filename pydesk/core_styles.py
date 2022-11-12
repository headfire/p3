from core_consts import *


class Brash:
    def __init__(self, brashName='NoEffectBrash', material=None, color=None, transparency=None):
        self.brashName = brashName
        self.material, self.color, self.transparency = material, color, transparency

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
        self.brashName = parentBrash.brashName + '.' + self.brashName


DEFAULT_STYLE_RULES = [

    ('', SOLID_BRASH_STYLE, Brash('DefSolidBrash', GOLD_MATERIAL)),

    ('', GENERAL_FACTOR_STYLE, 1),

    ('', POINT_RADIUS_FACTOR_STYLE, 1),
    ('', POINT_BRASH_STYLE, Brash('DefPointBrash', CHROME_MATERIAL, NICE_YELLOW_COLOR, None)),

    ('', LINE_RADIUS_FACTOR_STYLE, 1),
    ('', LINE_BRASH_STYLE, Brash('DefLineBrash', CHROME_MATERIAL, NICE_BLUE_COLOR, None)),

    ('', ARROW_RADIUS_FACTOR_STYLE, 1),
    ('', ARROW_LENGTH_FACTOR_STYLE, 1),

    ('', SURFACE_WIDTH_FACTOR_STYLE, 1),
    ('', SURFACE_BRASH_STYLE, Brash('DefSurfaceBrash', CHROME_MATERIAL, NICE_ORIGINAL_COLOR, None)),

    ('', LABEL_DELTA_FACTOR_STYLE, 1),
    ('', LABEL_HEIGHT_FACTOR_STYLE, 1),
    ('', LABEL_BRASH_STYLE, Brash('DefLabelBrash', PLASTIC_MATERIAL, NICE_WHITE_COLOR, None)),
]


class Styles:
    def __init__(self):
        self.renderName = ''

    @staticmethod
    def getScale():
        return 1

    def _getStyle(self, styleName: str):
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
        if not isinstance(brash, Brash):
            raise NameError('No brash style with name ' + styleName)
        return brash
