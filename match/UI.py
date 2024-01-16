from tkinter import *
from main import main

def command():
    dir = entry1.get()
    img2_path = entry2.get()
    list_img, similarity = main(dir, img2_path)
    for i in list_img:
        lb_v.config(text=f'路径为{i}的图片与模板图片的相似度为{similarity}')

win = Tk()
win.title('图片匹配')
win.geometry('500x500')

Label(win, text='输入磁盘（例如D:\)必须是英文', font=('宋体', 20)).pack()
entry1 = Entry(win, font=('宋体', 20))
entry1.pack()

Label(win, text='输入图片模板的路径', font=('宋体', 20)).pack()
entry2 = Entry(win, font=('宋体', 20))
entry2.pack()

Button(win, text='开始匹配', font=('宋体', 20), command=command).pack()

lb_v = Label(win)
lb_v.pack()

win.mainloop()