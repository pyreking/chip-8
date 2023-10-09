import tkinter as tk
from tkinter import filedialog

class Options:
    OPEN = 0
    PAUSE = 1
    EXIT = 2

class Chip8Menu(tk.Menu):
    PAUSE_LABELS = ["Pause", "Unpause"]

    def __init__(self, parent, cpu, step):
        tk.Menu.__init__(self, parent, tearoff = False)
        self.parent = parent
        self.cpu = cpu
        self.step = step

        self.file_menu = tk.Menu(self, tearoff = False)
        self.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.on_open)
        self.file_menu.add_command(label="Pause", command=self.on_pause, state="disabled")
        self.file_menu.add_command(label="Exit", command=self.on_exit)

        parent.config(menu=self)
    
    def on_open(self):
        self.cpu.paused = True

        file_types = [('All files', '*')]
        dialog = filedialog.Open(self, filetypes = file_types)
        filename = dialog.show()

        if filename != '':
            self.cpu.load_rom(filename)
            self.file_menu.entryconfigure(Options.PAUSE, state="active", label=self.PAUSE_LABELS[0])

        self.cpu.paused = False
        self.step()
    
    def on_pause(self):
        self.cpu.paused ^= 1
        idx = self.cpu.paused
        self.file_menu.entryconfig(Options.PAUSE, label=self.PAUSE_LABELS[idx])
        self.step()
    
    def on_exit(self):
        self.parent.destroy()
    
if __name__ == '__main__':
    root = tk.Tk()
    menu = Chip8Menu(root, None, None)

    root.mainloop()