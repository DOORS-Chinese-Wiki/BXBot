@echo off
rem BXBot 一键启动（前台运行，Ctrl+C 退出）
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
.venv\Scripts\python.exe -m bxbot run %*
pause
