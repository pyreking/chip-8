"""
file_menu.py:

Implements a file menu for the menu bar.
"""

import os.path
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
import pickle
import tkinter as tk
import datetime as dt
from menus.options.file_options import FileOptions
from menus.options.game_options import GameOptions

class FileMenu(tk.Menu):
    """A file menu for the menu bar.

    Attributes:
        none
    """

    def __init__(self, parent, cpu, game_menu, num_save_slots=5):
        """Initializes a file menu for the menu bar.

        A file menu that contains options for loading ROMs and using
        save states.

        Args:
            parent (tkinter.Tk): The parent window for the emulator.
            CPU (hardware.CPU): A virtual CHIP-8 CPU.
            game_menu (menus.GameMenu): The GameMenu from the menu bar.
            num_save_slots (int): The number of save slots to create for the menu.
        """
        tk.Menu.__init__(self, tearoff=False)
        self.parent = parent
        self.cpu = cpu
        self.game_menu = game_menu

        self.num_save_slots = num_save_slots

        # Create save and load menus.
        self.save_menu = tk.Menu(self, tearoff=False)
        self.load_menu = tk.Menu(self, tearoff=False)

        # Assign functions to each menu item.
        self.add_command(label="Open", accelerator="Ctrl+O", command=self.on_file_open)
        self.add_cascade(label="Save State", accelerator="Ctrl+S",
                         menu=self.save_menu, state="disabled")
        self.add_cascade(label="Load State", accelerator="Ctrl+L",
                         menu=self.load_menu, state="disabled")
        self.create_save_slots(num_save_slots)
        self.add_command(label="Exit", accelerator="Ctrl+W", command=self.on_exit)

        # Create keyboard shortcuts.
        parent.bind("<Control-o>", self.on_file_open)
        parent.bind("<Control-s>", self.on_save)
        parent.bind("<Control-l>", self.on_load)
        parent.bind("<Control-w>", self.on_exit)

    def create_save_slots(self, num_save_slots):
        """Creates save slots for the menu.

        Creates save slots for the menu based on the number set by
        the user.

        Args:
            num_save_slots (int): The number of save slots to create for the menu.

        Returns:
            void
        """
        # Create save slots for the save menu.
        for i in range(1, num_save_slots):
            func = lambda i0 = i: self.on_save(slot = i0)
            self.save_menu.add_command(label=f"{i}. <empty>", command=func)

        # Create save slots for the load menu.
        for i in range(1, num_save_slots):
            func = lambda i0 = i: self.on_load(slot = i0)
            self.load_menu.add_command(label=f"{i}. <empty>", command=func)

    def update_save_slot_labels(self, game_name):
        """Updates save slots labels for the menu.

        Updates the save slot labels for the save and load menus
        when a game is opened. Unused save slots are displayed
        as <empty> while used save slots are represented by the save
        file's creation time.

        Args:
            game_name (str): The name of the game that is being run.

        Returns:
            void
        """
        # Generate a list of filenames to check.
        save_files = [game_name + f"-{i}.sav" for i in range(1, self.num_save_slots)]

        # Update the save slot labels for the menu.
        for idx, file in enumerate(save_files):
            # The path to the file.
            path = f"../savs/{file}"
            # The default save slot label.
            label_text = "<empty>"

            # Update the save slot label if the file exists.
            if os.path.isfile(path):
                creation_date = os.path.getctime(path)
                label_text = dt.datetime.fromtimestamp(
                    creation_date).strftime('%Y-%m-%d %H:%M:%S')

            # Set the appropriate label for the save slot.
            self.save_menu.entryconfig(idx, label=label_text)
            self.load_menu.entryconfig(idx, label=label_text)

    def on_file_open(self, event=None):
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
            self.entryconfigure(FileOptions.SAVE, state="active")
            self.entryconfigure(FileOptions.LOAD, state="active")
            self.game_menu.entryconfigure(GameOptions.REWIND, state="active")
            self.game_menu.entryconfigure(
                GameOptions.FAST_FORWARD, state="active")

            self.parent.title(game_name)
            self.update_save_slot_labels(game_name)

        # Unpause the CPU.
        self.cpu.paused = False

        # Cycle the CPU.
        self.cpu.step()

    def on_save(self, event=None, slot=1):
        """Fires when the save option is selected from the menu.

        This function is fired when the save option
        is selected from the menu. Saves the emulation
        state to file. The filename for the save
        state is the creation date for the file.

        Args:
            event (tk.Tkinter): A Tkinter event. Default value is None.
            slot (int): The save slot for the save state.

        Returns:
            void
        """
        # Get the current date and time.
        creation_date = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Create the filename for the save state.
        path = "../savs/" + self.parent.title() + f"-{slot}.sav"
        # Get the current CPU state.
        state = self.cpu.save_state()

        # Updated the label for the save slot.
        self.save_menu.entryconfigure(slot - 1, label=creation_date)
        self.load_menu.entryconfigure(slot - 1, label=creation_date)

        # Dump the state to file.
        with open(path, "wb") as file:
            pickle.dump(state, file)

    def on_load(self, event=None, slot=1):
        """Fires when the load option is selected from the menu.

        This function is fired when the load option
        is selected from the menu. Load the emulation
        state from file.

        Args:
            event (tk.Tkinter): A Tkinter event. Default value is None.
            slot (int): The save slot to load from.

        Returns:
            void
        """
        # Pause emulation.
        self.cpu.paused = True

        # Determine the filename for the save state.
        path = "../savs/" + self.parent.title() + f"-{slot}.sav"

        # Load the save state if the file exists.
        try:
            with open(path, "rb") as file:
                state = pickle.load(file)
                self.cpu.load_state(state, clear_buffer=True)
        # Display a dialog box if the file does not exist.
        except FileNotFoundError:
            self.cpu.paused = False
            messagebox.showerror(
                "Save file not found",
                f"No save file found in slot {slot}.")
            self.cpu.step()

        # Enable the save option.
        self.entryconfigure(FileOptions.SAVE, state="active")

        # Unpause the CPU.
        self.cpu.paused = False

    def on_exit(self, event=None):
        """Fires when the exit option is selected from the menu.

        This function is fired when the exit option
        is selected from the menu. Closes the emulator.

        Returns:
            void
        """
        # Close the emulator.
        self.parent.destroy()
