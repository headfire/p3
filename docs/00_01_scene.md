# Библиотека Scene - система команд

Библиотека Scene предназначена для быстрого вывода объектов на экран и управление их внешним видом. Объекты загружаются в сцену, при этом им присваивается имя, которое позволяет в дальнейшем контролировать их отображение. 

Первоначальные настройки (до SceneStart)

```
ScenePresetDebug()
ScenePresetFullScreen()
ScenePresetScreenSize(with, height)
ScenePresetStereoMode(mode = mono/stareoTV/crossEye/anaglith)
ScenePresetAutorotate(speed)
ScenePresetRegAction(setupFunc, animateFunc, tStart, tEnd, step, mode=normal/exportToWeb/exportToPng, dirName)
```

Параметры просмотра - название, описание сцены и коментарии в точках останова (до SceneStart)

```
SceneViewTitle(title, describe)
SceneViewStopPoint(t, delayInDemoMode, comment)
```

Инициализация системы

```
SceneStart()
SceneReset()
SceneEnd()
```

Управление слоями и стилями

```
SceneLayer(layerName)
SceneSetStyle(styleName, styleValue)
SceneGetStyle(styleName)
SceneApplyStyle(objName, styleName, styleValue)
```

Навигация по уровням объектов и выяснение их свойств

```
SceneLevelRoot()
SceneLevelDown(levelName)
SceneLevelUp()
list(objName) = SceneLevelList()
level/point/line/flat/box/cyrcle/arc/sphere/cone/cylinder/shape/pointset = SceneObjType(objName)
nativeObj = SceneNativeObj(objName)
```

 Привязки работают с учетом преобразования локальных координат

```
SceneSetBase(objRelativePath, pivotName, xyz)
xyz = SceneGetBase(objRelativePath, pivotName)
dict(xyz) = SceneGetBases(objRelativePath)
```

Создание объектов. Если объект с именем есть он либо пересоздается либо видоизменяется для соответствия новым параметрам, если это возможно. Объекты создаются с учетом текущих стилей на текущем слое.

```
#Elementary linear object
SceneDrawPoint(objName, xyz)
SceneDrawLine(objName, xyzStart, xyzFinish, arrowStart, arrowFinish, growFactor, growType)
SceneDrawFlat(objName, xyz, xyz, xyz, growFactor, growType)

#Elementary 2D-curve object
SceneDrawCyrcle(objName, xyz, xyz, xyz)
SceneDrawArc(objName, xyz, xyz, xyz, arrowStart, arrowFinish, growFactor, growType)

#Elementary 3D-object
SceneDrawBox(objName, xyz)
SceneDrawSphere(objName, r)
SceneDrawCone(objName, r, h)
SceneDrawCylinder(objName, r, h)

#Complex object
#casheKey use for store and cashe object and control cashe strategy 
SceneDrawShape(objName, sh, cashekey)
SceneDrawPointSet( list(xyz), casheKey)

#Text object
SceneDrawMessage(objName, xyz, text)
SceneDrawLabel(objName, text = None)

#Standard drawing decortation
SceneDrawAxis(objName)
SceneDrawDesk(objName)
```

 Управление камерой

```
#CameraControl
SceneSetCamera(xyzCamera, xyzLookAt)
```

Трансформация объектов

```
SceneMove(xyzFrom, xyzTo)
SceneRotate(xyzCenter, xyzAxis, angle)
SceneScale(xyzCenter, xyzScale)
SceneLookAt(xyzCenter, xyzPivot, xyzLookAt, xyzMass, scaleFactor/-1notScale/0..1PivotToLookAt)
```

Встроенные интерполяторы 

```
#Float interpolator
SceneFIReset(linear/spline)
SceneFIAdd(t,float)
float = SceneFIGet(t)

#Point interpolator
ScenePIReset(linear/spline)
ScenePIAdd(t,xyz)
xyz=ScenePIGet(t)
```

