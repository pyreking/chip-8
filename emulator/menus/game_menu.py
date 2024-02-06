"""
game_menu.py:

Implements a menu for controlling emulation playback.
"""
import pickle
import gzip
import tkinter as tk
from tkinter import PhotoImage
from menus.options.game_options import GameOptions
import menus.speed_menu as sm

class GameMenu(tk.Menu):
    """A menu for controlling emulation playback.

    Attributes:
        none
    """
    def __init__(self, parent, cpu):
        """Initializes a menu for controlling emulation playback.

        A menu that contains options for pausing, rewinding, and
        changing emulation speed.

        Args:
            parent (tkinter.Tk): The parent window for the emulator.
            CPU (hardware.CPU): A virtual CHIP-8 CPU.
        """
        tk.Menu.__init__(self, tearoff=False)
        self.parent = parent
        self.cpu = cpu

        # Create icons for emulation controls.
        self.fast_forward_icon = PhotoImage(file="icons/fast_forward.png")
        self.rewind_icon = PhotoImage(file="icons/rewind.png")
        self.pause_icon = PhotoImage(file="icons/pause.png")

        # Create a menu for changing emulation speed.
        self.speed_menu = sm.SpeedMenu(self.cpu, 0.25, 3)

        # Create menu items.
        self.add_command(
            label="Pause", command=self.on_pause, accelerator="Ctrl+P", state="disabled")

        self.add_command(
            label="Rewind", command=self.on_rewind, accelerator="Ctrl+J", state="disabled")

        self.add_command(
            label="Fast Forward", command=self.on_fast_forward, accelerator="Ctrl+K",
            state="disabled")

        self.add_cascade(label="Speed", menu = self.speed_menu)

        # Create keyboard shortcuts.
        parent.bind("<Control-j>", self.on_rewind)
        parent.bind("<Control-k>", self.on_fast_forward)
        parent.bind("<Control-KeyRelease-j>", self.off_rewind)
        parent.bind("<Control-KeyRelease-k>", self.off_fast_forward)
        parent.bind("<Control-p>", self.on_pause)

    def on_pause(self, event = None):
        """Fires when the pause option is selected from the menu.

        This function is fired when the pause option
        is selected from the menu. Pauses the CPU when it is running.
        Otherwise, it unpauses the CPU.

        Args:
            event (None): A Tkinter event (default = None).

        Returns:
            void
        """
        # Pause or unpause the CPU.
        self.cpu.paused ^= 1

        # Get the pause status from the CPU.
        status = self.cpu.paused

        # Update the pause menu option with the correct label.
        self.entryconfig(GameOptions.PAUSE, label=GameOptions.PAUSE_LABELS[status])

        if status:
            self.cpu.screen.create_image(20,20,image=self.pause_icon, tag="pause")
        else:
            self.cpu.screen.delete("pause")

        # Cycle the CPU if it is not paused.
        self.cpu.step()

    def on_fast_forward(self, event = None):
        """Fires when the emulation is fast forwarded.

        This function is fired when emulation is fast
        forwarded. Triples the CPU speed.

        Args:
            event (None): A Tkinter event (default = None).

        Returns:
            void
        """
        # Create a fast forward icon.
        if self.cpu.speed != self.cpu.FAST_SPEED:
            self.cpu.screen.create_image(20,20,image=self.fast_forward_icon, tag="fast_forward")

        # Set the CPU speed to fast speed.
        self.cpu.speed = self.cpu.FAST_SPEED

    def off_fast_forward(self, event = None):
        """Fires when emulation plays again after the fast
        forward feature has been used.

        This function is fired when emulation
        plays again after the fast forward feature
        has been used. Sets the CPU to normal speed.

        Args:
            event (None): A Tkinter event (default = None).

        Returns:
            void
        """
        # Set the CPU speed to normal speed.
        self.cpu.speed = self.cpu.NORMAL_SPEED
        # Delete the fast forward icon.
        self.cpu.screen.delete("fast_forward")

    def on_rewind(self, event = None):
        """Fires when emulation is rewound.

        This function is fired when emulation is
        rewound. Rewinds emulation for a maximum
        of 600 frames.

        Args:
            event (None): A Tkinter event (default = None).

        Returns:
            void
        """
        # Create a rewind icon.
        if not self.cpu.paused:
            self.cpu.screen.create_image(20,20,image=self.rewind_icon, tag="rewind")

        # Rewind emulation for one frame.
        if len(self.cpu.rewind_buffer) > 0:
            # Pause emulation.
            self.cpu.paused = True
            # Get the uncompressed bytes for the previous frame.
            pickle_bytes = gzip.decompress(self.cpu.rewind_buffer.pop())
            # Get the CPU state for the previous frame.
            state = pickle.loads(pickle_bytes)
            # Load the CPU state from the previous frame into memory.
            self.cpu.load_state(state)

    def off_rewind(self, event = None):
        """Fires when emulation plays again after the rewind
        feature has been used.

        This function is fired when emulation is
        plays again after the rewind feature is used.
        Unpauses and cycles the CPU.

        Args:
            event (None): A Tkinter event (default = None).

        Returns:
            void
        """
        # Delete the rewind icon.
        self.cpu.screen.delete("rewind")
        # Unpause the CPU.
        self.cpu.paused = False
        # Cycle the CPU.
        self.cpu.step()
