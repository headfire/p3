from core_desk import *


def TestRender():
    pass


def TestSimpleRender():
    DrawSphere(15)


def TestMove():
    for ix in [-1, 1]:
        for iy in [-1, 1]:
            for iz in [-1, 1]:
                DrawSphere(10)
                DoMove(ix * 20, iy * 20, iz * 20)


def TestColor():
    n = 5
    for ix in range(n):
        for iy in range(n):
            for iz in range(n):
                SetColor([ix / (n - 1), iy / (n - 1), iz / (n - 1)])
                DrawSphere(10)
                DoMove(ix * 30, iy * 30, iz * 30)


def TestTransparency():
    SetColor(NICE_BLUE_COLOR)
    n = 5
    for ix in range(n):
        for iy in range(n):
            for iz in range(n):
                SetTransparency((ix + iy + iz) / ((n - 1) * 3))
                DrawSphere(10)
                DoMove(ix * 30, iy * 30, iz * 30)


def TestMaterial():
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


def TestRotate():
    SetMaterial(CHROME_MATERIAL)
    SetColor(NICE_BLUE_COLOR)
    for i in range(10):
        DrawSphere(10)
        DoMove(40, 0, 0)
        DoRotateZ(i * 360 / 10)

    SetMaterial(CHROME_MATERIAL)
    SetColor(NICE_YELLOW_COLOR)
    for i in range(10):
        DrawSphere(10)
        DoMove(80, 0, 0)
        DoRotateY(i * 360 / 10)

    SetMaterial(CHROME_MATERIAL)
    SetColor(NICE_RED_COLOR)
    for i in range(10):
        DrawSphere(10)
        DoMove(0, 120, 0)
        DoRotateX(i * 360 / 10)

    SetMaterial(CHROME_MATERIAL)
    SetColor(NICE_WHITE_COLOR)
    for i in range(10):
        DrawSphere(10)
        DoMove(0, 0, 0)
        DoRotate(Pnt(0, 0, 50), Pnt(0, 100, 100), i * 360 / 20)


def TestDirect():
    DrawSphere(10)

    DrawSphere(10)
    DoMove(100, 100, 500)
    DrawSphere(10)
    DoMove(-100, 100, 500)
    DrawSphere(10)
    DoMove(-100, -100, 500)
    DrawSphere(10)
    DoMove(100, -100, 500)

    DrawCone(50, 0, 200)
    DoMove(0, 0, 200)
    DoDirect(Pnt(0, 0, 0), Pnt(100, 100, 500))

    DrawCone(50, 0, 200)
    DoMove(0, 0, 200)
    DoDirect(Pnt(0, 0, 0), Pnt(-100, 100, 500))

    DrawCone(50, 0, 200)
    DoMove(0, 0, 200)
    DoDirect(Pnt(0, 0, 0), Pnt(-100, -100, 500))

    DrawCone(50, 0, 200)
    DoMove(0, 0, 200)
    DoDirect(Pnt(0, 0, 0), Pnt(100, -100, 500))


def TestBox():
    x, y, z = 10, 15, 20
    d = 3

    SetMaterial(CHROME_MATERIAL)

    SetColor(NICE_YELLOW_COLOR)
    DrawBox(x, y, z)

    SetColor(NICE_BLUE_COLOR)
    SetTransparency(SEMI_VISIBLE_TRANSPARENCY)

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


def TestSphere():
    DrawSphere(15)


def TestCone():
    for i in range(6):
        DrawCone(5 + i * 10, i * 10, 10)
        DoMove(0, 0, -i * 10)


def TestCylinder():
    for i in range(6):
        DrawCylinder(5 + i * 10, i + 2 + 5)
        DoMove(0, 0, -i * 10)


def TestTorus():
    DrawTorus(100, 20)
    DrawTorus(100, 20)
    DoRotateX(90)
    DoMove(100, 0, 0)


def TestLabel():
    for ix in [-1, 1]:
        for iy in [-1, 1]:
            for iz in [-1, 1]:

                SetColor(None)
                SetTransparency(0)
                DrawSphere(5)
                DoMove(ix * 20, iy * 20, iz * 20)

                SetColor([0, 0, 0.5])
                SetTransparency(0.5)
                DrawLabel(Pnt(ix * 20, iy * 20, iz * 20), 'P(' + str(ix) + ',' + str(iy) + ',' + str(iz) + ')')


tests = [
    TestRender,
    TestSimpleRender,

    TestColor,
    TestTransparency,
    TestMaterial,

    TestMove,
    TestRotate,
    TestDirect,

    TestSphere,
    TestBox,
    TestCone,
    TestCylinder,
    TestTorus,
    TestLabel,
]

tests.pop()()
Render()

'''
for test in tests:
    Clear()
    test()
    Render()
'''
