@echo off
REM 双击直接运行：默认跑 day2_numpy_practice.py
REM 也可以把任意 .py 文件拖到这个文件上，就会跑那个文件

cd /d "%~dp0"

set "PY=C:\Users\18172\miniconda3\envs\ai-met\python.exe"

if "%~1"=="" (
    set "TARGET=day2_numpy_practice.py"
) else (
    set "TARGET=%~1"
)

echo Running: %TARGET%
echo ----------------------------------------
"%PY%" "%TARGET%"
echo ----------------------------------------
echo Done.
pause
