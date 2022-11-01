rem [screen  web  stl] [1..10]
call %HEADFIRE_CONDA%\scripts\activate.bat
set PYTHONPATH=%HEADFIRE_P3%\libs\pydesk
python ..\src\dao.py %1 %2
pause
