@echo off
chcp 65001
cd /d %~dp0

echo ================================
echo 清理 Python 缓存 (__pycache__)
echo ================================
for /r %%i in (.) do (
    if /i "%%~nxi"=="__pycache__" (
        if exist "%%i" (
            echo 删除 %%i
            rmdir /s /q "%%i"
        )
    )
)

echo ================================
echo 清理临时文件 (*.pyc, *.pyo)
echo ================================
for /r %%i in (*.pyc) do del /f /q "%%i"
for /r %%i in (*.pyo) do del /f /q "%%i"

echo ================================
echo 清理 output/ 目录
echo ================================
if exist output (
    rmdir /s /q output
    echo 已删除 output 目录
)

echo ================================
echo 清理颜色配置文件
echo ================================
if exist config.json (
    echo 正在备份 config.json...
    copy config.json config.json.bak >nul
    echo 是否要删除颜色配置文件? (y/n)
    set /p choice=
    if /i "%choice%"=="y" (
        del config.json
        echo 已删除 config.json
    ) else (
        echo 保留配置文件
    )
)

echo ================================
echo 清理完成!
echo ================================
pause