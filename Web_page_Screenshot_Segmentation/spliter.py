import cv2
import argparse
import os


def draw_line_from_file(image_file, heights, color=(0, 0, 255)):
    """
    :param image_file: 图片文件路径
    :param heights: 分割线高度列表
    :param color: 分割线颜色
    :return: 分割后的图片路径
    """
    try:
        image = cv2.imread(image_file)
    except:
        raise Exception(
            "Failed to read image file, Please check if the file path contains '.' or Chinese characters. "
            "读取图片失败，请检查文件路径是否包含'.'或者中文字符")
    for height in heights:
        cv2.line(image, (0, height), (image.shape[1], height), color, 2)
    result_name = image_file.split('.')[-2] + 'result.jpg'
    abs_path = os.path.abspath('result/' + result_name)
    cv2.imwrite(abs_path, image)
    return abs_path


def draw_line(image, heights, color=(0, 0, 255)):
    for height in heights:
        cv2.line(image, (0, height), (image.shape[1], height), color, 2)
    return image

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_file', type=str,
                        help='图片文件路径')
    parser.add_argument('--height_list', '-hl', type=str, default='[]', help='分割线高度列表')
    parser.add_argument('--color', type=str, default='(0, 0, 255)', help='分割线颜色')
    args = parser.parse_args()
    image_file = args.image_file
    heights = eval(args.height_list)
    color = eval(args.color)
    res = draw_line_from_file(image_file, heights, color)
    print(res)
