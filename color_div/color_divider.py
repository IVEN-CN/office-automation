"""将不同颜色的色卡图片分到新的文件夹，文件夹用颜色命名"""
import os
import cv2
import numpy as np
import os
import re

# roll = np.ones([500, 500])


def get_file_path(file_dir) -> list:
    """获取相对路径下文件夹的所有文件的路径
    file_dir: 文件夹路径"""
    path_list = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            path_list.append(os.path.join(root, file))
    return path_list


def color_detect(img_: np.ndarray,      # eara.npy是平铺识别面积，eara0.npy是模特识别面积
                 colorfile,
                 ereafile='area.npy') -> bool:
    range_ = np.load(colorfile)
    area = np.load(ereafile)
    lower = range_[0]
    upper = range_[1]
    hsv = cv2.cvtColor(img_, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)
    # contours是轮廓集，hierarchy是轮廓属性
    contours, hierarchy = cv2.findContours(mask,  # 二值图像
                                           cv2.RETR_TREE,  # 轮廓检索模式
                                           cv2.CHAIN_APPROX_SIMPLE)  # 轮廓近似方法

    for contour in contours:
        # 对每个轮廓进行矩形拟合
        x, y, w, h = cv2.boundingRect(contour)
        brcnt = np.array([[[x, y]], [[x + w, y]], [[x + w, y + h]], [[x, y + h]]])
        if w * h >= area:
            return True
    return False


def mkdir(path):
    """创建文件夹"""
    color = ['白色', '黑色', '浅紫', '杏色', '浅蓝', '浅绿', '粉红', '浅黄']
    for i in color:
        try:
            os.mkdir(os.path.join(path, i))
        except FileExistsError:
            pass


def delete_empty_folders(folder_path):
    """删除空文件夹"""
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)


def mvfile(path: list, target):
    """移动文件"""
    for i in path:
        os.system(f'move {i} {target}')


def main(*num, path, erea):
    
    for i in num:       # 检查参数是否正确
        if '(' not in i or ')' not in i:
            raise ValueError('参数错误,main参数应该是类似(1)的形式')
        
    file_path = get_file_path(path)
    for i in file_path:
        try:
            num_ = f'({re.search(r'\((\d+)\)', i).group(1)})'       # num_ = '(1)'  (类似)
            if '主图' in i or '细节' in i or '详情页' in i or num in num_:
                file_path.remove(i)
        except:
            pass
        
    mkdir(path)     # 创建颜色文件夹

    for i in file_path:
        img = cv2.imread(i)
        if img is None:
            continue
        if color_detect(img, '杏色.npy', ereafile=erea):
            mvfile([i], os.path.join(path, '杏色'))
        elif color_detect(img, '浅蓝.npy', ereafile=erea):
            mvfile([i], os.path.join(path, '浅蓝'))
        elif color_detect(img, '浅绿.npy', ereafile=erea):
            mvfile([i], os.path.join(path, '浅绿'))
        elif color_detect(img, '浅黄.npy', ereafile=erea):
            mvfile([i], os.path.join(path, '浅黄'))
        elif color_detect(img, '粉红.npy', ereafile=erea):
            mvfile([i], os.path.join(path, '粉红'))
        elif color_detect(img, '黑色.npy', ereafile=erea):
            mvfile([i], os.path.join(path, '黑色'))
        elif color_detect(img, '白色.npy', ereafile=erea):
            mvfile([i], os.path.join(path, '白色'))
        elif color_detect(img, '浅紫.npy', ereafile=erea):
            mvfile([i], os.path.join(path, '浅紫'))
        else:
            print(i)
            print('未知颜色')
    delete_empty_folders(path)


if __name__ == '__main__':
    main(path='D:\\41tm\\KC-41-XOU173', erea='area.npy')  # eara.npy是平铺识别面积，eara0.npy是模特识别面积
    # print(color_detect(cv2.imread('D:\\DIV\\KC-41-XOU145\\750X1000\\1000(7).jpg'), '粉红.npy', 'area.npy'))
