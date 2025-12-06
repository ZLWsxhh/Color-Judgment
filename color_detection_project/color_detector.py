import cv2
import numpy as np
import json
import os
from utils import calc_delta_e

class ColorDetector:
    def __init__(self, config_path="config.json", threshold=25.0):
        """
        初始化颜色检测器
        """
        self.config_path = config_path
        self.threshold = threshold
        self.ref_colors = self.load_reference_colors()
        
        print(f"加载的参考颜色: {list(self.ref_colors.keys())}")

    def load_reference_colors(self):
        """从 JSON 文件加载 LAB 参考颜色"""
        if not os.path.exists(self.config_path):
            print(f"[WARN] 未找到配置文件: {self.config_path}")
            return {}
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
                colors_config = config_data.get("colors", {})
                print(f"成功加载 {len(colors_config)} 种颜色的参考数据")
                return colors_config
        except Exception as e:
            print(f"[ERROR] 配置文件加载失败: {e}")
            return {}

    def get_dominant_color(self, frame):
        """
        提取图像的主色调（LAB格式）
        """
        if frame.size == 0:
            return np.array([0, 0, 0], dtype=np.float32)
            
        # 使用整个图像计算平均颜色
        lab_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        mean_color = cv2.mean(lab_frame)
        return np.array([mean_color[0], mean_color[1], mean_color[2]], dtype=np.float32)

    def detect_color(self, frame):
        """
        检测图像中的主色调
        :param frame: BGR格式图像
        :return: 颜色名称和置信度
        """
        # 获取主色调
        avg_color = self.get_dominant_color(frame)
        
        # 与参考颜色比对
        detected_color_name = "Unknown"
        min_dist = float("inf")
        
        for name, ref_samples in self.ref_colors.items():
            for sample in ref_samples:
                sample_arr = np.array(sample, dtype=np.float32)
                dist = calc_delta_e(avg_color, sample_arr)
                if dist < min_dist:
                    min_dist = dist
                    detected_color_name = name
        
        # 检查是否超过阈值
        if min_dist > self.threshold:
            detected_color_name = "Unknown"
        
        return detected_color_name, min_dist

    def draw_detection_result(self, frame, color_name, confidence):
        """
        在图像上绘制检测结果
        """
        result = frame.copy()
        
        # 在左上角显示检测结果
        text = f"Color: {color_name}"
        color = (0, 255, 0) if color_name != "Unknown" else (0, 0, 255)
        
        # 绘制背景矩形增强可读性
        cv2.rectangle(result, (10, 10), (300, 80), (0, 0, 0), -1)
        
        # 显示颜色名称
        cv2.putText(result, text, (20, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
        
        # 显示置信度（如果是Unknown则不显示）
        if color_name != "Unknown":
            conf_text = f"Confidence: {confidence:.1f}"
            cv2.putText(result, conf_text, (20, 80), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return result