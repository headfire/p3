# Установка OpenCascade - Python 3.7 - Win64


## Устанавливаем среду Анаконда 3 (Python 3.7) 

Путем экспериментов установлено что наиболее стабильно все работает на версии Python 3.7. 
Создаем среду с требуемой версией.
Для нашей версии достаточно пакета "Миниконда".

Скачиваем установщик: [https://repo.anaconda.com/miniconda/Miniconda3-py37_4.10.3-Windows-x86_64.exe](https://repo.anaconda.com/miniconda/Miniconda3-py37_4.10.3-Windows-x86_64.exe)

Выбираем опцию *For All* и папку *с:/conda*.

В списке программ кнопки `Пуск` появилось меню `Anaconda3`. Копируем из него ярлык `Anaconda Prompt` на рабочий стол


## Устанавливаем библиотеки 

Qt (графическая подсистема)
PythonOCC (OpenCascade for Python 3) 

Оставаясь в командной строке conda набираем команды
```
conda install pyqt
conda install -c dlr-sc pythonocc-core
```

## Скачивание и запуск примеров 

Устанавливаем Git.
Загружаем и запускаем отсюда [https://git-scm.com/download/win]( https://git-scm.com/download/win). Все настройки оставляем по умолчанию.

Клонируем репозиторий с примерами

```
c:
cd c:\projects
git clone https://github.com/tpaviot/pythonocc-demos.git
cd pythonocc-demos\examples
python core_helloworld.py
```

Должно открыться окно с следующей картинкой

![Test Image 3](../images/core_helloworld.png?)

Это значит что среда настроена правильно.

Клонируем проект headfire/point

```
c:
cd c:\projects
git clone https://github.com/headfire/point.git
cd point
python makeDaoShape.py
```


## Полезные ссылки

* [https://www.opencascade.com/](https://www.opencascade.com/)  
* [https://www.opencascade.com/doc/occt-6.9.1/refman/html/index.html](https://www.opencascade.com/doc/occt-6.9.1/refman/html/index.html)
* [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
* [https://github.com/tpaviot/pythonocc-core](https://github.com/tpaviot/pythonocc-core)
* [https://github.com/tpaviot/pythonocc-demos](https://github.com/tpaviot/pythonocc-demos)
* [https://git-scm.com/download/win](https://git-scm.com/download/win)

 

