# Начальные настройки слоев и стилей

### Слой hide - для скрытых объектов

```
SceneLayer('hide')
SceneSetStyle('visible', False)        
SceneSetStyle('color', (0, 0, 1))       
SceneSetStyle('transparency', 0 )       
SceneSetStyle('lineType', 'solid')  
SceneSetStyle('lineWidth', 3)
SceneSetStyle('pointSize', 3 )       
SceneSetStyle('textColor', (55/255, 74/255, 148/255))       
SceneSetStyle('textHeight', 20)       
```

### Слой info - для вспомогательных построений

```
SceneLayer('info')
SceneSetStyle('visible', True)        
SceneSetStyle('color', (0.5, 0.5, 0.5))       
SceneSetStyle('transparency', 0 )       
SceneSetStyle('lineType', 'dash')       
SceneSetStyle('lineWidth', 1)       
SceneSetStyle('pointSize', 3 )       
SceneSetStyle('textColor', (0.5, 0.5, 0.5))       
SceneSetStyle('textHeight', 20)       
```

### Слой base - для опорных объектов, важных для чертежа

```
SceneLayer('base')
SceneSetStyle('visible', True)        
SceneSetStyle('color', (1, 0, 0))       
SceneSetStyle('transparency', 0 )       
SceneSetStyle('lineType', 'dash')       
SceneSetStyle('lineWidth', 2)       
SceneSetStyle('pointSize', 3 )       
SceneSetStyle('textColor', (189/255, 60/255, 45/255))       
SceneSetStyle('textHeight', 20)       
```

### Слой main - для основных объектов

```
SceneLayer('main')
SceneSetStyle('visible', True)        
SceneSetStyle('color', (0, 0, 1))       
SceneSetStyle('transparency', 0 )       
SceneSetStyle('lineType', 'solid')       
SceneSetStyle('lineWidth', 3)       
SceneSetStyle('pointSize', 3 )       
SceneSetStyle('textColor', (55/255, 74/255, 148/255))       
SceneSetStyle('textHeight', 20)       
```

### Важно

Последний настроенный слой **main** становится текущим на котором начинается рисование
