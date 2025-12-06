# Color Detection Project - Linux 部署指南

## 系统要求
- Ubuntu 18.04+ / Debian 10+ / CentOS 7+ / Fedora 32+
- Python 3.6+
- USB 摄像头

## 快速开始

### 1. 一键安装
```bash
# 下载项目
git clone <项目地址>
cd color_detection_project

# 运行安装脚本
chmod +x install_linux.sh
./install_linux.sh


### 2. 手动安装

# 安装系统依赖
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv git \
    libgl1-mesa-glx libglib2.0-0 libsm6 libxrender1 libxext6

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装Python依赖
pip install --upgrade pip
pip install -r requirements_linux.txt


### 3. 相机权限配置

bash
# 将用户添加到video组
sudo usermod -a -G video $USER

# 重新登录或重启使权限生效


## 使用方法
## 直接运行

bash
./run.sh

## 菜单方式运行

bash
./run_menu.sh

## 手动运行

bash
source .venv/bin/activate
python main.py

## 故障排除

#1. 相机无法打开

bash
# 检查相机设备
ls -l /dev/video*

# 检查用户组
groups $USER

# 临时权限修复
sudo chmod 666 /dev/video0

#2. 中文显示问题

bash
# 安装中文字体
sudo apt-get install fonts-noto-cjk

#3. OpenCV 依赖问题

bash
# 安装缺失的依赖
sudo apt-get install -y libgtk2.0-dev libgtk-3-dev

#4. 虚拟环境问题

bash
# 重新创建虚拟环境
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements_linux.txt

## 文件说明
install_linux.sh - Linux一键安装脚本

run.sh - 直接启动脚本

run_menu.sh - 菜单启动脚本

requirements_linux.txt - Linux专用依赖

## 支持的系统
✅ Ubuntu 18.04+

✅ Debian 10+

✅ CentOS 7+

✅ Fedora 32+

✅ Arch Linux

✅ Raspberry Pi OS

## 注意事项
安装完成后可能需要重新登录

不同的Linux发行版可能需要调整依赖包名

如果使用虚拟机，需要确保USB摄像头直通

树莓派用户可能需要额外安装硬件加速库

## text

## 使用说明

# 1. 给安装脚本执行权限
```bash
chmod +x install_linux.sh
#2. 运行安装脚本
bash
./install_linux.sh
#3. 运行程序
bash
# 直接运行
./run.sh

# 或使用菜单方式
./run_menu.sh
#4. 相机权限配置（如果需要）
bash
# 检查相机设备
ls /dev/video*

# 如果无法访问相机，运行以下命令后重新登录
sudo usermod -a -G video $USER

这个安装脚本会自动：

检查系统依赖

安装必要的系统包

创建Python虚拟环境

安装Python依赖

配置相机权限

创建便捷的启动脚本

支持主流的Linux发行版，包括Ubuntu、Debian、CentOS、Fedora等。

