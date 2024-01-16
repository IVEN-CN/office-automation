"""将不同颜色的色卡图片分到新的文件夹，文件夹用颜色命名"""
import os
import cv2
import numpy as np

roll = np.ones([500, 500])


def get_file_path(file_dir) -> list:
    """获取相对路径下文件夹的所有文件的路径
    file_dir: 文件夹路径"""
    path_list = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            path_list.append(os.path.join(root, file))
    return path_list


def color_detect(img_: np.ndarray,
                 colorfile) -> bool:
    range_ = np.load(colorfile)
    lower = range_[0]
    upper = range_[1]
    hsv = cv2.cvtColor(img_, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)
    if np.isin(roll, mask).any():
        cv2.imshow('test', mask)
        cv2.waitKey(0)
        return True
    else:
        cv2.imshow('test', mask)
        cv2.waitKey(0)
        return False


def mkdir():
    """创建文件夹"""
    color = ['白色', '黑色', '浅紫', '杏色', '浅蓝', '浅绿', '粉红']
    for i in color:
        try:
            os.mkdir(i)
        except FileExistsError:
            pass


def mvfile(path: list, target):
    """移动文件"""
    for i in path:
        os.system(f'move {i} {target}')

def mian():
    file_path = get_file_path('./U007')
    for i in file_path:
        if '主图' in i or '细节' in i:
            file_path.remove(i)

    mkdir()

    for i in file_path:
        img = cv2.imread(i)
        if img is None:
            continue
        if color_detect(img, '浅紫.npy'):
            mvfile([i], '浅紫')
        elif color_detect(img, '杏色.npy'):
            mvfile([i], '杏色')
        elif color_detect(img, '浅蓝.npy'):
            mvfile([i], '浅蓝')
        elif color_detect(img, '浅绿.npy'):
            mvfile([i], '浅绿')
        elif color_detect(img, '粉红.npy'):
            mvfile([i], '粉红')
        elif color_detect(img, '黑色.npy'):
            mvfile([i], '黑色')
        elif color_detect(img, '白色.npy'):
            mvfile([i], '白色')
        else:
            print(i)
            print('未知颜色')

if __name__ == '__main__':
    img = cv2.imread('750(9).jpg')
    print(color_detect(img, '粉红.npy'))
