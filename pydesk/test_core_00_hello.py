from core_render import ScreenRenderLib
from core_draw import Pnt, SphereDraw
from core_position import Translate
from core_consts import *
from core_style import Style

screen = ScreenRenderLib()
screen.renderStart()

screen.render(SphereDraw(Pnt(0, 0, 0), 100))

screen.renderFinish()
