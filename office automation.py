from cutter.cut import cut_img as cut
import renamer.main1
import renamer.main2
import shutil
import os
import color_div.color_divider

def done(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        print('done')
    return wrapper

@done
def main(path):
    list_path = renamer.main1.get_file_path(path)
    img1200_path = []
    img_path = []

    for i in list_path:         # 获取1200*800的图片路径
        if '1200' in i:
            img1200_path.append(i)
    
    for i in img1200_path:      # 裁剪
        cut(i, path, path)

    # 更新list_path
    list_path = renamer.main1.get_file_path(path)

    for i in list_path:         # 获取需要分类的图片路径
        if '800' in i or '1000' in i or '1200' in i:
            img_path.append(i)

    # region 将需要分类的图片线拷贝到主图文件夹
    # 尝试创建主图文件夹
    try:
        os.mkdir(os.path.join(path, '主图'))
    except FileExistsError:
        pass

    # 将图片拷贝到主图文件夹
    for i in img_path:
        shutil.copy(i, os.path.join(path, '主图'))
    # endregion
        
    # 重命名主图文件夹的文件
    renamer.main2.rename2(os.path.join(path, '主图'))

    # 颜色分类
    color_div.color_divider.main(path, 'area0.npy')
    color_div.color_divider.main(path, 'area.npy')

if __name__ == '__main__':
    main('./')