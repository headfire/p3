# Установка OpenCascade - Python 3.7 - Win64

## Устанавливаем пакет для разработки на Python 3 Анаконда 3

Для нашей версии достаточно пакета "Миниконда".

Скачиваем установщик: [https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe)

Запускаем и оставляем все опции по умолчанию.

В списке программ кнопки `Пуск` появилось меню `Anaconda3`. Копируем из него ярлык `Anaconda Prompt` на рабочий стол

## Создаем среду Python 3.7

Путем экспериментов установлено что наиболее стабильно все работает на версии Python 3.7 Создаем среду с требуемой версией в conda

```
conda create -n py37 python=3.7
conda activate py37
```

## Устанавливаем среду разработки Spyder

Запускаем ярлык созданный на предыдущем шаге

Набираем в командной строке conda
```
conda install -c anaconda spyder
```
Для проверки запускаем Spyder

```
spyder
```

На предложение установить kite отвечаем dismiss (оно не работает как надо)

Проверяем что все работает и закрываем Spyder

**Важно:** вместе со Spyder устанавливается библиотека Qt, необходимая для работы OpenCascade. Если вы используйте другую IDE, инсталлируйте Qt отдельно.

## Устанавливаем библиотеку PythonOCC (OpenCascade for Python 3)

Оставаясь в командной строке conda инсталлируем библиотеку PythonOCC
```
conda install -c dlr-sc pythonocc-core=7.4.0
```

## Устанавливаем Git

Загружаем и запускаем отсюда [https://git-scm.com/download/win]( https://git-scm.com/download/win). Все настройки оставляем по умолчанию.

## Создаем проект Spyder с примерами OpenCascade

Запускаем командную строку Windows `Windows (клавиша с эмблемой) + X ; Командная строка`

В проводнике создаём папку где будут хранится Ваши проекты по OpenCascade, например `c:/dev/occ `

Заходим в проводнике в папку и запускаем командную строку с папкой в качестве текущей директории

```
Справка - запуск командной строки из проводника 
Windows 7: Shift + Right Mouse - Command Line Here
Windows 10: Набираем cmd в верхней строке проводника вместо пути
```

Клонируем репозиторий с примерами

```
git clone https://github.com/tpaviot/pythonocc-demos.git
```

Запускаем spyder (Через командную строку Anaconda)

* Выбираем в меню `Projects->New Project...`
* Выбираем вариант `Existing directory`
* Выбираем папку с примерами `pythonocc-demos`
* Нажимаем `Create project`

Открываем в spyder окно проекта и выбираем в нем файл `\examples\core_helloworld.py`
и запускаем на  выполнение

Должно открыться окно с следующей картинкой



![Test Image 3](../images/core_helloworld.png?)



Это значит что среда настроена правильно.

## Создаем проект Spyder с данными уроками

Действуем также как в предыдущем пункте, только изменяем адрес репозитория

```
git clone https://github.com/headfire/occ-tutorial.git
```

## Полезные советы

**Быстрый запуск Spyder** 

1. Из ярлыка Anaconda Prompt узнайте нахождение файла `activate,bat`. 

2. В конец файла этого файла добавьте 
   
   ```
   call conda activate py37
   call spyder
   ```
   
   среда разработки будет загружаться автоматически по ярлыку

**Быстрый поиск нужной функции**

1. В меню Spyder выбираем `Serch->Find in files`
2. В боковой панели выбираем директорию `...conda\Lib\site-packages\OCC`
3. Ищем функции и классы по фрагментам имен

## Полезные ссылки

* [https://www.opencascade.com/](https://www.opencascade.com/) 
* [https://www.opencascade.com/doc/occt-6.9.1/refman/html/index.html](https://www.opencascade.com/doc/occt-6.9.1/refman/html/index.html)
* [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
* [https://anaconda.org/anaconda/spyder](https://anaconda.org/anaconda/spyder)
* [https://github.com/tpaviot/pythonocc-core](https://github.com/tpaviot/pythonocc-core)
* [https://github.com/tpaviot/pythonocc-demos](https://github.com/tpaviot/pythonocc-demos)
* [https://git-scm.com/download/win](https://git-scm.com/download/win)

 

