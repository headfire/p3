from core_render import ScreenRenderLib
from core_draw import SphereDraw, BoxDraw, ConeDraw, CylinderDraw
from core_position import Translate

screen = ScreenRenderLib()
screen.renderStart()

r = 5
drawList = [
    SphereDraw(r),
    BoxDraw(r, r, r),
    BoxDraw(r, r/1.5, r*1.5),
    ConeDraw(r, r/1.5, r*1.5),
    ConeDraw(r, 0, r*2),
    CylinderDraw(r, r * 2),
]

x = 0
for draw in drawList:
    screen.render(draw, Translate(x, 0, 0))
    x += 12

screen.renderFinish()
