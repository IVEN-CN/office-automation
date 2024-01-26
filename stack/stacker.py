"""将一个png图片贴在另一个jpg文件里，并且保存"""
import cv2
import numpy as np
import os

def paste(a:np.ndarray, b:np.ndarray, position:tuple[int,int]):
    """将a数组贴在b数组上，position为贴图的左上角坐标"""
    shape = a.shape

    for i in range(shape[0]):
        for k in range(shape[1]):
            b[position[0]+i][position[1]+k] = a[i][k]
    return b

def paste_png_to_jpg(png_path, jpg_path, position:tuple[int,int]=(600, 750), test:bool=False):

    # 调整png图片的大小
    png = cv2.imread(png_path, cv2.IMREAD_UNCHANGED)
    png = cv2.resize(png, (140, 76))

    # 读取jpg图片
    jpg = cv2.imread(jpg_path)

    # 获取png图片的alpha通道，并转换为浮点数
    alpha = png[:, :, 3].astype(float)/255

    # 对alpha通道进行阈值处理，消除黑边
    alpha = cv2.threshold(alpha, 0.5, 1, cv2.THRESH_BINARY)[1]

    # 创建一个3通道的alpha图像
    alpha = cv2.merge((alpha, alpha, alpha))

    # 获取png图片的rgb通道
    rgb_png = png[:, :, :3]

    roi = jpg[position[1]:position[1]+png.shape[0], position[0]:position[0]+png.shape[1]]

    # 使用alpha通道作为掩码，将png图片贴在jpg图片上
    jpg[position[1]:position[1]+png.shape[0], position[0]:position[0]+png.shape[1]] = (alpha * rgb_png + (1 - alpha) * roi).astype(np.uint8) # type: ignore

    if test:
        cv2.imshow('jpg', jpg)
        cv2.waitKey(0)
    else:
        cv2.imwrite(jpg_path, jpg)


if __name__ == '__main__':
    paste_png_to_jpg(r'./blue.png', r'./1200(6).jpg', (600, 750),test=False)