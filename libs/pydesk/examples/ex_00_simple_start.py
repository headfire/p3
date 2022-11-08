from render import ScreenRenderLib
from draw import SphereDraw

screen = ScreenRenderLib()
screen.renderStart()
screen.render(SphereDraw(100))
screen.renderFinish()
