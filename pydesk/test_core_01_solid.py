from core_render import ScreenRenderLib
from core_draw import SphereDraw, BoxDraw
from core_position import Translate

screen = ScreenRenderLib()
screen.renderStart()

size = 10
drawList = [
    SphereDraw(size/2),
    BoxDraw(size, size, size),
    BoxDraw(size, size/1.5, size*1.5)
]

x = 0
for draw in drawList:
    screen.render(draw, Translate(x, 0, 0))
    x += 15

screen.renderFinish()
