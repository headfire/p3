from core_render import ScreenRenderLib
from core_draw import SphereDraw
from core_position import Translate
from core_consts import *
from core_styles import Brash

screen = ScreenRenderLib()
screen.renderStart()

# default brash
screen.render(SphereDraw(100))

# no material - gold default
screen.render(SphereDraw(50), Translate(-100,0,0), Brash())
screen.render(SphereDraw(50), Translate(100,0,0), Brash())

# blue plastic sphere on up
screen.render(SphereDraw(50), Translate(0,0,100), Brash(PLASTIC_MATERIAL, NICE_BLUE_COLOR))

# blue plastic transparent sphere on down
screen.render(SphereDraw(50), Translate(0,0,-100), Brash(PLASTIC_MATERIAL, NICE_BLUE_COLOR, 0.7))


screen.renderFinish()
