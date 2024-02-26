from cutter.cut import cut_img as cut
import renamer.main1
import renamer.main2
import shutil
import os
import color_div.color_divider
import re
import random
import time
import argparse
import stack.stacker

class PathLike(str):
    pass

def done(func):             # 装饰器
    def wrapper(*args, **kwargs):
        print('processing...')
        func(*args, **kwargs)
        print('done')
    return wrapper

@done
def main(path: PathLike, position: tuple[int, int] | None=None, ifcolordiv=True, ifmain=True, ifstack=False, stack_path=None, morecolor=False):
    """path：工作路径
    ifcolordiv：是否需要颜色分类
    ifmain:是否对主图操作，即若提供了主图并且主图文件夹已经存在(不对主图操作)则为False，否则为True
    ifstack:是否需要贴图，对于套装图片，需要贴图，对于单件图片，不需要贴图"""
    list_path = renamer.main1.get_file_path(path)
    list_path = [i for i in list_path if 'jpg' in i or 'png' in i or 'jpeg' in i]  # 获取所有图片路径
    img1200_path = []
    img_path = []

    if ifstack and stack_path is None and position is None:          # 检查参数
        raise ValueError('stack_path is None')

    if ifmain == False:
        main_path = [i for i in list_path if '主图' in str(i) or 'main' in str(i)]              # 主图文件的路径
        list_path = [i for i in list_path if '主图' not in str(i) and 'main' not in str(i)]      # 非主图文件的路径

        for i in main_path:
            k = os.path.dirname(i)
            filename = os.path.basename(i)
            if filename[-3:] in ['jpg', 'png']:
                cut(k, filename)

    for i in list_path:         # 获取1200*800的图片路径
        if '1200' in i:
            img1200_path.append(i)

    if ifstack:                 # 粘贴png
        stack.stacker.paste_png_to_jpg(stack_path, img1200_path[0], position=position, test=True) # type: ignore
        for i in img1200_path:
            stack.stacker.paste_png_to_jpg(stack_path,i, position=position, test=False) # type: ignore
    
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
        if morecolor == False:
            color_div.color_divider.main(path=path, area='area0.npy')       # 分类模特
            color_div.color_divider.main(path=path, area='area1.npy')       # 分类衣服
        else:
            color_div.color_divider.main_more_color(path_=path, area='area1.npy')       # 分类多颜色衣服
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

    # 读取主图文件夹所有图片的路径
    main_path = renamer.main1.get_file_path(os.path.join(path, '主图'))
    main_path = [i for i in main_path if '800'in i]
    main_path = random.sample(main_path, k=2)
    # 将文件复制到path路径
    for num, i in enumerate(main_path):
        shutil.copy(i, path)
        file_path = os.path.join(path, os.path.basename(i))
        # 重命名文件
        os.rename(file_path, os.path.join(path, f'主图({num+1}).jpg'))


if __name__ == '__main__':
    arg = argparse.ArgumentParser()
    arg.add_argument('--path', type=str, help='工作路径')
    arg.add_argument('--xposition', type=int, help='粘贴的png的x位置')
    arg.add_argument('--yposition', type=int, help='粘贴的png的y位置')
    arg.add_argument('--ifcolordiv', default='true', type=str, help='是否需要颜色分类')
    arg.add_argument('--ifmain', default='true', type=str, help='是否对主图操作，即若提供了主图并且主图文件夹已经存在(不对主图操作)则为False，否则为True')
    arg.add_argument('--morecolor', default='false', type=str, help='是否是多件衣服图片')
    arg.add_argument('--ifstack', default='false', type=str, help='是否需要贴图png')
    arg.add_argument('--stack_path', type=str, help='粘贴的png的路径')
    opt = arg.parse_args()

    # region 参数处理
    if opt.ifcolordiv == 'true':
        opt.ifcolordiv = True
    elif opt.ifcolordiv == 'false':
        opt.ifcolordiv = False
    else:
        raise ValueError('ifcolordiv is unexpected value,it should be true or false')
    
    if opt.ifmain == 'true':
        opt.ifmain = True
    elif opt.ifmain == 'false':
        opt.ifmain = False
    else:
        raise ValueError('ifcolordiv is unexpected value,it should be true or false')
    
    if opt.morecolor == 'true':
        opt.morecolor = True
    elif opt.morecolor == 'false':
        opt.morecolor = False
    else:
        raise ValueError('ifcolordiv is unexpected value,it should be true or false')

    if opt.ifstack == 'true':
        opt.ifstack = True
    elif opt.ifstack == 'false':
        opt.ifstack = False
    else:
        raise ValueError('ifcolordiv is unexpected value,it should be true or false')
    # endregion

    main(path=opt.path, position=(opt.xposition,opt.yposition), ifcolordiv=opt.ifcolordiv, ifmain=opt.ifmain, morecolor=opt.morecolor, ifstack=opt.ifstack, stack_path=opt.stack_path) # type: ignore