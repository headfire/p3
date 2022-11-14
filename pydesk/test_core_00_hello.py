from core_render import ScreenRenderLib
from core_draw import Pnt, SphereDraw


screen = ScreenRenderLib()
screen.renderStart()

screen.render(SphereDraw(Pnt(0, 0, 0), 100))

screen.renderFinish()
