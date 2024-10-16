@echo off

net session >nul 2>&1
if %errorlevel% neq 0 (
    echo This script requires administrative privileges.
    echo Please run this script as an administrator.
    pause
    exit /b
)

setlocal
setx /M ANDROID_HOME "C:\Users\moj\AppData\Local\Android\Sdk"
setx /M JAVA_HOME "C:\Program Files\Java\jdk-17"

set /p NEW_PATH="where did you install LD Player: "

if "%NEW_PATH%"=="" (
    echo No path entered. Exiting...
    exit /b
)

set CURRENT_PATH=%PATH%
set NEW_PATH=%CURRENT_PATH%;%NEW_PATH%
setx /M PATH "%NEW_PATH%"
pause
