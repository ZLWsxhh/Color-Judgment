@echo off
cd /d %~dp0

echo ================================
echo 激活虚拟环境...
echo ================================
call .venv\Scripts\activate

echo ================================
echo 安装依赖 (requirements.txt) ...
echo ================================
pip install -r requirements.txt

echo ================================
echo 启动 main.py ...
echo ================================
python main.py

echo ================================
echo 程序已退出
echo ================================
pause
