"""
chip8_menu.py:

Implements a menu bar for the CHIP-8 interpreter.

The test program creates a new menu bar and binds it to a window.
"""
import tkinter as tk
import menus.file_menu as fm
import menus.game_menu as gm
import menus.settings_menu as sm

class MenuBar(tk.Menu):
    """A menu bar for the CHIP-8 interpreter.

    Attributes:
        parent: The parent Tk window for the menu bar.
        cpu: A virtual CHIP-8 CPU.
        step: A function that cycles the virtual CHIP-8 CPU.
        file_menu: A file menu for the menu bar.
    """

    def __init__(self, parent, cpu, step, config):
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
        self.config = config
        
        self.game_menu = gm.GameMenu(self.cpu, self.step, self.parent)
        self.file_menu = fm.FileMenu(self.cpu, self.step, self.parent, self.game_menu)
        self.settings_menu = sm.SettingsMenu(self.cpu, self.step, self.parent, self.config)
        
        self.add_cascade(label="File", menu=self.file_menu)
        self.add_cascade(label="Game", menu=self.game_menu)
        self.add_cascade(label="Settings", menu=self.settings_menu)