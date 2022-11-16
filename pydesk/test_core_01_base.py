from core_render import *
from core_draw import *

screen = ScreenRenderLib()
screen.renderStart()

for x in range(0, 250, 50):
    for y in range(0, 250, 50):
        for z in range(0, 250, 50):
            draw = SphereDraw(Pnt(x, y, z), 15)\
                .doSt(COLOR, (abs(x)/200, abs(y)/200, abs(z)/200))\
                .doSt(TRANSPARENCY, (x+y+z)/600)
            screen.render(draw)

screen.renderFinish()
