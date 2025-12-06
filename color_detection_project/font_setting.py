import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

def put_chinese_text(image, text, position, font_size=20, color=(0, 255, 0)):
    """使用PIL绘制中文，避免乱码"""
    # 加载系统中文字体（确保路径正确）
    # Windows系统默认黑体字体路径
    font_path = "C:/Windows/Fonts/simhei.ttf"
    # Linux系统示例（需根据实际路径调整）
    # font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    
    try:
        # 加载字体
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        # 字体加载失败时使用默认字体（可能显示方块）
        print(f"[警告] 无法加载字体文件: {font_path}，使用默认字体")
        font = ImageFont.load_default()
    
    # 转换OpenCV图像为PIL图像（BGR转RGB）
    img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    
    # 绘制文字
    draw.text(position, text, font=font, fill=color)
    
    # 转回OpenCV格式（RGB转BGR）
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

# 测试代码
if __name__ == "__main__":
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    img = put_chinese_text(img, "测试中文显示", (50, 240), font_size=30, color=(0, 255, 0))
    cv2.imshow("中文显示测试", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()