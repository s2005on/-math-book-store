@echo off
setlocal
cd /d "%~dp0"
py -3 start.py
if errorlevel 1 (
  echo.
  echo Khoi dong that bai. Hay cai Python 3.11+ va kiem tra ket noi Internet.
  pause
)
