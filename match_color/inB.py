"""录入已经使用的款号进入csv文件"""
import tkinter as tk
import csv

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

    tk.Label(win, text="输入已使用的款号").pack()
    entry = tk.Entry(win)
    entry.pack()
    tk.Button(win, text="录入",command=writein).pack()

    win.mainloop()

def writein():
    with open('已使用.csv', 'a+') as f:
        reader = csv.reader(f)
        lst = [i[0] for i in reader]
        writer = csv.writer(f)
        if entry.get() not in lst:
            writer.writerow([entry.get()])


if __name__ == '__main__':
    ui()