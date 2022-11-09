from core_render import ScreenRenderLib
from core_draw import SphereDraw
from core_position import Translate
from core_const import *
from core_styles import Brash

# Первичное тестирование работоспособности библиотеки

# создаем экранное устройство с параметрами по умолчанию
# объект стилей не указан - значит по умолчанию ScreenStyles() - для приятного рисования
# масштаб 1:1, область рисования 400мм
screen = ScreenRenderLib()
screen.renderStart()

# выводим на экран сферу радиусом 100
# position не указывается - значит в начале координат
# brash не указывается - значит по умолчанию (для сферы - SOLID_BRASH_STYLE - Brash(GOLD_MATERIAL))
# должна появится сфера золотого цвета в центре экрана
screen.render(SphereDraw(100))

# тест position, brash, transparent
# вверху должна появится синяя cфера
screen.render(SphereDraw(50), Translate(0,0,100), Brash(PLASTIC_MATERIAL, NICE_BLUE_COLOR))
# внизу должна появится синяя cфера полупрозрачная
screen.render(SphereDraw(50), Translate(0,0,-100), Brash(PLASTIC_MATERIAL, NICE_BLUE_COLOR, 0.7))


screen.renderFinish()
