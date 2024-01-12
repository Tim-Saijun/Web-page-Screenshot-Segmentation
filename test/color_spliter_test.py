import cv2
import numpy as np


def on_var_color_trackbar(val):
    global var_color_threshold
    var_color_threshold = val


def on_color_diff_trackbar(val):
    global color_difference_threshold
    color_difference_threshold = val


# 初始化阈值
var_color_threshold = 200
color_difference_threshold = 12

# 创建窗口
cv2.namedWindow('settings')
cv2.namedWindow('Marked Image')

# 创建滑动条
cv2.createTrackbar('Var Color Threshold', 'settings', var_color_threshold, 500, on_var_color_trackbar)
cv2.createTrackbar('Color Difference Threshold', 'settings', color_difference_threshold, 50, on_color_diff_trackbar)

# 读取图像
image = cv2.imread('../imgs/shinetruss.jpeg')
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)

# 缩放因子
scale_factor = 0.3

while True:
    marked_image = image.copy()

    previous_row_color = None

    # 遍历每一行
    for i in range(image_gray.shape[0]):
        row = image_gray[i, :, :]

        # 计算当前行的平均颜色值和方差
        average_color = np.mean(row, axis=0)
        var_color = np.var(row, axis=0)

        if var_color[0] < var_color_threshold and var_color[1] < var_color_threshold and var_color[2] < var_color_threshold:
            if previous_row_color is not None:
                color_difference = np.linalg.norm(average_color - previous_row_color)

                if color_difference > color_difference_threshold:
                    cv2.line(marked_image, (0, i), (marked_image.shape[1], i), (0, 0, 255), 2)

            previous_row_color = average_color

    # 缩放标记后的图像用于展示
    resized_marked_image = cv2.resize(marked_image, (
    int(marked_image.shape[1] * scale_factor), int(marked_image.shape[0] * scale_factor)))

    # 显示缩放后的带标记的图片
    cv2.imshow('Marked Image', resized_marked_image)

    # 等待并检查是否按下了'q'键
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cv2.destroyAllWindows()

# 可选：保存原始尺寸的结果图片
cv2.imwrite('marked_image.jpg', marked_image)
