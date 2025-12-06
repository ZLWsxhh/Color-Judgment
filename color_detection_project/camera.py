import cv2
import numpy as np  # 添加这行导入
import config

def init_camera():
    """
    初始化相机：设置分辨率、帧率、曝光、白平衡，返回相机捕获对象
    优化聚焦和图像质量
    """
    # 1. 初始化相机（使用DSHOW驱动，解决USB相机兼容性问题）
    cap = cv2.VideoCapture(config.CAMERA_INDEX, cv2.CAP_DSHOW)
    if not cap.isOpened():
        raise RuntimeError("无法打开摄像头！请检查：\n1. config.py中CAMERA_INDEX是否正确（0=默认相机，1=USB相机）\n2. 相机是否被其他程序占用")

    # 2. 设置画面分辨率（从config读取，1280×720=720P）
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
    
    # 3. 设置帧率（目标30fps）
    target_fps = 30
    cap.set(cv2.CAP_PROP_FPS, target_fps)
    
    # 4. 设置MJPG编码（更好的压缩和质量）
    fourcc_mjpg = cv2.VideoWriter_fourcc(*"MJPG")
    cap.set(cv2.CAP_PROP_FOURCC, fourcc_mjpg)
    
    # 5. 自动对焦设置（如果相机支持）
    try:
        # 启用自动对焦
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        # 设置对焦范围（0-255，根据相机调整）
        cap.set(cv2.CAP_PROP_FOCUS, 200)
    except:
        print("[INFO] 相机不支持自动对焦设置")
    
    # 6. 曝光设置（优化曝光控制）
    try:
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # 关闭自动曝光
        cap.set(cv2.CAP_PROP_EXPOSURE, -3)         # 曝光值：-4（适中亮度）
    except:
        print("[INFO] 相机不支持曝光设置")
    
    # 7. 白平衡设置
    try:
        cap.set(cv2.CAP_PROP_AUTO_WB, 1)           # 关闭自动白平衡
        cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 5500) # 设置白平衡温度（5500K=日光）
    except:
        print("[INFO] 相机不支持白平衡设置")
    
    # 8. 其他图像质量设置
    try:
        cap.set(cv2.CAP_PROP_BRIGHTNESS, 60)        # 亮度
        cap.set(cv2.CAP_PROP_CONTRAST, 50)         # 对比度
        cap.set(cv2.CAP_PROP_SATURATION, 80)       # 饱和度
        cap.set(cv2.CAP_PROP_SHARPNESS, 60)        # 锐度
    except:
        print("[INFO] 相机不支持部分图像质量设置")

    # 验证设置
    actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"相机分辨率: {int(actual_width)}×{int(actual_height)}")
    print(f"相机帧率: {actual_fps:.1f}fps")
    print(f"对焦状态: {'自动' if cap.get(cv2.CAP_PROP_AUTOFOCUS) else '手动'}")

    return cap

def apply_sharpening(frame, strength=1.5):
    """
    应用图像锐化处理
    :param frame: 输入图像
    :param strength: 锐化强度
    :return: 锐化后的图像
    """
    # 创建锐化核
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]]) * strength
    # 应用卷积锐化
    sharpened = cv2.filter2D(frame, -1, kernel)
    return sharpened

def adjust_gamma(frame, gamma=1.2):
    """
    调整图像伽马值，增强对比度
    :param frame: 输入图像
    :param gamma: 伽马值 (>1 变暗，<1 变亮)
    :return: 调整后的图像
    """
    # 构建伽马校正查找表
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    # 应用伽马校正
    return cv2.LUT(frame, table)