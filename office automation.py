from cutter.cut import cut_img as cut
import renamer.main1
import renamer.main2
import shutil
import os
import color_div.color_divider
import re

def done(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        print('done')
    return wrapper

@done
def main(*num, path):       # num是不需要移动到主图文件夹的图片序号,类似于(1),(2),(3)
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

    for i in list_path:         # 获取需拷贝到主图的图片路径
        try:
            # 获取括号内数字
            match = re.search(r'\((\d+)\)', i)
            if match is not None:
                num_ = match.group(1)
            else:
                raise TypeError('没有匹配到括号内的数字')
            if '800' in i or '1000' in i or '1200' in i or num_ not in num:
                img_path.append(i)
        except:
            pass

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
    color_div.color_divider.main(path=path, erea='area0.npy')
    color_div.color_divider.main(path=path, erea='area.npy')

if __name__ == '__main__':
    main(path='D:\\41short\\KC-41-XOU174')