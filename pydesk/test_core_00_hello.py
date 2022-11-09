from core_render import ScreenRenderLib
from core_draw import SphereDraw

# Первичное тестирование работоспособности библиотеки

# создаем экранное устройство с параметрами по умолчанию
# объект стилей не указан - значит по умолчанию ScreenStyles() - для приятного рисования
# масштаб 1:1, область рисования 400мм
#
screen = ScreenRenderLib()
screen.renderStart()

# выводим на экран сферу радиусом 100
# position не указывается - значит в начале координат
# brash не указывается - значит по умолчанию (для сферы - SOLID_BRASH_STYLE - Brash(GOLD_MATERIAL))
screen.render(SphereDraw(100))

screen.renderFinish()
