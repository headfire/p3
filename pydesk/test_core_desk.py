from core_desk import *
from OCC.Core.GC import GC_MakeArcOfCircle
from math import pi


def TestRender():
    pass


def TestSimpleRender():
    DrawSphere(15)


def TestMove():
    for ix in [-1, 1]:
        for iy in [-1, 1]:
            for iz in [-1, 1]:
                DrawSphere(10)
                DoMove(Pnt(ix * 20, iy * 20, iz * 20))


def TestColor():
    n = 5
    for ix in range(n):
        for iy in range(n):
            for iz in range(n):
                SetColor([ix / (n - 1), iy / (n - 1), iz / (n - 1)])
                DrawSphere(10)
                DoMove(Pnt(ix * 30, iy * 30, iz * 30))


def TestTransparency():
    SetColor(NICE_BLUE_COLOR)
    n = 5
    for ix in range(n):
        for iy in range(n):
            for iz in range(n):
                SetTransparency((ix + iy + iz) / ((n - 1) * 3))
                DrawSphere(10)
                DoMove(Pnt(ix * 30, iy * 30, iz * 30))


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
            DoMove(Pnt(ix * 30, iy * 30, 0))


def TestRotate():
    SetMaterial(CHROME_MATERIAL)
    SetColor(NICE_BLUE_COLOR)
    n = 24
    for i in range(n):
        DrawSphere(10)
        DoMove(Pnt(100, 0, 0))
        DoRotateZ(i * 360 / n)

    SetMaterial(CHROME_MATERIAL)
    SetColor(NICE_YELLOW_COLOR)
    for i in range(n):
        DrawSphere(10)
        DoMove(Pnt(100, 0, 0))
        DoRotateY(i * 360 / n)

    SetMaterial(CHROME_MATERIAL)
    SetColor(NICE_RED_COLOR)
    for i in range(n):
        DrawSphere(10)
        DoMove(Pnt(0, 100, 0))
        DoRotateX(i * 360 / n)

    SetMaterial(CHROME_MATERIAL)
    SetColor(NICE_WHITE_COLOR)
    for i in range(n):
        DrawSphere(10)
        DoRotate(Pnt(0, 0, 50), Pnt(0, 100, 100), i * 360 / n)


def TestDirect():
    DrawSphere(10)

    DrawSphere(10)
    DoMove(Pnt(100, 100, 500))
    DrawSphere(10)
    DoMove(Pnt(-100, 100, 500))
    DrawSphere(10)
    DoMove(Pnt(-100, -100, 500))
    DrawSphere(10)
    DoMove(Pnt(100, -100, 500))

    DrawCone(50, 0, 200)
    DoMove(Pnt(0, 0, 200))
    DoDirect(Pnt(0, 0, 0), Pnt(100, 100, 500))

    DrawCone(50, 0, 200)
    DoMove(Pnt(0, 0, 200))
    DoDirect(Pnt(0, 0, 0), Pnt(-100, 100, 500))

    DrawCone(50, 0, 200)
    DoMove(Pnt(0, 0, 200))
    DoDirect(Pnt(0, 0, 0), Pnt(-100, -100, 500))

    DrawCone(50, 0, 200)
    DoMove(Pnt(0, 0, 200))
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
    DoMove(Pnt(0, 0, z + d))
    DrawBox(x, y, d)
    DoMove(Pnt(0, 0, -d - d))

    DrawBox(x, d, z)
    DoMove(Pnt(0, y + d, 0))
    DrawBox(x, d, z)
    DoMove(Pnt(0, -d - d, 0))

    DrawBox(d, y, z)
    DoMove(Pnt(x + d, 0, 0))
    DrawBox(d, y, z)
    DoMove(Pnt(-d - d, 0, 0))


def TestSphere():
    DrawSphere(15)


def TestCone():
    for i in range(6):
        DrawCone(5 + i * 10, i * 10, 10)
        DoMove(Pnt(0, 0, -i * 10))


def TestCylinder():
    for i in range(6):
        DrawCylinder(5 + i * 10, i + 2 + 5)
        DoMove(Pnt(0, 0, -i * 10))


def TestTorus():
    DrawTorus(100, 20)
    DrawTorus(100, 20)
    DoRotateX(90)
    DoMove(Pnt(100, 0, 0))


def TestLabel():
    for ix in [-1, 1]:
        for iy in [-1, 1]:
            for iz in [-1, 1]:
                SetColor(None)
                SetTransparency(0)
                DrawSphere(5)
                DoMove(Pnt(ix * 20, iy * 20, iz * 20))

                SetColor(Rgb(0, 0, 0.5))
                SetTransparency(0.5)
                DrawLabel(Pnt(ix * 20, iy * 20, iz * 20), 'P(' + str(ix) + ',' + str(iy) + ',' + str(iz) + ')')


def TestPoint():
    SetMaterial(CHROME_MATERIAL)
    SetColor(NICE_BLUE_COLOR)
    for ix in [-1, 1]:
        for iy in [-1, 1]:
            for iz in [-1, 1]:
                DrawPoint(Pnt(ix * 20, iy * 20, iz * 20))
                DrawLabel(Pnt(ix * 20, iy * 20, iz * 20), 'P(' + str(ix) + ',' + str(iy) + ',' + str(iz) + ')')


def TestLine():
    pnt000 = Pnt(0, 0, 0)
    pnt001 = Pnt(0, 0, 100)
    pnt010 = Pnt(0, 100, 0)
    pnt011 = Pnt(0, 100, 100)
    pnt100 = Pnt(100, 0, 0)
    pnt101 = Pnt(100, 0, 100)
    pnt110 = Pnt(100, 100, 0)
    pnt111 = Pnt(100, 100, 100)

    DrawPoint(pnt000)
    DrawPoint(pnt001)
    DrawPoint(pnt010)
    DrawPoint(pnt011)
    DrawPoint(pnt100)
    DrawPoint(pnt101)
    DrawPoint(pnt110)
    DrawPoint(pnt111)

    SetColor(NICE_BLUE_COLOR)
    DrawLine(pnt000, pnt001)
    DrawLine(pnt001, pnt011)
    DrawLine(pnt011, pnt010)
    DrawLine(pnt010, pnt000)

    DrawLine(pnt100, pnt101)
    DrawLine(pnt101, pnt111)
    DrawLine(pnt111, pnt110)
    DrawLine(pnt110, pnt100)

    DrawLine(pnt000, pnt100)
    DrawLine(pnt001, pnt101)
    DrawLine(pnt010, pnt110)
    DrawLine(pnt011, pnt111)


def TestVector():
    pntC = Pnt(50, 50, 50)

    pnt000 = Pnt(0, 0, 0)
    pnt001 = Pnt(0, 0, 100)
    pnt010 = Pnt(0, 100, 0)
    pnt011 = Pnt(0, 100, 100)
    pnt100 = Pnt(100, 0, 0)
    pnt101 = Pnt(100, 0, 100)
    pnt110 = Pnt(100, 100, 0)
    pnt111 = Pnt(100, 100, 100)

    DrawPoint(pnt000)
    DrawPoint(pnt001)
    DrawPoint(pnt010)
    DrawPoint(pnt011)

    SetColor(NICE_BLUE_COLOR)
    DrawVector(pntC, pnt000)
    DrawVector(pntC, pnt001)
    DrawVector(pntC, pnt010)
    DrawVector(pntC, pnt011)

    DrawVector(pntC, pnt100)
    DrawVector(pntC, pnt101)
    DrawVector(pntC, pnt110)
    DrawVector(pntC, pnt111)


def TestArrow():
    pntC = Pnt(50, 50, 50)

    pnt000 = Pnt(0, 0, 0)
    pnt001 = Pnt(0, 0, 100)
    pnt010 = Pnt(0, 100, 0)
    pnt011 = Pnt(0, 100, 100)
    pnt100 = Pnt(100, 0, 0)
    pnt101 = Pnt(100, 0, 100)
    pnt110 = Pnt(100, 100, 0)
    pnt111 = Pnt(100, 100, 100)

    DrawPoint(pnt000)
    DrawPoint(pnt001)
    DrawPoint(pnt010)
    DrawPoint(pnt011)

    SetColor(NICE_BLUE_COLOR)
    DrawArrow(pntC, pnt000)
    DrawArrow(pntC, pnt001)
    DrawArrow(pntC, pnt010)
    DrawArrow(pntC, pnt011)

    DrawArrow(pntC, pnt100)
    DrawArrow(pntC, pnt101)
    DrawArrow(pntC, pnt110)
    DrawArrow(pntC, pnt111)


def getPntRotate(pCenter, p, angle):
    ax = gp_Ax1(pCenter, gp_Dir(0, 0, 1))
    pnt = gp_Pnt(p.XYZ())
    pnt.Rotate(ax, angle)
    return pnt


def TestWire():
    r = 50

    r2 = r / 2

    gpPntMinC = gp_Pnt(0, r2, 0)

    origin = gp_Pnt(0, 0, 0)

    p = {
        0: origin,
        1: getPntRotate(gpPntMinC, origin, -pi / 4),
        2: gp_Pnt(-r2, r2, 0),
        3: getPntRotate(gpPntMinC, origin, -pi / 4 * 3),
        4: gp_Pnt(0, r, 0),
        5: gp_Pnt(r, 0, 0),
        6: gp_Pnt(0, -r, 0),
        7: gp_Pnt(r2, -r2, 0)
    }

    arc0 = GC_MakeArcOfCircle(p[0], p[1], p[2]).Value()
    arc1 = GC_MakeArcOfCircle(p[2], p[3], p[4]).Value()
    arc2 = GC_MakeArcOfCircle(p[4], p[5], p[6]).Value()
    arc3 = GC_MakeArcOfCircle(p[6], p[7], p[0]).Value()

    edge0 = BRepBuilderAPI_MakeEdge(arc0).Edge()
    edge1 = BRepBuilderAPI_MakeEdge(arc1).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(arc2).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(arc3).Edge()

    wire = BRepBuilderAPI_MakeWire(edge0, edge1, edge2, edge3).Wire()
    DrawWire(wire)


def TestCircle():
    pnt1 = Pnt(0, 0, 0)
    pnt2 = Pnt(100, 0, 0)
    pnt3 = Pnt(50, 70, 0)
    pnt4 = Pnt(50, 50, 70)

    DrawPoint(pnt1)
    DrawPoint(pnt2)
    DrawPoint(pnt3)
    DrawPoint(pnt4)

    DrawCircle(pnt1, pnt2, pnt3)
    DrawCircle(pnt1, pnt2, pnt4)
    DrawCircle(pnt1, pnt3, pnt4)
    DrawCircle(pnt2, pnt3, pnt4)


def TestDesk():
    DrawDesk()


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

    TestPoint,
    TestLine,
    TestVector,
    TestArrow,
    TestWire,
    TestCircle,
    TestDesk,
]

# TestLabel()
# Render()
# exit()

tests.pop()()
Render()

'''
for test in tests:
    Clear()
    test()
    Render()
'''
