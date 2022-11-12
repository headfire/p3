from core_render import ScreenRenderLib
from core_draw import Pnt, SphereDraw, LabelDraw
# from core_position import Translate
from core_consts import *
from core_style import Style

screen = ScreenRenderLib()
screen.renderStart()

for x in range(0, 250, 50):
    for y in range(0, 250, 50):
        for z in range(0, 250, 50):
            draw = SphereDraw(Pnt(x, y, z), 10)
            draw.style = Style(GOLD_MATERIAL, (abs(x)/200, abs(y)/200, abs(z)/200), (x+y+z)/600)
            screen.render(draw)
            if (x == 200 or x == 0) and (y == 200 or y == 0) and (z == 200 or z == 0):
                screen.render(LabelDraw(Pnt(x, y, z), str(x)+'-'+str(y)+'-'+str(z)))

screen.renderFinish()
