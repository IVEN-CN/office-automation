"""将提供的800*1200尺寸的图片居中裁剪成800*800和750*1000"""
import os
import cv2
import re

def cut_img_(path1200:str, path1000:str='./', path800:str='./', elflag:bool=True):
    """将提供的800*1200尺寸的图片居中裁剪成800*800和750*1000
    path1200: 800*1200图片的路径
    path1000: 750*1000图片的路径
    path800: 800*800图片的路径
    elflge: 是否对主图文件夹进行操作"""

    img = cv2.imread(path1200)
    if img.shape != (1200, 800, 3):
        raise ValueError('图片尺寸不正确')

    img1 = img[200:1000, :]             # 800*800   
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

    cv2.imwrite(path1000, img2)
    cv2.imwrite(path800, img1)

    if flag == 1 and elflag:
        newname = newpath.replace('main', '主图')
        os.rename(newpath, newname)

def cut_img(path,filename, elflag=True):
    global flag, newpath
    flag = 0
    if '主图' in path:
        newpath = path.replace('主图', 'main')
        os.rename(path, newpath)
        flag = 1
        _path = os.path.join(newpath, filename)
        cut_img_(_path, newpath, newpath,elflag=elflag)
    else:
        _path = os.path.join(path, filename)
        cut_img_(_path, path, path,elflag=elflag)

def cut_cut(*filename, path):
    for i in filename:
        cut_img(path,i)

if __name__ == '__main__':
    cut_cut('1200(1).jpg','1200(5).jpg',path=r'D:\41short\KC-41-XOU179\主图')
