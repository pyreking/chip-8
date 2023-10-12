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
import chip8_menu as cm

class Chip8(tk.Frame):
    """The main window for the emulator.

    Attributes:
        cpu: A virtual CHIP-8 CPU.
    """

    # The framerate for the emulator.
    FPS = 60

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
        speaker = sp.Speaker("../sound/beep.wav")

        # Create a virtual CHIP-8 CPU.
        self.cpu = comp.CPU(screen, keypad, speaker)

        # Create a new menu bar for the parent window.
        menu = cm.Chip8Menu(root, self.cpu, self.step)

        # Add the menu bar to the parent window.
        parent.config(menu=menu)

        # Load all of the sprites into memory.
        self.cpu.load_sprites_into_memory()

    def step(self):
        """Cycles the CPU.

        Cycles the CPU when it is not paused. Automatically calls
        itself multiple times per second depending on the framerate.

        Returns:
            void
        """
        if not self.cpu.paused:
            # Cycle the CPU.
            self.cpu.cycle()
            # Fire this function again when a new frame is needed.
            self.after(int(1000 / Chip8.FPS), self.step)

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
