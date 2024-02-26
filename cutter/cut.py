"""将提供的800*1200尺寸的图片居中裁剪成800*800和750*1000"""
import os
import cv2
import re

def cut_img_(path1200:str, path1000:str='./', path800:str='./', elflag:bool=True):
    """将提供的800*1200尺寸的图片居中裁剪成800*800和750*1000
    path1200: 800*1200图片的路径
    path1000: 750*1000图片的路径
    path800: 800*800图片的路径
    elflge: 是否是对主图文件夹进行操作"""

    img = cv2.imread(path1200)
    if img.shape != (1200, 800, 3):
        raise ValueError('图片尺寸不正确')

    # img1 = img[200+15:1000+15, :]       # 800*800   
    img1 = img[200:1000, :]       # 800*800
    img2 = img[100:1100, 25:25+750]     # 750*1000
    match = re.search(r'\((\d+)\)', path1200)
    if match is not None:
        num = match.group(1)
    else:
        raise TypeError('没有匹配到括号内的数字')

    name800 = '800(' + num + ').jpg'
    name1000 = '1000(' + num + ').jpg'

    path1000 = os.path.join(path1000, name1000)
    path800 = os.path.join(path800, name800)

    cv2.imwrite(path1000, img2, [cv2.IMWRITE_JPEG_QUALITY, 99, cv2.IMWRITE_JPEG_OPTIMIZE, 1])
    cv2.imwrite(path800, img1, [cv2.IMWRITE_JPEG_QUALITY, 99, cv2.IMWRITE_JPEG_OPTIMIZE, 1])

    if flag == 1 and elflag:
        newname = newpath.replace('main', '主图')
        os.rename(newpath, newname)

def cut_img(path,filename, elflag=True):
    """path: 图片所在文件夹的路径
       filename: 图片的文件名
       elflag: 是否是对主图文件夹进行操作"""
    global flag, newpath
    flag = 0
    fb_flag = 0

    if '前' in filename:
        newname = filename.replace('前', 'front')
        os.rename(os.path.join(path, filename), os.path.join(path, newname))
        fb_flag = 1
    elif '后' in filename:
        newname = filename.replace('后', 'back')
        os.rename(os.path.join(path, filename), os.path.join(path, newname))
        fb_flag = 1

    if '主图' in path:
        newpath = path.replace('主图', 'main')
        os.rename(path, newpath)
        flag = 1
        _path = os.path.join(newpath, filename)
        cut_img_(_path, newpath, newpath,elflag=elflag)
    else:
        _path = os.path.join(path, filename)
        cut_img_(_path, path, path,elflag=elflag)

    if fb_flag == 1:
        if 'front' in newname:                                                      # type: ignore
            newname = newname.replace('front', '前')                                # type: ignore
            os.rename(os.path.join(path, newname), os.path.join(path, filename))
        elif 'back' in newname:                                                     # type: ignore
            newname = newname.replace('back', '后')                                 # type: ignore
            os.rename(os.path.join(path, newname), os.path.join(path, filename))
def cut_cut(*filename, path):
    """filename: 图片的文件名
       path: 主图文件夹的路径"""
    for i in filename:
        cut_img(path,i)

if __name__ == '__main__':
    cut_cut(
            '1200(1).jpg',
            # '1200(2).jpg',
            # '1200(3).jpg',
            # '1200(4).jpg', 
            '1200(5).jpg',
            path=r'D:\code_python\office_automation\2-26spacious\U258\主图'
            )
