"""将过审的款号通过cnn识别图片中的文字，将识别的文字存储到csv文件中，作为已过审的款号数据库"""
import os
import tkinter as tk
import csv
from openpyxl import load_workbook
import win32com.client as win32
import zipfile
import cv2
import easyocr
import shutil

def writein():
    with open('已通过.csv', 'a+') as f:
        reader = csv.reader(f)
        lst = [i[0] for i in reader]
        writer = csv.writer(f)
        if entry.get() not in lst:
            writer.writerow([entry.get()])

def ui():
    global entry
    win = tk.Tk()
    win.title("InA UI")

    # 获取屏幕宽度和高度
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    x = int((screen_width / 2) - (250 / 2))
    y = int((screen_height / 2) - (100 / 2))

    win.geometry(f"250x100+{x}+{y-100}")

    tk.Label(win, text="输入已通过的款号").pack()
    entry = tk.Entry(win)
    entry.pack()
    tk.Button(win, text="录入",command=writein).pack()

    win.mainloop()

def xls2xlsx(path:str):
    """将xls文件批量转换为xlsx文件
    * path: 文件夹路径"""
    path_list = os.listdir(path)
    path_list = [i for i in path_list if '否决' not in i]
    e = win32.gencache.EnsureDispatch('Excel.Application')
    e.DisplayAlerts = False  # 禁用警告
    e.EnableEvents = False  # 禁用宏
    for i in path_list:
        if 'xlsm' not in i and 'xlsx' not in i:
            wb = e.Workbooks.Open(os.path.join(path, i))
            wb.SaveAs(os.path.join(path, i+'x'), FileFormat=51)
            wb.Close()
        elif 'xlsx' not in i and 'xlsm' in i:
            # 加载.xlsm文件
            wb = load_workbook(filename=os.path.join(path, i), read_only=False)
            # 保存为.xlsx文件
            filename = i[:-1]+'x'
            wb.save(os.path.join(path, filename))
        else:
            pass
        print(f'{i}转换完成')

reader = easyocr.Reader(['en'], gpu=True)

def detect(_img):
    img = cv2.cvtColor(_img[0:55,:], cv2.COLOR_BGR2GRAY)
    res = reader.readtext(img)
    for (bbox, text, prob) in res:  # bbox:文字框坐标，text:识别的文字，prob:识别的概率
        text = text.replace(' ', '').replace('I', '1').replace('$', 'S').replace('[J', 'U').replace('}', 'K').replace('1J', 'U')
        if prob < 0.001:
            break
        print(f'text:{text},probablity:{prob}')
        return text
    
def deal_img(path:str):
    """在xlsx文件所在文件夹中批量识别xlsx内的图片中的文字
    ----------------
    用于将通过的款号记录进入数据库，方便后期查询
    * path: 文件夹路径"""
    # region 解压图片
    pass_lst = []
    path_list = os.listdir(path)
    path_list = [i for i in path_list if 'xlsx' in i]
    for i in path_list:
        with zipfile.ZipFile(os.path.join(path,i)) as f:        # 解压xlsx文件
            for file in f.namelist():
                if 'xl/media' in file:
                    f.extract(file, path)
                    img_path = os.path.join(path, 'xl/media')
                    path_list = [i for i in os.listdir(img_path)]
    # endregion
                    
    # region 读取图片
                    for i in path_list:
                        img = cv2.imread(os.path.join(img_path, i))
                        text = detect(img)
                        if text is not None:
                            pass_lst.append(text)
                        os.remove(os.path.join(path+'/xl/media', i))
    shutil.rmtree(os.path.join(path, 'xl'))
                    
    # endregion
    
    # region 存储已通过的款号
    with open('已通过.csv', 'a+', newline='') as f:
        writer = csv.writer(f)
        reader_csv = csv.reader(f)
        lst = [i[0] for i in reader_csv]
        for i in pass_lst:
            if i not in lst:
                writer.writerow([i])

def test(path:str):
    file = os.listdir(path)
    for i in file:
        img = cv2.imread(os.path.join(path, i))
        # cv2.namedWindow('test', cv2.WINDOW_NORMAL)
        # cv2.createTrackbar('h1', 'test', 0, img.shape[0], lambda x: None)
        # cv2.createTrackbar('h2', 'test', img.shape[1], img.shape[1], lambda x: None)

        while img is not None:
            # h1 = cv2.getTrackbarPos('h1', 'test')
            # h2 = cv2.getTrackbarPos('h2', 'test')
            # cv2.imshow('test', img[h1:h2,:])        # h1=0 h2=50
            cv2.imshow('test', img[0:55,:])
            cv2.imshow('test1', img)
            if cv2.waitKey(0):
                break

def main(path:str):
    xls2xlsx(path)
    deal_img(path)


if __name__ == '__main__':
    # test(r'D:\code_python\office_automation\match_color\test\xl\media')
    deal_img(r'D:\code_python\office_automation\match_color\test')
    # main(r'D:\code_python\office_automation\match_color\test')