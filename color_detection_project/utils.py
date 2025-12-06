import numpy as np
from skimage import color
import cv2

def calc_delta_e(lab1, lab2, method='CIE76'):
    """
    计算颜色差
    lab1, lab2: np.array([L, A, B])
    method: 'CIE76' 或 'CIE2000'
    """
    # 确保输入是3维数组（skimage要求）
    lab1 = np.array(lab1, dtype=np.float32).reshape(1, 1, 3)
    lab2 = np.array(lab2, dtype=np.float32).reshape(1, 1, 3)

    if method == 'CIE76':
        return np.linalg.norm(lab1 - lab2)
    elif method == 'CIE2000':
        return color.deltaE_ciede2000(lab1, lab2)[0][0]
    else:
        raise ValueError("method must be 'CIE76' or 'CIE2000'")

def draw_detections(image, detections, color=(0, 255, 0), thickness=2):
    """
    在图像上绘制检测到的区域
    image: OpenCV 图像 (numpy 数组)
    detections: 检测框列表，每个元素为 (x, y, w, h)
    color: 框的颜色，默认为绿色
    thickness: 框线宽
    返回已绘制的图像
    """
    for (x, y, w, h) in detections:
        cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)
    return image

def measure_sharpness(image):
    """
    测量图像锐度（用于对焦评估）
    :param image: 输入图像
    :return: 锐度分数
    """
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 使用拉普拉斯算子计算图像梯度
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    sharpness = laplacian.var()
    return sharpness