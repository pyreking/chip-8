import tkinter as tk
from tkinter import filedialog

class Chip8Menu(tk.Menu):
    def __init__(self, parent, cpu, step):
        tk.Menu.__init__(self, parent, tearoff=False)
        self.cpu = cpu
        self.step = step

        file_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.on_open)

        parent.config(menu=self)
    
    def on_open(self):
        self.cpu.paused = True

        file_types = [('All files', '*')]
        dialog = filedialog.Open(self, filetypes = file_types)
        filename = dialog.show()

        if filename != '':
            self.cpu.load_rom(filename)
            self.cpu.paused = False
            self.step()
        
        self.cpu.paused = False
    
if __name__ == '__main__':
    root = tk.Tk()
    menu = Chip8Menu(root, None, None)

    root.mainloop()
