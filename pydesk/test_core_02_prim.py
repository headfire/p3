from core_render import ScreenRenderLib
from core_draw import Pnt, LineDraw
from core_position import Translate

screen = ScreenRenderLib()
screen.renderStart()

r = 5
drawList = [
    LineDraw(Pnt(0, 0, 0), Pnt(200, 200, 200)),
]

x = 0
for draw in drawList:
    screen.render(draw, Translate(x, 0, 0))
    x += 12

screen.renderFinish()
