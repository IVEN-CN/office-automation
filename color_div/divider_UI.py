from tkinter import *
from color_div.color_divider import main

def main_UI():
    def callback(): 
        path = entry.get()
        main(path)
        
    win = Tk()
    win.title("Color Div main")
    win.geometry("400x300")

    Label(win, text='输入主文件夹路径：').pack()

    entry = Entry(win, width=40)
    entry.pack()

    Button(win, text='确定', command=callback).pack()

    win.mainloop()

if __name__ == '__main__':
    main_UI()