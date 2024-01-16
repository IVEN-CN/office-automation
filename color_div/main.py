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
                 colorfile,
                 ereafile='area.npy') -> bool:
    range_ = np.load(colorfile)
    area = np.load(ereafile)
    lower = range_[0]
    upper = range_[1]
    hsv = cv2.cvtColor(img_, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)
    # contours是轮廓集，hierarchy是轮廓属性
    contours, hierarchy = cv2.findContours(mask,                    # 二值图像
                                            cv2.RETR_TREE,           # 轮廓检索模式
                                            cv2.CHAIN_APPROX_SIMPLE) # 轮廓近似方法
    
    for contour in contours:
        # 对每个轮廓进行矩形拟合
        x, y, w, h = cv2.boundingRect(contour)
        brcnt = np.array([[[x, y]], [[x + w, y]], [[x + w, y + h]], [[x, y + h]]])
        if w * h >= area:
            return True
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

def main(path):
    file_path = get_file_path(path)
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
    main('./U007')
