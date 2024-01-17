from tkinter import *
from init_UI import init_UI
from main_UI import main_UI

def UI():      
    win = Tk()
    win.title("Color Div")
    win.geometry("400x300")

    Label(win, text='首次运行需要进行初始化').pack()

    Button(win, text='开始分类', command=main_UI).pack()
    Button(win, text='初始化', command=init_UI).pack()

    win.mainloop()

if __name__ == '__main__':
    UI()