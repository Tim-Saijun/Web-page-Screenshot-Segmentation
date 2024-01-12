import cv2
import numpy as np


def color_height_spliter(image, var_color_threshold, color_difference_threshold):
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    previous_row_color = None
    height_list = []

    # 遍历每一行
    for i in range(image_gray.shape[0]):
        row = image_gray[i, :]

        # 计算当前行的平均颜色值和方差
        average_color = np.mean(row, axis=0)
        var_color = np.var(row, axis=0)

        if var_color < var_color_threshold:
            if previous_row_color is not None:
                color_difference = np.linalg.norm(average_color - previous_row_color)

                if color_difference > color_difference_threshold:
                    # 获取高度
                    height_list.append(i)
            previous_row_color = average_color
    return height_list

def process_image(image, var_color_threshold, color_difference_threshold, scale_factor=0.3):
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    marked_image = image.copy()

    previous_row_color = None

    # 遍历每一行
    for i in range(image_gray.shape[0]):
        row = image_gray[i, :]

        # 计算当前行的平均颜色值和方差
        average_color = np.mean(row, axis=0)
        var_color = np.var(row, axis=0)

        if var_color < var_color_threshold:
            if previous_row_color is not None:
                color_difference = np.linalg.norm(average_color - previous_row_color)

                if color_difference > color_difference_threshold:
                    cv2.line(marked_image, (0, i), (marked_image.shape[1], i), (0, 0, 255), 2)

            previous_row_color = average_color

    # 缩放标记后的图像用于展示
    resized_marked_image = cv2.resize(marked_image, (int(marked_image.shape[1] * scale_factor), int(marked_image.shape[0] * scale_factor)))
    return resized_marked_image, marked_image

if  __name__ == '__main__':
    # 读取图像
    image = cv2.imread('../imgs/shinetruss.jpeg')

    # 参数
    var_color_threshold = 100
    color_difference_threshold = 15
    scale_factor = 0.3

    # 处理图像
    resized_marked_image, marked_image = process_image(image, var_color_threshold, color_difference_threshold, scale_factor)

    # 显示缩放后的带标记的图片
    cv2.imshow('Marked Image', resized_marked_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 保存原始尺寸的结果图片
    cv2.imwrite('marked_image1.jpg', marked_image)
