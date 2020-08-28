# Объект Scene - система команд

PythonOCC - это не просто порт библиотеки. В нем присутствует много кода на Python облегчающего работу. И это довольно удобно. Но чтобы еще более упростить создание и демонстрацию сцен в данных примерах создан объект Scene.

Объект Scene предназначен для быстрого вывода объектов на экран и управление их внешним видом. Объекты загружаются в сцену, при этом им присваивается имя, которое позволяет в дальнейшем контролировать его отображение. Возможны групповые операции, манипулирующие сразу с несколькими объектами, выбираемыми по маске. Также реализована возможность несложной анимации и управление параметрическими объектами. Еще объект сцена имеет методы для управления стереоскопическими режимами и методы экспорта сцены в последовательность PNG-файлов, последовательность OBJ-файлов, экспорт сцены в браузерный просмотрщик, основанный на технологии  Three.js.

Ниже набор команд объекта Scene.



addAxis(name)

addBoard(name)



addObject(obj, name) - добавляет объект в сцену ( добавляться могут любые объекты, но отображаются только объекты потомки AIS_InteractiveObject), также в качестве объекта может быть передана функция, возвращающая объект AIS_InteractiveObject (см ниже параметрические объекты)

addObjects(dict, mask, postfix='') - добавляет объекты из именованного списка, фильтруя их по mask и добавляя в конце postfix (для избежания пересечения имен)



setInfoStyle(mask, startFrame = None, finishFrame=None)

setMainStyle(mask, startFrame = None, finishFrame=None)

setLabel(mask, isOn=True, startFrame = None, finishFrame=None)

setComment(comment, startFrame = None, finishFrame = None)

setVisible(mask, isOn=True, startFrame = None, finishFrame=None)



setPointColor(mask, startR, startG, startB, startT, startFrame = None, finishR = None, finishB = None, finishT = None, finishFrame= None)

setLineColor(mask, startR, startG, startB, startT, startFrame = None, finishR = None, finishB = None, finishT = None, finishFrame= None)

setSurfaceColor(mask, startR, startG, startB, startT, startFrame = None, finishR = None, finishB = None, finishT = None, finishFrame= None)

setPointSize(mask, startSize,  startFrame = None, finishSize = None, finishFrame= None)

setLineSize(mask, startSize,  startFrame = None, finishSize = None, finishFrame= None)



setParameter(mask, paramName, startValue,  startFrame = None, finishValue = None, finishFrame= None)



setTranslation(mask, startVector, startFrame = None, finishVector = None, finishFrame = None)

setScale(mask, startVector, startFrame = None, finishVector = None, finishFrame = None)

setRotation(mask, startVector, startAngle, startFrame = None, finishVector = None, finishAngle = None, finishFrame = None)



start(with, height, stereoMode='flat', isFullscreen=false, isRayTracing=false, startFrame=None, finishFrame=None) - открывает окно нужных размеров, в требуемом стерео-режиме ('flat','crossEye','stereoTV','anaglyph'), и если нужно - на полный экран

exportPNG(with, height, stereoMode='flat', dir, filePrefix, startFrame=None, finishFrame=None)

exportOBJ(mask, dir, file_prefix, startFrame=None, finishFrame=None)

exportScene(startFrame=None, finishFrame=None)

