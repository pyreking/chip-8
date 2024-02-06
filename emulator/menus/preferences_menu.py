"""
preferences_menu.py:

Implements a menu for changing the default key bindings
for the emulator.
"""

from tkinter import ttk
import tkinter as tk

class PreferencesMenu(tk.Toplevel):
    """A menu for changing the default key bindings
    for the emulator.

    Attributes:
        HEADINGS (List[str]): A list of headings for the menu.
        KEY_LABELS (List[str]): A list of labels for the 16 virtual CHIP-8 keys.
    """
    HEADINGS = ["Key", "Binding"]
    KEY_LABELS = ['1', '2', '3', 'C', '4', '5', '6',
                  'D', '7', '8', '9', 'E', 'A', '0',
                  'B', 'F']

    def __init__(self, parent, cpu, config):
        """Initializes a menu for changing the default
        key bindings for the emulator.

        Args:
            parent (tkinter.Tk): The parent window for the emulator.
            CPU (hardware.CPU): A virtual CHIP-8 CPU.
            config (config.ConfigWriter): A config writer for loading or saving settings.
        """
        super().__init__(parent)
        self.parent = parent
        self.cpu = cpu
        self.keypad = self.cpu.keypad
        self.config = config

        self.geometry('500x350')
        self.resizable(False, False)

        # Create the headings for the menu.
        self.tree = ttk.Treeview(self, columns=self.HEADINGS, show="headings")

        # Create the labels for the menu headings.
        for heading in self.HEADINGS:
            self.tree.heading(heading, text=heading)

        self.tree.column(0, anchor=tk.CENTER)
        self.tree.column(1, anchor=tk.CENTER)

        # Create the labels for the virtual CHIP-8 keys.
        for key_label in self.KEY_LABELS:
            self.tree.insert('', 'end', key_label, values=(key_label,))

        # Create the labels for the keys bound to the virtual CHIP-8 keys.
        for scan_code, virtual_key in self.keypad.key_bindings.items():
            key_label = hex(virtual_key).upper()[-1]
            self.tree.item(key_label, values=(key_label, chr(scan_code).upper()))

        # Load the correct labels for the key bindings.
        if "labels" in self.config.parser:
            self.config.load_labels(self.tree)

        # Set the default highlighting to gray.
        self.style = ttk.Style()
        self.style.map('Treeview', background=[('selected', 'lightgray')])

        # This is a function pointer that will be used to update
        # a key binding after a menu item has been selected.
        # When nothing is selected, it is None.
        self.on_next_key_down = None

        # Create events for the menu.
        self.bind('<ButtonRelease-1>', self.on_click)
        self.bind('<KeyPress>', self.on_key_down)
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.tree.pack(fill="both", expand=True)

    def on_click(self, event):
        """Fires when an item is selected from the menu.

        This function is fired when an item is selected
        from the menu. The selected item is highlighted
        in blue and waits for the next key press. After
        a key has been pressed, a key binding is created
        for the virtual CHIP-8 key that was selected
        and highlighting is disabled.

        Returns:
            void
        """
        # Highlight the selected item in blue.
        self.style.map('Treeview', background=[('selected', 'lightblue')])

        # Get the selection.
        item = self.tree.selection()[0]

        def on_next_key_down(event):
            """Fires on the next key.

            This function is fired after the next key press.
            Binds the pressed key to the selected virtual
            CHIP-8 key. If the pressed key is already bound
            to another virtual CHIP-8 key, then the old one
            is automatically deleted.

            Returns:
                void
            """
            # Get the pressed key along with its label.
            scan_code, scan_code_label = event.keycode, event.keysym.upper()

            # Get the label for the selected virtual CHIP-8 key.
            virtual_key_label = self.tree.item(item, "values")[0]
            # Get the hex value for the selected virtual CHIP-8 key.
            virtual_key = int(virtual_key_label, 16)

            # Update the key binding for the selected virtual CHIP-8 key.
            evicted_key = self.keypad.update_key_binding(virtual_key, scan_code)

            # Give a blank label to a deleted key binding.
            if evicted_key is not None:
                evicted_key_label = hex(evicted_key).upper()[-1]
                self.tree.item(evicted_key_label, values=(evicted_key_label,))

            # Update the label for the key binding.
            self.tree.item(item, values=(virtual_key_label, scan_code_label))

        # Queue the updated key binding.
        self.on_next_key_down = on_next_key_down

    def on_key_down(self, event):
        """Fires when a key is pressed.

        This function fires when a key is pressed.
        Updates the key binding for a virtual
        CHIP-8 key when it is selected from the
        menu. Does nothing if no option is selected
        from the menu.

        Returns:
            void
        """
        # Update the key bindings if a
        # menu option has been selected.
        if self.on_next_key_down:
            self.on_next_key_down(event)
            self.on_next_key_down = None
            # Change the default highlighting to light gray.
            self.style.map('Treeview', background=[('selected', 'lightgray')])

    def on_exit(self):
        """Fires when the menu is closed.

        This function fires when the menu is closed.
        Saves the updated settings to an ini file
        and unpauses emulation before closing.

        Returns:
            void
        """
        # Save the updated settings.
        self.config.save_settings(self.tree)
        # Unpause emulation.
        self.cpu.paused = False
        # Cycle the cpu if a game is running.
        if self.cpu.running:
            self.cpu.step()
        # Destroy the window.
        self.destroy()
