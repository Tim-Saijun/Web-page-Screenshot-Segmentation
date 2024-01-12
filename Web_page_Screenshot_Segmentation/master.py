import cv2
import os
from blank_spliter import find_height_spliter
from color_spliter import color_height_spliter
from spliter import draw_line


def remove_close_values(lst: list[int], threshold: int) -> list[int]:
    """
    给定一个列表，将里面数值差异在Threshold以内的数值进行去除，保留最大的那个数值，用于去除重复或接近的分割线
    """
    # Sort the list in ascending order
    lst.sort()
    # 如果最小的值小于threshold，直接删除
    if lst[0] < 200:
        del lst[0]
    # Iterate over the list in reverse (starting from the end)
    i = len(lst) - 1
    while i > 0:
        # Check if the difference between adjacent values is within the threshold
        if lst[i] - lst[i - 1] <= threshold:
            # Remove the smaller value
            del lst[i - 1]
        i -= 1
    return lst


def test():
    # 批量处理，可展示处理结果以及合并前的结果
    for image_file in os.listdir('../imgs'):
        img = cv2.imread(os.path.join('../imgs', image_file))
        img2 = img.copy()
        img3 = img.copy()
        heights = []
        regions = find_height_spliter(img, 102, 0.5)
        print(regions)
        heights.extend(regions)
        draw_line(img, regions, color=(0, 255, 0))
        regions = color_height_spliter(img2, 100, 15)
        print(regions)
        heights.extend(regions)
        draw_line(img, regions, color=(0, 0, 255))
        cv2.imwrite(image_file.split('.')[0] + 'result1.jpg', img)
        heights = remove_close_values(heights, 350)
        print(heights)
        draw_line(img2, heights, color=(0, 0, 255))
        cv2.imwrite(image_file.split('.')[0] + 'result2.jpg', img2)


def batch_process():
    # 不绘制中间文件
    for image_file in os.listdir('../imgs'):
        img = cv2.imread(os.path.join('../imgs', image_file))
        heights = []
        regions = find_height_spliter(img, 102, 0.5)
        heights.extend(regions)
        regions = color_height_spliter(img, 100, 15)
        heights.extend(regions)
        heights = remove_close_values(heights, 350)
        draw_line(img, heights, color=(0, 0, 255))
        cv2.imwrite('result/' + image_file.split('.')[0] + 'result2.jpg', img)


if __name__ == '__main__':
    batch_process()
