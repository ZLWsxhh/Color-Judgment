@echo off
chcp 65001 >nul   REM 设置终端编码为 UTF-8，避免乱码
cd /d %~dp0       REM 切换到当前批处理所在目录

:MENU
title Color Detection Project - Main Menu  REM Set window title
cls
echo =========================================
echo        COLOR DETECTION PROJECT
echo =========================================
echo 1. Run main.py (Normal mode)
echo 2. Run main.py (Debug mode)
echo 3. Enter development environment
echo 4. Clean cache and color config
echo 5. Rebuild virtual environment
echo 6. LAB reference color tool
echo 7. Exit
echo =========================================
set /p choice=Please select [1-7]:

if "%choice%"=="1" goto RUN_NORMAL
if "%choice%"=="2" goto RUN_DEBUG
if "%choice%"=="3" goto DEV
if "%choice%"=="4" goto CLEAN
if "%choice%"=="5" goto REBUILD
if "%choice%"=="6" goto LAB
if "%choice%"=="7" exit

goto MENU

:RUN_NORMAL
title Color Detection Project - Normal Mode  REM Window Title: Normal Mode
call .venv\Scripts\activate
set DEBUG_MODE=False
python main.py
pause
goto MENU

:RUN_DEBUG
title Color Detection Project - Debug Mode   REM Window Title: Debug Mode
call .venv\Scripts\activate
set DEBUG_MODE=True
python main.py
pause
goto MENU

:DEV
title Color Detection Project - Development  REM Window Title: Development Environment
call .venv\Scripts\activate
cmd
goto MENU

:CLEAN
title Color Detection Project - Cleaning     REM Window Title: Clear Cache
echo 正在清理...
call clean.bat
goto MENU

:REBUILD
title Color Detection Project - Rebuilding VENV  REM Window Title: Rebuild Virtual Environment
if exist .venv rmdir /s /q .venv
python -m venv .venv
if %errorlevel% neq 0 (
    echo Failed to create virtual environment. Please check Python installation.
    pause
    goto MENU
)
call .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
pause
goto MENU

:LAB
title Color Detection Project - LAB Tool     REM Window Title: LAB Reference Color Tool
call .venv\Scripts\activate
python tools\sample_lab.py
pause
goto MENU