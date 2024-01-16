from tkinter import *
import main

win = Tk()
win.title("Renamer")
win.geometry("200x100")

# Label
label = Label(win, text="输入文件夹（例如：./U007）")
label.pack()

# Entry
entry = Entry(win)
entry.pack()

# Button
def click():
    if entry.get() == "":
        return None
    main.main(entry.get())

button = Button(win, text="确定", command=click)
button.pack()

win.mainloop()