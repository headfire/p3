from core_desk import *


def DrawTestNull():
    pass


def DrawTestSphere():
    DrawSphere(15)


def DrawTestMove():
    for ix in [-1, 1]:
        for iy in [-1, 1]:
            for iz in [-1, 1]:
                DrawSphere(10)
                DoMove(ix * 20, iy * 20, iz * 20)


def DrawTestColor():
    n = 5
    for ix in range(n):
        for iy in range(n):
            for iz in range(n):
                SetColor([ix / (n - 1), iy / (n - 1), iz / (n - 1)])
                DrawSphere(10)
                DoMove(ix * 30, iy * 30, iz * 30)


def DrawTestTransparency():
    SetColor(NICE_BLUE_COLOR)
    n = 5
    for ix in range(n):
        for iy in range(n):
            for iz in range(n):
                SetTransparency((ix + iy + iz) / ((n - 1) * 3))
                DrawSphere(10)
                DoMove(ix * 30, iy * 30, iz * 30)


def DrawTestMaterial():
    mats = [
        BRASS_MATERIAL,
        BRONZE_MATERIAL,
        COPPER_MATERIAL,
        GOLD_MATERIAL,
        PEWTER_MATERIAL,

        PLASTER_MATERIAL,
        PLASTIC_MATERIAL,
        SILVER_MATERIAL,
        STEEL_MATERIAL,
        STONE_MATERIAL,

        SHINY_PLASTIC_MATERIAL,
        SATIN_MATERIAL,
        METALIZED_MATERIAL,
        NEON_GNC_MATERIAL,
        CHROME_MATERIAL,

        ALUMINIUM_MATERIAL,
        OBSIDIAN_MATERIAL,
        NEON_PHC_MATERIAL,
        JADE_MATERIAL,
        CHARCOAL_MATERIAL,

        WATER_MATERIAL,
        GLASS_MATERIAL,
        PLASTIC_MATERIAL,
        PLASTIC_MATERIAL,
        PLASTIC_MATERIAL,
    ]
    SetColor(NICE_YELLOW_COLOR)
    n = 5
    for ix in range(n):
        for iy in range(n):
            SetMaterial(mats[ix * 5 + iy])
            DrawSphere(10)
            DoMove(ix * 30, iy * 30, 0)


def DrawTestBox():
    x, y, z = 10, 15, 20
    d = 3

    SetMaterial(CHROME_MATERIAL)

    SetColor(NICE_YELLOW_COLOR)
    DrawBox(x, y, z)

    SetColor(NICE_BLUE_COLOR)
    SetTransparency(SEMI_TRANSPARENCY)

    DrawBox(x, y, d)
    DoMove(0, 0, z + d)
    DrawBox(x, y, d)
    DoMove(0, 0, -d - d)

    DrawBox(x, d, z)
    DoMove(0, y + d, 0)
    DrawBox(x, d, z)
    DoMove(0, -d - d, 0)

    DrawBox(d, y, z)
    DoMove(x + d, 0, 0)
    DrawBox(d, y, z)
    DoMove(-d - d, 0, 0)


# DrawTestNull()
# DrawTestSphere()
# DrawTestMove()
# DrawTestColor()
# DrawTestTransparency()
# DrawTestMaterial()
DrawTestBox()
Render()
