from core_position import Translate
from core_render import *
from core_draw import *


screen = ScreenRenderLib()
screen.renderStart()

screen.styler.add###Styles([('*:cone', Style(CHROME_MATERIAL))])  # todo

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
    screen.render(draw, Translate(x, 0, 0))
    x += 12

screen.renderFinish()
