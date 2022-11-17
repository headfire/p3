from core_render import *
from core_draw import *

screen = ScreenRenderLib()
screen.renderStart()

pntC = Pnt(50, 50, 50)

pnt000 = Pnt(0, 0, 0)
pnt001 = Pnt(0, 0, 100)
pnt010 = Pnt(0, 100, 0)
pnt011 = Pnt(0, 100, 100)
pnt100 = Pnt(100, 0, 0)
pnt101 = Pnt(100, 0, 100)
pnt110 = Pnt(100, 100, 0)
pnt111 = Pnt(100, 100, 100)

screen.render(PointDraw(pnt000))
screen.render(PointDraw(pnt010))
screen.render(PointDraw(pnt111))

screen.render(VectorDraw(pnt000, pnt010))
screen.render(VectorDraw(pnt000, pnt111))
screen.render(LineDraw(pnt010, pnt111))

screen.render(FaceDraw([pnt000, pnt010, pnt111]))

screen.renderFinish()
