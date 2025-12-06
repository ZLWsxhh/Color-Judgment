import cv2
import numpy as np
from color_detector import ColorDetector
import config
import os
import sys
import time

def main():
    try:
        # 初始化相机
        cap = cv2.VideoCapture(config.CAMERA_INDEX, cv2.CAP_DSHOW)
        if not cap.isOpened():
            print("[ERROR] 无法打开摄像头！")
            return
            
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
        
    except Exception as e:
        print(f"[ERROR] 相机初始化失败: {e}")
        return

    # 初始化颜色检测器
    detector = ColorDetector(threshold=config.COLOR_DETECTION_THRESHOLD)

    # 获取相机参数
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    print("===================================")
    print(f"相机分辨率: {width}x{height}")
    print(f"帧率: {fps:.1f}fps")
    print(f"颜色阈值: {config.COLOR_DETECTION_THRESHOLD}")
    print("按 'q' 退出程序")
    print("===================================")

    # 性能监控
    frame_count = 0
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] 获取帧失败")
            break

        frame_count += 1
        
        # 计算FPS
        if frame_count % 30 == 0:
            elapsed = time.time() - start_time
            current_fps = frame_count / elapsed
            print(f"处理速度: {current_fps:.1f} FPS")
            frame_count = 0
            start_time = time.time()

        # 执行颜色检测
        detected_color, confidence = detector.detect_color(frame)
        
        # 绘制检测结果
        result_frame = detector.draw_detection_result(frame, detected_color, confidence)
        
        # 显示结果
        window_title = "Real-time Color Detection"
        cv2.imshow(window_title, result_frame)
        
        # 在控制台输出检测结果（可选）
        if detected_color != "Unknown" and frame_count % 10 == 0:
            print(f"检测到颜色: {detected_color} (置信度: {confidence:.1f})")

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()