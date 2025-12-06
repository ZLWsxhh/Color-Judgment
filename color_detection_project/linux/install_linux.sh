#!/bin/bash

# Color Detection Project - Linux 一键安装脚本
echo "========================================="
echo "   Color Detection Project Linux 安装"
echo "========================================="

# 检查是否以root运行
if [ "$EUID" -eq 0 ]; then
    echo "[警告] 不建议使用root用户运行，请使用普通用户"
    read -p "是否继续? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检查系统类型
if [[ $(uname) != "Linux" ]]; then
    echo "[错误] 此脚本仅适用于Linux系统"
    exit 1
fi

# 定义颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 函数：打印带颜色的消息
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查依赖
check_dependencies() {
    print_status "检查系统依赖..."
    
    local missing_deps=()
    
    # 检查Python3
    if ! command -v python3 &> /dev/null; then
        missing_deps+=("python3")
    fi
    
    # 检查pip3
    if ! command -v pip3 &> /dev/null; then
        missing_deps+=("python3-pip")
    fi
    
    # 检查其他依赖
    if ! command -v git &> /dev/null; then
        missing_deps+=("git")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_warning "缺少依赖: ${missing_deps[*]}"
        return 1
    fi
    
    print_status "所有依赖已安装"
    return 0
}

# 安装系统依赖
install_system_deps() {
    print_status "安装系统依赖..."
    
    if command -v apt-get &> /dev/null; then
        # Debian/Ubuntu
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-venv git \
            libgl1-mesa-glx libglib2.0-0 libsm6 libxrender1 libxext6
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL
        sudo yum install -y python3 python3-pip git \
            mesa-libGL glib2 libSM libXrender libXext
    elif command -v dnf &> /dev/null; then
        # Fedora
        sudo dnf install -y python3 python3-pip git \
            mesa-libGL glib2 libSM libXrender libXext
    elif command -v pacman &> /dev/null; then
        # Arch Linux
        sudo pacman -S --noconfirm python python-pip git \
            mesa libglvnd libsm libxrender libxext
    else
        print_error "不支持的包管理器"
        return 1
    fi
    
    print_status "系统依赖安装完成"
}

# 创建虚拟环境
create_venv() {
    print_status "创建Python虚拟环境..."
    
    if [ -d ".venv" ]; then
        print_warning "虚拟环境已存在，是否重新创建?"
        read -p "重新创建虚拟环境? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf .venv
            python3 -m venv .venv
        fi
    else
        python3 -m venv .venv
    fi
    
    if [ $? -ne 0 ]; then
        print_error "创建虚拟环境失败"
        return 1
    fi
    
    print_status "虚拟环境创建成功"
}

# 安装Python依赖
install_python_deps() {
    print_status "安装Python依赖..."
    
    source .venv/bin/activate
    
    # 升级pip
    pip install --upgrade pip
    
    # 安装依赖
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        # 如果没有requirements.txt，直接安装所需包
        pip install opencv-python numpy scipy scikit-image matplotlib pillow
    fi
    
    if [ $? -ne 0 ]; then
        print_error "依赖安装失败"
        return 1
    fi
    
    print_status "Python依赖安装完成"
}

# 配置相机权限
setup_camera_permissions() {
    print_status "配置相机权限..."
    
    # 将用户添加到video组
    if ! groups $USER | grep -q '\bvideo\b'; then
        print_status "将用户 $USER 添加到video组..."
        sudo usermod -a -G video $USER
        print_warning "需要重新登录才能使权限生效"
    fi
    
    # 创建udev规则（如果需要）
    if [ ! -f "/etc/udev/rules.d/99-color-detection.rules" ]; then
        echo 'SUBSYSTEM=="video4linux", GROUP="video", MODE="0666"' | sudo tee /etc/udev/rules.d/99-color-detection.rules > /dev/null
        sudo udevadm control --reload-rules
        sudo udevadm trigger
    fi
    
    print_status "相机权限配置完成"
}

# 创建启动脚本
create_launch_script() {
    print_status "创建启动脚本..."
    
    cat > run.sh << 'EOF'
#!/bin/bash

# Color Detection Project - Linux 启动脚本

cd "$(dirname "$0")"

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "虚拟环境不存在，请先运行 install_linux.sh"
    exit 1
fi

# 激活虚拟环境
source .venv/bin/activate

# 检查是否支持中文字体
if [ ! -f "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf" ] && \
   [ ! -f "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc" ]; then
    echo "警告: 系统中文字体可能缺失，如需中文显示请安装字体:"
    echo "sudo apt-get install fonts-noto-cjk"
fi

# 运行主程序
python main.py

deactivate
EOF

    chmod +x run.sh
    
    cat > run_menu.sh << 'EOF'
#!/bin/bash

# Color Detection Project - 菜单启动脚本

cd "$(dirname "$0")"

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "虚拟环境不存在，请先运行 install_linux.sh"
    exit 1
fi

# 激活虚拟环境
source .venv/bin/activate

# 显示菜单
echo "========================================="
echo "   Color Detection Project - Linux"
echo "========================================="
echo "1. 正常运行模式"
echo "2. 调试模式"
echo "3. LAB颜色采样工具"
echo "4. 清理缓存"
echo "5. 退出"
echo "========================================="

read -p "请选择 [1-5]: " choice

case $choice in
    1)
        echo "启动正常模式..."
        python main.py
        ;;
    2)
        echo "启动调试模式..."
        DEBUG_MODE=True python main.py
        ;;
    3)
        echo "启动LAB采样工具..."
        python sample_lab.py
        ;;
    4)
        echo "清理缓存..."
        find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
        find . -name "*.pyc" -delete
        find . -name "*.pyo" -delete
        echo "清理完成"
        ;;
    5)
        echo "退出"
        ;;
    *)
        echo "无效选择"
        ;;
esac

deactivate
EOF

    chmod +x run_menu.sh
    
    print_status "启动脚本创建完成"
}

# 主安装流程
main() {
    echo "开始安装 Color Detection Project..."
    echo "当前目录: $(pwd)"
    echo "用户: $USER"
    echo ""
    
    # 检查依赖
    if ! check_dependencies; then
        print_warning "尝试安装缺失的依赖..."
        install_system_deps
    fi
    
    # 创建虚拟环境
    if ! create_venv; then
        print_error "安装失败"
        exit 1
    fi
    
    # 安装Python依赖
    if ! install_python_deps; then
        print_error "安装失败"
        exit 1
    fi
    
    # 配置相机权限
    setup_camera_permissions
    
    # 创建启动脚本
    create_launch_script
    
    echo ""
    echo "========================================="
    echo "  安装完成!"
    echo "========================================="
    echo "使用方法:"
    echo "  ./run.sh          - 直接运行"
    echo "  ./run_menu.sh     - 菜单方式运行"
    echo ""
    echo "注意事项:"
    echo "  1. 可能需要重新登录才能使相机权限生效"
    echo "  2. 如果需要中文显示，请安装中文字体:"
    echo "     sudo apt-get install fonts-noto-cjk"
    echo "  3. 相机设备通常为 /dev/video0 或 /dev/video1"
    echo "========================================="
}

# 运行主函数
main "$@"