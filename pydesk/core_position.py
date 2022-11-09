from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Vec, gp_Ax1, gp_Trsf


class Position:

    def __init__(self):
        self.trsf = gp_Trsf()

    def next(self, nextChange):
        self.trsf *= nextChange.trsf
        return self

    def _dump(self):
        for iRow in range(1, 4):
            prn = ''
            for iCol in range(1, 5):
                prn += '  ' + str(self.trsf.Value(iRow, iCol))
            print(prn)

    def getTrsf(self):
        return self.trsf


class Translate(Position):

    def __init__(self, dx, dy, dz):
        super().__init__()
        self.trsf.SetTranslation(gp_Vec(dx, dy, dz))


class TranslateToPnt(Translate):

    def __init__(self, pnt):
        super().__init__(pnt.X, pnt.Y, pnt.Z)


class Rotate(Position):

    def __init__(self, pntAxFrom, pntAxTo, angle):
        super().__init__()
        ax1 = gp_Ax1(pntAxFrom, gp_Dir(gp_Vec(pntAxFrom, pntAxTo)))
        self.trsf.SetRotation(ax1, angle)


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
