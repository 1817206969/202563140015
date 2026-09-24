@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Running day3_play.py with ai-met python...
echo ==========================================
"C:\Users\18172\miniconda3\envs\ai-met\python.exe" day3_play.py
echo ==========================================
echo Done.
pause
