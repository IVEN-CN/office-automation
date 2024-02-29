import cv2
import os
from color_div.color_divider import mvfile
import argparse

def ct(_path:str):
    """将详情页图片分割成11张图片
    * _path: 图片所在的文件夹路径"""
    path_lst = os.listdir(_path)
    for i in path_lst:
        if '详情页' in i:
            path = os.path.join(_path, i)
            break
        raise FileNotFoundError('未找到详情页文件夹')
    if '详情页' in path:        # type: ignore
        os.rename(path, path.replace('详情页', 'details'))
        path = path.replace('详情页', 'details')
    img = cv2.imread(path)
    if img is None:
        return None
    
    img1 = img[:652, :]
    img2 = img[652:652+656,:]
    img3 = img[652+656:652+656+1354]
    img4 = img[652+656+1354:652+656+1354+1185]
    img5 = img[652+656+1354+1185:652+656+1354+1185+993]
    img6 = img[652+656+1354+1185+993:652+656+1354+1185+993+1139]
    img7 = img[652+656+1354+1185+993+1139:652+656+1354+1185+993+1139+1170]
    img8 = img[652+656+1354+1185+993+1139+1170:652+656+1354+1185+993+1139+1170+1387]
    img9 = img[652+656+1354+1185+993+1139+1170+1387:652+656+1354+1185+993+1139+1170+1387+1302]
    img10 = img[652+656+1354+1185+993+1139+1170+1387+1302:652+656+1354+1185+993+1139+1170+1387+1302+1338]
    img11 = img[652+656+1354+1185+993+1139+1170+1387+1302+1338:652+656+1354+1185+993+1139+1170+1387+1302+1338+1240+150]

    cv2.imwrite(path.replace('details', '1'), img1)
    cv2.imwrite(path.replace('details', '2'), img2)
    cv2.imwrite(path.replace('details', '3'), img3)
    cv2.imwrite(path.replace('details', '4'), img4)
    cv2.imwrite(path.replace('details', '5'), img5)
    cv2.imwrite(path.replace('details', '6'), img6)
    cv2.imwrite(path.replace('details', '7'), img7)
    cv2.imwrite(path.replace('details', '8'), img8)
    cv2.imwrite(path.replace('details', '9'), img9)
    cv2.imwrite(path.replace('details', '10'), img10)
    cv2.imwrite(path.replace('details', '11'), img11)

    try:
        os.mkdir(os.path.join(os.path.dirname(path), '详情页'))
    except FileExistsError:
        pass
    for i in range(1,12):
        mvfile([path.replace('details', str(i))], os.path.join(os.path.dirname(path), '详情页'))

    os.remove(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, help='图片所在的文件夹路径')
    opts = parser.parse_args()

    ct(opts.path)