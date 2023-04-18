from core_desk import *
from OCC.Core.GC import GC_MakeArcOfCircle
from math import pi, sqrt


def TestRender():
    pass


def TestSimpleRender():
    DrawSphere(15)


def TestMove():
    for ix in [-1, 1]:
        for iy in [-1, 1]:
            for iz in [-1, 1]:
                DrawSphere(10)
                DoMove(Decart(ix * 20, iy * 20, iz * 20))


def TestColor():
    n = 5
    for ix in range(n):
        for iy in range(n):
            for iz in range(n):
                SetSolidBrash(ChromeBrash(([ix / (n - 1), iy / (n - 1), iz / (n - 1)])))
                DrawSphere(10)
                DoMove(Decart(ix * 30, iy * 30, iz * 30))


def TestTransparency():
    n = 5
    for ix in range(n):
        for iy in range(n):
            for iz in range(n):
                SetSolidBrash(PlasticBrash(BLUE_COLOR, (ix + iy + iz) / ((n - 1) * 3)))
                DrawSphere(10)
                DoMove(Decart(ix * 30, iy * 30, iz * 30))


def TestStandardBrash():

    colors = [
        WHITE_COLOR,
        GRAY_COLOR,
        DARK_GRAY_COLOR,

        RED_COLOR,
        GREEN_COLOR,
        BLUE_COLOR,

        YELLOW_COLOR,
        CYAN_COLOR,
        MAGENTA_COLOR,

        DARK_RED_COLOR,
        DARK_GREEN_COLOR,
        DARK_BLUE_COLOR,

        DARK_YELLOW_COLOR,
        DARK_CYAN_COLOR,
        DARK_MAGENTA_COLOR,

        WOOD_COLOR,
        PAPER_COLOR,
        STEEL_COLOR,
        GOLD_COLOR,
    ]

    i = 0
    for color in colors:
        i = i + 1
        for tr in range(5):
            SetSolidBrash(PlasticBrash(color, tr/4))
            DrawSphere(10)
            DoMove(Decart(i * 30, tr * 30, 0))
            SetSolidBrash(ChromeBrash(color, tr/4))
            DrawSphere(10)
            DoMove(Decart(i * 30, tr * 30, 100))


def TestRotate():
    SetSolidBrash(ChromeBrash(BLUE_COLOR))
    n = 24
    for i in range(n):
        DrawSphere(10)
        DoMove(Decart(100, 0, 0))
        DoRotateZ(i * 360 / n)

    SetSolidBrash(ChromeBrash(YELLOW_COLOR))
    for i in range(n):
        DrawSphere(10)
        DoMove(Decart(100, 0, 0))
        DoRotateY(i * 360 / n)

    SetSolidBrash(ChromeBrash(RED_COLOR))
    for i in range(n):
        DrawSphere(10)
        DoMove(Decart(0, 100, 0))
        DoRotateX(i * 360 / n)

    SetSolidBrash(ChromeBrash(WHITE_COLOR))
    for i in range(n):
        DrawSphere(10)
        DoRotate(Decart(0, 0, 50), Decart(0, 100, 100), i * 360 / n)


def TestDirect():
    DrawSphere(10)

    DrawSphere(10)
    DoMove(Decart(100, 100, 500))
    DrawSphere(10)
    DoMove(Decart(-100, 100, 500))
    DrawSphere(10)
    DoMove(Decart(-100, -100, 500))
    DrawSphere(10)
    DoMove(Decart(100, -100, 500))

    DrawCone(50, 0, 200)
    DoMove(Decart(0, 0, 200))
    DoDirect(Decart(0, 0, 0), Decart(100, 100, 500))

    DrawCone(50, 0, 200)
    DoMove(Decart(0, 0, 200))
    DoDirect(Decart(0, 0, 0), Decart(-100, 100, 500))

    DrawCone(50, 0, 200)
    DoMove(Decart(0, 0, 200))
    DoDirect(Decart(0, 0, 0), Decart(-100, -100, 500))

    DrawCone(50, 0, 200)
    DoMove(Decart(0, 0, 200))
    DoDirect(Decart(0, 0, 0), Decart(100, -100, 500))


def TestBox():
    x, y, z = 10, 15, 20
    d = 3

    SetSolidBrash(ChromeBrash(YELLOW_COLOR))
    DrawBox(x, y, z)

    SetSolidBrash(ChromeBrash(BLUE_COLOR, 0.5))

    DrawBox(x, y, d)
    DoMove(Decart(0, 0, z + d))
    DrawBox(x, y, d)
    DoMove(Decart(0, 0, -d - d))

    DrawBox(x, d, z)
    DoMove(Decart(0, y + d, 0))
    DrawBox(x, d, z)
    DoMove(Decart(0, -d - d, 0))

    DrawBox(d, y, z)
    DoMove(Decart(x + d, 0, 0))
    DrawBox(d, y, z)
    DoMove(Decart(-d - d, 0, 0))


def TestSphere():
    DrawSphere(15)


def TestCone():
    for i in range(6):
        DrawCone(5 + i * 10, i * 10, 10)
        DoMove(Decart(0, 0, -i * 10))


def TestCylinder():
    for i in range(6):
        DrawCylinder(5 + i * 10, i + 2 + 5)
        DoMove(Decart(0, 0, -i * 10))


def TestTorus():
    DrawTorus(100, 20)
    DrawTorus(100, 20)
    DoRotateX(90)
    DoMove(Decart(100, 0, 0))


def TestLabel():
    SetSolidBrash(ChromeBrash(BLUE_COLOR, 0.5))
    SetLabelBrash(LabelBrash(YELLOW_COLOR))
    for ix in [-1, 1]:
        for iy in [-1, 1]:
            for iz in [-1, 1]:
                DrawSphere(2)
                DoMove(Decart(ix * 20, iy * 20, iz * 20))
                DrawLabel(Decart(ix * 20, iy * 20, iz * 20), 'P(' + str(ix) + ',' + str(iy) + ',' + str(iz) + ')')


def TestPoint():
    for ix in [-1, 1]:
        for iy in [-1, 1]:
            for iz in [-1, 1]:
                DrawPoint(Decart(ix * 20, iy * 20, iz * 20))
                DrawLabel(Decart(ix * 20, iy * 20, iz * 20), 'P(' + str(ix) + ',' + str(iy) + ',' + str(iz) + ')')


def TestLine():
    pnt000 = Decart(0, 0, 0)
    pnt001 = Decart(0, 0, 100)
    pnt010 = Decart(0, 100, 0)
    pnt011 = Decart(0, 100, 100)
    pnt100 = Decart(100, 0, 0)
    pnt101 = Decart(100, 0, 100)
    pnt110 = Decart(100, 100, 0)
    pnt111 = Decart(100, 100, 100)

    DrawPoint(pnt000)
    DrawPoint(pnt001)
    DrawPoint(pnt010)
    DrawPoint(pnt011)
    DrawPoint(pnt100)
    DrawPoint(pnt101)
    DrawPoint(pnt110)
    DrawPoint(pnt111)

    SetLineBrash(ChromeBrash(BLUE_COLOR))
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


def TestArrow():
    pntC = Decart(50, 50, 50)

    pnt000 = Decart(0, 0, 0)
    pnt001 = Decart(0, 0, 100)
    pnt010 = Decart(0, 100, 0)
    pnt011 = Decart(0, 100, 100)
    pnt100 = Decart(100, 0, 0)
    pnt101 = Decart(100, 0, 100)
    pnt110 = Decart(100, 100, 0)
    pnt111 = Decart(100, 100, 100)

    DrawPoint(pnt000)
    DrawPoint(pnt001)
    DrawPoint(pnt010)
    DrawPoint(pnt011)

    SetLineBrash(ChromeBrash(BLUE_COLOR))
    DrawArrow(pntC, pnt000)
    DrawArrow(pntC, pnt001)
    DrawArrow(pntC, pnt010)
    DrawArrow(pntC, pnt011)

    DrawArrow(pntC, pnt100)
    DrawArrow(pntC, pnt101)
    DrawArrow(pntC, pnt110)
    DrawArrow(pntC, pnt111)


def TestArrow2():
    pntC = Decart(50, 50, 50)

    pnt000 = Decart(0, 0, 0)
    pnt001 = Decart(0, 0, 100)
    pnt010 = Decart(0, 100, 0)
    pnt011 = Decart(0, 100, 100)
    pnt100 = Decart(100, 0, 0)
    pnt101 = Decart(100, 0, 100)
    pnt110 = Decart(100, 100, 0)
    pnt111 = Decart(100, 100, 100)

    DrawPoint(pnt000)
    DrawPoint(pnt001)
    DrawPoint(pnt010)
    DrawPoint(pnt011)

    SetLineBrash(ChromeBrash(BLUE_COLOR))
    DrawArrow2(pntC, pnt000)
    DrawArrow2(pntC, pnt001)
    DrawArrow2(pntC, pnt010)
    DrawArrow2(pntC, pnt011)

    DrawArrow2(pntC, pnt100)
    DrawArrow2(pntC, pnt101)
    DrawArrow2(pntC, pnt110)
    DrawArrow2(pntC, pnt111)


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
    pnt1 = Decart(0, 0, 0)
    pnt2 = Decart(100, 0, 0)
    pnt3 = Decart(50, 70, 0)
    pnt4 = Decart(50, 50, 70)

    DrawPoint(pnt1)
    DrawPoint(pnt2)
    DrawPoint(pnt3)
    DrawPoint(pnt4)

    DrawCircle(pnt1, pnt2, pnt3)
    DrawCircle(pnt1, pnt2, pnt4)
    DrawCircle(pnt1, pnt3, pnt4)
    DrawCircle(pnt2, pnt3, pnt4)


def TestBoard():
    DrawBoard()


def TestAxis():

    SetLineBrash(ChromeBrash(RED_COLOR))
    DrawAxis(Decart(0, 0, 0), Decart(200, 0, 0), 50)

    SetLineBrash(ChromeBrash(GREEN_COLOR))
    DrawAxis(Decart(0, 0, 0), Decart(0, 200, 0), 50)

    SetLineBrash(ChromeBrash(BLUE_COLOR))
    DrawAxis(Decart(0, 0, 0), Decart(0, 0, 200), 50)

    SetLineBrash(ChromeBrash(WHITE_COLOR))
    DrawPoint(Decart(0, 0, 0))
    dlen = 200/sqrt(3)
    DrawAxis(Decart(0, 0, 0), Decart(dlen, dlen, dlen), 50)

    SetLabelBrash(ChromeBrash(YELLOW_COLOR))
    DrawLabel(Decart(200, 0, 0), 'X')
    DrawLabel(Decart(0, 200, 0), 'Y')
    DrawLabel(Decart(0, 0, 200), 'Z')


def TestAxisSystem():
    # DrawDesk()
    DrawAxisSystem(Decart(0, 0, 100), Decart(300, 300, 400), 50)
    # DrawLimits()


def TestBoxFrame():
    DrawBoxFrame(Decart(0, 0, 100), Decart(300, 300, 400), True)


def TestLimits():
    DrawLimits(Decart(-300, -300, 100), Decart(300, 300, 400))
# DrawLimits(Decart(0, 0, 0), Decart(200, 200, 100))


def TestDesk():
    DrawDesk(True, True, True)
# DrawDecor()


'''
def TestLimits():
    DrawCoord(Decart(0, 0, 100), Decart(300, 300, 400))
'''

tests = [
    TestRender,
    TestSimpleRender,

    TestColor,
    TestTransparency,
    TestStandardBrash,

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
    TestArrow,
    TestArrow2,
    TestWire,
    TestCircle,
    TestBoard,
    TestAxis,
    TestAxisSystem,
    TestBoxFrame,
    TestLimits,
    TestDesk,
]

# TestLabel()
# Render()
# exit()

tests.pop()()
Show()

'''
for test in tests:
    Clear()
    test()
    Render()
'''
