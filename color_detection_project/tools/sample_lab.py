import cv2
import numpy as np
import json
import os

CONFIG_PATH = "config.json"

def load_config():
    """加载已有 config.json，如果不存在则返回空字典"""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"colors": {}, "rois": {}}

def save_config(data):
    """保存到 config.json"""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def list_colors(config):
    """显示已保存的颜色列表"""
    colors = config.get("colors", {})
    if not colors:
        print("当前没有保存任何颜色")
        return
    
    print("已保存的颜色:")
    for i, color_name in enumerate(colors.keys(), 1):
        sample_count = len(colors[color_name])
        print(f"  {i}. {color_name} ({sample_count}个样本)")

def delete_color(config, color_name):
    """删除指定颜色"""
    colors = config.get("colors", {})
    rois = config.get("rois", {})
    
    if color_name in colors:
        del colors[color_name]
        if color_name in rois:
            del rois[color_name]
        print(f"已删除颜色: {color_name}")
        return True
    else:
        print(f"颜色 '{color_name}' 不存在")
        return False

def main():
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    config = load_config()
    colors_config = config.get("colors", {})
    rois_config = config.get("rois", {})

    # 当前绘制的 ROI 列表
    current_rois = []
    drawing = False
    start_point = None
    current_color = None

    print("===================================")
    print(" LAB Reference Color Sampling Tool")
    print("===================================")
    print("操作方法:")
    print(" - 按 'c' 选择颜色")
    print(" - 按 'l' 列出已保存的颜色")
    print(" - 按 'd' 删除指定颜色")
    print(" - 鼠标拖动绘制 ROI 区域")
    print(" - 按 's' 保存当前颜色的所有 ROI")
    print(" - 按 'r' 删除最后一个 ROI")
    print(" - 按 'q' 退出")
    print("===================================")

    def draw_rois(frame, rois):
        """绘制所有 ROI"""
        for roi in rois:
            x1, y1, x2, y2 = roi
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return frame

    def mouse_callback(event, x, y, flags, param):
        nonlocal drawing, start_point, current_rois
        
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            start_point = (x, y)
            
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                temp_frame = frame.copy()
                cv2.rectangle(temp_frame, start_point, (x, y), (0, 255, 0), 2)
                temp_frame = draw_rois(temp_frame, current_rois)
                cv2.imshow("LAB Sampling Tool", temp_frame)
                
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            end_point = (x, y)
            # 确保 ROI 有效
            if abs(x - start_point[0]) > 10 and abs(y - start_point[1]) > 10:
                current_rois.append((start_point[0], start_point[1], x, y))
                print(f"添加 ROI: {start_point} -> {end_point}")

    cv2.namedWindow("LAB Sampling Tool")
    cv2.setMouseCallback("LAB Sampling Tool", mouse_callback)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to grab frame")
            break

        # 显示当前状态
        status_frame = frame.copy()
        if current_color:
            cv2.putText(status_frame, f"当前颜色: {current_color}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(status_frame, f"ROI数量: {len(current_rois)}", (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # 绘制 ROI
        status_frame = draw_rois(status_frame, current_rois)
        cv2.imshow("LAB Sampling Tool", status_frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("c"):
            # 选择颜色
            color_name = input("请输入颜色名称 (例如 Blue, Red, Green): ").strip()
            if color_name:
                current_color = color_name
                current_rois = []  # 开始新的颜色采样
                print(f"开始采样颜色: {color_name}")

        elif key == ord("l"):
            # 列出已保存的颜色
            list_colors(config)

        elif key == ord("d"):
            # 删除颜色
            color_name = input("请输入要删除的颜色名称: ").strip()
            if color_name:
                if delete_color(config, color_name):
                    # 更新配置
                    config["colors"] = colors_config
                    config["rois"] = rois_config
                    save_config(config)
                    print("配置已保存")

        elif key == ord("s") and current_color and current_rois:
            # 保存当前颜色的所有 ROI
            color_samples = []
            roi_positions = []
            success_count = 0
            
            for roi in current_rois:
                x1, y1, x2, y2 = roi
                # 确保坐标在图像范围内
                x1, x2 = max(0, min(x1, x2)), min(frame.shape[1], max(x1, x2))
                y1, y2 = max(0, min(y1, y2)), min(frame.shape[0], max(y1, y2))
                
                if x2 <= x1 or y2 <= y1:
                    continue
                    
                roi_area = frame[y1:y2, x1:x2]
                
                if roi_area.size == 0:
                    continue
                    
                try:
                    # 计算 ROI 平均 LAB
                    lab_roi = cv2.cvtColor(roi_area, cv2.COLOR_BGR2LAB)
                    avg_lab = np.mean(lab_roi.reshape(-1, 3), axis=0).astype(int).tolist()
                    color_samples.append(avg_lab)
                    roi_positions.append([x1, y1, x2, y2])
                    success_count += 1
                except Exception as e:
                    print(f"处理ROI时出错: {e}")
                    continue
            
            if success_count > 0:
                # 保存到配置
                colors_config[current_color] = color_samples
                rois_config[current_color] = roi_positions
                
                config["colors"] = colors_config
                config["rois"] = rois_config
                save_config(config)
                
                print(f"[SUCCESS] 成功保存 {current_color}: {success_count} 个样本到 {CONFIG_PATH}")
                print(f"LAB值示例: {color_samples[0]}")
                current_rois = []  # 清空当前 ROI
            else:
                print("[ERROR] 保存失败：没有有效的ROI区域")

        elif key == ord("r"):  # 改为r键删除ROI，避免与删除颜色冲突
            # 删除最后一个 ROI
            if current_rois:
                removed = current_rois.pop()
                print(f"删除 ROI: {removed}")

        elif key == ord("q"):
            print("退出采样工具")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()