import tkinter as tk
import color_div.init
import office_automation
import cutter.cut
import office_automation


def main0win():
    win = tk.Tk()
    win.title('初始化')
    
    tk.Label(win, text='首先备份！！！').pack()
    tk.Label(win, text='是否需要颜色分类？').pack()
    tk.Button(win, text='是', command=mainwin).pack()
    tk.Button(win, text='否', command=main1win).pack()

    win.mainloop()


def main1win():
    def win1_callback():
        office_automation.main(path=entry.get(), ifcolordiv=False)
    win = tk.Tk()
    win.title('自动化')

    tk.Label(win, text='输入文件夹路径，包含所有1200尺寸图片').pack()

    entry = tk.Entry(win)
    entry.pack()

    tk.Button(win, text='确定', command=win1_callback).pack()

    win.mainloop()
def mainwin():
    win = tk.Tk()
    win.title('自动化')
    win.geometry('500x200')

    tk.Label(win, text='准备好对应颜色的1200尺寸的平铺图，以及需要分类的模特图(无需裁剪的)').pack()
    tk.Button(win, text='第一步', command=firstwin).pack()

    tk.Label(win, text='在文件夹中提供1200尺寸的所有颜色平铺图已经不裁剪的模特图(1.jpg)').pack()
    tk.Button(win, text='第二步', command=secondwin).pack()

    tk.Label(win, text='在主图文件夹准备2张1200尺寸的主图的模特图').pack()
    tk.Button(win, text='第三步', command=thirdwin).pack()

    win.mainloop()


def firstwin():
    def first_callback():
        color_div.init.main(entry.get())
    win = tk.Tk()
    win.title('第一步')
    win.geometry('400x100')

    tk.Label(win, text=r'请输入路径:(D:\41short\KC-41-XOU128\1200(6).jpg)').pack()
    entry = tk.Entry(win)
    entry.pack()
    tk.Button(win, text='确定', command=first_callback).pack()

    win.mainloop()


def secondwin():
    def second_callback():
        office_automation.main(path=entry.get())
    win = tk.Tk()
    win.title('第二步')
    win.geometry('400x100')

    tk.Label(win, text='记得检查主图文件夹,删除不需要的图片！').pack()
    tk.Label(win, text=r'请输入路径:(D:\41short\KC-41-XOU128)').pack()
    entry = tk.Entry(win)
    entry.pack()
    tk.Button(win, text='确定', command=second_callback).pack()

    win.mainloop()


def thirdwin():
    def third_callback():
        cutter.cut.cut_cut(entry1.get(), entry2.get(),path=entry.get())
    win = tk.Tk()
    win.title('第三步')
    win.geometry('400x150')

    tk.Label(win, text=r'请输入路径:(D:\41short\KC-41-XOU128)').pack()
    entry = tk.Entry(win)
    entry.pack()

    tk.Label(win, text='请输入需要裁剪的模特图文件名').pack()
    entry1 = tk.Entry(win)
    entry1.pack()
    entry2 = tk.Entry(win)
    entry2.pack()

    tk.Button(win, text='确定', command=third_callback).pack()

    win.mainloop()


if __name__ == '__main__':
    main0win()

