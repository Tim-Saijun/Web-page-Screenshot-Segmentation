import cv2
import argparse
import os
from pathlib import Path


def split_and_save_image(img, heights, output_dir):
    img = cv2.imread(img)
    img_height = img.shape[0]
    # Ensure the output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Initialize the start of the first slice
    start_y = 0
    # Iterate over the split heights
    if heights[0] < 200:
        del heights[0]
    if len(heights) == 0:
        heights.append(img_height)

    heights = [h for h in heights if h < img_height]
    # If the last height is less than the image height, add the image height to the list to include the last segment
    if heights[-1] < img_height:
        heights.append(img_height)

    for i, height in enumerate(heights):
        # Define the end of the slice
        end_y = height
        # Slice the image
        img_slice = img[start_y:end_y, :]
        # Save the slice
        slice_path = os.path.join(output_dir, f'slice_{i}.png')
        # slice_path = os.path.abspath(slice_path)
        cv2.imwrite(slice_path, img_slice)
        # The start of the next slice
        start_y = end_y

    return output_dir

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_file', '-f',type=str,
                        help='图片文件路径')
    parser.add_argument('--height_list', '-hl', type=str, default='[]', help='分割线高度列表')
    parser.add_argument('--output_dir', '-o', type=str, default='split_images', help='分割完成后的图片保存目录，建议给每个要处理的图片传入一个不同的目录')
    args = parser.parse_args()
    image_file = args.image_file
    heights = eval(args.height_list)
    output_dir = args.output_dir
    res = split_and_save_image(image_file, heights,output_dir)
    res = os.path.abspath(res)
    print(res)
