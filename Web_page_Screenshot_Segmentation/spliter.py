import cv2

def draw_line(image,heights,color = (0,0,255)):
    for height in heights:
        cv2.line(image, (0, height), (image.shape[1], height), color, 2)
    return image