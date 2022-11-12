from core_render import ScreenRenderLib
from core_draw import SphereDraw
from core_position import Translate
from core_consts import *
from core_style import Style

screen = ScreenRenderLib()
screen.renderStart()

screen.render(SphereDraw(100))
screen.render(SphereDraw(50), Translate(0, 0, 100),
              Style(PLASTIC_MATERIAL, NICE_BLUE_COLOR)
              )
screen.render(SphereDraw(50), Translate(0, 0, -100),
              Style(PLASTIC_MATERIAL, NICE_BLUE_COLOR, 0.7)
              )


screen.renderFinish()
