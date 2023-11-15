import tkinter as tk
import menus.preferences_menu as preferences

class SettingsMenu(tk.Menu):
    def __init__(self, parent, cpu, config):
        tk.Menu.__init__(self, tearoff=False)
        self.parent = parent
        self.cpu = cpu
        self.config = config

        self.add_command(label="Preferences", accelerator="Ctrl+B", command = self.on_preferences_open)
        parent.bind("<Control-b>", self.on_preferences_open)

    def on_preferences_open(self, event = None):
        self.cpu.paused = True
        preferences_menu = preferences.PreferencesMenu(self.parent, self.cpu, self.config)
        preferences_menu.grab_set()