"""将提供的800*1200尺寸的图片居中裁剪成800*800和750*1000"""
import os
import cv2
import re

def cut(path1200:str, path1000:str='./', path800:str='./'):
    """将提供的800*1200尺寸的图片居中裁剪成800*800和750*1000
    path1200: 800*1200图片的路径
    path1000: 750*1000图片的路径
    path800: 800*800图片的路径"""
    img = cv2.imread(path1200)
    h, w, _ = img.shape
    img1 = img[200:1000, :]             # 800*800   
    img2 = img[100:1100, 25:25+750]     # 750*1000
    num = re.search(r'\((\d+)\)', path1200).group(1)  # 取括号内的数字

    name800 = '800(' + num + ').jpg'
    name1000 = '1000(' + num + ').jpg'

    path1000 = os.path.join(path1000, name1000)
    path800 = os.path.join(path800, name800)

    cv2.imwrite(path1000, img2)
    cv2.imwrite(path800, img1)


if __name__ == '__main__':
    cut('./1200(1).jpg')