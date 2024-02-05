"""
settings_menu.py:

Implements a menu for changing user settings.
"""
import tkinter as tk
import menus.preferences_menu as preferences


class SettingsMenu(tk.Menu):
    """A menu for changing user settings.

    Attributes:
        none
    """

    def __init__(self, parent, cpu, config):
        """Initializes a menu for changing user settings.

        Args:
            parent (tkinter.Tk): The parent window for the display.
            cpu (hardware.CPU): A virtual CHIP-8 CPU.
            config (config.ConfigWriter): A config writer for loading or saving settings.
        """
        tk.Menu.__init__(self, tearoff=False)
        self.parent = parent
        self.cpu = cpu
        self.config = config

        # Add a command for opening the preferences menu.
        self.add_command(label="Preferences",
                        accelerator="Ctrl+B",
                        command=self.on_preferences_open)
        # Add a shortcut for opening the preferences menu.
        parent.bind("<Control-b>", self.on_preferences_open)

    def on_preferences_open(self, event=None):
        """Fires when the preferences option is selected from the menu.

        This function is fired when the preferences
        menu is selected from the menu. Pauses emulation
        and opens the preferences menu.

        Args:
            event (tkinter.Event): A Tkinter event. Default value is None.

        Returns:
            void
        """
        # Pause emulation.
        self.cpu.paused = True
        # Open the preferences menu.
        preferences_menu = preferences.PreferencesMenu(self.parent, self.cpu, self.config)
        # Set focus to the preferences menu.
        preferences_menu.grab_set()
