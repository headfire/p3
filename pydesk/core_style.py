from OCC.Core.Graphic3d import Graphic3d_NameOfMaterial

BRASS_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_BRASS
BRONZE_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_BRONZE
COPPER_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_COPPER
GOLD_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_GOLD
PEWTER_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_PEWTER
PLASTER_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_PLASTER
PLASTIC_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_PLASTIC
SILVER_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_SILVER
STEEL_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_STEEL
STONE_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_STONE
SHINY_PLASTIC_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_SHINY_PLASTIC
SATIN_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_SATIN
METALIZED_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_METALIZED
NEON_GNC_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_NEON_GNC
CHROME_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_CHROME
ALUMINIUM_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_ALUMINIUM
OBSIDIAN_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_OBSIDIAN
NEON_PHC_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_NEON_PHC
JADE_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_JADE
CHARCOAL_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_CHARCOAL
WATER_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_WATER
GLASS_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_GLASS
DIAMOND_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_DIAMOND
TRANSPARENT_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_TRANSPARENT
DEFAULT_MATERIAL = Graphic3d_NameOfMaterial.Graphic3d_NOM_DEFAULT

WOOD_COLOR = 208/255, 117/255, 28/255
PAPER_COLOR = 230/255, 230/255, 230/255
STEEL_COLOR = 100/255, 100/255, 100/255

NICE_WHITE_COLOR = 240/255, 240/255, 240/255
NICE_GRAY_COLOR = 100/255, 100/255, 100/255
NICE_RED_COLOR = 200/255, 30/255, 30/255
NICE_BLUE_COLOR = 100/255, 100/255, 255/255
NICE_YELLOW_COLOR = 255/255, 255/255, 100/255
NICE_ORIGINAL_COLOR = 241/255, 79/255, 160/255

MATERIAL = 'MATERIAL_STYLE'
COLOR = 'COLOR_STYLE'
TRANSPARENCY = 'TRANSPARENCY_STYLE'
SCALE = 'SCALE_STYLE'
SCALE_GEOM = 'SCALE_GEOM_STYLE'
SCALE_ARROW = 'SCALE_ARROW_STYLE'
SCALE_PX = 'SCALE_PX_STYLE'


LABEL_HEIGHT_PX = 20  # not scaled
LABEL_DELTA = 5
POINT_RADIUS = 4
LINE_RADIUS = 2
LINE_ARROW_RADIUS = 4
LINE_ARROW_LENGTH = 15
FACE_WIDTH = 1

AO_SIZE_XYZ = 1189, 841, 1

M_1_1_SCALE = (1, 1)
M_5_1_SCALE = (5, 1)

DESK_HEIGHT = 20
DESK_BORDER_SIZE = 60
DESK_PAPER_SIZE = 1189, 841, 1
DESK_PIN_OFFSET = 30
DESK_PIN_RADIUS = 10
DESK_PIN_HEIGHT = 2
DESK_DEFAULT_DRAW_AREA_SIZE = 400


class Style:
    def __init__(self, material=None, color=None, transparency=None):
        self.values = {}
        self.set(MATERIAL, material)
        self.set(COLOR, color)
        self.set(TRANSPARENCY, transparency)

    def get(self, styleName, defValue=None):
        value = self.values.get(styleName)
        if value is not None:
            return value
        return defValue

    def set(self, styleName, styleValue):
        if styleValue is not None:
            self.values[styleName] = styleValue

    def mergeOne(self, styleName, mergedStyleValue):
        if self.get(styleName) is None:
            self.set(styleName, mergedStyleValue)

    def merge(self, mergedStyle):
        for styleName, styleValue in mergedStyle.values.items():
            self.mergeOne(styleName, styleValue)
        return self

    def do(self, styleName, styleValue):
        self.set(styleName, styleValue)
        return self


LABEL_STYLE = Style(SILVER_MATERIAL)
POINT_STYLE = Style(CHROME_MATERIAL, NICE_YELLOW_COLOR)
LINE_STYLE = Style(CHROME_MATERIAL, NICE_BLUE_COLOR)
FACE_STYLE = Style(CHROME_MATERIAL, NICE_RED_COLOR, 0.5)
SOLID_STYLE = Style(GOLD_MATERIAL)
SURFACE_STYLE = Style(PLASTIC_MATERIAL, NICE_GRAY_COLOR)

STANDARD_STYLES = [
    ('*:label', LABEL_STYLE),
    ('*:point', POINT_STYLE),
    ('*:line', LINE_STYLE),
    ('*:solid', SOLID_STYLE),
    ('*:surface', SURFACE_STYLE),
    ('*:face', FACE_STYLE)
]
