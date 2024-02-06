"""
chip8_menu.py:

Implements a menu bar for the CHIP-8 interpreter.
"""
import tkinter as tk
import menus.file_menu as fm
import menus.game_menu as gm
import menus.settings_menu as sm


class MenuBar(tk.Menu):
    """A menu bar for the CHIP-8 interpreter.
    
    Attributes:
        none
    """

    def __init__(self, parent, cpu, config):
        """Initializes the menu bar for the emulator.

        Args:
            parent (tkinter.Tk): The parent window for the menu bar.
            cpu (hardware.CPU): A virtual CHIP-8 CPU.
            step (function): A function that cycles the virtual CHIP-8 CPU.
        """
        # Initialize the tkinter Menu.
        tk.Menu.__init__(self, parent, tearoff=False)

        # Set up instance variables.
        self.parent = parent
        self.cpu = cpu
        self.config = config

        # Create menus.
        self.game_menu = gm.GameMenu(self.parent, self.cpu)
        self.file_menu = fm.FileMenu(self.parent, self.cpu, self.game_menu)
        self.settings_menu = sm.SettingsMenu(
            self.parent, self.cpu, self.config)

        # Add menus to menu bar.
        self.add_cascade(label="File", menu=self.file_menu)
        self.add_cascade(label="Game", menu=self.game_menu)
        self.add_cascade(label="Settings", menu=self.settings_menu)
