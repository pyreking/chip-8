"""
keypad.py:

Implements a virtual CHIP-8 keypad for the emulator.

The test program prints the first virtual keypress to standard output.
"""
import tkinter as tk
from collections import defaultdict
from bidict import bidict


class KeyPad:
    """A virtual keypad for the CHIP-8 interpreter.

    Attributes:
        keys_down: A dictionary that maps virtual CHIP-8 keys to a bools.
        A virtual key maps to True when it is down and False when it is up.

        on_next_key_down: A function that executes on the next virtual key press (default = None).
    """

    def __init__(self, window):
        """Initializes a virtual CHIP-8 keypad.

        A virtual keypad that map scan codes to virtual CHIP-8 keys.

        Args:
            window (tkinter.Tk): The window that uses the virtual CHIP-8 keypad.
        """
        # Tracks virtual CHIP-8 keys that are in the key down state.
        self.keys_down = defaultdict(bool)

        # A mapping of scan codes to virtual CHIP-8 keys.
        self.key_bindings = bidict({
            49: 0x1,  # 1
            50: 0x2,  # 2
            51: 0x3,  # 3
            52: 0xC,  # 4
            81: 0x4,  # Q
            87: 0x5,  # W
            69: 0x6,  # E
            82: 0xD,  # R
            65: 0x7,  # A
            83: 0x8,  # S
            68: 0x9,  # D
            70: 0xE,  # F
            90: 0xA,  # Z
            88: 0x0,  # X
            67: 0xB,  # C
            86: 0xF,  # V
        })

        # This variable should be initialized to a function
        # by the CPU.
        self.on_next_key_down = None

        # Set up the keyboard bindings.
        window.bind('<KeyPress>', self.on_key_down)
        window.bind('<KeyRelease>', self.on_key_up)

    def is_valid_scan_code(self, scan_code):
        """Checks a key for a valid scan code.

        Checks a scan code for a valid mapping to a virtual CHIP-8 key.

        Args:
            scan_code (int): A keyboard scan code in hex.

        Returns:
            bool: True if the scan code maps to a virtual CHIP-8 key. False otherwise.
        """
        return scan_code in self.key_bindings

    def is_key_down(self, virtual_key):
        """Checks a key for a key down event.

        Checks a virtual CHIP-8 key for a key down event.

        Args:
            virtual_key (int): A virtual CHIP-8 key in hex.

        Returns:
            bool: True if the virtual key is pressed. False otherwise.
        """
        return self.keys_down[virtual_key]

    def on_key_down(self, event):
        """Fires when a key is pressed.

        This function is fired when a key is pressed.
        Sets the pressed key to the key down state.
        Does nothing if the pressed key does not map
        to a virtual CHIP-8 key.

        Args:
            event (tkinter.Event): A KeyPress event.

        Returns:
            void
        """
        scan_code = event.keycode

        if self.is_valid_scan_code(scan_code):
            # Set the virtual CHIP-8 key to the key down state.
            virtual_key = self.key_bindings[scan_code]
            self.keys_down[virtual_key] = True

            if self.on_next_key_down:
                # If this variable has been set to something,
                # use it as a function.
                self.on_next_key_down(virtual_key)
                self.on_next_key_down = None

    def on_key_up(self, event):
        """Fires when a key is released.

        This function is fired when a key is released.
        Sets the released key to the key up state.
        Does nothing if the released key does not map
        to a virtual CHIP-8 key.

        Args:
            event (tkinter.Event): A KeyRelease event.

        Returns:
            void
        """
        scan_code = event.keycode

        if self.is_valid_scan_code(scan_code):
            # Set the virtual key to the key up state.
            virtual_key = self.key_bindings[scan_code]
            self.keys_down[virtual_key] = False

    def update_key_binding(self, virtual_key, scan_code):
        """Updates the key binding assigned to a virtual CHIP-8 key.

        Updates the key binding assigned to a virtual CHIP-8 key
        in a bi-directional dictionary. If a scan code has already
        been assigned to a different virtual CHIP-8 key, the old
        binding will be deleted before the new one is created.

        Args:
            virtual_key (int): A virtual CHIP-8 key in hex.
            scan_code (int): A keyboard scan code in hex.

        Returns:
            evicted_key (int): The virtual CHIP-8 key
            associated with the binding that was deleted
            during the update. Default is None if no key
            binding was deleted.
        """
        evicted_key = None

        if scan_code in self.key_bindings:
            evicted_key = self.key_bindings[scan_code]

        if virtual_key in self.key_bindings.inverse:
            del self.key_bindings.inverse[virtual_key]

        self.key_bindings[scan_code] = virtual_key

        return evicted_key


if __name__ == "__main__":
    # A test program for the virtual CHIP-8 KeyPad.
    #
    # Creates a virtual CHIP-8 KeyPad and binds it to a new window. Prints
    # the first key press to standard output.

    # Create a new window.
    root = tk.Tk()
    root.geometry('300x200')

    # Create a new KeyPad.
    keyboard = KeyPad(root)

    def on_next_key_down(virtual_key):
        """Prints a virtual CHIP-8 key to standard output.

        Args:
            virtual_key (int): A virtual CHIP-8 key in hex.
        """
        print(f"Virtual key pressed: {virtual_key}")

    # Print the next key press to standard output.
    keyboard.on_next_key_down = on_next_key_down

    # Start the main GUI loop.
    root.mainloop()
