from tkinter import *

def nothing():
    print('just minding my business')

root = Tk()

menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label='File', menu=subMenu)
subMenu.add_command(label='New Project...', command=nothing)

root.mainloop()
