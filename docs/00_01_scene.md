# Библиотека Scene - система команд

Объект Scene предназначен для быстрого вывода объектов на экран и управление их внешним видом. Объекты загружаются в сцену, при этом им присваивается имя, которое позволяет в дальнейшем контролировать его отображение. 



Первоначальные настройки (до SceneStart)

- ScenePresetDebug()

- ScenePresetWindowSize(with, height, isFullScreen)

- ScenePresetStereoMode(mode = mono/stareoTV/crossEye/anaglith)

  

Настройки анимации (до SceneStart)

- SceneStopPoint(t, delayInDemoMode, comment)

- SceneRegAction(eraseFlag, setupFunc, animateFunc(None for dtatic), tStart, tEnd, step ,mode=normal/exportToWeb/exportToPng, dirName)

  

SceneStart()

SceneEnd()



SceneLayer(layerName)

SceneSetStyle(styleName, styleValue)

SceneGetStyle(styleName)

SceneApplyStyle(objName, propName, propValue)

 

SceneLevelDown(levelName)

SceneLevelUp()

 

Привязки работают с учетом преобразования локальных координат

SceneSetPivot(path, pivotName, xyz)

xyz = SceneGetPivot(path, pivotname)

[xyz] = SceneGetPivots(path)

  

SceneDrawPoint(name, xyz)

SceneDrawLine(name, xyzStart, xyzFinish, arrowStart, arrowFinish, growFactor, growType)

SceneDrawFlat(name, xyz, xyz, xyz, growFactor, growType)

SceneDrawCyrcle(name, xyz, xyz, xyz)

SceneDrawArc(name, xyz, xyz, xyz, arrowStart, arrowFinish, growFactor, growType)

 

SceneDrawBox(name, xyz)

SceneDrawSphere(name, r)

SceneDrawCone(name, r, h)

SceneDrawCylr(name, r, h)

 

SceneDrawShape(name, sh, filename)

SceneDrawMessage(name, xyz, text)

SceneDrawLabel(name, text = None)

 

Стандартные декорации

SceneDrawAxis(name)

SceneDrawBox(name)

 

obj = SceneGetNativeObject(name)

 

SceneMove(xyzFrom, xyzTo)

SceneRotate(xyzCenter, xyzAxis, angle)

SceneScale(xyzCenter, xyzScale)

SceneOrientTo(xyzCenter, xyzPivot, xyzMass ,xyzOrientTo, ScaleFactor)

 

 

SceneFIReset(linear/spline)

SceneFIAdd(t,float)

float = SceneFIGet(t)

 

ScenePIReset(linear/spline)

ScenePIAdd(t,xyz)

xyz=ScenePIGet(t)