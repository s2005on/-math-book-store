@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 start.py
) else (
  python start.py
)
if errorlevel 1 (
  echo.
  echo Khong the khoi dong. Can Python 3.11+ va Internet trong lan dau.
  echo Hay kiem tra dong loi phia tren.
  pause
)
