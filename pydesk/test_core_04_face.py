from core_render import *
from core_draw import *


def getFaceDraw():

    pnt000 = Pnt(0, 0, 0)
    pnt010 = Pnt(0, 100, 0)
    pnt111 = Pnt(100, 100, 100)

    dr = Draw()

    dr.addItem(PointDraw(pnt000))
    dr.addItem(PointDraw(pnt010))
    dr.addItem(PointDraw(pnt111))

    dr.addItem(VectorDraw(pnt000, pnt010))
    dr.addItem(VectorDraw(pnt000, pnt111))
    dr.addItem(LineDraw(pnt010, pnt111))

    dr.addItem(FaceDraw([pnt000, pnt010, pnt111]))

    return dr


screen = ScreenRenderLib(1200, 1000)
screen.renderStart()
for i in range(6):
    screen.render(getFaceDraw().doPs(Rotate(Pnt(0, 0, 0), Pnt(0, 0, 1), i * 60)))
screen.renderFinish()
