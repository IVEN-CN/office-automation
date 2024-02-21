"""将不同颜色的色卡图片分到新的文件夹，文件夹用颜色命名"""
from math import e
import os
import shutil
import time
import cv2
import numpy as np
import os
import re

# roll = np.ones([500, 500])


def get_file_path(file_dir: str) -> list:
    """获取相对路径下文件夹的所有文件的路径
    file_dir: 文件夹路径"""
    path_list = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            path_list.append(os.path.join(root, file))
    return path_list


def color_detect(img_: np.ndarray,      # eara.npy是平铺识别面积，eara0.npy是模特识别面积
                 colorfile: str,
                 areafile: str='area.npy') -> bool:
    try:
        range_ = np.load(colorfile)
        area = np.load(areafile)
    except:
        return False
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
    color = ['白色', 
             '黑色', 
             '浅紫', 
             '杏色', 
             '浅蓝', 
             '浅绿', 
             '粉红', 
             '浅黄', 
             '红色',
             '黄色',
             '深灰',
             '卡其',
             '虾玉色',
             '雾霾蓝',
             '天蓝',
             '水蓝',
             '橙色',
             '克莱因蓝',
             '草绿'
             '紫色',
             '啡色',
             '彩兰',
             '花灰'
             
            ]
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


def main(*num, path, area):
    
    for i in num:       # 检查参数是否正确
        if '(' not in i or ')' not in i:
            raise ValueError('参数错误,main参数应该是类似(1)的形式')
        
    file_path = get_file_path(path)
    for i in file_path:
        try:
            match = re.search(r'\((\d+)\)', i)
            if match is not None:
                num_ = match.group(1)
            else:
                raise TypeError('没有匹配到括号内的数字')
            if '主图' in i or '细节' in i or '详情页' in i or num_ in num:
                file_path.remove(i)
        except:
            pass
        
    mkdir(path)     # 创建颜色文件夹

    for i in file_path:
        img = cv2.imread(i)
        if img is None:
            continue
        if color_detect(img, '卡其.npy', areafile=area):
            mvfile([i], os.path.join(path, '卡其'))
        elif color_detect(img, '杏色.npy', areafile=area):
            mvfile([i], os.path.join(path, '杏色'))
        elif color_detect(img, '浅蓝.npy', areafile=area):
            mvfile([i], os.path.join(path, '浅蓝'))
        elif color_detect(img, '浅绿.npy', areafile=area):
            mvfile([i], os.path.join(path, '浅绿'))
        elif color_detect(img, '浅黄.npy', areafile=area):
            mvfile([i], os.path.join(path, '浅黄'))
        elif color_detect(img, '虾玉色.npy', areafile=area):
            mvfile([i], os.path.join(path, '虾玉色'))
        elif color_detect(img, '粉红.npy', areafile=area):
            mvfile([i], os.path.join(path, '粉红'))
        elif color_detect(img, '黑色.npy', areafile=area):
            mvfile([i], os.path.join(path, '黑色'))
        elif color_detect(img, '浅紫.npy', areafile=area):
            mvfile([i], os.path.join(path, '浅紫'))
        elif color_detect(img, '红色.npy', areafile=area):
            mvfile([i], os.path.join(path, '红色'))
        elif color_detect(img, '黄色.npy', areafile=area):
            mvfile([i], os.path.join(path, '黄色'))
        elif color_detect(img, '深灰.npy', areafile=area):
            mvfile([i], os.path.join(path, '深灰'))
        elif color_detect(img, '雾霾蓝.npy', areafile=area):
            mvfile([i], os.path.join(path, '雾霾蓝'))
        elif color_detect(img,'紫色.npy', areafile=area):
            mvfile([i], os.path.join(path, '紫色'))
        elif color_detect(img,'啡色.npy', areafile=area):
            mvfile([i], os.path.join(path, '啡色'))
        elif color_detect(img,'彩兰.npy', areafile=area):
            mvfile([i], os.path.join(path, '彩兰'))
        elif color_detect(img, '花灰.npy', areafile=area):
            mvfile([i], os.path.join(path, '花灰'))
        elif color_detect(img, '白色.npy', areafile=area):
            mvfile([i], os.path.join(path, '白色'))
        else:
            print(i)
            print('未知颜色')
    delete_empty_folders(path)


def main_more_color(path_: str, area):
    """识别多种颜色
    path_: 文件夹路径
    area: 面积文件路径"""
    dict_ = {}
    path = get_file_path(path_)
    for file_path in path:
        img = cv2.imread(file_path)
        if img is None:
            continue

        dict_[file_path] = []

        # region 对于童装套装的颜色识别
        if color_detect(img, '草绿.npy', areafile=area) and len(dict_[file_path]) < 3:
            dict_[file_path].append('草绿')
        if color_detect(img, '黑色.npy', areafile=area) and len(dict_[file_path]) < 3:
            dict_[file_path].append('黑色')
        if color_detect(img, '浅紫.npy', areafile=area) and len(dict_[file_path]) < 3:
            dict_[file_path].append('浅紫')
        if color_detect(img, '红色.npy', areafile=area) and len(dict_[file_path]) < 3:
            dict_[file_path].append('红色')
        if color_detect(img, '黄色.npy', areafile=area) and len(dict_[file_path]) < 3:
            dict_[file_path].append('黄色')
        if color_detect(img, '天蓝.npy', areafile=area) and len(dict_[file_path]) < 3:
            dict_[file_path].append('天蓝')
        if color_detect(img, '水蓝.npy', areafile=area) and len(dict_[file_path]) < 3:
            dict_[file_path].append('水蓝')
        if color_detect(img, '橙色.npy', areafile=area) and len(dict_[file_path]) < 3:
            dict_[file_path].append('橙色')
        if color_detect(img, '克莱因蓝.npy', areafile=area) and len(dict_[file_path]) < 3:
            dict_[file_path].append('克莱因蓝')
        if color_detect(img, '粉红.npy', areafile=area) and len(dict_[file_path]) < 3:
            dict_[file_path].append('粉红')
        if color_detect(img, '白色.npy', areafile=area) and len(dict_[file_path]) < 3:
            dict_[file_path].append('白色')
        # endregion
            
        class_name: str = ''
        for index, i in enumerate(dict_[file_path]):
            class_name += i
            if index != len(dict_[file_path]) - 1:
                class_name += '+'
        try:
            os.mkdir(os.path.join(path_, class_name))
        except FileExistsError:
            pass
        shutil.move(file_path, os.path.join(path_, class_name))
            

if __name__ == '__main__':
    main(path=r'D:\42male2-5\S255', area='area1.npy')  # eara.npy是平铺识别面积，eara0.npy是模特识别面积
    # print(color_detect(cv2.imread(r'D:\OA\U096\1000(6).jpg'), '黄色.npy', 'area1.npy'))
    # print(main_more_color(r'D:\code_python\office automation\test', 'area1.npy'))
