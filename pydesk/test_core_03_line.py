from core_render import ScreenRenderLib
from core_draw import Pnt, PointDraw, LineDraw, VectorDraw, Circle3Draw
# from core_position import Translate

from core_brash import Brash
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
screen.render(PointDraw(pnt001))
screen.render(PointDraw(pnt010))
screen.render(PointDraw(pnt011))
screen.render(PointDraw(pnt100))
screen.render(PointDraw(pnt101))
screen.render(PointDraw(pnt110))
screen.render(PointDraw(pnt111))

screen.render(LineDraw(pnt000, pnt001))
screen.render(LineDraw(pnt001, pnt011))
screen.render(LineDraw(pnt011, pnt010))
screen.render(LineDraw(pnt010, pnt000))

screen.render(LineDraw(pnt100, pnt101))
screen.render(LineDraw(pnt101, pnt111))
screen.render(LineDraw(pnt111, pnt110))
screen.render(LineDraw(pnt110, pnt100))

screen.render(LineDraw(pnt000, pnt100))
screen.render(LineDraw(pnt001, pnt101))
screen.render(LineDraw(pnt010, pnt110))
screen.render(LineDraw(pnt011, pnt111))

brash = Brash(color=(0.1, 0.7, 0.1))
screen.render(VectorDraw(pnt000, pntC), brash=brash)
screen.render(VectorDraw(pnt111, pntC), brash=brash)

brash = Brash(color=(0.1, 0.7, 0.7))
screen.render(Circle3Draw(pnt000, pnt111, pnt100), brash=brash)



screen.renderFinish()
