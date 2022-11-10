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
