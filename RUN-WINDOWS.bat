@echo off
setlocal
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  py -3 -m venv .venv
  if errorlevel 1 goto error
)
call .venv\Scripts\python.exe -m pip install -r server\requirements.txt
if errorlevel 1 goto error
call .venv\Scripts\python.exe -m uvicorn server.app:app --host 127.0.0.1 --port 8017
exit /b 0
:error
echo Khong the khoi dong. Hay cai Python 3.11+ va thu lai.
pause
exit /b 1
