from cutter.cut import cut_img as cut
import renamer.main1
import renamer.main2
import shutil
import os
import color_div.color_divider
import re
import os
import random
import time
import stack.stacker

def done(func):             # 装饰器
    def wrapper(*args, **kwargs):
        print('processing...')
        func(*args, **kwargs)
        print('done')
    return wrapper

@done
def main(path, ifcolordiv=True, ifmain=True, ifstack=False, stack_path=None):
    """path：工作路径
    ifcolordiv：是否需要颜色分类
    ifmain:是否对主图操作，即若提供了主图并且主图文件夹已经存在(不对主图操作)则为False，否则为True
    ifstack:是否需要贴图，对于套装图片，需要贴图，对于单件图片，不需要贴图"""
    list_path = renamer.main1.get_file_path(path)
    img1200_path = []
    img_path = []

    if ifstack and stack_path is None:          # 检查参数
        raise ValueError('stack_path is None')

    if ifmain == False:
        list_path = [i for i in list_path if '主图' not in str(i) or 'main' not in str(i)]      # 非主图文件的路径
        main_path = [i for i in list_path if '主图' in str(i) or 'main' in str(i)]              # 主图文件的路径

        for i in main_path:
            k = os.path.dirname(i)
            filename = os.path.basename(i)
            if filename[-3:] in ['jpg', 'png']:
                cut(k, filename)

    for i in list_path:         # 获取1200*800的图片路径
        if '1200' in i:
            img1200_path.append(i)

    if ifstack:                 # 粘贴png
        stack.stacker.paste_png_to_jpg(stack_path, img1200_path[0], test=True)
        for i in img1200_path:
            stack.stacker.paste_png_to_jpg(stack_path,i)
    
    for i in img1200_path:      # 裁剪
        k = os.path.dirname(i)
        filename = os.path.basename(i)  # Extract the file name
        cut(k, filename, elflag=False)

    # 更新list_path
    list_path = renamer.main1.get_file_path(path)
    if ifmain == False:
        list_path = [i for i in list_path if '主图' not in str(i) ]
        list_path = [i for i in list_path if 'main' not in str(i) ]


    for i in list_path:         # 获取所有图片路径
        if '1200' in i or '1000' in i or '800' in i:
            img_path.append(i)

    if ifmain:                  # 主图分类
        # region 将需要分类的图片拷贝到主图文件夹
        # 尝试创建主图文件夹
        try:
            os.mkdir(os.path.join(path, '主图'))
        except FileExistsError:
            pass

        # 将1200图片拷贝到主图文件夹
        try:
            list_random = random.sample(img1200_path, k=5)
            for i in list_random:
                shutil.copy(i, os.path.join(path, '主图'))
                time.sleep(0.1)
        except ValueError:
            for i in img1200_path:
                shutil.copy(i, os.path.join(path, '主图'))
        # endregion
            
        # region 裁剪主图文件夹图片
        path_main = os.path.join(path, '主图')
        main_image_files = renamer.main1.get_file_path(path_main)           # 获取主图文件夹的图片路径
        for i in main_image_files:
            k = os.path.dirname(i)
            filename = os.path.basename(i)                                  # 确定文件名
            cut(k, filename, elflag=True)                                   # 裁剪
        
        # endregion
        
        # 重命名主图文件夹的文件
        renamer.main2.rename2(os.path.join(path, '主图'))

        # region 检查主图的多余文件
        check_path = renamer.main1.get_file_path(os.path.join(path, '主图'))
        list_ = ['1', '2', '3', '4', '5']
        for i in check_path:
            match = re.search(r'\((\d+)\)', i)
            if match:
                num__ = match.group(1)
                if num__ not in list_:
                    os.remove(i)
        # endregion

    if ifcolordiv:          # 颜色分类
        color_div.color_divider.main(path=path, erea='area0.npy')       # 分类模特
        color_div.color_divider.main(path=path, erea='area1.npy')       # 分类衣服
    else:                   # 尺寸分类
        folder_names = ['800X1200', '800X800', '750X1000']
        for folder_name in folder_names:        # 尝试创建文件夹
            folder_path = os.path.join(path, folder_name)
            os.makedirs(folder_path)
        for i in img_path:                      # 将图片分类,并移动到对应文件夹
            if '1200' in i:
                shutil.move(i, os.path.join(path, '800X1200'))
            elif '1000' in i:
                shutil.move(i, os.path.join(path, '750X1000'))
            elif '800' in i:
                shutil.move(i, os.path.join(path, '800X800'))
            else:
                pass


if __name__ == '__main__':
    main(path=r'D:\OA\U064',ifcolordiv=True,ifmain=False)
    