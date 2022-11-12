from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Vec, gp_Ax1, gp_Trsf


def _d1(f):
    return '%.2f' % f


def _d3(nm, x, y, z):
    return nm + '(' + _d1(x) + ', ' + _d1(y) + ', ' + _d1(z) + ')'


def _dp(nm, pnt):
    return _d3(nm, pnt.X(), pnt.Y(), pnt.Z())


class Position:

    def __init__(self):
        self.trsf = gp_Trsf()
        self.describe = 'Position()'

    def next(self, nextChange):
        self.trsf *= nextChange.trsf
        self.describe += ' -> ' + nextChange.describe
        return self


    def _dump(self):
        for iRow in range(1, 4):
            prn = ''
            for iCol in range(1, 5):
                prn += '  ' + str(self.trsf.Value(iRow, iCol))
            print(prn)


class Translate(Position):

    def __init__(self, dx, dy, dz):
        super().__init__()
        self.trsf.SetTranslation(gp_Vec(dx, dy, dz))
        self.describe = _d3('Translate', dx, dy, dz)


class TranslateToPnt(Translate):

    def __init__(self, pnt):
        super().__init__(pnt.X, pnt.Y, pnt.Z)


class Rotate(Position):

    def __init__(self, pntAxFrom, pntAxTo, angle):
        super().__init__()
        ax1 = gp_Ax1(pntAxFrom, gp_Dir(gp_Vec(pntAxFrom, pntAxTo)))
        self.trsf.SetRotation(ax1, angle)
        self.describe = 'Rotate(' + _dp('axFrom', pntAxFrom) + _dp('axTo', pntAxTo) + _d1(angle) + ')'


class Direct(Position):

    def __init__(self, pntFrom, pntTo):
        super().__init__()

        dirVec = gp_Vec(pntFrom, pntTo)
        targetDir = gp_Dir(dirVec)

        rotateAngle = gp_Dir(0, 0, 1).Angle(targetDir)
        if not gp_Dir(0, 0, 1).IsParallel(targetDir, 0.001):
            rotateDir = gp_Dir(0, 0, 1)
            rotateDir.Cross(targetDir)
        else:
            rotateDir = gp_Dir(0, 1, 0)

        self.trsf.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), rotateDir), rotateAngle)
        self.trsf.SetTranslationPart(gp_Vec(gp_Pnt(0, 0, 0), pntFrom))
        self.debug = 'Direct(' + _dp('axFrom', pntFrom) + _dp('axTo', pntTo) + ')'
