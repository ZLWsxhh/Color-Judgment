@echo off
cd /d %~dp0

echo ================================
echo 删除旧虚拟环境 (.venv)
echo ================================
if exist .venv (
    rmdir /s /q .venv
    echo 已删除旧虚拟环境
) else (
    echo 未找到旧虚拟环境
)

echo ================================
echo 创建新虚拟环境 (.venv)
echo ================================
python -m venv .venv
if %errorlevel% neq 0 (
    echo 创建虚拟环境失败，请检查 Python 是否安装
    pause
    exit /b 1
)

echo ================================
echo 激活虚拟环境并安装依赖
echo ================================
call .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

echo ================================
echo 虚拟环境重建完成!
echo 可以使用 setup.bat 或 dev.bat 运行程序
echo ================================
pause
