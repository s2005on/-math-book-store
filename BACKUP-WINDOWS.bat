@echo off
setlocal
cd /d "%~dp0"
if not exist "server\data" (
 echo Chua co du lieu de sao luu.
 pause
 exit /b 0
)
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set TODAY=%%a_%%b_%%c
if not exist "backups" mkdir "backups"
set "TARGET=backups\backup_%RANDOM%_%RANDOM%"
mkdir "%TARGET%"
xcopy /E /I /Y "server\data" "%TARGET%\data" >nul
if errorlevel 1 (
 echo Loi sao luu du lieu.
) else (
 echo Da sao luu vao %TARGET%
)
pause
