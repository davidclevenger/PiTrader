from tkinter import *

# our root window
root = Tk()

# labels are simple text boxes
label_name = Label(root, text="Username")
label_pass = Label(root, text="Password")

# entries are text user input
entry_name = Entry(root)
entry_pass = Entry(root)

# organizing layout
label_name.grid(row=0, column=0, sticky=E)
label_pass.grid(row=1, column=0, sticky=E)

entry_name.grid(row=0, column=1)
entry_pass.grid(row=1, column=1)

# check box
c = Checkbutton(root, text="Keep me logged in")
c.grid(columnspan=2)

# binding a function to a widget
def hello(event):
    print("yo yo yo pls buy my CD")

def hellohelp(event):
    print("just tap it 4head")

def newproj(event):
    print("new project")

# make a button that calls hello()
button_1 = Button(root, text="hello")
button_1.bind("<Button-1>", hello)
button_1.bind("<Button-2>", hellohelp)

button_1.grid(row=3, columnspan=2)

menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="New Project...", command='newproj')
subMenu.add_command(label="Save", command='save')
subMenu.add_command(label="Save As...", command='saveas')
subMenu.add_separator()
subMenu.add_command(label='Quit', command=root.quit)

root.mainloop()

