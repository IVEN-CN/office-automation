from tkinter import *
from init import main

def init_UI():
    win = Tk()
    win.title("Color Div init")
    win.geometry("400x300")

    def callback():
        path = entry.get()
        main(path)
    # region 创建控件
    Label(win, text='输入图片路径：').pack()

    entry = Entry(win, width=40)
    entry.pack()

    Button(win, text='确定', command=callback).pack()
    # endregion

    win.mainloop()

if __name__ == '__main__':
    init_UI()