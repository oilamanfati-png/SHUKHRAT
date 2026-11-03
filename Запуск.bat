@echo off
cd /d "%~dp0"
echo Запуск Berad Tech...
python berad.py
if errorlevel 1 (
  echo.
  echo Python не найден. Установите Python с python.org
  pause
)
