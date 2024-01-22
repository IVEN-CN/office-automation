from tkinter import *
import cv2
import os
from skimage.metrics import structural_similarity


def get_file_path(file_dir) -> list:
    """获取相对路径下文件夹的所有文件的路径
    file_dir: 文件夹路径"""
    file_path = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            file_path.append(os.path.join(root, file))
    return file_path


def compare_img(img1_path:str, img2_path:str) -> float:
    """比较两张图片的相似度
    img1_path: 图片1的路径
    img2_path: 图片模板的路径"""
    lt0 = [".jpg", ".png", ".jpeg"]
    if img1_path[-4:] not in lt0 or img2_path[-4:] not in lt0:
        return 0
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    if img1.shape != img2.shape:
        height, width = img1.shape[:2]
        img2 = cv2.resize(img2, (width, height), interpolation=cv2.INTER_CUBIC)

    # 将图像转换为灰度
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 计算SSIM,score越大相似度越高，diff越小
    (score, diff) = structural_similarity(gray1, gray2, full=True)
    print(f"图像SSIM:{score}")
    return score


def main(dir, img2_path):     # 绝对路径
    """比较文件夹下所有图片与模板图片的相似度
    dir: 文件夹路径
    img2_path: 图片模板的路径"""
    list_img = []
    file_path = get_file_path(dir)
    similarity = 0  # Initialize similarity variable
    for i in file_path:
        similarity = compare_img(i, img2_path)
        if similarity > 0.7:
            print(f'路径为{i}的图片与模板图片的相似度为{similarity}')
            list_img.append(i)
    return list_img, similarity


def command():
    dir = entry1.get()
    img2_path = entry2.get()
    list_img, similarity = main(dir, img2_path)
    for i in list_img:
        lb_v.config(text=f'路径为{i}的图片与模板图片的相似度为{similarity}')

win = Tk()
win.title('图片匹配')
win.geometry('500x500')

Label(win, text='输入磁盘（例如D:\\)必须是英文', font=('宋体', 20)).pack()
entry1 = Entry(win, font=('宋体', 20))
entry1.pack()

Label(win, text='输入图片模板的路径', font=('宋体', 20)).pack()
entry2 = Entry(win, font=('宋体', 20))
entry2.pack()

Button(win, text='开始匹配', font=('宋体', 20), command=command).pack()

lb_v = Label(win)
lb_v.pack()

win.mainloop()