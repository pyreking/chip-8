from tkinter import filedialog
from pathlib import Path
from menus.options.file_options import FileOptions
from menus.options.game_options import GameOptions
import tkinter as tk
import os.path
import datetime as dt
import pickle
import tkinter.messagebox as messagebox

class FileMenu(tk.Menu):
    def __init__(self, cpu, step, parent, game_menu, num_save_slots = 5):
        tk.Menu.__init__(self, tearoff=False)
        self.cpu = cpu
        self.step = step
        self.parent = parent
        self.game_menu = game_menu

        self.num_save_slots = num_save_slots
        self.save_menu = tk.Menu(self, tearoff=False)
        self.load_menu = tk.Menu(self, tearoff=False)

        self.add_command(label="Open", accelerator="Ctrl+O", command=self.on_file_open)
        self.add_cascade(label="Save State", accelerator="Ctrl+S", menu = self.save_menu, state="disabled")
        self.add_cascade(label="Load State", accelerator="Ctrl+L", menu = self.load_menu, state="disabled")
        self.create_save_slots(num_save_slots)
        self.add_command(label="Exit", accelerator="Ctrl+W", command=self.on_exit)

        parent.bind("<Control-o>", self.on_file_open)
        parent.bind("<Control-s>", self.on_save)
        parent.bind("<Control-l>", self.on_load)
        parent.bind("<Control-w>", self.on_exit)
    
    def create_save_slots(self, num_save_slots):
        for i in range(1, num_save_slots):
            func = lambda i0 = i: self.on_save(slot = i0) 
            self.save_menu.add_command(label=f"{i}. <empty>", command=func)
        
        for i in range(1, num_save_slots):
            func = lambda i0 = i: self.on_load(slot = i0) 
            self.load_menu.add_command(label=f"{i}. <empty>", command=func)

    def update_save_slot_labels(self, game_name):
        save_files = [game_name + f"-{i}.sav" for i in range(1, 6)]

        for idx, file in enumerate(save_files):
            path = f"../savs/{file}"
            label_text = "<empty>"

            if os.path.isfile(path):
                creation_date = os.path.getctime(path)
                label_text = dt.datetime.fromtimestamp(creation_date).strftime('%Y-%m-%d %H:%M:%S')
            
            self.save_menu.entryconfig(idx, label = label_text)
            self.load_menu.entryconfig(idx, label = label_text)
    
    def on_file_open(self, event = None):
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

            self.game_menu.entryconfigure(
                GameOptions.PAUSE, state="active", label=GameOptions.PAUSE_LABELS[0])
            self.entryconfigure(FileOptions.SAVE, state = "active")
            self.entryconfigure(FileOptions.LOAD, state = "active")
            self.game_menu.entryconfigure(GameOptions.REWIND, state = "active")
            self.game_menu.entryconfigure(GameOptions.FAST_FORWARD, state = "active")

            self.parent.title(game_name)
            self.update_save_slot_labels(game_name)

        # Unpause the CPU.
        self.cpu.paused = False

        # Cycle the CPU.
        self.step()

    def on_save(self, event = None, slot = 1):
        creation_date = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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

        self.entryconfigure(FileOptions.SAVE, state = "active")

        # Unpause the CPU.
        self.cpu.paused = False
    
    def on_exit(self, event = None):
        """Fires when the exit option is selected from the menu.

        This function is fired when the exit option
        is selected from the menu. Closes the emulator.

        Returns:
            void
        """
        # Close the emulator.
        self.parent.destroy()