from core_render import ScreenRenderLib
from core_draw import Pnt, LineDraw #, VectorDraw
# from core_position import Translate

screen = ScreenRenderLib()
screen.renderStart()

screen.render(LineDraw(Pnt(0, 0, 0), Pnt(200, 200, 200)))
# screen.render(VectorDraw(Pnt(0, 0, 0), Pnt(200, 0, 0)))

screen.renderFinish()
