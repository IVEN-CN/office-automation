from cutter.cut import cut_img as cut
import renamer.main1
import renamer.main2
import shutil
import os
import color_div.color_divider
import re
import os
import random

def done(func):
    def wrapper(*args, **kwargs):
        print('processing...')
        func(*args, **kwargs)
        print('done')
    return wrapper

@done
def main(*num, path, ifcolordiv=True):       # num是不需要移动到主图文件夹的图片序号,类似于(1),(2),(3)
    list_path = renamer.main1.get_file_path(path)
    img1200_path = []
    img_path = []

    for i in list_path:         # 获取1200*800的图片路径
        if '1200' in i:
            img1200_path.append(i)
    
    for i in img1200_path:      # 裁剪
        k = os.path.dirname(i)
        filename = os.path.basename(i)  # Extract the file name
        cut(k, filename, elflag=False)

    # 更新list_path
    list_path = renamer.main1.get_file_path(path)

    # region 将需要分类的图片拷贝到主图文件夹
    # 尝试创建主图文件夹
    try:
        os.mkdir(os.path.join(path, '主图'))
    except FileExistsError:
        pass

    # 将1200图片拷贝到主图文件夹
    for i in random.choices(img1200_path, k=5):
        shutil.copy(i, os.path.join(path, '主图'))
    # endregion
        
    # region 裁剪主图文件夹图片
    path_main = os.path.join(path, '主图')
    main_image_files = renamer.main1.get_file_path(path_main)           # 获取主图文件夹的图片路径
    for i in main_image_files:
        k = os.path.dirname(i)
        filename = os.path.basename(i)                                  # 确定文件名
        cut(k, filename, elflag=True)                                  # 裁剪
        
    # endregion
        
    # 重命名主图文件夹的文件
    renamer.main2.rename2(os.path.join(path, '主图'))

    # region 检查主图的多余文件
    check_path = renamer.main1.get_file_path(os.path.join(path, '主图'))
    list_ = ['1', '2', '3', '4', '5']
    for i in check_path:
        num__ = re.search(r'\((\d+)\)', i).group(1)
        if num__ not in list_:
            os.remove(i)
    # endregion

    if ifcolordiv:       # 颜色分类
        color_div.color_divider.main(path=path, erea='area0.npy')
        color_div.color_divider.main(path=path, erea='area1.npy')
    else:               # 尺寸分类
        folder_names = ['800X1200', '800X800', '750X1000']
        for folder_name in folder_names:
            folder_path = os.path.join(path, folder_name)
            os.makedirs(folder_path)
        for i in img_path:
            if '1200' in i:
                shutil.move(i, os.path.join(path, '800X1200'))
            elif '1000' in i:
                shutil.move(i, os.path.join(path, '750X1000'))
            elif '800' in i:
                shutil.move(i, os.path.join(path, '800X800'))
            else:
                pass


if __name__ == '__main__':
    main(path=r'D:\41shortPure',ifcolordiv=False)