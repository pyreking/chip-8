"""
chip8.py:

Creates an emulator window for the CHIP-8 interpreter.

The main program creates a new emulator window for the CHIP-8 interpreter.
"""

import tkinter as tk
import hardware.cpu as comp
import hardware.screen as sc
import hardware.keypad as kp
import hardware.speaker as sp
import menus.menu_bar as mb
import config.config_writer as cw

class Chip8(tk.Frame):
    """The main window for the emulator.

    Attributes:
        cpu: A virtual CHIP-8 CPU.
    """
    def __init__(self, parent, scale, *args, **kwargs):
        """Initializes the main window for the emulator.

        Args:
            parent (tkinter.Tk): The parent window for the emulator.
            cpu (CPU): A virtual CHIP-8 CPU.
            scale (int): The scale factor for the virtual CHIP-8 display.
            args (tuple): Packing arguments inherited from the superclass.
            kwargs (dict[str, Any]): Packing arguments inherited from the superclass.
        """

        # Initialize the tkinter Frame for the window.
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Create a virtual CHIP-8 display.
        screen = sc.Screen(self, width=64 * scale, height=32 * scale,
                           bg="white", highlightthickness=0)

        # Show the virtual CHIP-8 display.
        screen.pack(fill=tk.BOTH, expand=tk.YES)

        # Create a virtual CHIP-8 keypad and bind it to the parent window.
        keypad = kp.KeyPad(parent)

        # Create a virtual CHIP-8 speaker.
        speaker = sp.Speaker("sound/beep.wav")

        # Create a virtual CHIP-8 CPU.
        self.cpu = comp.CPU(screen, keypad, speaker)

        # Read settings from a config file.
        config = cw.ConfigWriter("../settings/config.ini", keypad)

        # Create a new menu bar for the parent window.
        menu = mb.MenuBar(root, self.cpu, config)

        # Add the menu bar to the parent window.
        parent.config(menu=menu)

        # Load key bindings.
        config.load_bindings()

        # Load all of the sprites into memory.
        self.cpu.load_sprites_into_memory()

if __name__ == "__main__":
    # The main program for the emulator.
    #
    # Creates a new emulator for the CHIP-8 interpreter.

    # Create the main window.
    root = tk.Tk()
    root.title("Chip8")

    # Create the emulator frame and bind it to the main window.
    emulator = Chip8(root, 18)
    emulator.pack(side="top", fill="both", expand=True)

    # Start the main GUI loop.
    root.mainloop()
