#!/usr/bin/env python 
import tkinter as tk 

class Application(tk.Frame): 
    
    def __init__(self, parent, *args, **kwargs):
        
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

#       frame = Frame(master)
#       frame.pack()

        self.prnt = Button(frame, text='Print message', command=self.prnt)
#       self.prnt.pack(side=LEFT)

        self.quit = Button(frame, text='Quit', command=frame.quit)
#       self.quit.pack(side=LEFT)

        # menu bar
        menubar = Menu(parent)
        self.parent.config(menu=menubar)

        # 'File' sub-menu
        subMenu = Menu(menubar)
        menubar.add_cascade(label='File', menu=subMenu)
        subMenu.add_command(label='Load configuration...', command=example)
        subMenu.add_command(label='Save configuration as...', command=example)
        subMenu.add_separator()
        subMenu.add_command(label='quit', command=root.quit)

    def prnt(self):
        print('wow hi it worked xD')

    def example(self):
        print('menu hi hi')

# end class

if __name__ == '__main__':

    root = tk.Tk()
    Application(root).pack(side='top', fill='both', expand=True
    root.title('PiTrader')
    root.mainloop() 

