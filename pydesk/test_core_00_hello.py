from core_render import *
from core_draw import *


screen = ScreenRenderLib()
screen.renderStart()

screen.render(SphereDraw(Pnt(0, 0, 0), 100))

screen.renderFinish()
