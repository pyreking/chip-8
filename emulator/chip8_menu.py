import tkinter as tk
from tkinter import filedialog

class Chip8Menu(tk.Menu):
    def __init__(self, parent, chip8):
        tk.Menu.__init__(self, parent, tearoff=False)
        self.chip8 = chip8

        file_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.on_open)

        parent.config(menu=self)
    
    def on_open(self):
        self.chip8.comp.paused = True

        file_types = [('All files', '*')]
        dialog = filedialog.Open(self, filetypes = file_types)
        filename = dialog.show()

        if filename != '':
            self.chip8.comp.load_rom(filename)
            self.chip8.step()
        
        self.chip8.comp.paused = False
    
if __name__ == '__main__':
    root = tk.Tk()
    menu = Chip8Menu(root, None)

    root.mainloop()
