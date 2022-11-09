from OCC.Core.Graphic3d import Graphic3d_NameOfMaterial

class Brash:
    def __init__(self, material, color256, transparency):
        self.material, self.color256, self.transparency = material, color256, transparency

    def getMaterial(self):
        return self.material

    def getColor(self):
        r, g, b = self.color256
        return (r/255, g/255, b/255)

    def getTransparency(self):
        return self.transparency


class Styles:

    def setRenderName(self, renderName: str): pass

    def getStyle(self, styleName: str):
      #  if styleName == 'SOLID_BRASH_STYLE':
        return Brash(GOLD_MATERIAL, NICE_YELLOW_COLOR, 0.7)
