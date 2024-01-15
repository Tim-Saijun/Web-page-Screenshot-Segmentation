import cv2
import os
import argparse
from .blank_spliter import find_height_spliter
from .color_spliter import color_height_spliter
from .drawer import draw_line


def remove_close_values(lst: list[int], threshold: int) -> list[int]:
    """
    给定一个列表，将里面数值差异在Threshold以内的数值进行去除，保留最大的那个数值，用于去除重复或接近的分割线
    """
    lst.sort()
    # 如果最小的值小于threshold，直接删除,在spliter中15行有相同的代码
    if lst[0] < 200:
        del lst[0]
    i = len(lst) - 1
    while i > 0:
        if lst[i] - lst[i - 1] <= threshold:
            del lst[i - 1]
        i -= 1
    return lst


def split_heights(file_path: str,
                  split: bool = False,
                  height_threshold: int = 102,
                  variation_threshold: float = 0.5,
                  color_threshold: int = 100,
                  color_variation_threshold: int = 15,
                  merge_threshold: int = 350
                  ):
    """
    Given the path of an image file, split the image into several parts.

    :param file_path: path of the image file
    :param split: whether to split the image
    :param height_threshold: the height threshold of the low variation region
    :param variation_threshold: the variation threshold of the low variation region
    :param color_threshold: the threshold of the color difference
    :param color_variation_threshold: the threshold of the color difference variation
    :param merge_threshold: the threshold of the least distance between two lines
    :return: list of heights of the split lines or the path of split image

    给定图像文件的路径，将图像分割成几个部分。

    :param file_path: 图像文件的路径
    :param split: 是否分割图像
    :param height_threshold: 低变化区域的高度阈值
    :param variation_threshold: 低变化区域的变化阈值
    :param color_threshold: 颜色差异的阈值
    :param color_variation_threshold: 颜色差异变化的阈值
    :param merge_threshold: 两条线之间最小距离的阈值
    :return: 分割线的高度列表 or 分割后的图像路径
    """
    try:
        img = cv2.imread(file_path)
    except:
        raise Exception(
            "Failed to read image file, Please check if the file path contains '.' or Chinese characters. "
            "读取图片失败，请检查文件路径是否包含'.'或者中文字符")
    heights = []
    regions = find_height_spliter(img, height_threshold, variation_threshold)
    heights.extend(regions)
    regions = color_height_spliter(img, color_threshold, color_variation_threshold)
    heights.extend(regions)
    heights = remove_close_values(heights, merge_threshold)
    if split:
        if os.path.exists('result') is False:
            os.mkdir('result')
        draw_line(img, heights, color=(0, 255, 0))
        cv2.imwrite('result/' + file_path.split('.')[-2] + 'result.jpg', img)
        absolute_path = os.path.abspath('result/' + file_path.split('.')[-2] + 'result.jpg')
        return absolute_path
    else:
        return heights


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
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str,
                        help='path of the image file')
    parser.add_argument('-s', '--split', type=bool, default=False,
                        help='whether to split the image')
    parser.add_argument('-ht', '--height_threshold', type=int, default=102,
                        help='the height threshold of the low variation region')
    parser.add_argument('-vt', '--variation_threshold', type=float, default=0.5,
                        help='the variation threshold of the low variation region')
    parser.add_argument('-ct', '--color_threshold', type=int, default=100,
                        help='the threshold of the color difference')
    parser.add_argument('-cvt', '--color_variation_threshold', type=int, default=15,
                        help='the threshold of the color difference variation')
    parser.add_argument('-mt', '--merge_threshold', type=int, default=350,
                        help='the threshold of the least distance between two lines')
    args = parser.parse_args()
    res = split_heights(args.file, args.split, args.height_threshold, args.variation_threshold,
                  args.color_threshold, args.color_variation_threshold, args.merge_threshold)
    print(res)
    # test()
    # batch_process()
