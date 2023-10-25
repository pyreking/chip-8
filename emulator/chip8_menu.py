"""
chip8_menu.py:

Implements a menu bar for the CHIP-8 interpreter.

The test program creates a new menu bar and binds it to a window.
"""
import tkinter as tk
import tkinter.messagebox as messagebox
import datetime
import pickle
import gzip
from tkinter import filedialog
from pathlib import Path
import os.path

class FileOptions:
    """A list of options for the menu bar.

    An enum class that reperesents the options availiable for the menu bar.
    """
    OPEN = 0
    PAUSE = 1
    SAVE = 2
    LOAD = 3
    REWIND = 4
    FAST_FORWARD = 5
    EXIT = 6

class Chip8Menu(tk.Menu):
    """A menu bar for the CHIP-8 interpreter.

    Attributes:
        parent: The parent Tk window for the menu bar.
        cpu: A virtual CHIP-8 CPU.
        step: A function that cycles the virtual CHIP-8 CPU.
        file_menu: A file menu for the menu bar.
    """

    # The labels for the pause option.
    PAUSE_LABELS = ["Pause", "Unpause"]

    def __init__(self, parent, cpu, step):
        """Initializes the menu bar for the emulator.

        Args:
            parent (tkinter.Tk): The parent window for the menu bar.
            cpu (CPU): A virtual CHIP-8 CPU.
            step (function): A function that cycles the virtual CHIP-8 CPU.
        """
        # Initialize the tkinter Menu.
        tk.Menu.__init__(self, parent, tearoff=False)

        # Set up instance variables.
        self.parent = parent
        self.cpu = cpu
        self.step = step

        # Create a file menu.
        self.file_menu = tk.Menu(self, tearoff=False)
        self.save_menu = tk.Menu(self, tearoff=False)
        self.load_menu = tk.Menu(self, tearoff=False)

        self.add_cascade(label="File", menu=self.file_menu)

        # Add open option.
        self.file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.on_open)

        # Add pause option.
        self.file_menu.add_command(
            label="Pause", command=self.on_pause, accelerator="Ctrl+P", state="disabled")
        
        self.file_menu.add_cascade(label="Save State", menu = self.save_menu, state="disabled")

        for i in range(1, 6):
            func = lambda i0 = i: self.on_save(slot = i0) 
            self.save_menu.add_command(label=f"{i}. <empty>", command=func)

        self.file_menu.add_cascade(label="Load State", menu = self.load_menu, state="disabled")

        for i in range(1, 6):
            func = lambda i0 = i: self.on_load(slot = i0) 
            self.load_menu.add_command(label=f"{i}. <empty>", command=func)
        
        self.file_menu.add_command(
            label="Rewind", command=self.on_rewind, accelerator="J", state="disabled")
        
        self.file_menu.add_command(
            label="Fast Forward", command=self.on_fast_forward, accelerator="K", state="disabled")

        # Add exit option.
        self.file_menu.add_command(label="Exit", accelerator="Ctrl+W", command=self.on_exit)

        # Set up keyboard shortcuts.
        parent.bind("<Control-o>", self.on_open)
        parent.bind("<Control-p>", self.on_pause)
        parent.bind("<Control-s>", self.on_save)
        parent.bind("<Control-l>", self.on_load)
        parent.bind("<KeyPress-j>", self.on_rewind)
        parent.bind("<KeyPress-k>", self.on_fast_forward)
        parent.bind("<KeyRelease-j>", self.off_rewind)
        parent.bind("<KeyRelease-k>", self.off_fast_forward)
        parent.bind("<Control-w>", self.on_exit)

    def on_rewind(self, event = None):
        if len(self.cpu.rewind_buffer) > 0:
            self.cpu.paused = True
            pickle_bytes = gzip.decompress(self.cpu.rewind_buffer.pop())
            state = pickle.loads(pickle_bytes)
            self.cpu.load_state(state)
    
    def on_fast_forward(self, event = None):
        self.cpu.speed = 30
    
    def off_fast_forward(self, event = None):
        self.cpu.speed = 10
    
    def off_rewind(self, event = None):
        self.cpu.paused = False
        self.step()

    def on_open(self, event = None):
        """Fires when the open option is selected from the menu.

        This function is fired when the open option
        is selected from the menu. Loads a ROM from the
        file browser.

        Returns:
            void
        """
        # Pause the CPU.
        self.cpu.paused = True

        # Accept all file types.
        file_types = [('All files', '*')]

        # Open the file browser.
        dialog = filedialog.Open(self, filetypes=file_types)

        # Get the filename of the ROM.
        filename = dialog.show()

        if filename != '':
            game_name = Path(filename).name
            # Load the ROM into memory.
            self.cpu.load_rom(filename)
            # Enable the pause option in the menu.
            self.file_menu.entryconfigure(
                FileOptions.PAUSE, state="active", label=self.PAUSE_LABELS[0])
            self.file_menu.entryconfigure(FileOptions.SAVE, state = "active")
            self.file_menu.entryconfigure(FileOptions.LOAD, state = "active")
            self.file_menu.entryconfigure(FileOptions.REWIND, state = "active")
            self.file_menu.entryconfigure(FileOptions.FAST_FORWARD, state = "active")
            self.parent.title(game_name)
            self.update_save_slot_labels(game_name)

        # Unpause the CPU.
        self.cpu.paused = False

        # Cycle the CPU.
        self.step()
    
    def update_save_slot_labels(self, game_name):
        save_files = [game_name + f"-{i}.sav" for i in range(1, 6)]

        for idx, file in enumerate(save_files):
            path = f"../savs/{file}"
            label_text = "<empy>"

            if os.path.isfile(path):
                creation_date = os.path.getctime(path)
                label_text = datetime.datetime.fromtimestamp(creation_date).strftime('%Y-%m-%d %H:%M:%S')
            
            self.save_menu.entryconfig(idx, label = label_text)
            self.load_menu.entryconfig(idx, label = label_text)

    def on_save(self, event = None, slot = 1):
        creation_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        path = "../savs/" + self.parent.title() + f"-{slot}.sav"
        state = self.cpu.save_state()

        self.save_menu.entryconfigure(slot - 1, label = creation_date)
        self.load_menu.entryconfigure(slot - 1, label = creation_date)
        
        with open(path, "wb") as file:
            pickle.dump(state, file)
    
    def on_load(self, event = None, slot = 1):
        self.cpu.paused = True

        # Get the filename of the ROM.
        path = "../savs/" + self.parent.title() + f"-{slot}.sav"

        try:
            with open(path, "rb") as file:
                state = pickle.load(file)
                self.cpu.load_state(state, clear_buffer = True)
        except FileNotFoundError:
            self.cpu.paused = False
            messagebox.showerror("Save file not found", f"No save file found in slot {slot}.")
            self.step()

        # Enable the pause option in the menu.
        self.file_menu.entryconfigure(
                FileOptions.PAUSE, state="active", label=self.PAUSE_LABELS[0])
        self.file_menu.entryconfigure(FileOptions.SAVE, state = "active")

        # Unpause the CPU.
        self.cpu.paused = False

    def on_pause(self, event = None):
        """Fires when the pause option is selected from the menu.

        This function is fired when the pause option
        is selected from the menu. Pauses the CPU when it is running.
        Otherwise, it unpauses the CPU.

        Returns:
            void
        """
        # Pause or unpause the CPU.
        self.cpu.paused ^= 1

        # Get the pause status from the CPU.
        idx = self.cpu.paused

        # Update the pause menu option with the correct label.
        self.file_menu.entryconfig(FileOptions.PAUSE, label=self.PAUSE_LABELS[idx])

        # Cycle the CPU if it is not paused.
        self.step()

    def on_exit(self, event = None):
        """Fires when the exit option is selected from the menu.

        This function is fired when the exit option
        is selected from the menu. Closes the emulator.

        Returns:
            void
        """
        # Close the emulator.
        self.parent.destroy()

if __name__ == '__main__':
    # A test program for the menu bar.
    #
    # Adds a menu bar to a new window.

    # Create a new window.
    root = tk.Tk()

    # Create a new menu bar.
    menu = Chip8Menu(root, None, None)

    # Add the menu bar to the parent window.
    root.config(menu=menu)

    # Start the main GUI loop.
    root.mainloop()
