"""
chip8_menu.py:

Implements a menu bar for the CHIP-8 interpreter.

The test program creates a new menu bar and binds it to a window.
"""

import tkinter as tk
from tkinter import filedialog

class Options:
    """A list of options for the menu bar.

    An enum class that reperesents the options availiable for the menu bar.
    """
    OPEN = 0
    PAUSE = 1
    EXIT = 2

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
        self.add_cascade(label="File", menu=self.file_menu)

        # Add open option.
        self.file_menu.add_command(label="Open", command=self.on_open)

        # Add pause option.
        self.file_menu.add_command(
            label="Pause", command=self.on_pause, state="disabled")

        # Add exit option.
        self.file_menu.add_command(label="Exit", command=self.on_exit)

        # Add the menu bar to the parent window.
        parent.config(menu=self)

    def on_open(self):
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
            # Load the ROM into memory.
            self.cpu.load_rom(filename)
            # Enable the pause option in the menu.
            self.file_menu.entryconfigure(
                Options.PAUSE, state="active", label=self.PAUSE_LABELS[0])

        # Unpause the CPU.
        self.cpu.paused = False

        # Cycle the CPU.
        self.step()

    def on_pause(self):
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
        self.file_menu.entryconfig(Options.PAUSE, label=self.PAUSE_LABELS[idx])

        # Cycle the CPU if it is not paused.
        self.step()

    def on_exit(self):
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

    # Start the main GUI loop.
    root.mainloop()
