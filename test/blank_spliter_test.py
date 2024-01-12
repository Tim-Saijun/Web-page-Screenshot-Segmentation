import logging
import time
import cv2
from log9 import  setup_logging # this can be replaced by 'import logging'
setup_logging()

def on_trackbar_change(_):
    # 创建原始图像的副本
    img_copy = original_image.copy()
    # 根据窗口大小调整图像尺寸
    resized_image = cv2.resize(img_copy, (720, 2000))
    # 获取滑动条当前位置作为参数
    height_threshold = cv2.getTrackbarPos('Height Threshold', 'Image')
    variation_threshold = cv2.getTrackbarPos('Variation Threshold', 'Image') / 100

    # 使用新参数重新处理图像
    regions = find_low_variation_regions(img_copy, height_threshold, variation_threshold)
    display_regions(img_copy, regions)
    cv2.imwrite(f'{time.time()}.jpg', img_copy)
    # 显示处理后的图像
    # cv2.resizeWindow('Image', 720, 2000)
    cv2.imshow('Image', img_copy)


def find_low_variation_regions(image, height_threshold, variation_threshold):
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gray', gray)
    cv2.imwrite('../gray.jpg', gray)
    # 初始化一些变量
    start_row = None
    regions = []

    logging.info(f"gray.shape[0]:{gray.shape[0]},gray.shape[1]:{gray.shape[1]},gray.shape:{gray.shape}")
    # 遍历图像行，寻找低变化区域
    for i in range(gray.shape[0]):
        row_variation = cv2.Laplacian(gray[i:i+1, :], cv2.CV_32F).var()
        if row_variation < variation_threshold:
            if start_row is None:
                start_row = i
        else:
            if start_row is not None and (i - start_row) >= height_threshold:
                regions.append((start_row, i))
            start_row = None

    # 处理最后一个区域
    if start_row is not None and (gray.shape[0] - start_row) >= height_threshold:
        regions.append((start_row, gray.shape[0]))

    return regions


def display_regions(image, regions):
    # 输出与标记结果
    for start, end in regions:
        logging.debug(f"一个低变化区域从行 {start} 到 {end}")
        cv2.rectangle(image, (0, start), (image.shape[1], end), (0, 255, 0), 2)


# 读取原始图像
original_image = cv2.imread(r'../imgs/ycwaterjet_cut.jpeg')

# 创建窗口和滑动条
cv2.namedWindow('Image')
cv2.createTrackbar('Height Threshold', 'Image', 100, 500, on_trackbar_change)
cv2.createTrackbar('Variation Threshold', 'Image', 50, 100, on_trackbar_change)
# cv2.resizeWindow('Image', 100, 300)
# 初始处理一次图像
on_trackbar_change(0)

# 等待用户交互或关闭窗口
cv2.waitKey(0)
cv2.destroyAllWindows()
