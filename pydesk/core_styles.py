from core_consts import *


class Brash:
    def __init__(self, material=None, color=None, transparency=None):
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

    def setRenderName(self, renderName: str):
        self.renderName = renderName

    def getStyle(self, styleName: str):
        if styleName == SOLID_BRASH_STYLE and self.renderName is not None:
            return Brash(GOLD_MATERIAL)
