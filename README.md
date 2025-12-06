# Color-Judgment: 多区域颜色识别多数投票系统
基于 Python + OpenCV 开发的实时颜色识别系统，支持自由画框标定、多区域检测与多数投票判定，适配有色差的同色物体识别，响应快速且准确率高。


## 项目地址
[GitHub 仓库](https://github.com/ZLWsxhh/Color-Judgment.git)


## 核心功能
**自由画框标定**：鼠标拖动选择任意区域，支持同一颜色多组 LAB 值标定（适配色差场景）
**多区域检测**：默认 6 个检测区域同步识别，支持自定义区域位置与尺寸
**多数投票机制**：6 个区域中 ≥4 个匹配才输出结果，大幅提升识别稳定性
**实时响应**：优化图像预处理流程，确保 30fps 流畅运行
**可视化展示**：检测结果直接叠加在相机画面，无需额外弹窗，包含区域结果与最终判定
**跨平台支持**：兼容 Windows 和 Linux 系统，支持 USB 相机/内置相机


## 项目目录结构

Color-Judgment/
└── color_detection_project/
    ├── data/                  # 数据目录
    │   ├── ref_colors.json    # 参考颜色模板文件
    │   └── samples/           # 示例样本目录
    ├── linux/                 # Linux 系统专用脚本
    │   ├── README_LINUX.md    # Linux 部署说明
    │   ├── install_linux.sh   # Linux 依赖安装脚本
    │   └── requirements_linux.txt  # Linux 依赖库列表
    ├── tools/                 # 工具脚本目录
    │   └── sample_lab.py      # LAB 颜色标定工具
    ├── all_in_one.bat         # Windows 一键启动菜单（推荐）
    ├── camera.py              # 相机初始化与配置模块
    ├── clean.bat              # Windows 缓存清理脚本
    ├── color_detector.py      # 核心检测类（多区域+投票机制）
    ├── config.json.bak        # 配置文件备份
    ├── config.py              # 系统配置（相机参数+阈值）
    ├── dev.bat                # Windows 开发环境启动脚本
    ├── font_setting.py        # 中文显示字体配置
    ├── main.py                # 主程序（相机采集+实时识别）
    ├── rebuild.bat            # Windows 虚拟环境重建脚本
    ├── requirements.txt       # Windows 依赖库列表
    ├── roi_config.json        # 检测区域配置文件
    ├── setup.bat              # Windows 依赖安装脚本
    ├── utils.py               # 工具函数（颜色差计算等）
    └── README.md              # 项目说明文档
```


## 快速部署
### 1. 环境准备
1. 克隆仓库：
   ```bash
   git clone https://github.com/ZLWsxhh/Color-Judgment.git
   cd Color-Judgment/color_detection_project
   ```
2. 安装 Python 3.7+（勾选「Add Python to PATH」）


### 2. Windows 系统（推荐）
#### 方式 1：一键启动（新手友好）
双击运行 `all_in_one.bat`，在弹出的菜单中选择功能：
- 1: 正常模式运行识别程序
- 2: 调试模式运行（输出详细日志）
- 3: 进入开发环境
- 4: 清理缓存文件
- 5: 重建虚拟环境
- 6: 启动 LAB 颜色标定工具（`tools/sample_lab.py`）
- 7: 退出程序

#### 方式 2：命令行部署
```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动标定工具（先标定颜色）
python tools/sample_lab.py

# 启动识别程序
python main.py
```


### 3. Linux 系统
参考 `linux/README_LINUX.md`，执行以下命令：
```bash
# 进入 Linux 脚本目录
cd linux

# 赋予脚本执行权限
chmod +x install_linux.sh

# 安装依赖（自动配置环境）
./install_linux.sh

# 返回项目根目录
cd ..

# 启动标定工具
python tools/sample_lab.py

# 启动识别程序
python main.py
```


## 使用教程
### 步骤 1：颜色标定（关键步骤）
1. 启动标定工具：
   - Windows：通过 `all_in_one.bat` 选择「6」，或命令行运行 `python tools/sample_lab.py`
   - Linux：命令行运行 `python tools/sample_lab.py`
2. 标定操作：
   - 相机启动后，对准待标定颜色物体（如红色杯子）
   - 鼠标拖动自由选择标定区域（建议宽高 ≥20px，覆盖物体不同色差部位）
   - 按 `s` 键保存，在命令行输入颜色名称（如「红色」）并回车
   - 同一颜色建议标定 3-5 组（覆盖不同亮度/角度的色差）
   - 按 `r` 键重置当前区域，按 `q` 键退出（标定数据自动保存到 `data/ref_colors.json`）


### 步骤 2：实时颜色识别
1. 启动识别程序：
   - Windows：通过 `all_in_one.bat` 选择「1」，或命令行运行 `python main.py`
   - Linux：命令行运行 `python main.py`
2. 操作说明：
   - 程序自动打开相机，画面显示 6 个检测区域（区域配置来自 `roi_config.json`）
   - 每个区域实时显示该区域识别结果，画面底部显示最终投票结果
   - 按 `s` 键保存当前帧（用于调试），按 `q` 键退出程序


## 核心配置文件说明
| 文件路径               | 作用说明                     |
|------------------------|------------------------------|
| `data/ref_colors.json` | 标定的颜色 LAB 值存储文件    |
| `roi_config.json`      | 检测区域的位置/尺寸配置      |
| `config.py`            | 相机参数、颜色阈值等系统配置 |


## 常见问题排查
### 1. 相机模糊
- 关闭自动对焦：在 `camera.py` 中添加 `cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)`
- 固定焦距：调整 `cap.set(cv2.CAP_PROP_FOCUS, 50)`（值范围 0-100）
- 清洁镜头，调整拍摄距离（10-50cm 最佳）

### 2. 标定文件格式错误
- 错误提示：`ValueError: 颜色数据必须包含3个分量`
- 解决方案：打开 `data/ref_colors.json`，确保每个颜色的标定值是 3 个数值的数组（如 `[53, 80, 67]`）

### 3. 中文显示乱码
- 检查 `font_setting.py` 中字体路径是否正确（默认使用系统黑体）
- Linux 系统需安装中文字体：`sudo apt-get install fonts-noto-cjk`


## 依赖库列表
- Windows：参考 `requirements.txt`
- Linux：参考 `linux/requirements_linux.txt`


## 许可证
本项目采用 MIT 许可证，欢迎 Fork、Star 和二次开发。


## 贡献
若发现 Bug 或有优化建议，欢迎提交 Issue 或 Pull Request。
