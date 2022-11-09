from core_render import ScreenRenderLib
from core_draw import SphereDraw

screen = ScreenRenderLib()
screen.renderStart()
screen.render(SphereDraw(100))
screen.renderFinish()
