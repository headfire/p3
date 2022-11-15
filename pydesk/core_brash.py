
'''
class Brash:
    def __init__(self, material=None, color=None, transparency=None):
        self.material, self.color, self.transparency = material, color, transparency

    def apply(self, style):
        if self.material is None:
            self.material = style.material
        if self.color is None:
            self.color = style.color
        if self.transparency is None:
            self.transparency = style.transparency
        return self
'''