import os
import cv2


def find_height_spliter(image, height_threshold, variation_threshold):
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 初始化一些变量
    start_row = None
    heights = []

    # 遍历图像行，寻找低变化区域
    for i in range(gray.shape[0]):
        row_variation = cv2.Laplacian(gray[i:i+1, :], cv2.CV_64F).var()
        if row_variation < variation_threshold:
            if start_row is None:
                start_row = i
        else:
            if start_row is not None and (i - start_row) >= height_threshold:
                heights.append(int((start_row + i) / 2)) # 取中间值作为分割处
            start_row = None

    # 处理最后一个区域
    if start_row is not None and (gray.shape[0] - start_row) >= height_threshold:
        heights.append(start_row)

    return heights

def find_low_variation_regions(image, height_threshold, variation_threshold):
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 初始化一些变量
    start_row = None
    regions = []

    # 遍历图像行，寻找低变化区域
    for i in range(gray.shape[0]):
        row_variation = cv2.Laplacian(gray[i:i+1, :], cv2.CV_64F).var()
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
        print(f"找到一个低变化区域从行 {start} 到 {end}")
        cv2.rectangle(image, (0, start), (image.shape[1], end), (0, 255, 0), 2)

def process_image(height_threshold, variation_threshold,file_name,original_image):
    # 创建原始图像的副本
    img_copy = original_image.copy()
    # 根据窗口大小调整图像尺寸
    resized_image = cv2.resize(img_copy, (720, 2000))

    # 使用新参数重新处理图像
    regions = find_low_variation_regions(img_copy, height_threshold, variation_threshold)
    display_regions(img_copy, regions)
    dir_name = str(height_threshold) + '_' + str(variation_threshold) + '_' + r'result/'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    cv2.imwrite(dir_name+file_name, img_copy)
    # 显示处理后的图像
    # cv2.imshow('Image', img_copy)



if __name__ == '__main__':
    # for height_threshold in range(110, 200, 10):
    #     for variation_threshold in range(0.1, 1, 0.1):
    height_threshold = 100
    variation_threshold = 0.5
    # 读取原始图像
    for image_file in os.listdir('../imgs'):
        original_image = cv2.imread(os.path.join('../imgs', image_file))
        process_image(height_threshold, variation_threshold,file_name=image_file,original_image=original_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

