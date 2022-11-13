from core_render import ScreenRenderLib
from core_draw import Pnt, SphereDraw, BoxDraw, ConeDraw, CylinderDraw, TorusDraw
from core_position import Translate

screen = ScreenRenderLib()
screen.renderStart()

r = 5
drawList = [
    SphereDraw(Pnt(0, 0, 0), r),
    BoxDraw(Pnt(0, 0, 0), r, r, r),
    BoxDraw(Pnt(0, 0, 0), r, r/1.5, r*1.5),
    ConeDraw(r, r/1.5, r*1.5),
    ConeDraw(r, 0, r*2),
    CylinderDraw(r, r * 2),
    TorusDraw(r*0.7, r/3),
]

x = 0
for draw in drawList:
    draw.position = Translate(x, 0, 0)
    screen.render(draw)
    x += 12

screen.renderFinish()
