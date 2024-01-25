"""将一个png图片贴在另一个jpg文件里，并且保存"""
import cv2
import numpy as np
import os

def paste(a:np.ndarray, b:np.ndarray, position:tuple):
    """将a数组贴在b数组上，position为贴图的左上角坐标"""
    shape = a.shape

def paste_png_to_jpg(png_path, jpg_path, x, y):

    # 调整png图片的大小
    png = cv2.imread(png_path, cv2.IMREAD_UNCHANGED)
    png = cv2.resize(png, (800, 800))

    # 读取jpg图片
    jpg = cv2.imread(jpg_path)

    # 获取png图片的alpha通道
    alpha = png[:, :, 3]

    # 获取png图片的rgb通道
    rgb = png[:, :, :3]

    cv2.imshow('jpg', jpg)
    cv2.waitKey(0)


if __name__ == '__main__':
    paste_png_to_jpg(r'./blue.png', r'./1200(6).jpg', 0, 0)