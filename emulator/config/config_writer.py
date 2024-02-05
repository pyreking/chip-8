"""
config_writer.py:

Saves or loads a config file containing user settings and key bindings.
"""
import configparser as parser


class ConfigWriter():
    """Saves or loads a config file containing user settings and key bindings.

    Attributes:
        none
    """

    def __init__(self, path, keypad):
        """Initializes an object that can save or load a config file containing
        user settings and keys bindings.

        Args:
            path (str): The path containing the config file to update.
                        A config file will be created if it does not exist.
            keypad (Keypad): The virtual CHIP-8 keypad for the emulator.
        """
        self.keypad = keypad
        self.parser = parser.ConfigParser()
        self.PATH = path
        self.parser.read(self.PATH)

        # Create a bindings label for the config file.
        #
        # ex: "69 = 5" means that the "E" key on the keyboard
        # has been assigned to the "5" key on the virtual
        # Chip-8 keypad.
        if "bindings" not in self.parser:
            self.parser.add_section("bindings")

        # Create a keysym label for the config file.
        #
        # ex: "5 = E" means that "5" on the virtual
        # CHIP-8 keypad will have an "E" label
        # in the preferences menu.
        if "labels" not in self.parser:
            self.parser.add_section("labels")

    def save_settings(self, tree):
        """Saves user settings and key bindings to an ini file.

        Args:
            tree (ttk.Treeview): A ttk.Treeview object corresponding to a
                                 list of preferences to save.

        Returns:
            void
        """
        # Clear the current user settings.
        self.parser['bindings'].clear()
        self.parser['labels'].clear()

        # Update the user settings.
        for scan_code, virtual_key in self.keypad.key_bindings.items():
            # Save the label for the current virtual CHIP-8 key.
            virtual_key_label = hex(virtual_key)[-1].upper()
            # Update the key binding.
            self.parser.set("bindings", str(scan_code), virtual_key_label)
            # Update the label for the key binding.
            self.parser.set(
                "labels",
                virtual_key_label,
                tree.item(
                    virtual_key_label,
                    option='values')[1])

        # Write the new settings to file.
        with open(self.PATH, 'w', encoding='UTF-8') as f:
            self.parser.write(f)

    def load_bindings(self):
        """Updates the key bindings for the emulator.

        Returns:
            void
        """
        # Update the key bindings based on the settings from the loaded ini
        # file.
        for scan_code, virtual_key in self.parser["bindings"].items():
            self.keypad.update_key_binding(
                int(virtual_key, 16), int(scan_code))

    def load_labels(self, tree):
        """Update the labels assigned to each virtual CHIP-8 key in the preferences menu.

        Args:
            tree (ttk.Treeview): A ttk.Treeview object corresponding to a
                                 list of preferences to update.

        Returns:
            void
        """
        # Update the labels assigned to each virtual CHIP-8 key in the
        # preferences menu.
        for virtual_key_label, scan_code_label in self.parser["labels"].items(
        ):
            tree.item(
                virtual_key_label.upper(),
                values=(
                    virtual_key_label.upper(),
                    scan_code_label))
