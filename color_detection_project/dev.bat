@echo off
cd /d %~dp0

echo ================================
echo 激活虚拟环境...
echo ================================
call .venv\Scripts\activate

echo ================================
echo 已进入开发环境
echo 你现在可以手动运行:
echo   python main.py
echo 或者安装新依赖:
echo   pip install package_name
echo ================================
cmd
